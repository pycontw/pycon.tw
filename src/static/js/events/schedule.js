(function ($) {

// $('.talk__title').addClass('hyphenate');
// Hyphenator.config({useCSS3hyphenation: true});
// Hyphenator.run();

$('.talk__title').dotdotdot({wrap: 'word', watch: true, fallbackToLetter: true});

// Scrollspy-like behavior to update the hash on scroll.
if (window.history && window.history.replaceState) {
	$(document).on('scroll', function () {
		var $document = $(this);
		var ids = ['2016-06-05', '2016-06-04', '2016-06-03'];
		var hash = '';
		$.each(ids, function () {
			if ($document.scrollTop() >= $('#' + this).offset().top - 1) {
				hash = '#' + this;
				return false;
			}
		});
		if (hash !== window.location.hash) {
			var nurl = window.location.pathname + window.location.search;
			window.history.replaceState('', '', nurl + hash);
		}
	});
}

})(jQuery);
