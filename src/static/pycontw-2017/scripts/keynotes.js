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
			if (typeof index !== 'number') {
				this.currentIndex = null
			} else {
				this.currentIndex = index
			}
		},
		getCurrent: function (key) {
			const info = this.backend.keynote[this.currentIndex]
			return info[key]
		},
	},
});

})();
