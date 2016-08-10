
jQuery(document).ready(function() {
	
	$.backstretch([
					  "/static/img/homepage1.jpg"
					, "/static/img/homepage2.jpg"
				  	, "/static/img/homepage3.jpg"
				 ], {duration: 3000, fade: 750});

	$('.form-signin input[type="text"], .form-signin input[type="password"], .login-form textarea').on('focus', function() {
		$(this).removeClass('input-error');
	});
	
	$('.form-signin').on('submit', function(e) {
		
		$(this).find('input[type="text"], input[type="password"], textarea').each(function(){
			if( $(this).val() == "" ) {
				e.preventDefault();
				$(this).addClass('input-error');
			}
			else {
				$(this).removeClass('input-error');
			}
		});
		
	});
	
	
});
