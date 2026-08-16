(function () {
    'use strict';

    function setupEventLocations() {
        document.querySelectorAll('.event-location-mode').forEach(function (locationMode) {
            const customLocation = locationMode.parentElement.querySelector('.event-location-custom');
            if (!customLocation) {
                return;
            }

            function updateVisibility() {
                customLocation.hidden = locationMode.value !== '__custom__';
            }

            locationMode.addEventListener('change', updateVisibility);
            updateVisibility();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupEventLocations);
    } else {
        setupEventLocations();
    }
}());
