/**
 * @file baseloader.js
 * @brief Base container instance for all site specific objects.
 */
function GlobalSiteContainer(){
	this.user = {
            id: "0",
            username: "Guest",
            gravatar: "images/male.png",
            url: "#",
        };
	
	this.setupUser = function(user){
		//console.log('In setupUser');
	    if(!('id' in user)){
	        ABC.user = {
	                id: "0",
	                username: "Guest",
	                gravatar: "images/male.png",
	                url: "#",
	            };
	    }
	    else{
	        ABC.user = user;
	    };
	  };

	  this.getCurrentUser = function getCurrentUser(){
	    //console.log('In getCurrentUser');
	    $.ajax({
	        url: '/rest/users/current/',
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
	        success: this.setupUser,

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
		
	  this.getCookie = function(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie != '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = jQuery.trim(cookies[i]);
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) == (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		};
	
	Object.defineProperties(this, {
								'csrf':{ 
									'get': function(){
											return (this.getCookie('csrftoken'));
											},
								},
		});
	
}; /* ABC = AestheticBlasphemyContainer*/

var ABC = ABC || new GlobalSiteContainer();

/* Actually call this function on Document Ready */
(function($){
    $.fn.ready(function(){
    	//console.log('Try to get current user');
        ABC.getCurrentUser();
        //console.log(ABC.csrf);
      });
})(window.jQuery);
