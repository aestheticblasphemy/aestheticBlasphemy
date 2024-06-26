import re
import six
import bs4
from bs4 import BeautifulSoup

from .utils import get_css_styles
"""

tags to be identified
Body, content


"""


def get_field_name_from_tag(current_tag):
    field_name = current_tag.split("_")[0:-1]
    return_name = "_".join(str(tag) for tag in field_name)
    return return_name

def get_pattern(current_tag):
    tag_start_pattern = "\\%\\% " + str(current_tag['name']) + " \\%\\%"
    tag_end_pattern = "\\%\\% endtag "+ str(current_tag['name']) + " \\%\\%"
    final_pattern =  tag_start_pattern + "(.*?)" + tag_end_pattern
    return final_pattern


def parse_content(db_object, tag):
    if str(tag['name']) == 'title_tag':
        return db_object.title
    final_pattern = get_pattern(tag)
    print(("pattern to be found ", final_pattern))
    ## DOTALL flag for including new line also
    patt = re.compile(final_pattern,flags=re.DOTALL)
    print(("pattern  ", patt))

#     print "data ", db_object.data
    result = patt.search(db_object.data)
#     print result
    if result:
        return result.group(1)
    else:
        return ""

def strip_tag_from_data(data):
    p = re.compile('\\%\\% .*? \\%\\%',flags=re.DOTALL)
    print("LOGS:: Stripping tags from data")
    line = p.sub('', data)
    return line


def has_no_id(tag):

    print(("tag return has no id ", tag.has_attr('id')))
    return  not tag.has_attr('id')

def has_enough_length(tag):
    """
    check for tag.string --> if it is None then it has more than one children.
    """
    print(("has_enough_length()-->", tag.name))

    if tag.string == None:
        tag_string = ''.join(str(tag_child.encode('utf-8')) for tag_child in tag.contents)
        print(("Printing contents string ", tag_string))
        flag = len(tag_string) > 100
        print(("returning ", flag))
        return flag
    else:
        print(("Printing string ", tag.string.encode('utf-8')))
        flag = len(tag.string.encode('utf-8')) > 100
        print(("returning ", flag))
        return flag

def has_eligible_child(tag):
    for tag_child in tag.contents:
        if has_enough_length(tag_child):
            return True
    return False

def insert_tag_id(data,id_count):
    """

    Search for all children of body tag:
    1. if it is <p> then check for id, set it if not present.
    2. if it is <ul> or <ol> traverse through its children.
        a) if length of <li> is greater then 100 then set the id.
        b) if none of the <li> is suitable for id then give its parent the id.
    3. if it is <img> then set the id.

    Each set operation --> increament the pid_count and then set it to id field
    return the dictionary containing content and final pid_count

    """


#    print soup.body.contents

    filter_elements = ['p','span','img']
    css_styles = get_css_styles()

    if isinstance(id_count, str):
        print(("s is unicode, %r" % id_count))
        id_count = str(id_count)

    print((type(id_count)))

    if isinstance(id_count, six.string_types):
        if len(id_count) == 0:
            print(("LOGS: PID_COUNT IS ", id_count))
            id_count = 0
        else:
            id_count = int(id_count)

    if isinstance(id_count, int):
        print("type is int")
    elif id_count == None:
        id_count = 0

    if isinstance(data, int):
        print("data is int")
        data = str(data)

    if len(data) > 0:

        print("Entering Soup")
        soup = BeautifulSoup(data,"html5lib")

        initial_content = ''.join(str(tag) for tag in soup.body.contents)
        initial_content = initial_content.replace('\xc2\xa0', ' ')

        print(("printing original html: \n {content}".format(content=initial_content)))

        # add description itemproperty in the first paragraph
        try:
            if soup('p') != None:
                soup('p')[0]['itemprop'] = "description"
            elif soup('li') != None:
                soup('li')[0]['itemprop'] = "description"
        except IndexError as ex:
            print(ex)

        for tag in soup.body.children:

            if tag.name == 'p' and has_no_id(tag):
                print("setting tag p")
                id_count = id_count + 1
                tag['id'] = id_count

            elif (tag.name == 'ul' or tag.name == 'ol') and has_no_id(tag):
                if has_eligible_child(tag) == True:
                    for tag_child in tag.contents:
                        if tag_child.name == 'li' and has_no_id(tag_child):
                            print(("setting tag ",tag_child.name))
                            id_count = id_count + 1
                            tag_child['id'] = id_count
                else:
                    print(("setting tag ", tag.name))
                    id_count = id_count + 1
                    tag['id'] =  id_count
            elif tag.name == 'img' and has_no_id(tag):
                id_count = id_count + 1
                tag['id'] = id_count



        for tag_child in soup.body.descendants:
            if tag_child.name == 'img':
                tag_child['itemprop'] = "image"
                if tag_child.get('class', None) != None:
                    tag_child['class'].append(css_styles['image'])
                else:
                    tag_child['class'] = css_styles['image']

            if tag_child.name in filter_elements:
                tag_child['style'] = " "

            if type(tag_child) == bs4.element.Tag and tag_child.get('class', None) != None:
                if 'rtecenter' in tag_child['class']:
                    tag_child['class'].remove('rtecenter')
                    tag_child['class'].append(css_styles['center'])
                elif 'rtejustify' in tag_child['class']:
                    tag_child['class'].remove('rtejustify')
                    tag_child['class'].append(css_styles['justify'])

        print("Now printing altered html ")
        final_content = ''.join(str(tag) for tag in soup.body.contents)
        final_content = final_content.replace('\xc2\xa0', ' ')
        print(final_content)
    else:
        final_content = data
    return_dict = {}
    return_dict['content'] = final_content
    return_dict['pid_count'] = id_count

    return return_dict
