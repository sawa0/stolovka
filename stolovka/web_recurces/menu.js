// Модуль управления меню

/**
 * Обработчик изменения недели
 */
function weekChange() {
    socket.emit('get_week_menu', document.getElementById('week').value);
}

/**
 * Обработка данных меню от сервера
 */
socket.on('week_menu', function (data) {
    document.getElementById('week').value = data[0];
    document.getElementById('menu_conteiner').innerHTML = '';

    // Формирование списка блюд для select
    var dishSelect = '';
    Object.keys(data[2]).forEach((dish) => {
        dish = parseInt(dish);
        if (data[2][dish]['isactive'] == 1) {
            dishSelect += `<option value='${dish}'>${data[2][dish]['name']}</option>`;
        }
    });

    let days = getWeekDatesFormatted(data[0]);
    var table = '';

    // Генерация таблиц для каждого дня недели
    for (var day = 0; day < 7; day++) {
        table += `
            <table id="day${day}" class="menu_filling_table">
                <tr class="table_borders_1_px">
                    <th colspan="2">
                        <div style="display: flex;justify-content: center;align-items: center;">
                            <div class="day_div">${days[day]}</div>
                            <div class="print_control_div">
                                <div class="print_icon">🖨️</div>
                                <input type="checkbox" ${data[4][day] ? 'checked' : ''} id="print_check${day}" onchange="printFlagChange(${day}, this.checked)">
                            </div>
                        </div>
                    </th>
                </tr>
        `;

        // Генерация строк для блюд (позиции 1-8)
        for (var pos = 1; pos < 9; pos++) {
            var dishID = '';
            var active = '';

            if (data[3][pos] == "") {
                dishID = data[1][day][pos];
            } else {
                dishID = data[3][pos];
                active = 'disabled';
            }

            var dishName = '';
            var dishPrice = '';

            if (dishID !== '' && data[2][dishID]) {
                const { name, price } = data[2][dishID];
                dishName = name;
                dishPrice = price.toFixed(2);
            }

            table += `
                <tr class="table_borders_1_px">
                    <td class="eda table_borders_1_px">
                        <div style="display: flex;">
                            <select class="menu_filling_table_dish_name" id="day${day}name${pos}" onchange="updateMenu(${day}, ${pos})" ${active}>
                                <option>${dishName}</option>
                                ${dishName !== '' ? '<option class="option_unset"></option>' : ''}
                                ${dishSelect}
                            </select>
                        </div>
                    </td>
                    <td class="price"><div id="price${pos}" class="menu_filling_table_price_input ${pos}dish_price">${dishPrice}</div></td>
                </tr>
            `;
        }

        table += `
            <tr style="background-color: #f2f2f2; padding-top: 0px; padding-bottom: 0px;">
                <td style="padding-top: 4px; padding-bottom: 4px;"><div style="display: flex; justify-content: flex-end;">Сумма:</div></td>
                <td style="padding-top: 4px; padding-bottom: 4px;"><div style="display: flex; justify-content: center;" id="day_summ${day}" class="day_summ"></div></td>
            </tr>
            </table>`;
    }

    // Генерация таблицы регулярного меню
    var regularMenuTableRows = '';

    for (var pos = 1; pos < 9; pos++) {
        var dishID = data[3][pos];
        var dishName = '';
        var dishPrice = '';

        if (dishID !== '' && data[2][dishID]) {
            const { name, price } = data[2][dishID];
            dishName = name;
            dishPrice = price;
        }

        regularMenuTableRows += `
            <tr class="table_borders_1_px">
                <td class="eda table_borders_1_px">
                    <div style="display: flex;height: 28px;">
                        <select class="menu_filling_table_dish_name" id="RegularMenuName${pos}" onchange="updateRegularMenu(${pos})">
                            <option>${dishName}</option>
                            ${dishName !== '' ? '<option class="option_unset"></option>' : ''}
                            ${dishSelect}
                        </select>
                    </div>
                </td>
                <td class="price"><div id="price${pos}" class="menu_filling_table_price_input">${dishPrice}</div></td>
            </tr>
        `;
    }

    table += `
        <table id="regular" class="menu_filling_table regular_menu_filling_table">
            <tr class="table_borders_1_px">
                <th colspan="2">
                    <div style="height: 20px;display: flex;flex-wrap: nowrap;justify-content: center;align-items: center;">
                        <div>Регулярное меню</div>
                        <div style="height: 16px;">
                            <div title="Части меню, повторяющееся каждый день. Например хлеб. (Желательно заполнять с конца, пустые строки не отображаются)" style="display: flex; height: 12px; width: 12px; background-color: #4caf50; justify-content: center; align-items: center; border-radius: 5px; margin-left: 5px; font-size: smaller; color: azure;">?</div>
                        </div>
                    </div>
                </th>
            </tr>
            ${regularMenuTableRows}
        </table>
    `;

    document.getElementById('menu_conteiner').innerHTML = table;

    // Подсчёт суммы для каждого дня
    for (var i = 0; i < 7; i++) {
        var summ = 0;
        var dayTable = document.getElementById('day' + i);

        for (var j = 1; j < 9; j++) {
            var price = parseFloat(dayTable.querySelector("#price" + j).innerHTML);
            if (price == "" || isNaN(price)) {
                continue;
            }
            summ += price;
        }

        document.getElementById("day_summ" + i).innerHTML = summ.toFixed(2);
    }
});

/**
 * Обновление регулярного меню
 * @param {number} row - Номер строки
 */
function updateRegularMenu(row) {
    socket.emit('regular_menu_update', [
        document.getElementById('week').value,
        [row, document.querySelector(`#RegularMenuName${row}`).value]
    ]);
}

/**
 * Обновление меню дня
 * @param {number} day - День недели (0-6)
 * @param {number} row - Номер строки (1-8)
 */
function updateMenu(day, row) {
    socket.emit('menu_update', [
        document.getElementById('week').value,
        [day, row, document.querySelector(`#day${day} #day${day}name${row}`).value]
    ]);
}

/**
 * Изменение флага печати для дня
 * @param {number} day - День недели (0-6)
 * @param {boolean} status - Статус флага
 */
function printFlagChange(day, status) {
    socket.emit('print_flag_change', [day, status]);
}

/**
 * Печать меню
 */
function printMenu() {
    for (var day = 0; day < 7; day++) {
        var table = document.getElementById('day' + day);

        if (table.classList.contains("hide_to_print")) {
            table.classList.remove('hide_to_print');
        }

        if (!document.getElementById('print_check' + day).checked) {
            table.classList.add('hide_to_print');
        }
    }
    print();
}
