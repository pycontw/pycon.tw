//icon樣式
var pyIcon = L.icon({
	iconUrl: 'https://i.imgur.com/AwHZfrC.png',
	iconSize: [32, 32],
	iconAnchor: [16, 16]
});
//圖層group
var venue = L.layerGroup();
//點位的樣式，並指定所屬圖層
L.marker([25.040997, 121.611417], {
	icon: pyIcon
}).addTo(venue)
.bindTooltip("中央研究院 人文社會科學館", {
	offset: [0, 11],
	permanent: 'True',
	direction: 'bottom'
}).openTooltip();
//底圖來源資訊
var mbAttr1 = 'Tiles &copy; <a href="http://stamen.com" target="_blank" rel="noopener">Stamen Design</a>, and <a href="https://www.mapbox.com/" target="_blank" rel="noopener">Mapbox</a>. Data &copy; <a href="http://openstreetmap.org" target="_blank" rel="noopener">OpenStreetMap</a> contributors.', mbUrl1 = 'http://{s}.sm.mapstack.stamen.com/((toner-background,$fff[@20],$002660[hsl-color]),(toner-lines,$fff[@10],$3b097b[hsl-color])[@90],(buildings,$fff[@20],$002660[hsl-color])[@20],(toner-labels,$fff[@40],$b2b1dc[hsl-color]))/{z}/{x}/{y}.png', mbAttr2 = 'Maps &copy; <a href="http://www.thunderforest.com" target="_blank" rel="noopener">Thunderforest</a>, Data &copy; <a href="http://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap </a> contributors.', mbUrl2 = 'https://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=6170aad10dfd42a38d4d8c709a536f38';

var stamen = L.tileLayer(mbUrl1, {
	attribution: mbAttr1
}),

transport = L.tileLayer(mbUrl2, {
	attribution: mbAttr2
});
//初始化地圖
var pymap = L.map('map', {
	center: [25.040997, 121.611417],
	zoom: 12,
	layers: [stamen, venue]
});
//圖層清單與功能
var baseLayers = {
	"Stamen": stamen,
	"Transport": transport
};
var overlays = {
	"會場點位": venue
};
L.control.layers(baseLayers, overlays).addTo(pymap);
