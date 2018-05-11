import $ from 'jquery'

$(() => {

// Schedule generation.
const $form = $('.generation-form')
$form.css('display', 'block')
$form.find('input[name="html"]').val($('.schedule-content').html())


// Replace localed URL with current locale prefix.
window.I18N = JSON.parse($('#i18n_variables').text())
function findPrefix(u) {
	const possiblePrefixes = []
	for (const prefix of window.I18N.LANGUAGE_PREFIXES) {
		if (u.startsWith(prefix)) {
			return prefix
		}
	}
	return ''
}
$('.localed-url').each($e => {
	const original = $e.attr('href')
	if (!original) {
		return
	}
	const prefix = findPrefix(original)
	if (!prefix) {
		return
	}
	const sub = original.substr(prefix.length)
	const replaced = `${window.I18N.LANGUAGE_PREFIX}${sub}`
	if (replaced !== original) {
		$e.attr('href', replaced)
	}
})

})
