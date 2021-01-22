$(document).ready(function () {
    $(".radio_option").change(function () {

        if ($('#optionsRadios2').prop("cheked")) {
            $('#mask').fadeIn(300);
        } else {
            $('#mask').fadeOut(300);
        }
    });
});