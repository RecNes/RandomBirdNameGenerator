/**
 * Created by sencer on 28.03.2015.
 */

$('#rabn').click(function(){
    $.get('/bird_name_requested/', {}, function(data){
        var bn = $('#bn');
        var sbn = $('#show_bird_name');
        sbn.fadeOut('slow', function() {
            bn.html(data);
        });
        sbn.fadeIn();
    });
});

//ZeroClipboard.config( { swfPath: "/static/js/zcb/ZeroClipboard.swf" } );
//
//$('#show_bird_name').click(function () {
//    var client = new ZeroClipboard( document.getElementById("bn") );
//    client.on( "ready", function( readyEvent ) {
//        alert( "ZeroClipboard SWF is ready!" );
//        client.on( "aftercopy", function( event ) {
//            `this` === `client`
//            `event.target` === the element that was clicked
//            event.target.style.display = "none";
//            alert("Copied text to clipboard: " + event.data["text/plain"] );
//        } );
//    } );
//});

