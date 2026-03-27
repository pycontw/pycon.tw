import {Controller} from 'stimulus'

export class MediaPopupController extends Controller {

	static targets = ['presenter', 'popup']

	_toggle(target, value) {
		target.classList.toggle('open', value)

	}

	open(event) {
		event.preventDefault()
		for (const target of this.popupTargets) {
			target.classList.toggle('open', false)
		}

		let target = null
		for (let e = event.target; !!e; e = e.parentElement) {
			const index = this.presenterTargets.indexOf(e)
			if (index >= 0) {
				target = this.popupTargets[index]
				break
			}
		}

		if (target) {
			target.classList.toggle('open', true)
			document.body.classList.toggle('overlay-open', true)
		}
	}

	close(event) {
		event.preventDefault()
		for (const target of this.popupTargets) {
			target.classList.toggle('open', false)
		}
		document.body.classList.toggle('overlay-open', false)
	}
}
