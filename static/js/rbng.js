/**
 * Created by Sencer Hamarat on 28.03.2015.
 */

$('#bird_name_form').submit(function () {
    var csrftoken = $.cookie('csrftoken');
    var sc = $('#get_scientific').prop('checked');
    var cn = $('#counter');
    var bn_div = $('#bn_div');
    var bn = $('#bird_name');
    var sn_div = $('#sn_div');
    var sn = $('#scientific_name');
    var sbn = $('#show_bird_name');
    $.post('/bird_name_requested/', {'sci_check': sc, 'csrfmiddlewaretoken': csrftoken}, function (data) {
        sbn.fadeOut(function () {
            $('.check').hide();  // hide "copied to clipboard" message
            bn_div.hide();  // If checkbox unchecked clean object html and hide object
            bn.html('');
            sn_div.hide();  // If checkbox unchecked clean object html and hide object
            sn.html('');

            var splited_data = data.split(",");

            bn.html(splited_data[0]);
            bn_div.show();
            if (sc) {
                sn.html(splited_data[1]);
                sn_div.show();
                cn.html(splited_data[2]);
            } else {
                cn.html(splited_data[1]);
            }
            $('#copy-button').show();
        });
        sbn.fadeIn();
    });
});

function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    $("#show_bird_name").appendChild(textArea);
    // document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        // console.log('Fallback: Copying text command was ' + msg);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
}

function copyTextToClipboard(text) {
    // console.log(text);
    if (!navigator.clipboard) {
        fallbackCopyTextToClipboard(text);
        return;
    }
    navigator.clipboard.writeText(text).then(function () {
        // console.log('Async: Copying to clipboard was successful!');
        var copied = $('.check');
        copied.show();
        copied.delay(750).fadeOut();

    }, function (err) {
        console.error('Async: Could not copy text: ', err);
    });
}
