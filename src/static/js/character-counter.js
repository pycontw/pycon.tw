(function ($) {

var showCharacterCount = function ($counter, $source) {
	var text = $source.val();
	var length = text ? text.length : 0;
	$counter.text(length);
	$counter.closest('.form-group').toggleClass(
		'has-error', length > parseInt($counter.data('limit')));
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
