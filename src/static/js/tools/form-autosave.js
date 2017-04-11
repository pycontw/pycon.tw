(function ($) {

if (!window.localStorage || !window.JSON) {
	return;
}

var FORM_AUTOSAVE_DATA_KEY = window.location.pathname + '#form';
var FORM_AUTOSAVE_TIMESTAMP_KEY = window.location.pathname + '#timestamp';

var autosave = function (object) {
	window.localStorage.setItem(
		FORM_AUTOSAVE_DATA_KEY, JSON.stringify(object));
	window.localStorage.setItem(
		FORM_AUTOSAVE_TIMESTAMP_KEY, Date.now().valueOf());
};

var getAutosaveData = function () {
	var val = window.localStorage.getItem(FORM_AUTOSAVE_DATA_KEY);
	return val ? JSON.parse(val) : null;
};

var removeAutosaveData = function () {
	window.localStorage.removeItem(FORM_AUTOSAVE_DATA_KEY);
}

var getAutosaveTimestamp = function () {
	var val = parseInt(window.localStorage.getItem(FORM_AUTOSAVE_TIMESTAMP_KEY));
	return isNan(val) ? new Date(0) : new Date(val);
};

// Read autosave data if it's more recent than the last submit.
(function (lastSave) {

if (lastSave !== null && getAutosaveTimestamp() < lastSave) {
	// The autosave data is stale.
	removeAutosaveData();
} else {
	// Populate autosaved data.
	var data = getAutosaveData();
	if (data) {
		$.each(data, function (key, value) {
			$('.proposal-form .form-control[name="' + key + '"]').val(value);
		});
	}
}

})(_FORM_LAST_SAVE_);

// Perform autosave when any form field updates.
$('.proposal-form .form-control').on('change keyup', function () {
	var data = {};
	$('.proposal-form .form-control').each(function () {
		data[this.name] = $(this).val();
	});
	autosave(data);
});

})(jQuery);
