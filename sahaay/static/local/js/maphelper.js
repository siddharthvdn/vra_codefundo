/*
* @Author: kaushiksk
* @Date:   2018-10-23 14:23:28
* @Last Modified by:   kaushiksk
* @Last Modified time: 2018-10-24 23:19:13
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


function initLocalMap() {
    
        var map;
    
        var mapOptions = {
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        
        map = new google.maps.Map(document.getElementById('map'), mapOptions);

        $.ajax({
          url: '/get-local-map-data',
          dataType: 'json',
        }).done(function(positions) {           

        positions.forEach(function(element){
            var geolocate = new google.maps.LatLng(element["location"][1], element["location"][0]);
            var marker = new google.maps.Marker({
                        position: geolocate,
                        map: map
                      });
            console.log(element);

            var infowindow = new google.maps.InfoWindow();

            google.maps.event.addListener(marker,'click', (function(marker,content,infowindow){ 
                    return function() {
                       infowindow.setContent(content);
                       infowindow.open(map,marker);
                    };
                })(marker,element["username"],infowindow));

            if(element["username"] == "{{g.user['username']}}"){
                map.setCenter(geolocate);
            } 

        });
    

        console.log("Map Drawn!");


        });
        


}