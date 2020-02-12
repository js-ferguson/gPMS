
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
                window.location.href = this.url;
            });
        }
    };
}

function placeClinic(latlng) {
    var obj = latlng;
    console.log(obj['lat']);
    for (var key in obj) {
        var marker = new google.maps.Marker({
            position: obj,
            map: map,
            title: latlng.name,
        });
        marker.addListener('click', function() {
            var getPosition = function (options) {
                return new Promise(function (resolve, reject) {
                    navigator.geolocation.getCurrentPosition(resolve, reject, options);
                });
            };
            getPosition()
                .then((position) => {
                    var url =  `https://www.google.com/maps/dir/?api=1&origin=${position.coords.latitude},${position.coords.longitude}&destination=${obj["lat"]},${obj["lng"]}&travelmode=driving`;

                    let a = document.createElement('a');
                    a.target = '_blank';
                    a.href = url;
                    a.click();
                })
                .catch((err) => {
                    console.error(err.message);
                });
        });
    }
}

function mapSelector() {
    setCurrentLocation();

    if (window.location.href.slice(22, -1) === "clinic_listing") {
        var latlng = JSON.parse(document.getElementById('latlng-data').textContent);
        map = new google.maps.Map(document.getElementById('listing-map'), {
            zoom: 10
        });
        placeMarkers(latlng);

    } else if (window.location.href.slice(22, 29) === "clinic/") {
        latlng = JSON.parse(document.getElementById('latlng-data').textContent);
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10
        });
        placeClinic(latlng);

    } else {
        latlng = JSON.parse(document.getElementById('latlng-data').textContent);
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10
        });
        placeMarkers(latlng);
    }
}

