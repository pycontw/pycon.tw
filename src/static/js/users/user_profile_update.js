(function ($) {

$('#id_photo').addClass('upload-btn-shadowed').change(function () {
	var name = $(this).val();
	var match = name.match(/[\/\\]([^\/\\]+)$/);
	if (match) {
		name = match[1];
	}
	$('#' + $(this).data('value-display')).text(name);
}).siblings('span').removeClass('hide');

})(jQuery);
