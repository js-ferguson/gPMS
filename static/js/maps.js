var map;

/*if (navigator.geolocation) {
     navigator.geolocation.getCurrentPosition(function (position) {
         initialLocation = new google.maps.LatLng(position.coords.latitude,
                                                  position.coords.longitude);
         map.setCenter(initialLocation);
     });
 }
 */

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude,
                                                     position.coords.longitude);
            map.setCenter(initialLocation);
        }); 

    }
}

var latlng = JSON.parse(document.getElementById('latlng-data').textContent);

console.log(latlng);
