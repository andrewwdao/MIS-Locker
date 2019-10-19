
$(document).ready(function(){
	$("#cancel").on("click", function() {
		$( "#connect" ).slideUp( "fast", function() {});
		$( "#connect_manual" ).slideUp( "fast", function() {});
		$( "#wifi" ).slideDown( "fast", function() {});
	});

	$("#ok-credits").on("click", function() {
		$( "#credits" ).slideUp( "fast", function() {});
		$( "#app" ).slideDown( "fast", function() {});
		
	});
	
	$("#acredits").on("click", function() {
		$( "#app" ).slideUp( "fast", function() {});
		$( "#credits" ).slideDown( "fast", function() {});
	});
})