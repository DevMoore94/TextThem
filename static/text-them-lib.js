//UTILITY FUNCTIONS AND VARIABLES
var TextThemUtil = {}

TextThemUtil.US_CA_PHONE_NO_REGEX = /^1[\s.\-]?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}$/;
TextThemUtil.MESSAGE_CHAR_LIMIT = 141

//FEATURE LIBRARY
function updateMessage(message){
    $("#InputMessage").val(message);
	$("#InputMessage").trigger('change');
}

function updateError(message){
    $(".error").text(message);
    $(".error").fadeOut(1500, function(){
        $(".error").text("");
        $(".error").removeAttr("style");
    });
}

function clearMessage(){
    updateMessage("")
}

function getRandom() {
	$.getJSON("/RandomGenerator", function(response) {
		var adjective = response.adjective;
		var noun = response.noun;
        updateMessage(adjective + " " + noun)
	});
}


function getRickRoll() {
    var message = "Never Gonna Give You Up, Never Gonna Let you Down: http://goo.gl/zPOD";
    updateMessage(message)
}



function getLocation(){
 if(navigator.geolocation){
     navigator.geolocation.getCurrentPosition(showPosition);
 } else {
     return null
 }
}

function showPosition(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    var path = "http://maps.google.com"
    var message = "Find me @ "+path+"/maps?q="+lat+", "+lng
    updateMessage(message)  
}
