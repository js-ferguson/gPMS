
function loadScript() {
    const apiKey = JSON.parse(document.getElementById('api-key').textContent); 
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = "https://maps.googleapis.com/maps/api/js?key=" + apiKey + "&callback=mapSelector";
    document.body.appendChild(script);
}

var map;

function setCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var initialLocation = new google.maps.LatLng(position.coords.latitude,
                                                         position.coords.longitude);
            map.setCenter(initialLocation);
        }); 
    }
}

function placeMarkers(latlng) {
    for (i = 0; i <= latlng.length; i++) {
        var obj = latlng[i];
        for (var key in obj) {
            var marker = new google.maps.Marker({
                position: obj,
                map: map,
                title: latlng[i].name,
                url:latlng[i].url
            });
            marker.addListener('click', function() {
                console.log('hi');
                window.location.href = this.url;
            });
        }
    };
}

function mapSelector() {
    setCurrentLocation();
    console.log(window.location.href.slice(22, -1));
   
    if (window.location.href.slice(22, -1) === "clinic_listing" || window.location.href.slice(22, -1)) {
        var latlng = JSON.parse(document.getElementById('latlng-data').textContent);
        map = new google.maps.Map(document.getElementById('listing-map'), {
            zoom: 10
        });
        console.log(latlng)
        placeMarkers(latlng);

    } else {
        latlng = JSON.parse(document.getElementById('latlng-data').textContent);
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10
        });
        placeMarkers(latlng);
    }
}

