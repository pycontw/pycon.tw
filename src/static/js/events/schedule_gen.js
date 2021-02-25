(function ($) {

var $form = $('.generation-form');
$form.removeClass('hide');
$form.find('input[name="html"]').val($('.schedule').html());

})(jQuery);
