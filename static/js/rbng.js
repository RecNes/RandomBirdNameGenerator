/**
 * Created by Sencer Hamarat on 28.03.2015.
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('#bird_name_form').submit(function(){
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken);
    var sc = $('#get_scientific').prop('checked');
    var cn = $('#counter');
    var bn = $('#bird_name');
    var sn = $('#scientific_name');
    var sbn = $('#show_bird_name');
    $.post('/bird_name_requested/', {'sci_check': sc, 'csrfmiddlewaretoken': csrftoken}, function(data){
        sbn.fadeOut(function() {
            $('.check').hide();  // hide "copied to clipboard" message
            sn.html('').hide();  // If checkbox unchecked clean object html and hide object
            var splited_data = data.split(",");
            bn.html(splited_data[0]);
            if (sc){
                sn.html(splited_data[1]).show();
                cn.html(splited_data[2]);
            } else {
                cn.html(splited_data[1]);
            }
            $('#copy-button').attr("data-clipboard-text", data).show();
        });
        sbn.fadeIn();
    });
});

var client = new ZeroClipboard( document.getElementById("copy-button") );

client.on( "ready", function( readyEvent ) {
    client.on( "aftercopy", function( event ) {
        $('#copy-button').hide();
        $('.check').show();
  });
});