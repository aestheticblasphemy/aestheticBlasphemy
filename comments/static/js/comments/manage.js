/**
 * @file manage.js
 * 
 * @brief Comment Management Commands
 */
var ABC = ABC || new GlobalSiteContainer();
$(document).ready(function(){
	
	var csrfSafeMethod = function(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	
    /**
     * Select All checkbox functionality
     */
    $('#checkall_id').on('click',function(){
        if(this.checked){
            $('.checkbox').each(function(){
                this.checked = true;
            });
        }else{
             $('.checkbox').each(function(){
                this.checked = false;
            });
        }
    });
    
    /**
     * Conditionally filter down each checkbox. Update state of global checkbox
     */
    $('.checkbox').on('click',function(){
        if($('.checkbox:checked').length == $('.checkbox').length){
            $('#checkall_id').prop('checked',true);
        }else{
            $('#checkall_id').prop('checked',false);
        }
    });
    
    
    /**
     * approveComments
     * 
     * @brief Send request to approve selected comments
     */
    var approveComments = function(){
      console.log('approveComments');
      
      selected = new Array();     
      $("input[name='selection']:checked").each(function(){
    	    selected.push($(this).val());
      	  });
      
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
        $("input[name='selection']:checked").each(function(){
        	$(this).parents('tr').find('.publish-state').css('color', 'green');
        	$(this).parents('tr').find('.publish-state').removeClass('fa-times');
        	$(this).parents('tr').find('.publish-state').addClass('fa-check');
      	});
    }

    /**
     * deleteComments
     * 
     * @brief Send request to delete selected comments
     */
    var deleteComments = function(){
      console.log('approveComments');
      
      selected = new Array();     
      $("input[name='selection']:checked").each(function(){
    	    selected.push($(this).val());
      	  });
      
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
	        success : commentsDeleted,
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
     * commentsDeleted
     * 
     * @brief Comments Deleted. Update DOM
     */
    var commentsDeleted = function(data){
    	console.log(data);
    	
    	location.reload();
    }
    
    /**
     * unpublishComments
     * 
     * @brief Send request to unpublish selected comments
     */
    var unpublishComments = function(){
      console.log('unpublishComments');
      
      selected = new Array();     
      $("input[name='selection']:checked").each(function(){
    	    selected.push($(this).val());
      	  });
      
      data={'selection': selected,
      		'action': 'Unpublish'};
      
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
	        success : commentsUnpublished,
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
     * commentsUnpublished
     * 
     * @brief Comments Unpublished. Update DOM
     */
    var commentsUnpublished = function(data){
    	console.log(data);
    	console.log($("input[name='selection']:checked"))
        $("input[name='selection']:checked").each(function(){
        	$(this).parents('tr').find('.publish-state').css('color', 'red');
        	$(this).parents('tr').find('.publish-state').removeClass('fa-check');
        	$(this).parents('tr').find('.publish-state').addClass('fa-times');
      	});
    }
    
    /**
     * commitActions
     * 
     * @brief Get what was selected from the management options and invoke its 
     * respective method.
     */
    var commitActions = function(e){
       console.log('Commit Actions');
       action = $('select[name="action"]').val();
       if (action === 'Approve'){
    	   approveComments();
       }
       else if(action==='Unpublish'){
    	   unpublishComments();
       }
       else if(action==='Delete'){
    	   deleteComments();
       }
    };
    
    $('#save_actions').on('click', commitActions);
});