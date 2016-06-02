(function ($) {

$('.talk__title').addClass('hyphenate');
Hyphenator.config({useCSS3hyphenation: true});
Hyphenator.run();

$('.talk__title').dotdotdot({'wrap': 'letter'});

})(jQuery);
