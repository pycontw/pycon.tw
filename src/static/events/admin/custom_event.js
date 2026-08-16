(function () {
    'use strict';

    function setupCustomLocation() {
        const locationMode = document.getElementById('id_location_mode');
        const customLocation = document.querySelector('.form-row.field-custom_location');
        if (!locationMode || !customLocation) {
            return;
        }

        function updateVisibility() {
            customLocation.hidden = locationMode.value !== '__custom__';
        }

        locationMode.addEventListener('change', updateVisibility);
        updateVisibility();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupCustomLocation);
    } else {
        setupCustomLocation();
    }
}());
