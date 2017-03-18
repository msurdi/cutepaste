$(document).ajaxStart(saveCaretPosition);
$(document).ajaxComplete(restoreCaretPosition);
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

function selectionChange(event) {
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

function selectAll(event) {
    let checkElements = $(".data-check");
    checkElements.prop("checked", true);
    $.publish("selectionChange");
}


function unselectAll(event) {
    let checkElements = $(".data-check");
    checkElements.prop("checked", false);
    $.publish("selectionChange");
}

let focused = null;
let focused_position = -1;

function saveCaretPosition() {
    focused = null;
    let activeElement = document.activeElement;
    if (activeElement && activeElement.id) {
        focused = activeElement.id;
        focused_position = -1;
        if (activeElement.hasAttribute("value") && activeElement.selectionStart != undefined) {
            focused_position = activeElement.value.slice(0, activeElement.selectionStart).length;
        }
    }
}
function restoreCaretPosition() {
    if (!focused) {
        return;
    }
    setTimeout(() => {
        let element = document.getElementById(focused);
        if (element) {
            element.focus();
        }
        if (focused_position > -1 && element.selectionStart != undefined) {
            element.selectionStart = element.selectionEnd = focused_position;
        }
    });

}


function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
