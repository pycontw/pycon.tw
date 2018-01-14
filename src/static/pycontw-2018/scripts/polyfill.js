(function () {

if (!NodeList.prototype.forEach) {
	NodeList.prototype.forEach = function (cb, scope) {
		let i = 0
		while (i < this.length) {
			if (i in this) {
				cb.call(scope, this[i], i, this)
			}
			i++
		}
	}
}

})();
