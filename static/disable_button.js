
function updateSubmitStatus() {
	if($("#InputNumber").parent().hasClass("has-success") && $("#InputMessage").parent().hasClass("has-success")){
		$("#submit_button").removeClass("disabled");
	} else{
		$("#submit_button").addClass("disabled");
	}
}


$(document).ready(function() {


	$("#InputNumber").on("change keyup paste click", function(){
		var current_number = $(this).val();

		if(current_number.match(TextThemUtil.US_CA_PHONE_NO_REGEX)){
			$(this).parent().removeClass("has-error");
			$(this).parent().addClass("has-success");
		}else {
			$(this).parent().removeClass("has-success");
			$(this).parent().addClass("has-error");
		}


		updateSubmitStatus();
	});

	$("#InputMessage").on("change keyup paste click", function(){
		var current_message = $(this).val();
		if(current_message.length > 0 && current_message.length < TextThemUtil.MESSAGE_CHAR_LIMIT){
			$(this).parent().removeClass("has-error");
			$(this).parent().addClass("has-success");
		} else {
			$(this).parent().removeClass("has-success");
			$(this).parent().addClass("has-error");
		}
		updateSubmitStatus();
	});

	$("form").bind("keyup keypress", function(e) {
		var code = e.keyCode || e.which; 
		if (code  == 13) {               
			e.preventDefault();
			return false;
		}
	});

});
