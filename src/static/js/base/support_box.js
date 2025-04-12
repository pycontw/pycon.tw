document.addEventListener("DOMContentLoaded", function () {
	const trigger = document.getElementById("supportBoxTrigger");
	const panel = document.getElementById("supportBoxPanel");
	const closeBtn = document.getElementById("supportBoxClose");

	if (trigger && panel && closeBtn) {
		trigger.addEventListener("click", function () {
			trigger.style.display = "none";
			panel.classList.add("open");
		});

		closeBtn.addEventListener("click", function () {
			panel.classList.remove("open");
			setTimeout(() => {
				trigger.style.display = "block";
			}, 300);
		});
	}
});
