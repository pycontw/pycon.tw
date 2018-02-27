import 'babel-polyfill'
import {Controller} from 'stimulus'

export class MenuController extends Controller {

	static targets = ['item', 'checker']

	connect() {
		// Click anywhere on the page to close the menu.
		document.documentElement.addEventListener('click', event => {
			// Don't run if the event originates from the menu, to avoid triggering
			// the handler twice when clicking on a menu item. Otherwise a menu item
			// will not be able to uncheck itself. Also notice we intentionally
			// exclude label elements to avoid it triggering the input's event.
			if (event.target.tagName !== 'LABEL' &&
					!this.checkerTargets.includes(event.target)) {
				this.exclude(event)
			}
		})
	}

	open(event) {
		const id = event.target.getAttribute('for')
		if (id) {
			document.getElementById(id).checked = true
		}
	}

	// Given an element, find the menu item surrounding it (if any).
	_getMenuItem(target) {
		let element = target
		while (element) {
			if (this.itemTargets.includes(element)) {
				return element
			}
			element = element.parentNode
		}
		return null
	}

	close(event) {
		// Don't close menu if the current element under cursor is a descendant of
		// the current menu item. This prevents the menu from being closed when
		// the mouse is leaving parent to hover onto the submenu.
		const item = this._getMenuItem(event.target)
		for (let element of document.querySelectorAll(':hover')) {
			while (element) {
				if (element === item) {
					return
				}
				element = element.parentNode
			}
		}
		this.exclude(event)
	}

	exclude(event) {
		// Close all menus except the one triggering this event.
		for (const target of this.checkerTargets) {
			if (target !== event.target && target.checked) {
				target.checked = false
			}
		}
	}
}
