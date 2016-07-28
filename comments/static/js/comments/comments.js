/**
 * @file comments.js
 * @brief Comments Javascript
 */

/* Use Getter and Setters to have a pointer like functionality here */
var ABC = ABC || new GlobalSiteContainer();

$(document).ready(function(){
	
	var csrfSafeMethod = function(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	
	/**
	 * Current Post's ID for fetching statistics.
	 * 
	 * @note it is assumed that the comment form is loaded before this call.
	 */
	ABC.post_id = parseInt($(".rest[data-id]").attr('data-id'));
	
	/**
	 * renderForm
	 * @brief Render the form in the page.
	 */
	var renderForm = function(data){
		//console.log('renderForm');
		$('#article-adjunct-tab-comments').prepend(data);
		/* Bind click event */
		$('#post_comment').on('click', postComment);
	};
	
	/**
	 * loadForm
	 * @brief Fetch the Form HTML from Server
	 */
	var loadForm = function(){
		$.ajax({
		    // the URL for the request
		    url: window.location.origin+'/comments/'+ABC.post_id+'/form/',
		 
		    // whether this is a POST or GET request
		    type: "GET",
		 
		    // the type of data we expect back
		    dataType : "html",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: renderForm,
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		        console.log(xhr['responseText']);
		    },
		 
		    // code to run regardless of success or failure
		    complete: function( xhr, status ) {
		        //alert( "The request is complete!" );
		    }
		});
	};
	
	/**
	 * replyToComment
	 * 
	 * @brief Clone the already existing form here and fill in the proper values
	 */
	var replyToComment = function(){
		comment = $(this).parents('.comments-container-item');
		id= parseInt(comment.attr('data-comment-id').split('_').slice(-1)[0]);
		console.log(id);
		form = $('.form-body').detach();
		form.find('#id_parent_comment').val(id);
		console.log(form.find('#id_parent_comment').val());
		form.insertAfter(comment);
	};

	/**
	 * postComment
	 * @brief : Posts an annotation.
	 * 
	 * This is a fixture right now, all it does is receive and check sanity of annotation and call the
	 * renderAnnotation method as if the server responded with a valid response.
	 */
	var postComment = function(e){
		e.preventDefault();
		/* Construct a JSON string of the data in annotation. */
		//console.log(this);
		/* Check login */
		if(ABC.user['id'] == 0)
		{
			/*TODO: Check if Name/Email have been provided. */
			console.log('Guest User');
			//return;
		}
		
		/* First find the parent's para-id */

		
		/* Current text must not be empty. Though this must be taken care of in HTML5 required flag*/
		post = ABC.post_id;
		author_name= $("#id_author_name").val();
		author_email= $("#id_author_email").val();
		author_url= $("#id_author_url").val();
		if(author_url.length >0){
			/* check for http:// pattern. if not found, append. */
			author_url = author_url.trim();
			if(author_url.indexOf('http://')==-1 || 
					author_url.indexOf('http://') != 0)
			{
				author_url = 'http://'+author_url;
			}
		}
		body = $("#id_body").val();
		
		//console.log(body);
		if(body === ''){
			console.log('Error. Body has no content.');
			$('#comments-error').html("Cannot make empty notes!");
			$('#comments-error').removeClass('hidden');
			return;
		}
		
		data = {
				body: body,
				author_name: (author_name.length > 0 ? author_name: null),
				author_email: (author_email.length >0? author_email: null),
				author_url: (author_url.length > 0? author_url: null),
				parent_comment: $('#id_parent_comment').val(),
				post: post,
				published : false,
			};
		
		console.log(JSON.stringify(data));
		
		/* POST it now! */
		//Form Validation goes here....

	    $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", ABC.csrf);
	            }
	        }
	    });
	    //Save Form Data........
	    $.ajax({
	        cache: false,
	        url : window.location.origin+"/comments/",
	        type: "POST",
	        dataType : "json",
	        contentType: "application/json;",
	        data : JSON.stringify(data),
	        context : this,
	        success : renderSingleComment,
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ');
	            console.log(xhRequest);
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
		
		/* Clear out form contents, if any. */
		$("#id_body").val("");
	    e.stopPropagation(); 
		return false;
	}
		
	/**
	 * commentDeleted
	 * @param data
	 */
	var commentDeleted = function(data){
    	console.log(data);
    	$('.comments-container-item[data-comment-id="cid_'+data[0]+'"]').remove();
	};
	
	/**
	 * deleteComment
	 * @param id: ID of paragraph to remove
	 */
	var deleteComment = function(id){
	      selected = new Array();
	      id= parseInt($(this).attr('data-comment-id').split('_').slice(-1)[0]);
	      
	      selected.push(id);
	      
	      console.log(selected);
	      
	      data={'selection': selected,
	    		'action': 'Delete'};

	      $.ajaxSetup({
		        beforeSend: function(xhr, settings) {
		            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		                xhr.setRequestHeader("X-CSRFToken", ABC.csrf);
		            }
		        }
		    });
		    //Save Form Data........
		    $.ajax({
		        cache: false,
		        url : window.location.origin+"/comments/approve/",
		        type: "POST",
		        dataType : "json",
		        contentType: "application/json;",
		        data : JSON.stringify(data),
		        context : this,
		        success : commentDeleted,
		        error : function (xhRequest, ErrorText, thrownError) {
		            //alert("Failed to process annotation correctly, please try again");
		            console.log('xhRequest: ');
		            console.log(xhRequest);
		            console.log('ErrorText: ' + ErrorText + "\n");
		            console.log('thrownError: ' + thrownError + "\n");
		        }
		    });	
		return false;
	};
	
	/**
	 * renderSingleComment
	 * @param data : Payload received from the server
	 * @brief Loads comments in their respective containers.
	 * 
	 */
	var renderSingleComment = function(data){
		data_list = [data];
		renderComments(data_list);
		//console.log('Scroll to active view');
		//console.log($('.comments-container-item[data-comment-id="cid_'+data['id']+'"]'));
		//console.log($('.comments-container-item[data-comment-id="cid_'+data['id']+'"]').offset());
		if(!$('.form-body').prev().hasClass('card-header')){
			console.log('reattach');
			form = $('.form-body').detach();
			console.log($('#article-adjunct-tab-comments .card-header'));
			form.insertAfter($('#article-adjunct-tab-comments .card-header'));
			form.find('#id_parent_comment').prop('selectedIndex',0);
			console.log(form.find('#id_parent_comment').val());
		}
		$('html, body').animate({
	        scrollTop: $('.comments-container-item[data-comment-id="cid_'+data['id']+'"]').offset().top
	    }, 2000);
		return false;
	}
	
	/**
	 * renderComments
	 * @param data : Payload received from the server
	 * @brief Loads annotations in their respective containers.
	 * 
	 */
	var renderComments = function(data){
		//console.log('renderComments');
		if ((typeof(commentContainer) === 'undefined') || 
											commentContainer === null){
			/* Create a fresh copy of the variable*/
			//console.log('It is null. Make a new one');
			var commentContainer = $('#article-adjunct-tab-comments');
			//console.log(commentContainer);
		}
		for(i=0; i< data.length;i++){
			//console.log('Comment:');
			//console.log(data[i]['parent_comment']);
			/* Find the annotations container inside that and append the comment */
			currentComment = $('<div class="comments-container-item">'+
                    			'<div class="comments-container--media">'+
                    				'<img class="comments-author-image" src=""/>'+
            					'</div>'+
            					'<div class="comments-container--block">'+
            					'<a class="comments-author-link" href="#"><span class="comments-author-name"></span></a>'+
            					'<span class="comments-container--text"></span>'+
            					'<div class="comments-control-box btn-group">'+
            					'<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+
            					'<span class="fa fa-ellipsis-v"</span></button>'+
            					'<div class="dropdown-menu">'+
            					'<span class="dropdown-item comments-control comment-reply">Reply</span>'+
            					'</div>'+
            					'</div>'+
            					'</div>'+
            					'</div>');
			
			/* Create the comment */
			currentComment.attr('data-comment-id', 'cid_'+data[i]['id']);
			if(data[i]['author']===null){
				currentComment.find('.comments-author-name').text(data[i]['author_name']);
				currentComment.find('.comments-author-link').attr('href',data[i]['author_url']);
				currentComment.find('.comments-author-image').attr('src', '/static/static/images/user.png');
			}else{
				currentComment.find('.comments-author-name').text(data[i]['author']['username']);
				currentComment.find('.comments-author-link').attr('href',data[i]['author']['url']);
				currentComment.find('.comments-author-image').attr('src', data[i]['author']['gravatar']);
			}
			currentComment.find('.comments-container--text').text(data[i]['body']);
			currentComment.find('.comment-reply').on('click', replyToComment);
			/* Also add to main container if the comment has no parent. */
			if(ABC.user['is_admin'] || (data[i]['author'] != null && data[i]['author']['id'] == ABC.user['id'])){
				controls = $('<span class="dropdown-item comments-control comment-delete">Delete</span>');
				currentComment.find('div.dropdown-menu').append(controls);
				currentComment.find('.comment-delete').attr('data-comment-id', 'cid_'+data[i]['id']);
				currentComment.find('.comment-delete').on('click', deleteComment);
				if(data[i]['published']==false && ABC.user['is_admin']){
					currentComment.find('div.dropdown-menu').append($('<span class="dropdown-item comments-control comment-publish">Publish</span>'));
					currentComment.find('.comment-publish').attr('data-comment-id', 'cid_'+data[i]['id']);
					currentComment.find('.comment-publish').on('click', publishComment);
				}
			}
			if(data[i]['published']== false){
				currentComment.append('<span class="comment-moderated text-muted">(Awaiting Moderation)</span>')
			}
			if(data[i]['parent_comment']===null){
				/* Append to main comments container*/
				commentContainer.append(currentComment);
				currentComment.wrap('<div class="comments-container-thread"></div>');
			}
			else{
				/* Find the parent container */
				currentObject = commentContainer.find('[data-comment-id="cid_'+data[i]['parent_comment']+'"]');
				/* Append as a child of its parent comment */
				currentComment.insertAfter(currentObject[0]);
				}
			}
		return false;
	};
	
	/**
     * publishComment
     * 
     * @brief Send request to approve selected comments
     */
    var publishComment = function(){
      console.log('publishComment');
      
      selected = new Array();     
      id= parseInt($(this).attr('data-comment-id').split('_').slice(-1)[0]);
      
      selected.push(id);
      
      console.log(selected);
      
      data={'selection': selected,
    		'action': 'Approve'};

      $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", ABC.csrf);
	            }
	        }
	    });
	    //Save Form Data........
	    $.ajax({
	        cache: false,
	        url : window.location.origin+"/comments/approve/",
	        type: "POST",
	        dataType : "json",
	        contentType: "application/json;",
	        data : JSON.stringify(data),
	        context : this,
	        success : commentsApproved,
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ');
	            console.log(xhRequest);
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
		return false;
    };
    /**
     * commentsApproved
     * 
     * @brief Comment Approved. Update DOM
     */
    var commentsApproved = function(data){
    	console.log(data);
    	console.log($('.comments-container-item[data-comment-id="cid_'+data[0]+'"]').find('.comment-moderated'));
    	$('.comments-container-item[data-comment-id="cid_'+data[0]+'"]').find('.comment-moderated').remove();
    }
	/*
	 * Load Comments
	 */
	var loadComments = function(){
		$.ajax({
		    // the URL for the request
		    url: window.location.origin+'/comments/'+ABC.post_id+'/',
		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json'
		    },
		 
		    // whether this is a POST or GET request
		    type: "GET",
		 
		    // the type of data we expect back
		    dataType : "json",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: renderComments,
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
		 
		    // code to run regardless of success or failure
		    complete: function( xhr, status ) {
		        //alert( "The request is complete!" );
		    }
		});
	};
	
	var scrollNav = function(e) {
		e.preventDefault();
		console.log('scrollNav');
		$('html, body').stop().animate({
	        scrollTop: $('#article-adjunct-tab-comments').offset().top
	    }, 1000);
		
		return(false);
	}
	
	/**
	 * Load form 
	 */
	loadForm();
	
	/**
	 * Load comments
	 */
	loadComments();
	
	/**
	 * Handle tabs
	 */
	$('.article-adjunct-nav--item a').on('click', function(e)  {
        var currentAttrValue = $(this).attr('href');
 
        // Show/Hide Tabs
        $(currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        $(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });
	
	$('#article-actions__gotoComments').on('click', scrollNav);
});
