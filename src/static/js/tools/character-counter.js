(function ($) {

var toInt = function (value, defaultValue) {
	var parsed = parseInt(value);
	return isNaN(parsed) ? defaultValue : parsed;
};

var showCharacterCount = function ($counter, $source) {
	var $fg = $source.closest('.form-group');
	var text = $source.val();
	var length = text ? eastasianwidth.length(
		text.replace(/^\s+|\s+$/g, '').replace(/\r?\n/g, '\r\n')) : 0;

	var max = toInt($counter.data('maxlength'), Infinity);
	$counter.text(isFinite(max) ? length + ' / ' + max : length);

	var min = $fg.find('label').hasClass('requiredField') ? 1 : -Infinity;
	var error = length > max || length < min;

	$fg.toggleClass('has-error', error)
		.closest('form')
		.find('input[type="submit"],button[type="submit"]')
		.prop('disabled', error);
};

$('textarea.character-counted')
		.not('*[disabled]').not('.character-counter-enabled')
		.each(function () {
	var $source = $(this);
	var $counter = $('#character-counter-template')
		.clone().removeClass('hide').removeAttr('id').insertAfter($source)
		.find('.character-counter').data('maxlength', $source.attr('maxlength'));
	$counter.next('.character-counter-tooltip').tooltip();

	$source.removeAttr('maxlength').on('input change', function () {
		showCharacterCount($counter, $(this));
	});
	showCharacterCount($counter, $source);
	$source.addClass('character-counter-enabled');
});

})(jQuery);
