/* Polyfill for hasAttribute */
if (!Element.prototype.hasAttribute) {
  Element.prototype.hasAttribute = function (name) {
    return this.getAttribute(name) !== null;
  };
}

/* Language selection on the navbar */
/* When the Javascript is enabled. Hide the select version.
 * Otherwise, use the fancier dropdown solution.
 */
(function ($) {

	/* Hide the form-based language selector and show the ul-based one. */
	$('form.navbar-lang').hide();
	$('ul.navbar-lang').show();

	/* Set the correct language option to the hidden form and submit. */
	$('ul.navbar-lang ul.dropdown-menu a').click(function() {
		var $this = $(this);
		$('#language-select')
			.val($this.data('lang'))
			.parents('form').submit();
	});

	/* The form-based selector without clicking the "Change" button. */
	$('#language-select').change(function () {
		$(this).closest('form').submit();
	});

})(jQuery);
