(function () {

const json = document.getElementById('vue-app-data').textContent

window.wm = new Vue({
	el: 'main.inner-wrapper',
	data: {
		backend: JSON.parse(json),
		currentIndex: null,
	},
	methods: {
		getSocialIconClass: key => ['fa', 'fa-' + key],
		showModal: function (e, index) {
			e.preventDefault()
			const body = document.getElementsByTagName('body')[0]
			if (typeof index !== 'number') {
				this.currentIndex = null
				body.classList.remove('popping-modal-open')
			} else {
				this.currentIndex = index
				body.classList.add('popping-modal-open')
			}
		},
		getCurrent: function (key) {
			const info = this.backend.keynote[this.currentIndex]
			return info[key]
		},
	},
});

})();
