(function ($) {
	$(function() {
		var $hashTab = $('.js-hash-tabs');
		if ($hashTab.length === 0) { return }

		if(location.hash) {
			$hashTab.find('a[href=' + location.hash + ']').tab('show');
		}

		$($hashTab).on("shown.bs.tab", function(e) {
			location.hash = e.target.getAttribute("href");
		});

		$(window).on('popstate', function() {
			var anchor = location.hash || $hashTab.find("a[data-toggle=tab]").first().attr("href");
			$hashTab.find('a[href=' + anchor + ']').tab('show');
		});

	});
})(jQuery);
