(function ($) {

$('.proposal-form').areYouSure({
	'message': 'Are you sure you want to leave this page?'
});

})(jQuery);

// Scroll progress.
(function ($) {

// Calculate scroll checkpoints.
var last;
var cp = [];
$('.proposal-form .form-group').each(function () {
	cp.push($(this).offset().top - 40);
	last = this;
});
cp.shift();
cp.push($(last).offset().top + $(last).height());


function updateScrollProgress() {
	var offset = $(this).scrollTop() + $(this).height();
	var tot = cp.length;
	var $widget = $('#proposal-scroll-progress-widget');

	// Calculate current progress.
	for (var i = 0; i < tot && cp[i] < offset; i++);
	var rat = i * 1.0 / tot;

	// Apply progress to UI.
	$('.text', $widget).html('<span class="current">' + i + '</span> / ' + tot);
	$('.top', $widget).height($widget.height() * (1.0 - rat));
}

$(window).scroll(updateScrollProgress);
updateScrollProgress();

})(jQuery);
