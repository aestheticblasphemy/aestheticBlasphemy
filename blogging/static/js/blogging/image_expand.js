$(document).ready(function(){
	
	var bindToEscape = function(event){
    	/* Bind to both command (for Mac) and control (for Win/Linux) */
    	if (event.keyCode == 27) {          
    		minimize();
    	}	
    };
    
    var minimize = function(e){
    	$("#img-modal").modal('hide');
    	/* Rebind maximize */
    	$('.img-max').bind('click', maximize);
    };
		
	var maximize = function(e){
		/* Get the sibling image and add it to overlay element */
		
		obj = $('img', $(this).parent()).clone();
		$("#img-modal").prepend(obj);
		
		/* trigger overlay */		
		$("#img-modal").modal('show');
		
		/* unbind maximize */
		$('.img-max').unbind('click', maximize);
		window.addEventListener('keydown', bindToEscape);
		
		/* bind restore on click anywhere or escape */
		$('.img-max').bind('click', minimize);
		
		e.stopPropagation();
		return(false);
	};
	
	/* Find images inside `article` */
	images = $('article img');

	for (i= images.length - 1; i>=0;i--){
		/* If their parents are not 'p' Wrap them in divs. Add a maximize icon to all */
		if(!$(images[i]).parent().is('p')){
			$(images[i]).wrap('<div class="center-block"></div>');
			$('<span class="fix-rb maximize icon pl-expand img-max"></span>').insertAfter($(images[i]));
		}
		else{
			$('<span class="fix-rb maximize icon pl-expand img-max"></span>').insertAfter($(images[i]));
		}
	}
	/* Bind buttons to open overlay and show image in fullscreen */
	$('.img-max').bind('click', maximize);
	
});
