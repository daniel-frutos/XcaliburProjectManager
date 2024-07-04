// viewer/static/viewer/js/map.js

function fetchProjectGeometries() {
    fetch('/projects/project-ids/')
        .then(response => response.json())
        .then(data => {
            const ids = data.ids;
            alert('Received project IDs: ' + ids.join(', '));  // Add this line for the alert
            fetchGeometries(ids);
        })
        .catch(error => console.error('Error fetching project IDs:', error));
}

function fetchGeometries(ids) {
    fetch('/viewer/geometries/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure you handle CSRF token
        },
        body: JSON.stringify({ ids: ids })
    })
    .then(response => response.json())
    .then(data => {
        // Load geometries into the map
        loadGeometriesOntoMap(data.geometries);
    })
    .catch(error => console.error('Error fetching geometries:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loadGeometriesOntoMap(geometries) {
    // Implement OpenLayers logic to load geometries onto the map
}

document.addEventListener('DOMContentLoaded', fetchProjectGeometries);
