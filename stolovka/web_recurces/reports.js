// Модуль управления отчётами

var activeReportData;
var activeReportUser = 0;
var detailsDate = "";

/**
 * Обработка данных отчётов от сервера
 */
socket.on('Reports', function (data) {
    activeReportData = data[2];
    document.getElementById('ReportMonth').value = data[0];

    document.getElementById('UserNameToReport').innerHTML = '<option value="0">Все пользователи</option>';

    data[1].forEach((user) => {
        const newOption = new Option(user[1], user[0].toString());

        if (activeReportUser == user[0]) {
            newOption.selected = true;
        }

        document.getElementById('UserNameToReport').add(newOption);
    });

    monthReport();
});

/**
 * Формирование месячного отчёта
 */
function monthReport() {
    const dictResult = activeReportData.reduce((acc, item) => {
        if (activeReportUser != 0 && activeReportUser != item[4]) {
            return acc;
        }

        const date = new Date(item[1]);
        const dayOfWeek = DAYS_OF_WEEK_SHORT[date.getUTCDay()];
        const day = date.getUTCDate();
        const month = MONTHS_SHORT[date.getUTCMonth()];
        const formattedDate = `${dayOfWeek}, ${day} ${month}`;
        const total = Number(item[6]);

        if (!acc[date]) {
            acc[date] = [item[1], formattedDate, total];
        } else {
            acc[date][2] = (parseFloat(acc[date][2]) + total).toFixed(2);
        }

        return acc;
    }, {});

    if (dictResult == undefined) {
        const usersTable = document.getElementById('report_table_body');
        usersTable.innerHTML = '';
        return;
    }

    const result = Object.values(dictResult);

    document.getElementById('month_cost').innerText = result.reduce((acc, item) => acc + parseFloat(item[2]), 0).toFixed(2) + " грн.";

    const usersTable = document.getElementById('report_table_body');
    usersTable.innerHTML = '';

    result.forEach((day) => {
        var row = `
            <tr id="${day[0]}" class="">
                <td>
                    <div class="display_flex">
                        <div class="report_day">${day[1]}</div>
                        <div class="report_day_price">${day[2]} грн.</div>
                    </div>
                </td>
                <td style="width: 120px;"><button onclick="dayReportDetails('${day[0]}')">Подробности</button></td>
                <td style="width: 131px;"><button onclick="downloadReport('${day[0]}')">Скачать отчёт</button></td>
                <td class="delete_btn_column"><button class="delete_btn" onclick="deleteDayReport('${day[0]}')">Очистить</button></td>
            </tr>
        `;
        usersTable.insertAdjacentHTML('beforeend', row);
    });
}

/**
 * Обновление месяца отчёта
 */
function reportsMonthUpdate() {
    socket.emit('getReports', document.getElementById('ReportMonth').value);
}

/**
 * Обновление фильтра отчётов
 */
function reportsFilterUpdate() {
    activeReportUser = document.getElementById('UserNameToReport').value;
    monthReport();
}

/**
 * Скачать отчёт
 * @param {string} day - День (по умолчанию текущий месяц)
 */
function downloadReport(day = document.getElementById('ReportMonth').value) {
    socket.emit('DownloadReport', [day, activeReportUser]);
}

socket.on('DownloadReport', function (data) {
    window.open("reports/" + data, '_blank');
});

/**
 * Показать детали отчёта за день
 * @param {string} day - День
 */
function dayReportDetails(day) {
    detailsDate = day;
    socket.emit('DayReportDetails', [day, activeReportUser]);
}

/**
 * Удалить заказ
 * @param {number} orderID - ID заказа
 */
function deleteOrder(orderID) {
    socket.emit('DeleteOrder', [orderID, [detailsDate, document.getElementById('UserNameToReport').value]]);
}

/**
 * Удалить отчёт за день
 * @param {string} day - День
 */
function deleteDayReport(day) {
    socket.emit('DayReportDelete', [day, activeReportUser]);
}

/**
 * Обработка деталей отчёта за день
 */
socket.on('DayReportDetails', function (data) {
    var reportDetailsTable = document.getElementById('ReportDitailsTable');

    reportDetailsTable.innerHTML = "";

    data.forEach((order) => {
        var bill = JSON.parse(order[5]);
        console.log(bill);

        var htmlBill = "";
        bill.forEach((dish) => {
            htmlBill += `<div style="display: flex;">
                            <div>${padString(dish[0], ".", 35)}</div>
                            <div style="display: flex;">
                                <div style="padding-left: 8px;width: 66px;">${dish[1][0]}</div>
                                <div>x</div>
                                <div>${dish[1][1]}</div>
                            </div>
                        </div>`;
        });

        var row = `
            <tr>
                <td style="align-content: flex-start;">
                    <div style="display: flex;">
                        <div class="order_id_div">
                            <div class="OrderID">ID#${order[0]}</div>
                            <div class="order_time_div">${order[2]}</div>
                        </div>
                        <div style="padding-top: 4px;padding-left: 6px;">
                            ${order[3]}
                        </div>
                    </div>
                </td>

                <td style="width: 430px;">
                    <div style="font-family: 'Courier New', Courier, monospace;">${htmlBill}</div>
                    <div style="display: flex;justify-content: flex-end;padding-top: 9px;">
                        <button class="delete_check_btn" onclick="deleteOrder(${order[0]})">Удалить</button>
                        <div style="width: 80px;border-top-left-radius: 0px;border-bottom-left-radius: 0px;" class="check_div">&#129534; ${order[6]}</div>
                    </div>
                </td>
            </tr>
        `;

        reportDetailsTable.insertAdjacentHTML('beforeend', row);
    });

    document.getElementById('ReportDitailsConteiner').style.display = 'block';
});

/**
 * Закрыть окно деталей отчёта
 */
function closeReportDetailsWindow() {
    socket.emit('getReports', document.getElementById('ReportMonth').value);
    document.getElementById('ReportDitailsConteiner').style.display = 'none';
}
