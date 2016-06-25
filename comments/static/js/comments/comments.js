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
	 * postComment
	 * @brief : Posts an annotation.
	 * 
	 * This is a fixture right now, all it does is receive and check sanity of annotation and call the
	 * renderAnnotation method as if the server responded with a valid response.
	 */
	var postComment = function(e){
		e.preventDefault();
		console.log('postComment');
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
		post = $("#id_post option:selected").val();
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
				parent_comment: null,
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
	        success : renderSingleAnnotation,
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ');
	            console.log(xhRequest);
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
		
		/* Clear out form contents, if any. */
	    e.stopPropagation(); 
		return false;
	}
		
	/**
	 * removeAnnotation
	 * @param data
	 */
	var removeAnnotation = function(data){
		//console.log('Remove Annotation response');
		//console.log(data);
	};
	
	/**
	 * deleteAnnotation
	 * @param id: ID of paragraph to remove
	 */
	var deleteAnnotation = function(id){
		id= parseInt($(this).attr('data-comment-id'));
		//console.log('Deleting annotation' + id);
		
		$.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", annotations.csrftoken);
	            }
	        }
	    });
	    //Save Form Data........
	    $.ajax({
	        cache: false,
	        url : "/rest/annotations/"+id+"/",
	        type: "DELETE",
	        dataType : "json",
	        contentType: "application/json;",
	        //data : JSON.stringify(data),
	        context : this,
	        success : removeAnnotation,
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ' + xhRequest + "\n");
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
	    
	    /* Update annotation count on adjoining container */
	    //console.log($(this).closest('.comments').find('.comments--toggle p'));
	    commentCount = parseInt($(this).closest('.comments').find('.comments--toggle p').text());
	    //console.log('Comment Count now is '+ commentCount);
	    if((commentCount -1)==0){
	    	$(this).closest('.comments').find('.comments--toggle p').text('+');
	    }
	    else{
	    	$(this).closest('.comments').find('.comments--toggle p').text(commentCount -1);
	    }
	    
	    /* Remove the annotation from flow */
	    $(this).closest('.comments-container-item').remove();
		return false;
	};
	/**
	 * renderSingleAnnotation
	 * @param data : Payload received from the server
	 * @brief Loads annotations in their respective containers.
	 * 
	 */
	var renderSingleAnnotation = function(data){
		data_list = [data];
		renderAnnotations(data_list);
		return false;
	}
	/**
	 * renderAnnotations
	 * @param data : Payload received from the server
	 * @brief Loads annotations in their respective containers.
	 * 
	 */
	var renderAnnotations = function(data){
		console.log('renderAnnotations');
		console.log('Data received: ');
		console.log(data);
		console.log('Length: '+ data.length);
		if (annotationCopy == null){
			/* Create a fresh copy of the variable*/
			//console.log('It is null. Make a new one');
			annotationCopy = $('#commentable-container');
			//console.log(annotationCopy);
		}
		for(i=0; i< data.length;i++){
//			console.log(annotationCopy.children('[data-section-id="'+data[i]['paragraph_id']+'"]'));
			/* Find the parent container */

			currentObject = annotationCopy.children('[data-section-id="'+data[i]['paragraph']+'"]');
			/* Find the annotations container inside that and append the comment */
			currentComment = $('<div class="comments-container-item">'+
                    			'<div class="comments-container--media">'+
                    				'<img class="comments-author-image" src=""/>'+
            					'</div>'+
            					'<div class="comments-container--block">'+
            					'<a class="comments-author-link" href="#"><span class="comments-author-name"></span></a>'+
            					'<span class="comments-container--text"></span>'+
            					'<div class="comments-control-box">'+
            					'<span class="comments-control comments-delete">Delete</span>'+
            					'<span class="comments-control">Shared with</span>'+
            					'</div>'+
            					'<span class="comments-delete glyphicon glyphicon-remove"></span>'+
            					'</div>'+
            					'</div>');
			
			/* Create the annotation */
			currentComment.find('.comments-author-image').attr('src', data[i]['author']['gravatar']);
			currentComment.find('.comments-author-name').text(data[i]['author']['username']);
			currentComment.find('.comments-author-link').attr('href',data[i]['author']['url']);
			currentComment.find('.comments-container--text').text(data[i]['body']);
			currentComment.find('.comments-delete').attr('data-comment-id', data[i]['id']);
			
			currentComment.find('.comments-delete').on('click', deleteAnnotation);
			/* Also add to main container if the user is a guest. */
			if((parseInt(data[i]['author']['id']) === parseInt(annotations.currentUser['id']))||
					(parseInt(annotations.currentUser['id'])===0)){
				/* Append to main visible list*/
				currentObject.find('[id *="user_annotations_"]').append(currentComment);
			}
			else{
				/* Append to the folded list */
				currentObject.find('[id *="other_annotations_"]').append(currentComment);
				/* Now that we have other annotations, unhide the show button too */
				console.log('Unhide the button');
				
				if(currentObject.find('.comments-bucket-toggle').hasClass('hidden')){
					currentObject.find('.comments-bucket-toggle').removeClass('hidden');
					/* Bind event to show fold or unfold other annotations*/
					currentObject.find('.comments-bucket-toggle').on('click', toggleOtherAnnotations);
				}				
				
				if(!currentObject.find('.comments-bucket-toggle').hasClass('unfolded')){
					currentObject.find('.comments-bucket-toggle').removeClass('unfolded');
					currentObject.find('.comments-bucket-toggle').addClass('folded');
				}
			}
			/* Also append it to the bucket list.*/
			$('#article-adjunct-tab-notes').append(currentComment.clone());
			
			/* Update the annotation count on the button */
			temp = currentObject.find('.comments--toggle p').text();
			//console.log('Comment Count is ' +temp);
			commentCount = ((temp = currentObject.find('.comments--toggle p').text()) ==='+') ? 1 : (parseInt(temp)+1);
			//console.log(currentObject.find('.comments-container'));
			currentObject.find('.comments--toggle p').text(commentCount);
			if(!currentObject.find('.comments--toggle').hasClass('has-annotations') && commentCount > 0)
			{
				currentObject.find('.comments--toggle').addClass('has-annotations');
			}
			//console.log('Updated comment count to '+ commentCount);
		}
		/* Put the variable back to sleep now */
		annotationCopy = null;
		return false;
	};
	
	
	/*
	 * Load Annotations
	 */
	var loadAnnotations = function(){
		/*
		 * At some point of time, this method will be making Ajax queries. For now, it is just calls renderAnnotations directly by passing fixtures.
		 */
		//renderAnnotations(fixtures);
		$.ajax({
		    // the URL for the request
		    url: '/rest/blogcontent/'+annotations.id+'/comments/',
		 
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
		    success: renderAnnotations,
		 
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
	
	
	/**
	 * toggleAnnotations
	 * @param event 
	 * @brief Hides or unhides the annotations depending on their current state.
	 * @detail TODO
	 */
	toggleAnnotations = function(e){
		/* 
		 * If the clicked annotation is the same is the one that was active, we need to close its annotations only,
		 * otherwise we must close it and open the currently active's annotations.
		 */
		activeID = parseInt($(this).parents('.annotation--container').attr('data-section-id'));
		
		/* Hide all other annotations first */
		$('.comments').children('.comments-container').addClass('hidden');
		/* If we clicked on the same bubble, it must collapse, and we return to initial state */
		if(annotations.currentAnnotation === activeID ){
			/* Remove the higlight class from the bubble: .annotation-highlight */
			$(this).removeClass('annotation-highlight');
			$(this).parents("#commentable-container").removeClass('annotations-active');
			annotations.currentAnnotation = 0;
			/*
			 * Unbind 'click anywhere' also from the entire document
			 */
			$(document).unbind('click');
			
			/* hide the form too */
			hideForm();
			return;
		}
		
		/* Else, we've selected a new bubble (and have already hidden everything.)*/
		/* 
		 * We could first find the previous object to remove the annotation-highlight class from it
		 * or we could directly ask jquery to remove that class from all.
		 * That is one reason why Jquery makes things seem very simple, though it might be a preformance hit
		 * internally. 
		 */
		//$('.comments--toggle').removeClass('annotation-highlight');
		/*
		 * If there is no previous annotation selected, then we must bind a 'click anywhere to close' 
		 * event to document.
		 */
		if(annotations.currentAnnotation === 0){
			$(document).on('click', function(e) {
				//console.log($(event.target));
				//console.log($(event.target).closest('.side-comment').length);

				/*
				 * If the element we clicked on is not close to the comments,
				 * close the annotations then.
				 */
				if (!($(e.target).closest('.comments').length)){
					/* Hide all other annotations */
					$('.comments').children('.comments-container').addClass('hidden');
					$('*[data-section-id="'+annotations.currentAnnotation+'"]').find('.comments--toggle').removeClass('annotation-highlight');
					$('#commentable-container').removeClass('annotations-active');
					/* Reset the currently selected Annotation state */
					annotations.currentAnnotation = 0;
					/* Also hide the form */
					hideForm();
					/* unbind this listener too*/
					$(document).unbind('click');
				}
			});
		}
		
		/* OR the other method */
		$('*[data-section-id="'+annotations.currentAnnotation+'"]').find('.comments--toggle').removeClass('annotation-highlight');
		/* Update state variable */
		annotations.currentAnnotation = parseInt($(this).parents('.annotation--container').attr('data-section-id'));
//		console.log('Current Annotation is: ' + annotations.currentAnnotation);
		/* find the parent with classname 'comments' */
		$(this).addClass('annotation-highlight');
		$(this).parent('.comments').children('.comments-container').removeClass('hidden');
		
		/* Add class annotations-active to the parent with ID commentable-container */
		if(!$(this).parents("#commentable-container").hasClass('annotations-active')){
			$(this).parents("#commentable-container").addClass('annotations-active');
		}
		
		/* show the form too */
		showForm(activeID);
		return false;
	};
	
	var bindAnnotations = function(){
		/* Find all annotation toggle buttons and bind the click event to them. */
		$('.comments--toggle').on('click', annotations.toggleAnnotations );
//		console.log('Binding complete');
	};
	
	var wrapContent = function(){
		index = parseInt($(this).attr('id'));
		
		if(!isNaN(index)){
			
			$(this).wrap('<div data-section-id="'+index+'" class="annotation--container clearfix"></div>');
			
			$('<div class="comments clearfix">'+
                '<h3 class="comments--toggle rectangular-speech"><p>+</p></h3>'+
                '<div class="comments-container hidden">'+
                '<div class="comments-container-bucket" id="user_annotations_'+index+'"></div>'+
                '<button class="comments-bucket-toggle folded hidden" type="button"> other annotations</button>'+
                '<div class="comments-container-bucket hidden" id="other_annotations_'+index+'"></div>'+
                '</div>'+
                '</div>').insertAfter($(this));
		}
		//else do not wrap
	};
		
	/*
	 * Load annotations
	 */
//	loadAnnotations();
	
	/*
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
	
	/* Show current active tab */
	$($('.article-adjunct-nav--list').children('.active').children('a').attr('href')).show().siblings().hide();
	
	/* Bind click event */
	$('#post_comment').on('click', postComment);
	
});