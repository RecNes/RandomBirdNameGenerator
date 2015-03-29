/**
 * Created by sencer on 28.03.2015.
 */

$('#rabn').click(function(){
    $.get('/bird_name_requested/', {}, function(data){
        var bn = $('#bn');
        var sbn = $('#show_bird_name');
        sbn.fadeOut(function() {
            bn.html(data);
        });
        sbn.fadeIn();
    });
});

$("div#show_bird_name").zclip({
    path:'{{ STATIC_URL }}js/ZeroClipboard.swf',
    copy:$('h3#bn').text(),
    beforeCopy:function(){
        $('.info').fadeOut();
    },
    afterCopy:function(){
        $('.check').fadeIn();
    }
});

