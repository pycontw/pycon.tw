
var proposals_creatable = document.getElementById("proposals.creatable");
var proposals_editable = document.getElementById("proposals.editable");
var proposals_withdrawable = document.getElementById("proposals.withdrawable");
var reviews_stage = document.getElementById("reviews.stage");
var reviews_visible_to_submitters = document.getElementById("reviews.visible.to.submitters");

$('.hotkey').click(function () {
    if ($(this).val() == "Call for Proposals") {
        Call_for_Proposals();
    }
    else if ($(this).val() == "First Round Review_1") {
        First_Round_Review_1()
    }
    else if ($(this).val() == "First Round Review") {
        First_Round_Review()
    }
    else if ($(this).val() == "Modification Stage") {
        Modification_Stage()
    }
    else if ($(this).val() == "Second Round Review") {
        Second_Round_Review()
    }
    else if ($(this).val() == "Internal Decision") {
        Internal_Decision()
    }
    else {
        Announcement_of_Acceptance()
    }

    /* 
    Proposal Review Stage Setting 
    Reference : https://github.com/pycontw/pycon.tw/blob/master/src/reviews/README.md 
    */
    function Call_for_Proposals(){
        proposals_creatable.checked = true;
        proposals_editable.checked = true;
        proposals_withdrawable.checked = true;
        reviews_stage.value = 0;
        reviews_visible_to_submitters.checked = false;
    }
    function First_Round_Review_1() {
        proposals_creatable.checked = false;
        proposals_editable.checked = false;
        proposals_withdrawable.checked = false;
        reviews_stage.value = "0";
        reviews_visible_to_submitters.checked = false;
    }
    function First_Round_Review() {
        proposals_creatable.checked = false;
        proposals_editable.checked = false;
        proposals_withdrawable.checked = false;
        reviews_stage.value = "1";
        reviews_visible_to_submitters.checked = false;
    }
    function Modification_Stage() {
        proposals_creatable.checked = false;
        proposals_editable.checked = true;
        proposals_withdrawable.checked = false;
        reviews_stage.value = "0";
        reviews_visible_to_submitters.checked = true;
    }
    function Second_Round_Review() {
        proposals_creatable.checked = false;
        proposals_editable.checked = false;
        proposals_withdrawable.checked = false;
        reviews_stage.value = "2";
        reviews_visible_to_submitters.checked = false;
    }
    function Internal_Decision() {
        proposals_creatable.checked = false;
        proposals_editable.checked = false;
        proposals_withdrawable.checked = false;
        reviews_stage.value = "0";
        reviews_visible_to_submitters.checked = false;
    }
    function Announcement_of_Acceptance() {
        proposals_creatable.checked = false;
        proposals_editable.checked = true;
        proposals_withdrawable.checked = false;
        reviews_stage.value = "0";
        reviews_visible_to_submitters.checked = true;
    }
});