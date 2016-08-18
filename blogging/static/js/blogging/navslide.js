$(document).ready(function(){
	var showSidebar = function(){
		$('#siteNavCollapse').addClass('slidein');
		$('html').on('click', clickHideSidebar);
		return (false);
	};
	
	var hideSidebar = function(){
		$('#siteNavCollapse').removeClass('slidein');
		$('html').off('click', clickHideSidebar);
		return(false);
	};
	
	var clickHideSidebar = function(e) {
		  var target = $(e.target);

		  if(target.closest('#siteNavCollapse').length === 0){
		  /*if ($('#siteNavCollapse').hasClass('slidein')) {*/
		    hideSidebar();
		  }
		};
	
	$('#navSlide').on('click', showSidebar);
	$('#navSlideback').on('click', hideSidebar);
	
	$('.collapse-container').on('show.bs.collapse', function () {
		$(this).siblings('.collapse-container').collapse('hide');
	});
});