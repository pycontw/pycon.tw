function clickOnDay1() {
	document.querySelector('.py-schedule-tabs__tab[data-target="day-1"]').click();
}

// Toggle schedule by day
const $scheduleTabs = document.querySelectorAll('.py-schedule-tabs__tab');
$scheduleTabs.forEach(function setupTab($tab) {
	$tab.addEventListener('click', function onClickTab(e) {
		const selectedDay = $tab.getAttribute('data-target');
		const tableClassInCommon = 'py-schedule-timetable';
		const tableToActivate = `.${selectedDay}.${tableClassInCommon}`;
		const activeClass = '--active';

		function inactivateAll($t) {
			$t.classList.remove('--active');
		}

		$scheduleTabs.forEach(inactivateAll)
		$tab.classList.add(activeClass);
		document.querySelectorAll(`.${tableClassInCommon}-header`).forEach(inactivateAll);
		document.querySelectorAll(`.${tableClassInCommon}-body`).forEach(inactivateAll);
		document.querySelector(`${tableToActivate}-header`).classList.add(activeClass);
		document.querySelector(`${tableToActivate}-body`).classList.add(activeClass);
	});
});

// Toggle timetable density
const $densityBtn = document.querySelector('.timetable-density-btn');
$densityBtn.addEventListener('click', function toggleDensity() {
	const choices = $densityBtn.getAttribute('data-display-choices').split(',');
	const currentChoice = $densityBtn.getAttribute('data-display-mode');
	const newChoice = choices.filter(function getNewChoice(c) {
		return c !== currentChoice;
	})[0];

	const $tables = document.querySelectorAll('.py-schedule-timetable-body');

	if (newChoice === 'default') {
		$tables.forEach(function setDefaultLayout($t) {
			const gridTemplateRows = $t.getAttribute('data-grid-template-rows');
			$t.style.gridTemplateRows = 'repeat(' + gridTemplateRows + ', 1fr)';
		});
	} else if (newChoice === 'compact') {
		$tables.forEach(function setCompactLayout($t) {
			$t.style.gridTemplateRows = null;
		});
	}

	$densityBtn.setAttribute('data-display-mode', newChoice);
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
	clickOnDay1();
});
