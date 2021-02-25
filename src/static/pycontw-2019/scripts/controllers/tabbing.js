import {Controller} from 'stimulus'

let controllerID = 0

function formatTabStorageKey(tabKey) {
	return `${window.location.pathname}-tabbing-${tabKey}`
}

function setTabState(tabKey, value) {
	if (!window.localStorage) {
		return
	}
	window.localStorage.setItem(formatTabStorageKey(tabKey), value)
}

function getTabState(tabKey) {
	if (!window.localStorage) {
		return null
	}
	let value = Number(window.localStorage.getItem(formatTabStorageKey(tabKey)))
	if (isNaN(value)) {
		value = 0
	}
	return value
}

export class TabbingController extends Controller {

	static targets = ['tab', 'pane']

	_activateTab(tab) {
		let index = -1

		// Find a tab to activate.
		for (const [i, t] of this.tabTargets.entries()) {
			if (t === tab) {
				t.classList.add('active')
				index = i
			} else {
				t.classList.remove('active')
			}
		}

		// Find the corresponding pane to show.
		for (const [i, p] of this.paneTargets.entries()) {
			if (i === index) {
				p.classList.remove('hidden')
			} else {
				p.classList.add('hidden')
			}
		}

		// Record this into local storage.
		setTabState(this.data.get('id'), index.toString())
	}

	_ensureSingleActive(tabs) {
		if (tabs.length < 1) {
			return
		}

		// Find an initial tab to show with the following priority:
		// 1. Check if the user has already set it in the local storage.
		// 2. Look for a tab marked as "active" in HTML.
		let activeTabs = []
		const state = Number(getTabState(this.data.get('id')))
		if (Number.isInteger(state) && state >= 0 && state < tabs.length) {
			activeTabs.push(tabs[state])
		} else {
			for (const tab of tabs) {
				if (tab.classList.contains('active')) {
					activeTabs.push(tab)
				}
			}
		}

		// If an initial tab is found, use it; otherwise activate the first tab.
		if (activeTabs.length < 1) {
			this._activateTab(tabs[0])
		} else {
			this._activateTab(activeTabs[0])
		}
	}

	connect() {
		this.element.classList.add('enabled')
		this._ensureSingleActive(this.tabTargets)
	}

	initialize() {
		// Give this tabbing group an ID, to be used when saving to local storage.
		this.data.set('id', controllerID.toString())
		controllerID += 1
	}

	activate(event) {
		this._activateTab(event.target)
	}
}
