document.querySelectorAll('.control-nav > .lang > nav > a').forEach(function (el) {
	el.addEventListener('click', function (e) {
		e.preventDefault();
		var form = document.getElementById('nav-lang-form');
		form.next.value = this.getAttribute('href');
		form.language.value = this.getAttribute('data-lang');
		form.submit();
	});
});
