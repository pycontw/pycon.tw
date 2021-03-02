(function ($) {

    if ($('select#id_recording_policy').find(':selected').val() == 'True') {
        $('#div_id_live_stream_policy').hide();
        $('select#id_live_stream_policy').val('True');
    }

    $('select#id_recording_policy').change(function(e){
        if ($(this).val() == 'False') {
            $('#div_id_live_stream_policy').fadeIn();
            $('select#id_live_stream_policy').val('False');
        } else {
            $('#div_id_live_stream_policy').fadeOut();
            $('select#id_live_stream_policy').val('True');
        }
    });

})(jQuery);