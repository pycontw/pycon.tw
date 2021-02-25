(function ($) {

$('.proposal-form').areYouSure({
	'message': 'Are you sure you want to leave this page?'
});

})(jQuery);


// Scroll progress.
(function ($) {

// Calculate scroll checkpoints.
var last;
var cp = [];
$('.proposal-form .form-group').each(function () {
	cp.push($(this).offset().top - 40);
	last = this;
});
cp.shift();
cp.push($(last).offset().top + $(last).height());


function updateScrollProgress() {
	var offset = $(this).scrollTop() + $(this).height();
	var tot = cp.length;
	var $widget = $('#proposal-scroll-progress-widget');

	// Calculate current progress.
	for (var i = 0; i < tot && cp[i] < offset; i++);
	var rat = i * 1.0 / tot;

	// Apply progress to UI.
	$('.text', $widget).html('<span class="current">' + i + '</span> / ' + tot);
	$('.top', $widget).height($widget.height() * (1.0 - rat));
}

$(window).scroll(updateScrollProgress);
updateScrollProgress();

})(jQuery);


// Example modal.
(function ($) {

var novice = $("#novice-examples-header").html();
var intermediate = $("#intermediate-examples-header").html();

var getContent = function(part) {
		return novice + $("#novice-" + part + "-example").html() +
					 intermediate + $("#intermediate-" + part + "-example").html();
};

var example_content = {
	"abstract": getContent("abstract"),
	"objective": getContent("objective"),
	"detailed description": getContent("description"),
	"outline": getContent("outline")
};

$('#proposalFieldExampleModal').on('show.bs.modal', function (event) {
	// Button that triggered the modal.
	var button = $(event.relatedTarget);
	// Extract info from data-* attributes.
	var content = button.data('content');
	// If necessary, you could initiate an AJAX request here (and then
	// do the updating in a callback). Update the modal's content. We'll
	// use jQuery here, but you could use a data binding library or other
	// methods instead.
	var modal = $(this)
	modal.find('.modal-title').html(example_title[content])
	modal.find('.modal-body div').html(example_content[content])
});

})(jQuery);
