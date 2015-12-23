(function (SimpleMDE) {

if (!Element.prototype.hasAttribute) {
  Element.prototype.hasAttribute = function (name) {
    return this.getAttribute(name) !== null;
  };
}

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
    'status': false
  });
}

})(SimpleMDE);
