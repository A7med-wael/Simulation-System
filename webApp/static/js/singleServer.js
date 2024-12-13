// singleServer.js
const singleServer = (() => {
    function init() {
        initEventHandlers([
            { selector: '#uploadFileButton', event: 'click', handler: (e) => handleFileUpload(e) },
            { selector: '#downloadDataButton', event: 'click', handler: downloadDataAsFile },
            { selector: '#clearDataButton', event: 'click', handler: () => $('#clearDataModal').modal('show') },
            { selector: '#confirmClearDataButton', event: 'click', handler: () => clearDataAjax(clearData, '/clear_data_a') },
            { selector: '#addServiceButton', event: 'click', handler: (e) => addService(e)},
            { selector: '#simulateButton', event: 'click', handler: (e) => simulateCustomersWithSpinner(e) }
        ]);
    }

    function simulateCustomersWithSpinner(e) {
        e.preventDefault();
        toggleLoadingSpinner($(this), true);
        simulateCustomers().always(() => toggleLoadingSpinner($(this), false));
    }

    function simulateCustomers() {
        const probabilitySimulation = $('#probabilityCheckbox').is(':checked');

        return ajaxRequest({
            url: '/simulate',
            data: { probability_simulation: probabilitySimulation },
            successHandler: handleSimulationSuccess,
            errorHandler: handleAjaxError('simulating customers')
        });
    }

    function handleSimulationSuccess(response) {
        let $customerTbody = $('.customer-data-table tbody');
        let $eventTbody = $('.event-data-table tbody');
        $customerTbody.empty();
        $eventTbody.empty();

        if (response.success) {
            // Check if any event has non-null probabilities
            const hasArrivalProb = response.events.some(data => data['Arrival Probability'] !== undefined);
            const hasCompletionProb = response.events.some(data => data['Completion Probability'] !== undefined);

            // Show or hide headers based on the presence of probability data
            $('.customer-data-table .arrival-prob').toggleClass('d-none', !hasArrivalProb);
            $('.customer-data-table .completion-prob').toggleClass('d-none', !hasCompletionProb);
            $('.event-data-table .arrival-prob').toggleClass('d-none', !hasArrivalProb);
            $('.event-data-table .completion-prob').toggleClass('d-none', !hasCompletionProb);

            response.events.forEach(data => {
                // Populate customer row template
                let customerRow = $(Templates.customerRow);
                if (data['Event Type'] === 'Arrival') {
                    customerRow.find('td').eq(0).text(data['Customer ID']);
                    customerRow.find('td').eq(1).text(data['Interval Time']);
                    customerRow.find('td').eq(2).text(data['Clock Time']);
                    customerRow.find('td').eq(3).text(data['Service Code']);
                    customerRow.find('td').eq(4).text(data['Service Title']);
                    customerRow.find('td').eq(5).text(data['Start Time']);
                    customerRow.find('td').eq(6).text(data['Service Duration']);
                    customerRow.find('td').eq(7).text(data['End Time']);
                    if (hasArrivalProb && data['Arrival Probability'] !== undefined) customerRow.find('td').eq(8).text(data['Arrival Probability']);
                    else customerRow.find('td').eq(8).remove();
                    if (hasCompletionProb && data['Completion Probability'] !== undefined) customerRow.find('td').eq(9).text(data['Completion Probability']);
                    else customerRow.find('td').eq(8).remove();
                    $customerTbody.append(customerRow);
                }

                // Populate event row template
                let eventRow = $(Templates.eventRow);
                eventRow.find('td').eq(0).text(data['Clock Time']);
                eventRow.find('td').eq(1).text(data['Event Type']);
                eventRow.find('td').eq(2).text(data['Customer ID']);
                eventRow.find('td').eq(3).text(data['Service Title']);
                if (hasArrivalProb && data['Arrival Probability'] !== undefined) eventRow.find('td').eq(4).text(data['Arrival Probability']);
                else eventRow.find('td').eq(4).remove();
                if (hasCompletionProb && data['Completion Probability'] !== undefined) eventRow.find('td').eq(5).text(data['Completion Probability']);
                else eventRow.find('td').eq(4).remove();
                $eventTbody.append(eventRow);
            });

            refreshPlot();
        }
    }

    function handleFileUpload(e) {
        e.preventDefault();
        let formData = new FormData($('#uploadFileForm')[0]);

        toggleLoadingSpinner($('#uploadFileButton'), true);

        ajaxRequest({
            url: '/upload_file',
            processData: false,
            contentType: false,
            data: formData,
            successHandler: handleUploadSuccess,
            errorHandler: handleAjaxError('uploading file'),
            completeHandler: function () {
                toggleLoadingSpinner($('#uploadFileButton'), false);
            }
        });
    }

    function handleUploadSuccess(response) {
        let $serviceList = $('.service-list ul');
        $serviceList.empty(); // Clear existing data

        // Check if data is present
        if (Array.isArray(response.data)) {
            response.data.forEach(data => {
                let item = Templates.serviceItem
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

        checkServiceList();
    }

    function downloadDataAsFile() {
        toggleLoadingSpinner($('#downloadDataButton'), true);
        ajaxRequest({
            url: '/download_data',
            type: 'GET',
            successHandler: handleDownloadDataSuccess,
            errorHandler: handleAjaxError('downloading data'),
            completeHandler: function () {
                toggleLoadingSpinner($('#downloadDataButton'), false);
            }
        });
    }

    function handleDownloadDataSuccess(response) {
        if (response.success) {
            const link = document.createElement('a');
            const {file_url} = response
            link.href = file_url;
            link.download = 'queue_data.xlsx';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            showFlashMessage('Error', response.message, 'danger');
        }
    }

    function refreshPlot() {
        $('#arrival_plot').attr('src', '/arrival_plot.png?' + new Date().getTime());
        $('#system_state_plot').attr('src', '/customers_system_plot.png?' + new Date().getTime());
    }

    function addService(e) {
        e.preventDefault();
        const form = $('#addServiceForm')[0];
        const formData = new FormData(form);

        toggleLoadingSpinner($('#addServiceButton'), true);

        ajaxRequest({
            url: '/add_service',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            successHandler: handleAddServiceSuccess,
            errorHandler: handleAjaxError('adding service'),
            completeHandler: function () {
                toggleLoadingSpinner($('#addServiceButton'), false);
            }
        });
    }

    function handleAddServiceSuccess(response) {
        const { service_code, service_title, service_duration } = response
        let item = Templates.serviceItem
            .replace('{{code}}', service_code)
            .replace('{{title}}', service_title)
            .replace('{{duration}}', service_duration);
        $('.service-list ul').append(item);

        $('#addServiceForm')[0].reset();
        checkServiceList();
    }

    function checkServiceList() {
        if ($('.service-list ul').children().length > 0) $('.current-services').removeClass('d-none');
        else $('.current-services').addClass('d-none');
    }

    function clearData() {
        $('.customer-data-table tbody').empty();
        $('.event-data-table tbody').empty();
        $('.service-list ul').empty();

        refreshPlot();
        checkServiceList();
    }

    return { init };
})();
