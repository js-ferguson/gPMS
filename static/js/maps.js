
function loadScript() {
    function isInPage(node) {
        return (node === document.body) ? false : document.body.contains(node);
    }
    if (isInPage(document.getElementById("api-key"))) {
        const apiKey = JSON.parse(document.getElementById('api-key').textContent); 
        var script = document.createElement('script');
        latlng = JSON.parse(document.getElementById('latlng-data').textContent);

        script.type = 'text/javascript';
        script.src = "https://maps.googleapis.com/maps/api/js?key=" + apiKey + "&callback=mapSelector";
        document.body.appendChild(script);
    }
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
                window.location.pathname = this.url;
            });
        }
    };
}

function placeClinic(latlng) {
    map.setCenter({lat: latlng['lat'], lng: latlng['lng']});
    var obj = latlng;
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

function placeDraggable(latlng) {
    map.setCenter({lat: latlng['lat'], lng: latlng['lng']});
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: latlng.name,
        url:latlng.url,
        animation: google.maps.Animation.DROP,
        draggable: true,
        raiseOnDrag: true
    });
    google.maps.event.addListener(marker, 'dragend', function(evt) {
        document.getElementById('current').innerHTML = '<p>Marker dropped: Current Lat: ' + evt.latLng.lat().toFixed(3) + ' Current Lng: ' + evt.latLng.lng().toFixed(3) + '</p>';

        const saveButton = document.createElement("BUTTON");
        saveButton.innerHTML = 'Save';
        saveButton.className = 'btn-small btn-primary btn-save';
        saveButton.onclick = function(){
            window.location.pathname = `profile/${evt.latLng.lat().toFixed(7)}/${evt.latLng.lng().toFixed(7)}/${latlng.clinic_id}`;
        };
        if ( !$('.btn-save').length ) {
            document.getElementById('save-loc').appendChild(saveButton);
        }
    });
    google.maps.event.addListener(marker, 'dragstart', function(evt) {
        document.getElementById('current').innerHTML = '<p>Currently dragging marker...</p>';
    });
}

function mapSelector(){
    var latlng = JSON.parse(document.getElementById('latlng-data').textContent);

    if (window.location.href.includes("clinic_listing")) {
        setCurrentLocation();
        map = new google.maps.Map(document.getElementById('listing-map'), {
            zoom: 10
        });
        placeMarkers(latlng);

    } else if (window.location.href.includes("/clinic/")) {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 17,
            mapTypeId: 'hybrid',
            disableDefaultUI: true,
        });
        placeClinic(latlng);

    } else if (window.location.href.includes("/profile/")) {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 17,
            mapTypeId: 'hybrid',
            disableDefaultUI: true,
        });
        placeDraggable(latlng);

    } else if (window.location.href.includes("/search/")) {
        setCurrentLocation();
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10,
            mapTypeId: 'hybrid',
            disableDefaultUI: true,
        });
        placeMarkers(latlng);

    } else {
        setCurrentLocation();
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10,
            mapTypeId: 'hybrid',
            disableDefaultUI: true,
        });
        placeMarkers(latlng);
    }
}

