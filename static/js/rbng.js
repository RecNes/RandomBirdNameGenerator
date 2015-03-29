/**
 * Created by sencer on 28.03.2015.
 */

$('#rabn').click(function(){
    $.get('/bird_name_requested/', {}, function(data){
        var bn = $('#bn');
        var sbn = $('#show_bird_name');
        $('.check').hide();
        sbn.fadeOut(function() {
            bn.html(data);
            $('#copy-button').attr("data-clipboard-text", data).show();
        });
        sbn.fadeIn();
    });
});

var client = new ZeroClipboard( document.getElementById("copy-button") );

client.on( "ready", function( readyEvent ) {
    client.on( "aftercopy", function( event ) {
//        event.target.style.visibility = "hidden";
        $('#copy-button').hide();
        $('.check').show();
  });
});