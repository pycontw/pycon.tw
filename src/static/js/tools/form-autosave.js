(function ($) {

if (!window.localStorage || !window.JSON) {
	return;
}

var autosave = function (object) {
	window.localStorage.setItem(
		window.location + '#form', JSON.stringify(object));
	window.localStorage.setItem(
		window.location + '#timestamp', Date.now().valueOf());
};

var getAutosaveData = function () {
	var key = window.location + '#form';
	var val = window.localStorage.getItem(key);
	return val ? JSON.parse(val) : null;
};

var removeAutosaveData = function () {
	var key = window.location + '#form';
	window.localStorage.removeItem(key);
}

var getAutosaveTimestamp = function () {
	var key = window.location + '#timestamp';
	var val = parseInt(window.localStorage.getItem(key));
	return isNan(val) ? new Date(0) : new Date(val);
};

// Read autosave data if it's more recent than the last submit.
(function (lastSave) {

if (getAutosaveTimestamp() < lastSave) {	// The autosave data is stale.
	removeAutosaveData();
} else {	// Populate autosaved data.
	$.each(getAutosaveData(), function (key, value) {
		$('.proposal-form .form-control[name="' + key + '"]').val(value);
	});
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
