/* Polyfill for hasAttribute */
if (!Element.prototype.hasAttribute) {
  Element.prototype.hasAttribute = function (name) {
    return this.getAttribute(name) !== null;
  };
}

(function ($) {

$('#language-select').change(function () {
  $(this).closest('form').submit();
});

})(jQuery);
