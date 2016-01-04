(function ($) {

var toInt = function (value, defaultValue) {
	var parsed = parseFloat(value);
	return isNaN(parsed) ? defaultValue : parsed;
};

var showCharacterCount = function ($counter, $source, initial) {
	var text = $source.val();
	var length = text ? text.length : 0;
	var error =
		length > toInt($counter.data('max-limit'), Infinity) ||
		length < toInt($counter.data('min-limit'), -Infinity)
	;
	$counter.text(length);
	var $fg = $counter.closest('.form-group').toggleClass('has-error', error);
	if (!initial) {
		$fg.closest('form').find('input[type="submit"]')
			.prop('disabled', error);
	}
};

$('.character-counter .character-count-display').each(function () {
	var $counter = $(this);
	$source = $('textarea#' + $counter.data('source-id'));
	$source.on('input change', function () {
		showCharacterCount($counter, $(this));
	});
	showCharacterCount($counter, $source);
});

})(jQuery);
