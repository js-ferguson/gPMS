
function loadScript() {
    const apiKey = JSON.parse(document.getElementById('api-key').textContent); 
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = "https://maps.googleapis.com/maps/api/js?key=" + apiKey + "&callback=mapSelector";
    document.body.appendChild(script);
}

var map;
var clinicRef;

function placeMarkers(latlng) {
    for (i = 0; i <= latlng.length; i++) {
        var obj = latlng[i];
        for (var key in obj) {
            var marker = new google.maps.Marker({
                position: obj,
                map: map,
            });
        }
    };
}

function mapSelector() {
    if (window.location.href.slice(22, -1) === "clinic_listing") {
        var latlng = JSON.parse(document.getElementById('latlng-data').textContent);
        console.log(latlng);
        map = new google.maps.Map(document.getElementById('listing-map'), {
            zoom: 10
        });
        placeMarkers(latlng);

    } else {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10
        });
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var initialLocation = new google.maps.LatLng(position.coords.latitude,
                                                         position.coords.longitude);
            console.log(initialLocation.toString());
            console.log(position);
            map.setCenter(initialLocation);
        }); 
     }
}


/* function initMap() {

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude,
                                                     position.coords.longitude);
            map.setCenter(initialLocation);
        }); 

    }
}
*/
//var listing_map;



/*function clinicListing() {
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
*/
