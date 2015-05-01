$().ready(function() {

	$("#matt-sucks").click(function(e) {

		console.log("well matt sucks so");

		$.post("/servo_post");

		// $.ajax({
		//   type: "POST",
		//   url: "../send_sms.py",
		//   data: { }
		// }).done(function( o ) {
		//    // do something
		// });

		// var jqxhr = $.ajax( "../send_sms.py" )
		//   .done(function() {
		//     alert( "success" );
		//   })
		//   .fail(function() {
		//     alert( "error" );
		//   })
		//   .always(function() {
		//     alert( "complete" );
		//   });

	});


});