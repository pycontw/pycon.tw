(function ($) {

$('#language-select').change(function () {
  $(this).closest('form').submit();
});

$('.script-only').show();

})(jQuery);
