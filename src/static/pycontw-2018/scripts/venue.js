import L from 'leaflet'
import 'leaflet-easybutton'

const venue = L.layerGroup()

// Marker style and layer definition.
L.marker([25.040997, 121.611417], {
	icon: L.icon({
		iconUrl: window.VENUE_ICON,
		iconSize: [56, 51],
		iconAnchor: [28, 28],
	}),
})
.addTo(venue)
.bindTooltip(window.VENUE_NAME, {
	offset: [-4, 20],
	direction: 'bottom',
})
.openTooltip()

// Tile attributions.
const mbAttr1 = 'Tiles &copy; <a href="https://stamen.com" target="_blank" rel="noopener">Stamen Design</a>, and <a href="https://www.mapbox.com/" target="_blank" rel="noopener">Mapbox</a>. Data &copy; <a href="https://openstreetmap.org" target="_blank" rel="noopener">OpenStreetMap</a> contributors.'
const mbUrl1 = 'http://{s}.sm.mapstack.stamen.com/((toner-background,$fff[@20],$002660[hsl-color]),(toner-lines,$fff[@10],$3b097b[hsl-color])[@90],(buildings,$fff[@20],$002660[hsl-color])[@20],(toner-labels,$fff[@40],$b2b1dc[hsl-color]))/{z}/{x}/{y}.png'
const mbAttr2 = 'Maps &copy; <a href="https://www.thunderforest.com" target="_blank" rel="noopener">Thunderforest</a>, Data &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap </a> contributors.'
const mbUrl2 = 'https://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=6170aad10dfd42a38d4d8c709a536f38'


const stamen = L.tileLayer(mbUrl1, {attribution: mbAttr1})
const transport = L.tileLayer(mbUrl2, {attribution: mbAttr2})

// Initialize map.
const pymap = L.map('venue-map', {
	center: [25.040997, 121.611417],
	zoom: 12,
	layers: [stamen, venue],
	scrollWheelZoom: false,
	zoomControl: false,
})
L.control.zoom({position: 'topright'}).addTo(pymap)

// Adjust map to center the icon in the non-covered area.
function centerMap() {
	const mapw = document.getElementById('venue-map').clientWidth
	const ovlw = document.getElementById('venue-info-overlay').clientWidth

	let lng = 121.611417
	if (ovlw && mapw > ovlw) {
		const bs = pymap.getBounds()
		lng -= (bs.getEast() - bs.getWest()) * ovlw / mapw / 2
	}
	pymap.panTo([25.040997, lng])
}
centerMap()
window.map = pymap

// Icon for venue.
L.easyButton(
	`<img src="${window.VENUE_BUTTON}" alt="Map Home" width="12" height="12">`,
	centerMap,
	{position: 'topright'},
).addTo(pymap)

// Layers and functionalities.
const baseLayers = {
	'Stamen': stamen,
	'Transport': transport,
}
const overlays = {
	'Venue': venue
}

// Layers and functionalities.
L.control.layers(baseLayers, overlays, {position: 'bottomright'}).addTo(pymap)
