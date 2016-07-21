$(document).ready(function(){
	var showSidebar = function(){
		console.log('showSidebar');
		$('#siteNavCollapse').addClass('slidein');
		return (false);
	};
	
	var hideSidebar = function(){
		console.log('hideSidebar');
		$('#siteNavCollapse').removeClass('slidein');
		return(false);
	};
	
	$('#navSlide').on('click', showSidebar);
	$('#navSlideback').on('click', hideSidebar);
});