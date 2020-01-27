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

function clinicListing() {
    ref = "http://localhost:5000/clinic_listing/";
    console.log(window.location.href.slice(22, -1));
    if (window.location.href.slice(22, -1) === "clinic_listing") {

        listing_map = new google.maps.Map(document.getElementById('listing-map'), {
            zoom: 10

        });
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                initialLocation = new google.maps.LatLng(position.coords.latitude,
                                                         position.coords.longitude);
                listing_map.setCenter(initialLocation);
            }); 

        }


    } 
}
clinicListing();

console.log(latlng);
