/*
* @Author: kaushiksk
* @Date:   2018-10-23 14:23:28
* @Last Modified by:   kaushiksk
* @Last Modified time: 2018-10-23 15:07:14
*/

function initMap() {

	if(!!navigator.geolocation) {
    
        var map;
    
        var mapOptions = {
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        
        map = new google.maps.Map(document.getElementById('map'), mapOptions);
    
        navigator.geolocation.getCurrentPosition(function(position) {
        	
        	document.getElementById('latitude').value = position.coords.latitude;
        	document.getElementById('longitude').value = position.coords.longitude;

            var geolocate = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            map.setCenter(geolocate);

          var marker = new google.maps.Marker({
					    position: geolocate,
					    map: map
					  });

          google.maps.event.addListener(map, 'click', function(event) {
          	document.getElementById('latitude').value = event.latLng.lat();
        	document.getElementById('longitude').value = event.latLng.lng();
            geolocate = new google.maps.LatLng(event.latLng.lat(), event.latLng.lng());
            
            if (marker && marker.setMap) {
   				 marker.setMap(null);
  				}

            marker = new google.maps.Marker({
					    position: geolocate,
					    map: map
					  });
			});



        });
        
    } else {
        document.getElementById('map').innerHTML = 'No Geolocation Support.';
    }


}