// parallelServer.js
const parallelServer = (() => {
    function init() {
        initEventHandlers([
            { selector: '#parallelUploadFileButton', event: 'click', handler: (e) => handleFileUpload(e) },
            { selector: '#parallelDownloadDataButton', event: 'click', handler: downloadDataAsFile },
            { selector: '#parallelClearDataButton', event: 'click', handler: () => $('#clearDataModal').modal('show') },
            { selector: '#ConfirmClearDataButton', event: 'click', handler: () => clearDataAjax(clearData, '/clear_data_parallel') },
            { selector: '#addArrivalButton', event: 'click', handler: (e) => addArrival(e) },
            { selector: '#addServerButton', event: 'click', handler: (e) => addServer(e) },
            { selector: '#parallelSimulateButton', event: 'click', handler: (e) => simulateServersWithSpinner(e) }
        ]);
    }

    function simulateServersWithSpinner(e) {
        e.preventDefault();
        toggleLoadingSpinner($(this), true);
        simulateServers().always(() => toggleLoadingSpinner($(this), false));
    }

    function downloadDataAsFile() {
        toggleLoadingSpinner($('#parallelDownloadDataButton'), true);
        ajaxRequest({
            url: '/download_parallel_data',
            type: 'GET',
            successHandler: handleDownloadDataSuccess,
            errorHandler: handleAjaxError('downloading data'),
            completeHandler: function () {
                toggleLoadingSpinner($('#parallelDownloadDataButton'), false);
            }
        });
    }

    function handleDownloadDataSuccess(response) {
        if (response.success) {
            const link = document.createElement('a');
            link.href = response.file_url;
            link.download = 'parallel_queue_data.xlsx';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            showFlashMessage('Error', response.message, 'danger');
        }
    }

    function handleFileUpload(e) {
        e.preventDefault();
        let formData = new FormData($('#parallelUploadFileForm')[0]);
        executeFileUpload(formData);
    }

    function executeFileUpload(formData) {
        const parallelUploadFileButton = $('#parallelUploadFileButton');
        toggleLoadingSpinner(parallelUploadFileButton, true);
        ajaxRequest({
            url: '/upload_file_parallel',
            processData: false,
            contentType: false,
            data: formData,
            successHandler: handleUploadSuccess,
            errorHandler: handleAjaxError('uploading file'),
            completeHandler: () => toggleLoadingSpinner(parallelUploadFileButton, false)
        });
    }

    function handleUploadSuccess(response) {
    clearTables();
    if (response.success) {
        response.arrivals.forEach(data => {
            populateArrivalRow(data);
        });
        response.servers.forEach(data => {
            populateServerRow(data);
        });
        $('#parallelUploadFileForm')[0].reset();
        showFlashMessage('Success!', 'File uploaded successfully.', 'success');
    } else {
        console.error('No data available in response', response);
        showFlashMessage('Warning!', 'No data received from the server.', 'warning');
    }
    checkArrivalServerBodyTables();
}

    function populateArrivalRow(data) {
        let arrivalRow = $(Templates.arrivalRow);
        arrivalRow.find('td').eq(0).text(data['Time Between Arrival']);
        arrivalRow.find('td').eq(1).text(data['Probability']);
        arrivalRow.find('td').eq(2).text(data['Accumulative Probability']);
        arrivalRow.find('td').eq(3).text(data['Digit Assignment From']);
        arrivalRow.find('td').eq(4).text(data['Digit Assignment To']);
        $('.arrival-data-table tbody').append(arrivalRow);
    }

    function populateServerRow(data) {
        let serverRow = $(Templates.serverRow);
        serverRow.find('td').eq(0).text(data['Server No.']);
        serverRow.find('td').eq(1).text(data['Server Probability']);
        serverRow.find('td').eq(2).text(data['Server Accumulative Probability']);
        serverRow.find('td').eq(3).text(data['Server Digit Assignment From']);
        serverRow.find('td').eq(4).text(data['Server Digit Assignment To']);
        $('.server-data-table tbody').append(serverRow);
    }

    function addArrival(e) {
        e.preventDefault();
        const formData = new FormData($('#addArrivalForm')[0]);
        executeAjax('/add_arrival', formData, handleAddArrivalSuccess, 'adding arrival data', $('#addArrivalButton'));
    }

    function handleAddArrivalSuccess(response) {
        clearArrivalTable();
        if (response.success) {
            response.events.forEach(data => populateArrivalRow(data));
        }
        checkArrivalServerBodyTables();
    }

    function addServer(e) {
        e.preventDefault();
        const formData = new FormData($('#addServerForm')[0]);
        executeAjax('/add_server', formData, handleAddServerSuccess, 'adding server', $('#addServerButton'));
    }

    function handleAddServerSuccess(response) {
        clearServerTable();
        if (response.success) {
            response.events.forEach(data => populateServerRow(data));
        }
        checkArrivalServerBodyTables();
    }

    function executeAjax(url, data, successHandler, errorMsg, button) {
        toggleLoadingSpinner(button, true);
        ajaxRequest({
            url: url,
            type: 'POST',
            processData: false,
            contentType: false,
            data: data,
            successHandler: successHandler,
            errorHandler: handleAjaxError(errorMsg),
            completeHandler: () => toggleLoadingSpinner(button, false)
        });
    }

    function simulateServers() {

        return ajaxRequest({
            url: '/simulate_servers',
            successHandler: handleSimulationSuccess,
            errorHandler: handleAjaxError('simulating customers')
        });
    }

    function handleSimulationSuccess(response) {
        let $serversTbody = $('.servers-data-table tbody');
        $serversTbody.empty();

        if (response.success) {
            response.events.forEach(data => {
                let serversRow = $(Templates.serversRow);
                serversRow.find('td').eq(0).text(data['Customer ID']);
                serversRow.find('td').eq(1).text(data['Server']);
                serversRow.find('td').eq(2).text(data['Clock Time']);
                serversRow.find('td').eq(3).text(data['Wait Time']);
                serversRow.find('td').eq(4).text((data['Clock Time'] + data['Wait Time']));
                serversRow.find('td').eq(5).text(data['Service Duration']);
                serversRow.find('td').eq(6).text(data['End Time']);
                serversRow.find('td').eq(7).text((data['End Time'] - data['Clock Time']));

                $serversTbody.append(serversRow);
            });

            $('#total-customers').text(response.metrics['Total Customers']);
            $('#average-wait-time').text(response.metrics['Average Waiting Time']);
            $('#able-utilization').text(response.metrics['Able Utilization Rate']);
            $('#baker-utilization').text(response.metrics['Baker Utilization Rate']);

            refreshPlot();
        }
    }
    
    function refreshPlot() {
        $('#servers_plot').attr('src', '/parallel_servers_plot.png?' + new Date().getTime());
    }

    function clearData() {
        clearTables();
        refreshPlot();
        checkArrivalServerBodyTables();
    }

    function clearTables() {
        $('.arrival-data-table tbody').empty();
        $('.server-data-table tbody').empty();
        $('.servers-data-table tbody').empty();
    }

    function clearArrivalTable() {
        $('.arrival-data-table tbody').empty();
    }

    function clearServerTable() {
        $('.server-data-table tbody').empty();
    }

    function checkArrivalServerBodyTables() {
        const $arrivalTbody = $('.arrival-data-table tbody'),
            $serverTbody = $('.server-data-table tbody');

        if ($arrivalTbody.children().length > 0) $('.arrival-data').removeClass('d-none');
        else $('.arrival-data').addClass('d-none');

        if ($serverTbody.children().length > 0) $('.server-data').removeClass('d-none');
        else $('.server-data').addClass('d-none');
    }

    return { init };
})();