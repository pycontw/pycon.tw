import {Controller} from 'stimulus'

export class TabbingController extends Controller {

	static targets = ['tab', 'pane']

	_activateTab(tab) {
		let index = -1
		for (const [i, t] of this.tabTargets.entries()) {
			if (t === tab) {
				t.classList.add('active')
				index = i
			} else {
				t.classList.remove('active')
			}
		}
		for (const [i, p] of this.paneTargets.entries()) {
			if (i === index) {
				p.classList.remove('hidden')
			} else {
				p.classList.add('hidden')
			}
		}
	}

	_ensureSingleActive(tabs) {
		if (tabs.length < 1) {
			return
		}
		let activeTabs = []
		for (const tab of tabs) {
			if (tab.classList.contains('active')) {
				activeTabs.push(tab)
			}
		}
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

	activate(event) {
		this._activateTab(event.target)
	}
}
