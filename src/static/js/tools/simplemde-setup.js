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
for (var i = 0; i < elementList.length; i++) {
       var element = elementList[i];
       element.innerHTML = SimpleMDE.prototype.markdown(
               element.textContent || element.innerText);
}

})(SimpleMDE);
