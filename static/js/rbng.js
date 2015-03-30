/**
 * Created by Sencer Hamarat on 28.03.2015.
 */

var csrftoken = $.cookie('csrftoken');

$('#bird_name_form').submit(function(){
    var sc = $('#get_scientific').prop('checked');
    var bn = $('#bird_name');
    var sn = $('#scientific_name');
    var sbn = $('#show_bird_name');
    $('.check').hide();
    $.post('/bird_name_requested/', {'sci_check': sc, 'csrfmiddlewaretoken': csrftoken}, function(data){
        sbn.fadeOut(function() {
            sn.html('').hide();  // If checkbox unchecked clean object html and hide object
            if (sc){
                var splited_data = data.split(",");
                bn.html(splited_data[0]);
                sn.html(splited_data[1]).show();
            } else {
                bn.html(data);
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