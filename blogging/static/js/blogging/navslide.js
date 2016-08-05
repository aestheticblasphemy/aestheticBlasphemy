$(document).ready(function(){
	var showSidebar = function(){
		$('#siteNavCollapse').addClass('slidein');
		$('body').on('click', clickHideSidebar);
		return (false);
	};
	
	var hideSidebar = function(){
		$('#siteNavCollapse').removeClass('slidein');
		$('body').off('click', clickHideSidebar);
		return(false);
	};
	
	var clickHideSidebar = function(e) {
		  if ($('#siteNavCollapse').hasClass('slidein')) {
		    hideSidebar();
		  }
		  return(false);
		};
	
	$('#navSlide').on('click', showSidebar);
	$('#navSlideback').on('click', hideSidebar);
	
	$('.collapse-container').on('show.bs.collapse', function () {
		$(this).siblings('.collapse-container').collapse('hide');
	});
});