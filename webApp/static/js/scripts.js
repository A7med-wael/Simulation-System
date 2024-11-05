// $(document).ready(function () {
//     $('#sidebarToggle').on('click', function() {
//         $('.sidebar').toggleClass('sidebar-collapsed');
//         $('.main-content').toggleClass('collapsed');
//         $(this).toggleClass('collapsed');
//     });
//
//     $('#darkModeToggle').on('click', function () {
//         const body = $('body');
//         const currentTheme = body.attr('data-bs-theme');
//         body.toggleClass('dark-mode light-mode');
//
//         if (currentTheme === 'light') {
//             body.attr('data-bs-theme', 'dark');
//             $(this).find('i').toggleClass('fa-sun fa-moon-stars');
//             $(this).find('span').text('Dark Mode');
//         } else {
//             body.attr('data-bs-theme', 'light');
//             $(this).find('i').toggleClass('fa-moon fa-sun');
//             $(this).find('span').text('Light Mode');
//         }
//     });
//
//     clearDataAjax();
//     checkServiceList();
//     let customerRowTemplate, eventRowTemplate, serviceItemTemplate,
//         arrivalRowTemplate,serverRowTemplate, flashMessageTemplate;
//
//     // Load templates via AJAX
//     loadTemplates().then(initEventHandlers);
//
//     function initEventHandlers() {
//         $('#uploadFileButton').on('click', function (e) {
//             e.preventDefault();
//             handleFileUpload();
//         });
//
//         $('#simulateButton').on('click', function (e) {
//             e.preventDefault();
//             toggleLoadingSpinner($(this), true);
//             simulateCustomers().always(() => toggleLoadingSpinner($(this), false));
//         });
//
//         $('#downloadDataButton').on('click', downloadDataAsFile);
//         $('#clearDataButton').on('click', () => $('#clearDataModal').modal('show'));
//         $('#confirmClearDataButton').on('click', clearDataAjax);
//
//         $('#addServiceButton').on('click', function (e) {
//             e.preventDefault();
//             addService();
//         });
//
//         $('#addArrivalButton').on('click', function (e) {
//             e.preventDefault();
//             addArrival();
//         });
//
//         $('#addServerButton').on('click', function (e) {
//             e.preventDefault();
//             addServer();
//         });
//     }
//
//     function loadTemplates() {
//         return $.when(
//             $.get('/static/templates/customerRowTemplate.html', function (data) {
//                 customerRowTemplate = data;
//             }),
//             $.get('/static/templates/eventRowTemplate.html', function (data) {
//                 eventRowTemplate = data;
//             }),
//             $.get('/static/templates/serviceItemTemplate.html', function (data) {
//                 serviceItemTemplate = data;
//             }),
//             $.get('/static/templates/arrivalRowTemplate.html', function (data) {
//                 arrivalRowTemplate = data;
//             }),
//             $.get('/static/templates/serverRowTemplate.html', function (data) {
//                 serverRowTemplate = data;
//             }),
//             $.get('/static/templates/flash-messages.html', function (data) {
//                 flashMessageTemplate = data;
//             })
//         );
//     }
//
//     function toggleLoadingSpinner(button, show) {
//         const spinner = button.find('.spinner-border');
//         show ? spinner.removeClass('d-none') : spinner.addClass('d-none');
//     }
//
//     function checkServiceList() {
//         if ($('.service-list ul').children().length > 0) $('.current-services').removeClass('d-none');
//         else $('.current-services').addClass('d-none');
//     }
//
//     function showFlashMessage(alertType, message, classAlertType) {
//         const flashMessageHTML = flashMessageTemplate
//             .replace('{{ alert_type }}', alertType)
//             .replace('{{ message }}', message);
//
//         const $flashMessage = $(flashMessageHTML);
//
//         $flashMessage.addClass(`alert-${classAlertType}`);
//
//         $('#flash-messages-container').append($flashMessage);
//
//         setTimeout(() => {
//             $flashMessage.fadeOut(500, function() {
//                 $(this).remove(); // Remove the element after fade-out
//             });
//         }, 30000); // 30 seconds in milliseconds
//     }
//
//     function clearData() {
//         // Clear all data
//         $('.customer-data-table tbody').empty();
//         $('.event-data-table tbody').empty();
//         $('.service-list ul').empty();
//
//         refreshPlot();
//         checkServiceList();
//     }
//
//     function handleFileUpload() {
//         let formData = new FormData($('#uploadFileForm')[0]);
//
//         toggleLoadingSpinner($('#uploadFileButton'), true);
//
//         $.ajax({
//             url: '/upload_file',
//             type: 'POST',
//             data: formData,
//             processData: false,
//             contentType: false,
//             success: handleUploadSuccess,
//             error: handleAjaxError('uploading file'),
//             complete: function () {
//                 toggleLoadingSpinner($('#uploadFileButton'), false);
//             }
//         });
//     }
//
//     function handleUploadSuccess(response) {
//         let $serviceList = $('.service-list ul');
//         $serviceList.empty(); // Clear existing data
//
//         // Check if data is present
//         if (Array.isArray(response.data)) {
//             response.data.forEach(data => {
//                 let item = serviceItemTemplate
//                     .replace('{{code}}', data.code)
//                     .replace('{{title}}', data.title)
//                     .replace('{{duration}}', data.duration);
//                 $serviceList.append(item);
//             });
//
//             $('#uploadFileForm')[0].reset();
//             showFlashMessage('Success!', 'File uploaded successfully.', 'success');
//         } else {
//             console.error('No data available in response', response);
//             showFlashMessage('Warning!', 'No data received from the server.', 'warning');
//         }
//
//         checkServiceList();
//     }
//
//     function simulateCustomers() {
//         const probabilitySimulation = $('#probabilityCheckbox').is(':checked');
//
//         return $.ajax({
//             url: '/simulate',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({ probability_simulation: probabilitySimulation }),
//             success: handleSimulationSuccess,
//             error: handleAjaxError('simulating customers')
//         });
//     }
//
//
//     function handleSimulationSuccess(response) {
//         let $customerTbody = $('.customer-data-table tbody');
//         let $eventTbody = $('.event-data-table tbody');
//         $customerTbody.empty();
//         $eventTbody.empty();
//
//         if (response.success) {
//             // Check if any event has non-null probabilities
//             const hasArrivalProb = response.events.some(data => data['Arrival Probability'] !== undefined);
//             const hasCompletionProb = response.events.some(data => data['Completion Probability'] !== undefined);
//
//             // Show or hide headers based on the presence of probability data
//             $('.customer-data-table .arrival-prob').toggleClass('d-none', !hasArrivalProb);
//             $('.customer-data-table .completion-prob').toggleClass('d-none', !hasCompletionProb);
//             $('.event-data-table .arrival-prob').toggleClass('d-none', !hasArrivalProb);
//             $('.event-data-table .completion-prob').toggleClass('d-none', !hasCompletionProb);
//
//             response.events.forEach(data => {
//                 // Populate customer row template
//                 let customerRow = $(customerRowTemplate);
//                 customerRow.find('td').eq(0).text(data['Customer ID']);
//                 customerRow.find('td').eq(1).text(data['Event Type']);
//                 customerRow.find('td').eq(2).text(data['Clock Time']);
//                 customerRow.find('td').eq(3).text(data['Service Code']);
//                 customerRow.find('td').eq(4).text(data['Service Title']);
//                 customerRow.find('td').eq(5).text(data['Service Duration']);
//                 customerRow.find('td').eq(6).text(data['End Time']);
//                 if (hasArrivalProb && data['Arrival Probability'] !== undefined) customerRow.find('td').eq(7).text(data['Arrival Probability']);
//                 else customerRow.find('td').eq(7).remove();
//                 if (hasCompletionProb && data['Completion Probability'] !== undefined) customerRow.find('td').eq(8).text(data['Completion Probability']);
//                 else customerRow.find('td').eq(7).remove();
//                 $customerTbody.append(customerRow);
//
//                 // Populate event row template
//                 let eventRow = $(eventRowTemplate);
//                 eventRow.find('td').eq(0).text(data['Clock Time']);
//                 eventRow.find('td').eq(1).text(data['Event Type']);
//                 eventRow.find('td').eq(2).text(data['Customer ID']);
//                 eventRow.find('td').eq(3).text(data['Service Title']);
//                 if (hasArrivalProb && data['Arrival Probability'] !== undefined) eventRow.find('td').eq(4).text(data['Arrival Probability']);
//                 else eventRow.find('td').eq(4).remove();
//                 if (hasCompletionProb && data['Completion Probability'] !== undefined) eventRow.find('td').eq(5).text(data['Completion Probability']);
//                 else eventRow.find('td').eq(4).remove();
//                 $eventTbody.append(eventRow);
//             });
//
//             refreshPlot();
//         }
//     }
//
//     function downloadDataAsFile()
//     {
//         toggleLoadingSpinner($('#downloadDataButton'), true);
//         $.ajax({
//             url: '/download_data',
//             type: 'GET',
//             success: handleDownloadDataSuccess,
//             error: handleAjaxError('downloading data'),
//             complete: function () {
//                 toggleLoadingSpinner($('#downloadDataButton'), false);
//             }
//         });
//     }
//
//     function handleDownloadDataSuccess(response) {
//         if (response.success) {
//             const link = document.createElement('a');
//             link.href = response.file_url;
//             link.download = 'queue_data.xlsx';
//             document.body.appendChild(link);
//             link.click();
//             document.body.removeChild(link);
//         } else {
//             showFlashMessage('Error', response.message, 'danger');
//         }
//     }
//
//     function addService() {
//         const form = $('#addServiceForm')[0];
//         const formData = new FormData(form);
//
//         toggleLoadingSpinner($('#addServiceButton'), true);
//
//         $.ajax({
//             url: '/add_service',
//             type: 'POST',
//             processData: false,
//             contentType: false,
//             data: formData,
//             success: handleAddServiceSuccess,
//             error: handleAjaxError('adding service'),
//             complete: function () {
//                 toggleLoadingSpinner($('#addServiceButton'), false);
//             }
//         });
//     }
//
//     function addArrival() {
//         const form = $('#addArrivalForm')[0];
//         const formData = new FormData(form);
//
//         toggleLoadingSpinner($('#addArrivalButton'), true);
//
//         $.ajax({
//             url: '/add_arrival',
//             type: 'POST',
//             processData: false,
//             contentType: false,
//             data: formData,
//             success: handleAddArrivalSuccess,
//             error: handleAjaxError('adding arrival data'),
//             complete: function () {
//                 toggleLoadingSpinner($('#addArrivalButton'), false);
//             }
//         });
//     }
//
//     function addServer() {
//         const form = $('#addServerForm')[0];
//         const formData = new FormData(form);
//
//         toggleLoadingSpinner($('#addServerButton'), true);
//
//         $.ajax({
//             url: '/add_server',
//             type: 'POST',
//             processData: false,
//             contentType: false,
//             data: formData,
//             success: handleAddServerSuccess,
//             error: handleAjaxError('adding server'),
//             complete: function () {
//                 toggleLoadingSpinner($('#addServerButton'), false);
//             }
//         });
//     }
//
//     function handleAddServiceSuccess(response) {
//         let item = serviceItemTemplate
//             .replace('{{code}}', response.service_code)
//             .replace('{{title}}', response.service_title)
//             .replace('{{duration}}', response.service_duration);
//         $('.service-list ul').append(item);
//
//         $('#addServiceForm')[0].reset();
//         checkServiceList();
//     }
//
//
//     function handleAddArrivalSuccess(response) {
//         let $arrivalTbody = $('.arrival-data-table tbody');
//         $arrivalTbody.empty();
//
//         if (response.success) {
//             response.events.forEach(data => {
//                 let arrivalRow = $(arrivalRowTemplate);
//                 arrivalRow.find('td').eq(0).text(data['Time Between Arrival']);
//                 arrivalRow.find('td').eq(1).text(data['Probability']);
//                 arrivalRow.find('td').eq(2).text(data['Accumulative Probability']);
//                 arrivalRow.find('td').eq(3).text(data['Digit Assignment From']);
//                 arrivalRow.find('td').eq(4).text(data['Digit Assignment To']);
//             });
//         }
//     }
//
//     function handleAddServerSuccess(response) {
//         let $serverTbody = $('.servers-data-table tbody');
//         $serverTbody.empty();
//
//         if (response.success) {
//             response.events.forEach(data => {
//                 let serverRow = $(serverRowTemplate);
//                 serverRow.find('td').eq(0).text(data['Server No.']);
//                 serverRow.find('td').eq(1).text(data['Probability']);
//                 serverRow.find('td').eq(2).text(data['Accumulative Probability']);
//                 serverRow.find('td').eq(3).text(data['Digit Assignment From']);
//                 serverRow.find('td').eq(4).text(data['Digit Assignment To']);
//             });
//         }
//     }
//
//     function clearDataAjax() {
//         $.ajax({
//             url: '/clear_data',
//             type: 'GET',
//             success: function () {
//                 clearData(); // Clear data on success
//                 $('#clearDataModal').modal('hide');
//             },
//             error: handleAjaxError('clearing data')
//         });
//     }
//
//     function handleAjaxError(action) {
//         return function (xhr, status, error) {
//             showFlashMessage('Error!', `${action}: ' + ${error}`, 'danger');
//         };
//     }
//
//     function refreshPlot() {
//         $('#arrival_plot').attr('src', '/arrival_plot.png?' + new Date().getTime());
//         $('#system_state_plot').attr('src', '/customers_system_plot.png?' + new Date().getTime());
//         $('#servers_plot').attr('src', '/parallel_servers_plot.png?' + new Date().getTime());
//     }
// });
