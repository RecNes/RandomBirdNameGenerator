/**
 * Created by sencer on 28.03.2015.
 */

//function display_random_bird_name() {
//    $.get('/rango/like_category/', {}, function(data){
//        $('#generated_bird_name').html(data);
//    });
//}

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


$('#show_bird_name').click(function () {
    var text_val = $('#bn').text();
    var r;
    alert(text_val);
    r = text_val.createTextRange();
    r.execCommand('copy');
});

//    holdtext.innerText = copytext.innerText;
//    Copied = holdtext.createTextRange();
//    Copied.execCommand("Copy");
