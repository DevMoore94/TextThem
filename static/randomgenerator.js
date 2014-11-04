var noun = null;
var adjective = null;

function get_random() {
	$.getJSON("/RandomGenerator", function(response) {
		adjective = response.adjective;
		noun = response.noun;
	});
}


function set_text() {
	$("#InputMessage").val(adjective + " " + noun);
	get_random();
}

$(document).ready( function() {
	get_random();
});
