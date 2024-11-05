// main.js
$(document).ready(function () {
    $('#sidebarToggle').on('click', function() {
        $('.sidebar').toggleClass('sidebar-collapsed');
        $('.main-content').toggleClass('collapsed');
        $(this).toggleClass('collapsed');
    });

    $('#darkModeToggle').on('click', function () {
        const body = $('body');
        const currentTheme = body.attr('data-bs-theme');
        body.toggleClass('dark-mode light-mode');

        if (currentTheme === 'light') {
            body.attr('data-bs-theme', 'dark');
            $(this).find('i').toggleClass('fa-sun fa-moon-stars');
            $(this).find('span').text('Dark Mode');
        } else {
            body.attr('data-bs-theme', 'light');
            $(this).find('i').toggleClass('fa-moon fa-sun');
            $(this).find('span').text('Light Mode');
        }
    });

    // Initialize other modules after loading templates
    loadTemplates().then(() => {
        singleServer.init();
        parallelServer.init();
    });
});
