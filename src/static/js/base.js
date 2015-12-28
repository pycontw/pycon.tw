(function ($) {

$('#language-select').change(function () {
  $(this).closest('form').submit();
});

})(jQuery);
