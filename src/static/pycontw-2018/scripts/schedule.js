function clickOnDefaultDay() {
	const dayTarget = new Date().getDate() === 6 ? 'day-2' : 'day-1';
	const selector = '.py-schedule-tabs__tab[data-target="' + dayTarget + '"]';
	document.querySelector(selector).click();
}

// Toggle schedule by day
const $scheduleTabs = document.querySelectorAll('.py-schedule-tabs__tab');
$scheduleTabs.forEach(function setupTab($tab) {
	$tab.addEventListener('click', function onClickTab(e) {
		const selectedDay = $tab.getAttribute('data-target');
		const tableClassInCommon = 'py-schedule-timetable';
		const tableToActivate = `.${selectedDay}.${tableClassInCommon}`;
		const listClassInCommon = 'py-schedule-time-list';
		const listToActivate = `.${selectedDay}.${listClassInCommon}`;
		const activeClass = '--active';

		function inactivateAll($t) {
			$t.classList.remove('--active');
		}

		$scheduleTabs.forEach(inactivateAll)
		$tab.classList.add(activeClass);
		document.querySelectorAll(`.${tableClassInCommon}-header`).forEach(inactivateAll);
		document.querySelectorAll(`.${tableClassInCommon}-body`).forEach(inactivateAll);
		document.querySelectorAll(`.${listClassInCommon}`).forEach(inactivateAll);

		document.querySelector(`${tableToActivate}-header`).classList.add(activeClass);
		document.querySelector(`${tableToActivate}-body`).classList.add(activeClass);
		document.querySelector(`${listToActivate}`).classList.add(activeClass);
	});
});

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

document.addEventListener('DOMContentLoaded', function onReady() {
	clickOnDefaultDay();
});
