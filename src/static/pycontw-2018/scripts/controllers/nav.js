import {Controller} from 'stimulus'

export class TopNavController extends Controller {

	static targets = ['menu', 'toggler']

	toggle() {
		this.menuTarget.classList.toggle('open')
		const curr = this.menuTarget.classList.contains('open')
		this.togglerTargets.forEach(e => e.setAttribute(
			'aria-expanded', curr.toString(),
		))
	}
}
