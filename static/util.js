var TextThemUtil = {}

TextThemUtil.US_CA_PHONE_NO_REGEX = /^1[\s.\-]?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}$/;
TextThemUtil.MESSAGE_CHAR_LIMIT = 141
$(document).ready(function() { 

    $('#Cell_phone').hide();
    $('#Cell_phone').each(function(i) {
        if (this.complete) {
            $(this).fadeIn("slow");
        } else {
            $(this).load(function() {
                $(this).fadeIn("slow");
            });
        }
    });
});
