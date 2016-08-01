$(document).ready(function(){
	var showSidebar = function(){
		$('#siteNavCollapse').addClass('slidein');
		return (false);
	};
	
	var hideSidebar = function(){
		$('#siteNavCollapse').removeClass('slidein');
		return(false);
	};
	
	$('#navSlide').on('click', showSidebar);
	$('#navSlideback').on('click', hideSidebar);
	
	$('.collapse-container').on('show.bs.collapse', function () {
		$(this).siblings('.collapse-container').collapse('hide');
	});
});