/**
 * Created by Sencer Hamarat on 28.03.2015.
 */

$('#bird_name_form').submit(function () {
    let csrftoken = $.cookie('csrftoken');
    let sc = $('#get_scientific').prop('checked');
    let cn = $('#counter');
    let bn_div = $('#bn_div');
    let bn = $('#bird_name');
    let sn_div = $('#sn_div');
    let sn = $('#scientific_name');
    let sbn = $('#show_bird_name');

    // $.get('/bnapi/', {'format': 'json'},
    $.ajax({url: "/bnapi/?format:json"}).then(
        function (data) { // 'csrfmiddlewaretoken': csrftoken
            console.log(data);
            sbn.fadeOut(function () {
                $('.check').hide();  // hide "copied to clipboard" message
                bn_div.hide();  // If checkbox unchecked clean object html and hide object
                bn.html('');
                sn_div.hide();  // If checkbox unchecked clean object html and hide object
                sn.html('');

                let splited_data = data.split(",");

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


const copyTextToClipboard = str => {
    const cbel = document.createElement('textarea');    // Create a textarea element
    cbel.style.position = 'absolute';
    cbel.style.left = '-9999px';                        // Move outside of the screen to make invisible
    cbel.value = str;                                   // Set its value to that you want copied
    cbel.setAttribute('readonly', '');                  // Making it readonly to be anti-tamper
    document.body.appendChild(cbel);                    // Append the <textarea> element to the HTML document
    const selected =
        document.getSelection().rangeCount > 0          // Check if there is any content selected previously
            ? document.getSelection().getRangeAt(0)     // Store selection if found
            : false;                                    // Mark as false to know no selection existed before
    cbel.select();                                      // Select the <textarea> content
    document.execCommand('copy');                       // Copy - only works as a result of a user action (e.g. click events)
    let copied = $('.check');
    copied.show();
    copied.delay(750).fadeOut();
    document.body.removeChild(cbel);                    // Remove the textarea element
    if (selected) {                                     // If a selection existed before copying
        document.getSelection().removeAllRanges();      // Unselect everything on the HTML document
        document.getSelection().addRange(selected);     // Restore the original selection
    }
};