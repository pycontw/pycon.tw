(function () {

// https://gist.github.com/benjamincharity/6058688
function smoothScroll(el, to, duration) {
	if (duration < 0) {
		return
	}
	var difference = to - $(window).scrollTop()
	var perTick = difference / duration * 10
	this.scrollToTimerCache = setTimeout(function () {
		if (!isNaN(parseInt(perTick, 10))) {
			window.scrollTo(0, $(window).scrollTop() + perTick)
			smoothScroll(el, to, duration - 10)
		}
	}.bind(this), 10)
}

function scrollTo(target) {
	smoothScroll($(window), $(target).offset().top, 200)
	if (window.history && window.history.pushState) {
		if (target !== window.location.hash) {
			window.history.pushState(
				'', '', window.location.pathname + window.location.search + target)
		}
	}
}

$('.quick-jump-link').on('click', function (e) {
	e.preventDefault()
	scrollTo($(e.currentTarget).attr('href'))
})

$('.back-to-top').on('click', function (e) {
	e.preventDefault()
	smoothScroll($(window), 0, 200)
})

function padZero(number, digits) {
	let s = number
	while (s.length < digits) {
		s = '0' + s
	}
	return s
}

// Jump directly to the table on the correct date.
const today = new Date()
const todayId = [
	padZero(today.getFullYear(), 4),
	padZero(today.getMonth() + 1, 2),
	padZero(today.getDate(), 2),
].join('-')
if ($(todayId).length > 0) {
	scrollTo(todayId, 200)
}

})();

