Turbolinks.start();
console.log("Start!");
document.addEventListener("turbolinks:load", () => {
    processIntercoolerTags();
    restoreCaretPosition();
});

document.addEventListener("turbolinks:click", saveCaretPosition);

$(document).ajaxStart(saveCaretPosition);

$(document).ajaxComplete(restoreCaretPosition);


function processIntercoolerTags() {
    if (event.data.timing.visitStart) { // This is to skip initial page load event
        Intercooler.processNodes(document.body);
    }
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