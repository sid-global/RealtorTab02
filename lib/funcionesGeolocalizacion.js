// JavaScript Document

var dirIP = "corprocessu.com"
var puerto = "8001"

function initialize() {	
	// Se crea el marker mostrando en su ventana la informacion del parámetro texto
	function createMarker(point, texto, tipo) {
	  // Se crea el icono, y dependiendo del tipo, se le asigna una imagen
	  var letteredIcon = new GIcon(G_DEFAULT_ICON);
	  /*if (tipo == 1) {
		  // Kiosco
		  letteredIcon.image = "Geoiconos/shop.ico";
	  } else if (tipo == 2) {
		  // Oficina
		  letteredIcon.image = "Geoiconos/office.ico";
	  }*/
	  letteredIcon.image = "Geoiconos/office.ico";
	
	  // Se establecen las opciones del marker
	  markerOptions = { icon:letteredIcon };
	  var marker = new GMarker(point, markerOptions);
	
	  GEvent.addListener(marker, "click", function() {
		marker.openInfoWindowHtml(texto);
	  });
	  return marker;
	}
	
	// Se agragan en el mapa los markers correspondientes a los puntos almacenados en BD
	jQuery.get("http://"+dirIP+":"+puerto+"/t_inm_inmueble_0004_consulta_coordenadas_inmueble",{"TK":"123456","codigo":localStorage.cod},function(data) {
		miRes10 = jQuery.parseJSON(data);
		$.each(miRes10, function(i, item) {
			var map = new GMap2(document.getElementById("map_canvas"));
			map.addControl(new GSmallMapControl());
			map.addControl(new GMapTypeControl());
			map.setCenter(new GLatLng(item.latitud,item.longitud), 15);  
						
			// Se especifican para todos los tipos su tamaño, sombra, etc.
			var baseIcon = new GIcon(G_DEFAULT_ICON);
			baseIcon.shadow = "http://www.google.com/mapfiles/shadow50.png";
			baseIcon.iconSize = new GSize(22, 31);
			baseIcon.shadowSize = new GSize(37, 34);
			baseIcon.iconAnchor = new GPoint(9, 34);
			baseIcon.infoWindowAnchor = new GPoint(9, 3);
			
	  		var point = new GLatLng(item.latitud, item.longitud);
	  		map.addOverlay(createMarker(point, ("Código#" + localStorage.cod), item.tipo));
	  	});
	});
	
}