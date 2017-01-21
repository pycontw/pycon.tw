(function (SimpleMDE) {

var elementList = document.getElementsByTagName('textarea');
for (var i = 0; i < elementList.length; i++) {
	var element = elementList[i];
	if (!element.hasAttribute('data-simplemde')) {
		continue;
	}
	new SimpleMDE({
		'element': element,
		'indentWithTabs': false,
		'spellChecker': false,
		'status': false,
		'tabSize': 4
	});
}

})(SimpleMDE);


(function (SimpleMDE) {

if (!document.querySelectorAll)
	return;

var elementList = document.querySelectorAll(
	'.editor-readonly > .editor-preview');
Array.prototype.forEach.call(elementList, function (e) {
	var source = e.textContent || e.innerText;
	e.innerHTML = SimpleMDE.prototype.markdown(source);
});

})(SimpleMDE);
