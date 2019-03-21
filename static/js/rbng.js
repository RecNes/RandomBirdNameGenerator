/**
 * Created by Sencer Hamarat on 28.03.2015.
 */

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$('#bird_name_form').submit(function(){
    var csrftoken = getUrlParameter('csrfmiddlewaretoken');
    // var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    var sc = $('#get_scientific').prop('checked');
    var cn = $('#counter');
    var bn = $('#bird_name');
    var sn = $('#scientific_name');
    var sbn = $('#show_bird_name');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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