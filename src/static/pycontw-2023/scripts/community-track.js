import 'blueimp-gallery/js/blueimp-gallery.min.js'

let galleryArr=document.getElementsByClassName('links')
Array.prototype.forEach.call(galleryArr,el=>{
    el.onclick = function (event) {
        event = event || window.event
        var target = event.target || event.srcElement,
          link = target.src ? target.parentNode : target,
          options = { index: link, event: event },
          links = this.getElementsByTagName('a')
        blueimp.Gallery(links, options)
    }
})