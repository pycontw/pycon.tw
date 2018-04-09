import {Controller} from 'stimulus'

export class TopNavController extends Controller {

	static targets = ['menu', 'toggler']

	connect() {
		this.menuTarget.classList.remove('no-script')
		this.togglerTarget.classList.remove('no-script')
	}

	toggle() {
		this.menuTarget.classList.toggle('open')
		const curr = this.menuTarget.classList.contains('open')
		this.togglerTarget.setAttribute('aria-expanded', curr.toString())
		document.body.classList.toggle('overlay-open', curr)
	}
}
