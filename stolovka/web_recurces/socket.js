// WebSocket соединение и базовая инициализация

var socket = io.connect(document.domain + ':' + location.port);
var activePage = null;

socket.on('connect', function () {
    console.log('WebSocket connection established');
    socket.emit('regestration', "order");
});

socket.on('reboot', function (data) {
    setTimeout(function () {
        location.reload();
    }, 5000);
});

/**
 * Инициализация при загрузке страницы
 */
document.addEventListener('DOMContentLoaded', function () {
    const date = new Date();

    // Установка ISO-недели
    const weekValue = getISOWeek(date);
    document.getElementById('week').value = weekValue;

    // Установка месяца отчёта
    const formattedDate = formatReportMonth(date);
    document.getElementById('ReportMonth').value = formattedDate;

    console.log(`ISO неделя установлена: ${weekValue}`);

    // Открываем первую страницу
    openPage('menu');
});

/**
 * Переключение между страницами
 * @param {string} key - Ключ страницы
 */
function openPage(key) {
    if (activePage != null) {
        document.getElementById("sidebar_btn_" + activePage).classList.remove('sidebar_btn_active');
        document.getElementById(activePage + "_page").style.display = "none";
        document.getElementById(activePage + "_header_container").style.display = "none";
    }

    activePage = key;
    document.getElementById("sidebar_btn_" + activePage).classList.add('sidebar_btn_active');
    document.getElementById(activePage + "_page").style.display = "block";
    document.getElementById(activePage + "_header_container").style.display = "flex";

    // Загрузка данных для активной страницы
    switch (activePage) {
        case "menu":
            socket.emit('get_week_menu', document.getElementById('week').value);
            break;
        case "users":
            socket.emit('getUsers');
            break;
        case "purchase":
            socket.emit('getPurchase');
            break;
        case "dish_list":
            socket.emit('getDishList');
            break;
        case "reports":
            socket.emit('getReports', document.getElementById('ReportMonth').value);
            break;
        case "settings":
            socket.emit('getSettings');
            break;
    }

    closeRecipeWindow();
}
