(function ($) {

var $hashTab = $('.js-hash-tabs');
if (!window.localStorage || $hashTab.length === 0) {
	return;
}

var getTab = function () {
	return localStorage.getItem('review_proposal_tab');
};

$hashTab.on('shown.bs.tab', function(e) {
	localStorage.setItem('review_proposal_tab', e.target.getAttribute('href'));
});

var tab = getTab();
if (tab) {
	$hashTab.find('a[href=' + tab + ']').tab('show');
}
$(window).on('popstate', function() {
	var tab = getTab() || $hashTab.find("a[data-toggle=tab]").attr('href');
	$hashTab.find('a[href=' + tab + ']').tab('show');
});

})(jQuery);
