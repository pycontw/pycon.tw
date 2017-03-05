document.querySelectorAll('.control-nav > .lang > nav > a').forEach(function (el) {
	el.addEventListener('click', function (e) {
		e.preventDefault();
		var form = document.getElementById('nav-lang-form');
		form.next.value = this.getAttribute('href');
		form.language.value = this.getAttribute('data-lang');
		form.submit();
	});
});

(function() {
  const controlRootEl = () => {
    if ($('body').hasClass('show-menu')) {
      $('html').css({
        overflow: 'hidden',
        position: 'fixed'
      });
    } else {
      $('html').css({
        overflow: 'auto',
        position: 'relative'
      });
    }
  };

  $('.btn-menu').on('click', (e) => {
    e.preventDefault();

    $('body').toggleClass('show-menu');
    controlRootEl();
  });

  $('.header-nav > .parent > a:first-child').on('click', (e) => {
    e.preventDefault();

    $(e.target).parent().toggleClass('expanded');
  });

  $('.btn-show-lang-menu').on('click', (e) => {
    $('.header-nav').hide();
    $('.header-menu-nav').show();
  })

  $('.btn-back-to-menu').on('click', (e) => {
    $('.header-nav').show();
    $('.header-menu-nav').hide();
  })

  $('.btn-close').on('click', (e) => {
    $('body').removeClass('show-menu');
    controlRootEl();
  })
})();
