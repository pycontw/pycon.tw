(function () {

const json = document.getElementById('vue-app-data').textContent

window.wm = new Vue({
	el: 'main.inner-wrapper',
	data: function () {
		const backendData = JSON.parse(json)

		let counter = 0
		const sponsors = []
		for (const key in backendData.sponsors) {
			backendData.sponsors[key].sponsors.forEach(function (o) {
				o.index = counter
				sponsors.push(o)
				counter++
			})
		}

		return {
			backend: backendData,
			sponsors: sponsors,
			currentIndex: null,
		}
	},
	methods: {
		getDeckClasses: function (key) {
			return ['sponsor-card-deck', key + '-deck']
		},
		showModal: function (e, index) {
			e.preventDefault()
			const body = document.getElementsByTagName('body')[0]
			if (typeof index !== 'number' ||
					index < 0 || index >= this.sponsors.length) {
				this.currentIndex = null
				body.classList.remove('popping-modal-open')
			} else {
				this.currentIndex = index
				body.classList.add('popping-modal-open')
			}
		},
		getCurrent: function (key) {
			if (this.currentIndex === null) {
				return null
			}

			return this.sponsors[this.currentIndex][key]
		},
	},
})

})();
