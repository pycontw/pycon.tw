(function ($, SimpleMDE) {

$('.markdown-field').not('.markdown-field-rendered').each(function () {
	this.innerHTML = SimpleMDE.prototype.markdown(
		this.textContent || this.innerText);
	$(this).addClass(
		'markdown-field-rendered ' +
		'editor-preview ' +
		'editor-preview-active');
});

})(jQuery, SimpleMDE);
