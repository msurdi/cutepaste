$(document).on("beforeAjaxSend.ic", setupCsrfHeader);
$.subscribe("selectionChange", selectionChange);
$.subscribe("selectAll", selectAll);
$.subscribe("unselectAll", unselectAll);

function setupCsrfHeader(event, ajaxSetup) {
    let csrftoken = $("#csrftoken").val();
    if (!csrfSafeMethod(ajaxSetup.type) && !this.crossDomain) {
        ajaxSetup.headers["X-CSRFToken"] = csrftoken;
    }
}

function selectionChange() {
    let hideElements = $(".on-selection-hide");
    let showElements = $(".on-selection-show");
    let anySelected = $(".data-check:checked").length > 0;
    if (anySelected) {
        hideElements.hide();
        showElements.show();
    } else {
        hideElements.show();
        showElements.hide();
    }
}

function selectAll() {
    let checkElements = $(".data-check");
    checkElements.prop("checked", true);
    $.publish("selectionChange");
}


function unselectAll() {
    let checkElements = $(".data-check");
    checkElements.prop("checked", false);
    $.publish("selectionChange");
}


function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
