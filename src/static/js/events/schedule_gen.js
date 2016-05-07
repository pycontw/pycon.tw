(function ($) {

$('.generation-form').removeClass('hide').submit(function (e) {
	// Fill HTML into the form field.
	$(this).find('input[name="html"]').val($('.schedule').html());
	// Do submit (default action).
});


})(jQuery);
