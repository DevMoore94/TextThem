function updateSubmitStatus(){
	if($("#InputNumber").parent().hasClass("has-success") && $("#InputName").parent().hasClass("has-success")){
		$("#addContactbtn").removeClass("disabled");
	} else{
		$("#addContactbtn").addClass("disabled");
	}
}

$(document).ready(function(){


	$("#InputNumber").on("change keyup paste click", function(){
		var current_number = $(this).val();

		if(current_number.length > 0){
			$(this).parent().removeClass("has-error");
			$(this).parent().addClass("has-success");
		} else {
			$(this).parent().removeClass("has-success");
			$(this).parent().addClass("has-error");
		}
		updateSubmitStatus();

	});

	$("#InputName").on("change keyup paste click", function(){
		var current_message = $(this).val();
		if(current_message.length > 0){
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