// templates.js
let Templates = {};

function loadTemplates() {
    return $.when(
        $.get('/static/templates/customerRowTemplate.html', data => Templates.customerRow = data),
        $.get('/static/templates/eventRowTemplate.html', data => Templates.eventRow = data),
        $.get('/static/templates/serviceItemTemplate.html', data => Templates.serviceItem = data),
        $.get('/static/templates/arrivalRowTemplate.html', data => Templates.arrivalRow = data),
        $.get('/static/templates/serverRowTemplate.html', data => Templates.serverRow = data),
        $.get('/static/templates/serversRowTemplate.html', data => Templates.serversRow = data),
        $.get('/static/templates/flash-messages.html', data => Templates.flashMessage = data)
    );
}
