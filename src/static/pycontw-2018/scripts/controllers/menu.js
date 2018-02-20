import {Controller} from 'stimulus'

export class MenuController extends Controller {

	static targets = ['item']

	connect() {
		// Click anywhere on the page to close the menu.
		document.documentElement.addEventListener('click', event => {
			// Don't run if the event originates from the menu, to avoid triggering
			// the handler twice when clicking on a menu item. Otherwise a menu item
			// will not be able to uncheck itself.
			if (!self.itemTargets.includes(event.target)) {
				this.exclude(event)
			}
		})
	}

	exclude(event) {
		// Close all menus except the one triggering this event.
		for (const target of this.itemTargets) {
			if (target !== event.target && target.checked) {
				target.checked = false
			}
		}
	}
}
