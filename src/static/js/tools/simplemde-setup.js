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

if (!document.querySelectorAll || !window.DOMParser)
	return;

var elementList = document.querySelectorAll(
	'.editor-readonly > .editor-preview');
for (var i = 0; i < elementList.length; i++) {
	var element = elementList[i];
	var source = element.textContent || element.innerText;

	var doc = new DOMParser().parseFromString(source, 'text/html');
	element.innerHTML = SimpleMDE.prototype.markdown(
		doc.documentElement.textContent);
}

})(SimpleMDE);
