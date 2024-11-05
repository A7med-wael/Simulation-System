// utils.js
function toggleLoadingSpinner(button, show) {
    const spinner = button.find('.spinner-border');
    show ? spinner.removeClass('d-none') : spinner.addClass('d-none');
}

function showFlashMessage(alertType, message, classAlertType) {
    const flashMessageHTML = Templates.flashMessage
        .replace('{{ alert_type }}', alertType)
        .replace('{{ message }}', message);

    const $flashMessage = $(flashMessageHTML).addClass(`alert-${classAlertType}`);
    $('#flash-messages-container').append($flashMessage);

    setTimeout(() => {
        $flashMessage.fadeOut(500, function() { $(this).remove(); });
    }, 30000);
}
