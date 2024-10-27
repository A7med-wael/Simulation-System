$(document).ready(function () {
    clearDataAjax();
    let customerRowTemplate, eventRowTemplate, serviceItemTemplate, flashMessageTemplate;

    // Load templates via AJAX
    loadTemplates().then(function () {
        // Upload file using AJAX
        $('#uploadFileButton').on('click', handleFileUpload);

        // Simulate customers using AJAX
        $('#simulateButton').on('click', function (e) {
            e.preventDefault();
            simulateCustomers();
        });

        $('#downloadDataButton').on('click', function (e) {
            e.preventDefault();
            downloadDataAsFile();
        });

        // Add new service using AJAX
        $('#addServiceButton').on('click', function (e) {
            e.preventDefault();
            addService();
        });

        // Clear data using AJAX
        $('#clearDataButton').on('click', function (e) {
            e.preventDefault();
            $('#clearDataModal').modal('show'); // Show the modal
        });

        $('#confirmClearDataButton').on('click', clearDataAjax);
    });

    function loadTemplates() {
        return $.when(
            $.get('/static/templates/customerRowTemplate.html', function (data) {
                customerRowTemplate = data;
            }),
            $.get('/static/templates/eventRowTemplate.html', function (data) {
                eventRowTemplate = data;
            }),
            $.get('/static/templates/serviceItemTemplate.html', function (data) {
                serviceItemTemplate = data;
            }),
            $.get('/static/templates/flash-messages.html', function (data) {
                flashMessageTemplate = data;
            })
        );
    }

    function showFlashMessage(alertType, message, classAlertType) {
        const flashMessageHTML = flashMessageTemplate
            .replace('{{ alert_type }}', alertType)
            .replace('{{ message }}', message);

        const $flashMessage = $(flashMessageHTML);

        $flashMessage.addClass(`alert-${classAlertType}`);

        $('#flash-messages-container').append($flashMessage);

        setTimeout(() => {
            $flashMessage.fadeOut(500, function() {
                $(this).remove(); // Remove the element after fade-out
            });
        }, 30000); // 30 seconds in milliseconds
    }

    function clearData() {
        // Clear all data
        $('.customer-data-table tbody').empty();
        $('.event-data-table tbody').empty();
        $('.service-list ul').empty();
        refreshPlot();
    }

    function handleFileUpload(e) {
        e.preventDefault();
        let formData = new FormData($('#uploadFileForm')[0]);

        $.ajax({
            url: '/upload_file',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: handleUploadSuccess,
            error: handleAjaxError('uploading file')
        });
    }

    function handleUploadSuccess(response) {
        let $serviceList = $('.service-list ul');
        $serviceList.empty(); // Clear existing data

        // Check if data is present
        if (Array.isArray(response.data)) {
            response.data.forEach(data => {
                let item = serviceItemTemplate
                    .replace('{{code}}', data.code)
                    .replace('{{title}}', data.title)
                    .replace('{{duration}}', data.duration);
                $serviceList.append(item);
            });

            $('#uploadFileForm')[0].reset();
            showFlashMessage('Success!', 'File uploaded successfully.', 'success');
        } else {
            console.error('No data available in response', response);
            showFlashMessage('Warning!', 'No data received from the server.', 'warning');
        }
    }

    function simulateCustomers() {
        $.ajax({
            url: '/simulate',
            type: 'POST',
            success: handleSimulationSuccess,
            error: handleAjaxError('simulating customers')
        });
    }


    function handleSimulationSuccess(response) {
        let $customerTbody = $('.customer-data-table tbody');
        let $eventTbody = $('.event-data-table tbody');
        $customerTbody.empty();
        $eventTbody.empty();

        if (response.success) {
            response.events.forEach(data => {
                let row = customerRowTemplate
                    .replace('{{Customer ID}}', data['Customer ID'])
                    .replace('{{Event Type}}', data['Event Type'])
                    .replace('{{Clock Time}}', data['Clock Time'])
                    .replace('{{Service Code}}', data['Service Code'])
                    .replace('{{Service Title}}', data['Service Title'])
                    .replace('{{Service Duration}}', data['Service Duration'])
                    .replace('{{End Time}}', data['End Time']);
                $customerTbody.append(row);

                let item = eventRowTemplate
                    .replace('{{Clock Time}}', data['Clock Time'])
                    .replace('{{Event Type}}', data['Event Type'])
                    .replace('{{Customer ID}}', data['Customer ID'])
                    .replace('{{Service Title}}', data['Service Title']);
                $eventTbody.append(item);
            });

            refreshPlot();
        }
    }

    function downloadDataAsFile()
    {
        $.ajax({
            url: '/download_data',
            type: 'GET',
            success: handleDownloadDataSuccess,
            error: handleAjaxError('downloading data')
        });
    }

    function handleDownloadDataSuccess(response) {
        if (response.success) {
            const link = document.createElement('a');
            link.href = response.file_url;
            link.download = 'queue_data.xlsx';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            showFlashMessage('Error', response.message, 'danger');
        }
    }

    function addService() {
        let formData = {
            service_code: $('#service_code').val(),
            service_title: $('#service_title').val(),
            service_duration: $('#service_duration').val()
        };

        $.ajax({
            url: '/add_service',
            type: 'POST',
            data: formData,
            success: handleAddServiceSuccess,
            error: handleAjaxError('adding service')
        });
    }

    function handleAddServiceSuccess(response) {
        let item = serviceItemTemplate
            .replace('{{code}}', response.service_code)
            .replace('{{title}}', response.service_title)
            .replace('{{duration}}', response.service_duration);
        $('.service-list ul').append(item);

        $('#addServiceForm')[0].reset();
    }

    function clearDataAjax() {
        $.ajax({
            url: '/clear_data',
            type: 'GET',
            success: function () {
                clearData(); // Clear data on success
                $('#clearDataModal').modal('hide');
            },
            error: handleAjaxError('clearing data')
        });
    }

    function handleAjaxError(action) {
        return function (xhr, status, error) {
            showFlashMessage('Error!', `${action}: ' + ${error}`, 'danger');
        };
    }

    function refreshPlot() {
        $('#plot').attr('src', '/plot.png?' + new Date().getTime()); // Add timestamp to bypass cache
    }
});
