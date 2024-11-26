document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    // Load holes data from the JSON injected in the HTML
    const holes = holesData;

    // Add markers for holes
    holes.forEach(hole => {
        L.marker([hole.lat, hole.lng]).addTo(map)
            .bindPopup(`Hole ${hole.hole}: Par ${hole.par}, Distance ${hole.distance} ft`);
    });

    document.getElementById('getAdvice').addEventListener('click', function () {
        var holeNumber = parseInt(document.getElementById('holeSelect').value);
        var discType = document.getElementById('discSelect').value;

        fetch('/advice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ hole: holeNumber, disc_type: discType }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('adviceText').innerText = data.advice;
            });
    });
});