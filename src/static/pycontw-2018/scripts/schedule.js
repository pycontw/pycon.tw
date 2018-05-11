// Schedule generation.
const form = document.querySelector('.generation-form')
if (form) {
	const html = document.querySelector('.schedule-content').innerHTML
	form.querySelector('input[name="html"]').value = html
	form.style.display = 'block'
}


// Replace localed URL with current locale prefix.
const I18N = JSON.parse(document.getElementById('i18n_variables').textContent)
function findPrefix(u) {
	const possiblePrefixes = []
	for (const prefix of I18N.LANGUAGE_PREFIXES) {
		if (u.startsWith(prefix)) {
			return prefix
		}
	}
	return ''
}
for (const el of document.querySelectorAll('.localed-url')) {
	const original = el.getAttribute('href')
	if (!original) {
		continue
	}
	const prefix = findPrefix(original)
	if (!prefix) {
		continue
	}
	const sub = original.substr(prefix.length)
	el.setAttribute('href', `${I18N.LANGUAGE_PREFIX}${sub}`)
}
