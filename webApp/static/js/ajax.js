// ajax.js
function handleAjaxError(action) {
    return function (xhr, status, error) {
        showFlashMessage('Error!', `${action}: ${error}`, 'danger');
    };
}

function ajaxRequest({url, type = 'POST', processData = true,
                         contentType = 'application/json' || false,
                         data, successHandler, errorHandler, completeHandler}) {
    return $.ajax({
        url,
        type,
        contentType: contentType,
        processData: processData,
        data: (type === 'POST' && contentType === 'application/json') ? JSON.stringify(data) : data,
        success: successHandler,
        error: errorHandler,
        complete: completeHandler
    });
}

function clearDataAjax(clearDataFunction) {
    return $.ajax({
        url: '/clear_data',
        type: 'GET',
        success: function () { clearDataFunction(); $('#clearDataModal').modal('hide'); },
        error: handleAjaxError('clearing data')
    });
}

function initEventHandlers(events) {
    events.forEach(({ selector, event, handler }) => {
        $(selector).on(event, handler);
    });
}