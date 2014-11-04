function updateSubmitStatus(){
	if($("#InputNumber").parent().hasClass("has-success") && $("#InputName").parent().hasClass("has-success")){
		$("#addContactbtn").removeClass("disabled");
	} else{
		$("#addContactbtn").addClass("disabled");
	}
}

$(document).ready(function(){

	$('#phonebookModal').on('hidden.bs.modal', function () {
          var str = ($("#contactForm input[type='radio']:checked").val());
          var str_parsed = str.split(" - ")
          $('#InputNumber').val(str_parsed[1])
          $('#InputNumber').trigger('change');

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
        })


});