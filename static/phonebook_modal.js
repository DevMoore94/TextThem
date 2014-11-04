$(document).ready(function(){

	$('#phonebookModal').on('hidden.bs.modal', function () {
          var str = ($("#contactForm input[type='radio']:checked").val());
          var str_parsed = str.split(" - ")
          $('#InputNumber').val(str_parsed[1])
          $('#InputNumber').trigger('change');
        })
});