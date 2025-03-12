var socket = io.connect(document.domain + ':' + location.port);

socket.on('connect', function () {  // подключение к серверу
    console.log('WebSocket connection established');
    socket.emit('regestration', "order");
});

socket.on('reboot', function (data) {setTimeout(function () {location.reload();}, 5000);});

var active_page = null;

document.addEventListener('DOMContentLoaded', function () {
    /* == Устанавливаем текущую дату == */

    const date = new Date();

    const getWeekNumber = (date) => {
        const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
        return Math.ceil(((date - firstDayOfYear) / 86400000 + firstDayOfYear.getDay() + 1) / 7);
    };
    document.getElementById('week').value = `${date.getFullYear()}-W${String(getWeekNumber(date)).padStart(2, '0')}`;

    const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    document.getElementById('ReportMonth').value = formattedDate

    /* == Открываем первую страницу == */
    openpage('menu');
});

function openpage(key) {
    if (active_page != null) {
        document.getElementById("sidebar_btn_" + active_page).classList.remove('sidebar_btn_active');
        document.getElementById(active_page + "_page").style.display = "none";
        document.getElementById(active_page + "_header_container").style.display = "none";
    }
    active_page = key;
    document.getElementById("sidebar_btn_" + active_page).classList.add('sidebar_btn_active');
    document.getElementById(active_page + "_page").style.display = "block";
    document.getElementById(active_page + "_header_container").style.display = "flex";

    if (active_page == "menu") {
        socket.emit('get_week_menu', document.getElementById('week').value);
    }
    if (active_page == "users") {
        socket.emit('getUsers');
    }
    if (active_page == "purchase") {
        socket.emit('getPurchase');
    }
    if (active_page == "dish_list") {
        socket.emit('getDishList');
    }
    if (active_page == "reports") {
        socket.emit('getReports', document.getElementById('ReportMonth').value);
    }
    if (active_page == "settings") {
        socket.emit('getSettings');
    }

    СloseRecipeWindow()
}
/*=*=*=*=*=*=*   JS для меню   *=*=*=*=*=*=*/
function WeekChange() {
    socket.emit('get_week_menu', document.getElementById('week').value);
}

socket.on('week_menu', function (data) {

    document.getElementById('week').value = data[0];
    document.getElementById('menu_conteiner').innerHTML = '';

    function getWeekDatesFormatted(weekString) {
        const [year, week] = weekString.split('-W').map(Number);

        const daysOfWeek = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];
        const months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];

        const firstDayOfYear = new Date(year, 0, 1);
        const firstMonday = new Date(firstDayOfYear.getFullYear(), 0, 1 + (firstDayOfYear.getDay() || 7) - 1);
        const weekStart = new Date(firstMonday.getTime() + ((week - 1) * 7 + 1 - firstMonday.getDay()) * 24 * 60 * 60 * 1000);

        const weekDates = Array.from({ length: 7 }, (_, i) => {
            const date = new Date(weekStart.getTime() + i * 24 * 60 * 60 * 1000);
            const day = date.getDate();
            const month = months[date.getMonth()];
            return `${daysOfWeek[i]}, ${day} ${month}`;
        });

        return weekDates;
    }

    var dish_select;
    Object.keys(data[2]).forEach((dish) => {
        dish = parseInt(dish)
        if (data[2][dish]['isactive'] == 1) {
            dish_select = dish_select + `<option value='${dish}'>${data[2][dish]['name']}</option>`;
        }
    });

    let days = getWeekDatesFormatted(data[0]);
    var table = '';

    for (var day = 0; day < 7; day++) {
        table = table + `
            <table id="dey${day}" class="menu_filling_table">
                <tr class="table_borders_1_px">
                    <th colspan="2">
                        <div style="display: flex;justify-content: center;align-items: center;">
                            <div class="day_div">${days[day]}</div>
                            <div class="print_control_div">
                                <div class="print_icon">🖨️</div>
                                <input type="checkbox" ${data[4][day] ? 'checked' : ''} id="print_check${day}" onchange="print_flag_change(${day}, this.checked)"></input>
                            </div>
                        </div>
                    </th>
                </tr>
        `;
        for (var pos = 1; pos < 9; pos++) {

            var DishID = '';
            var active = '';

            if (data[3][pos] == "") {
                DishID = data[1][day][pos];
            } else {
                DishID = data[3][pos];
                active = 'disabled';
            }

            var DishName = '';
            var DishPrice = '';

            if (DishID !== '' && data[2][DishID]) {
                const { name, price } = data[2][DishID];
                DishName = name;
                DishPrice = price;
            }

            table = table + `
<tr class="table_borders_1_px">
    <td class="eda table_borders_1_px">

        <div style="display: flex;">
            <select class="menu_filling_table_dish_name" id="dey${day}name${pos}" onchange="UpdateMenu(${day}, ${pos})" style="width: 300px;" ${active}>
                <option>${DishName}</option>
                ${DishName !== '' ? '<option class="option_unset"></option>' : ''}
                ${dish_select}
            </select>
        </div>
        
    </td>
    <td class="price" ><div id="price${pos}" class="menu_filling_table_price_input  ${pos}dish_price">${DishPrice}</div></td>
</tr>
`;
        }
        table = table + `
        <tr>
            <td><div style="display: flex; justify-content: flex-end;">Сумма:</div></td>
            <td><div style="display: flex; justify-content: center;" id="day_summ${day}" class="day_summ"></div></td>
        </tr>
        </table>`;
    }

    var regular_menu_table_rows = '';


    for (var pos = 1; pos < 9; pos++) {

        var DishID = data[3][pos];
        var DishName = '';
        var DishPrice = '';

        if (DishID !== '' && data[2][DishID]) {
            const { name, price } = data[2][DishID];
            DishName = name;
            DishPrice = price;
        }

        regular_menu_table_rows = regular_menu_table_rows + `
<tr class="table_borders_1_px">
    <td class="eda table_borders_1_px">

        <div style="display: flex;height: 28px;">
            <select class="menu_filling_table_dish_name" id="RegularMenuName${pos}" onchange="UpdateRegularMenu(${pos})" style="width: 300px;">
                <option>${DishName}</option>
                ${DishName !== '' ? '<option class="option_unset"></option>' : ''}
                ${dish_select}
            </select>
        </div>
        
    </td>
    <td class="price" ><div id="price${pos}" class="menu_filling_table_price_input">${DishPrice}</div></td>
</tr>
`;
    }


    table = table + `
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

                ${regular_menu_table_rows}

            </table>
        `;

    document.getElementById('menu_conteiner').innerHTML = table;

    for (var i = 0; i < 7; i++) {
        var summ = 0;
        var day_table = document.getElementById('dey' + i)

        for (var j = 1; j < 9; j++) {
            var price = parseFloat(day_table.querySelector("#price" + j).innerHTML)
            if (price == "" || isNaN(price)) { continue; }
            summ += price;
        }

        document.getElementById("day_summ" + i).innerHTML = summ.toFixed(2);
    }
});

function UpdateRegularMenu(row) { socket.emit('regular_menu_update', [document.getElementById('week').value, [row, document.querySelector(`#RegularMenuName${row}`).value]]) }

function UpdateMenu(day, row) { socket.emit('menu_update', [document.getElementById('week').value, [day, row, document.querySelector(`#dey${day} #dey${day}name${row}`).value]]) }

function print_flag_change(day, status) {socket.emit('print_flag_change', [day, status]);}

function print_memu() {
    for (var day = 0; day < 7; day++) {

        var table = document.getElementById('dey' + day);

        if (table.classList.contains("hide_to_print")) {
            table.classList.remove('hide_to_print');
        }

        if ( !document.getElementById('print_check' + day).checked) {
            table.classList.add('hide_to_print');
        }
    }
    print();
}
/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=*   JS для users  *=*=*=*=*=*=*/
socket.on('users', function (data) {
    const users_table = document.getElementById('users_table');
    users_table.innerHTML = '';

    data.sort((a, b) => a[1].localeCompare(b[1], 'uk'));

    data.forEach((user) => {
        var users_rows = `
            <tr id="userRow${user[0]}" class="user_column">
                <td>
                    <input class="table_input_user_name" type="text" id="UserName${user[0]}" value="${user[1]}" onfocus="showEditButton(${user[0]})" onblur="hideEditButtonWithDelay(${user[0]})">
                    <button id="editButton${user[0]}" style="display: none;" title="Сохранить изменённое имя" style="hiden;" onclick="EditUserName(${user[0]})">✏️</button>
                </td>
                <td class="dish_status"><div style="display: flex;"><div class="user_status_div">${user[2] ? '✔️' : '❌'}</div><div><button class="change_user_status_btn" title="Деактивированный пользователь не будет отображатся в списке пользователей на странице заказов. его всегда можно будет активировать снова" onclick="ChangeUserStatus(${user[0]})">${user[2] ? 'Деактивировать' : 'Активировать'}</button></div></div></td>
                <td class="delete_btn_column"><button title="Удалить пользователя (не удалит его из отчётов. если пользователь временно не будет пользоватся столовой деактивируйте его.)" class="delete_btn" onclick="DeleteUser(${user[0]})">Удалить</button></td>
            </tr>
        `;
        users_table.insertAdjacentHTML('beforeend', users_rows);
    });
    FilterUserList();
});

function FilterUserList() {
    var filter = document.getElementById('newUserName').value.toLowerCase();

    const userColumns = document.getElementsByClassName('user_column');

    if (filter === '') {
        for (let i = 0; i < userColumns.length; i++) { userColumns[i].style.display = 'table-row'; }
    } else {
        for (let i = 0; i < userColumns.length; i++) {
            const input = userColumns[i].querySelector('input');
            const text = input.value.toLowerCase();
            if (text.includes(filter)) {
                userColumns[i].style.display = 'table-row';
            } else {
                userColumns[i].style.display = 'none';
            }
        }
    }
}

function ChangeUserStatus(id) { socket.emit('ChangeUserStatus', id); }

function DeleteUser(id) { socket.emit('DeleteUser', id); }

function EditUserName(id) { socket.emit('EditUserName', [id, document.getElementById('UserName' + id).value]); }

function NewUser() {
    socket.emit('newUserName', document.getElementById('newUserName').value);
    document.getElementById('newUserName').value = '';
}

function showEditButton(userId) { var editButton = document.getElementById("editButton" + userId); editButton.style.display = "inline-block"; } // Показываем кнопку
function hideEditButton(userId) { var editButton = document.getElementById("editButton" + userId); editButton.style.display = "none"; } // Скрываем кнопку
function hideEditButtonWithDelay(userId) { setTimeout(function () { hideEditButton(userId); }, 300); }
/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=* JS для purchase *=*=*=*=*=*=*/
socket.on('Purchase', function (data) {
    const purchase_table = document.getElementById('purchase_table');
    purchase_table.innerHTML = '';

    data.sort((a, b) => a[1].localeCompare(b[1], 'uk'));

    data.forEach((ingredient) => {
        var purchase_rows = `
        <tr class="ingredients_column">
            <td>
                <input class="table_input_ingredient_name" type="text" id="IngredientName${ingredient[0]}" value="${ingredient[1]}" onfocus="showIngredientNameEditButton(${ingredient[0]})" onblur="hideIngredientNameEditButtonWithDelay(${ingredient[0]})">
                <button id="editIngredientNameButton${ingredient[0]}" style="display: none;" title="Сохранить изменённое название" onclick="EditIngredientName(${ingredient[0]})">✏️</button>
            </td>
            <td class="ingredient_volume">
                <div class="ingredient_volume_div"><input id="newPrice${ingredient[0]}" value="${ingredient[3]}" class="price_input" type="number" max="999" onblur="editPrice(${ingredient[0]})"><div class="ingredient_price_volume">грн/${ingredient[2]}</div></div>
            </td>
            <td class="delete_btn_column">
                <button class="delete_btn" onclick="DeleteIngredientConfirmationDialog(${ingredient[0]})">Удалить</button>
            </td>
        </tr>
        `;

        purchase_table.insertAdjacentHTML('beforeend', purchase_rows);
    });
    FilterIngredientList();
});

function editPrice(id) {
    var newPrice = document.getElementById('newPrice' + id).value
    if (newPrice.trim() === '') { return; }
    socket.emit('newPrice', [id, newPrice]);
}

function NewIngredient() {
    var newIngredient = [document.getElementById('newIngredientName').value,
    document.getElementById('newIngredientVolume').value,
    document.getElementById('newIngredientPrice').value];
    if (newIngredient[0] == '') { alert('Необходимо указать название нового ингредиента'); return; }

    document.getElementById('newIngredientName').value = '';
    document.getElementById('newIngredientVolume').value = 'кг.';
    document.getElementById('newIngredientPrice').value = '';

    if (newIngredient[2] == '') { newIngredient[2] = 0 }

    socket.emit('NewIngredient', newIngredient);
}

function FilterIngredientList() {
    var filter = document.getElementById('newIngredientName').value.toLowerCase();

    const ingredientColumns = document.getElementsByClassName('ingredients_column');

    if (filter === '') {
        for (let i = 0; i < ingredientColumns.length; i++) { ingredientColumns[i].style.display = 'table-row'; }
    } else {
        for (let i = 0; i < ingredientColumns.length; i++) {
            const input = ingredientColumns[i].querySelector('input');
            const text = input.value.toLowerCase();
            if (text.includes(filter)) {
                ingredientColumns[i].style.display = 'table-row';
            } else {
                ingredientColumns[i].style.display = 'none';
            }
        }
    }
}

function EditIngredientName(id) {
    var newIngredientName = document.getElementById('IngredientName' + id).value.trim();
    if (newIngredientName === '') { alert('Имя не может быть пустым'); return; }
    socket.emit("UpdateIngredientName", [id, newIngredientName])
}

function cancelIngredientDelete() {
    IngredientToDelete = 0;
    document.getElementById("accept_ingredient_delete_conteiner").style.display = 'none';
}

var IngredientToDelete = 0;

function DeleteIngredientConfirmationDialog(IngredientID) {
    IngredientToDelete = IngredientID;
    document.getElementById("accept_ingredient_delete_conteiner").style.display = 'block';
}

function DeleteIngredient() {
    document.getElementById("accept_ingredient_delete_conteiner").style.display = 'none';
    socket.emit("DeleteIngredient", IngredientToDelete);
    IngredientToDelete = 0;
}

function showIngredientNameEditButton(dishId) { var editButton = document.getElementById("editIngredientNameButton" + dishId); editButton.style.display = "inline-block"; } // Показываем кнопку

function hideIngredientNameEditButton(dishId) { var editButton = document.getElementById("editIngredientNameButton" + dishId); editButton.style.display = "none"; } // Скрываем кнопку

function hideIngredientNameEditButtonWithDelay(dishId) { setTimeout(function () { hideIngredientNameEditButton(dishId); }, 300); }

/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=*  JS для dishes  *=*=*=*=*=*=*/
socket.on('Dishes', function (data) {
    const dish_table = document.getElementById('dish_table');
    dish_table.innerHTML = '';

    data.sort((a, b) => a[1].localeCompare(b[1], 'uk'));

    data.forEach((dish) => {
        var dish_rows = `
        <tr class="dish_column">
            <td>
                <input class="table_input_dish_name" type="text" id="DishName${dish[0]}" value="${dish[1]}" onfocus="showDishNameEditButton(${dish[0]})" onblur="hideDishNameEditButtonWithDelay(${dish[0]})">
                <button id="editDishNameButton${dish[0]}" style="display: none;" title="Сохранить изменённое название" style="hiden;" onclick="EditDishName(${dish[0]})">✏️</button>
            </td>
            <td class="dish_status"><div style="display: flex;"><div class="dish_price">${dish[4]} грн</div><div><button style="border-top-left-radius: 0px; border-bottom-left-radius: 0px;" onclick="Recipe(${dish[0]})">Рецептура</button></div></div></td>
            <td class="dish_status"><div style="display: flex;"><div class="dish_status_div">${dish[2] ? '✔️' : '❌'}</div><div><button class="change_dish_status_btn" title="Деактивированное блюдо не будет отображатся в списке блюд. Его всегда можно будет активировать снова" onclick="ChangeDishStatus(${dish[0]})">${dish[2] ? 'Деактивировать' : 'Активировать'}</button></div></div></td>
            <td class="delete_btn_column"><button title="Удалить блюдо" class="delete_btn" onclick="DeleteDishConfirmationDialog(${dish[0]})">Удалить</button></td>
        </tr>
        `;

        dish_table.insertAdjacentHTML('beforeend', dish_rows);
    });
    FilterDishList();
});

function showDishNameEditButton(dishId) { var editButton = document.getElementById("editDishNameButton" + dishId); editButton.style.display = "inline-block"; } // Показываем кнопку

function hideDishNameEditButton(dishId) { var editButton = document.getElementById("editDishNameButton" + dishId); editButton.style.display = "none"; } // Скрываем кнопку

function hideDishNameEditButtonWithDelay(dishId) { setTimeout(function () { hideDishNameEditButton(dishId); }, 300); }

function NewDish() {
    if (document.getElementById("newDishName").value === '') { alert('Название блюда не может быть пустым'); return; }
    socket.emit("NewDish", document.getElementById("newDishName").value);
    document.getElementById("newDishName").value = "";
}

function EditDishName(id) { socket.emit("EditDishName", [id, document.getElementById('DishName' + id).value]) }

function ChangeDishStatus(id) { socket.emit("ChangeDishStatus", id) }

function FilterDishList() {
    var filter = document.getElementById('newDishName').value.toLowerCase();
    const dishColumns = document.getElementsByClassName('dish_column');

    if (filter === '') {
        for (let i = 0; i < dishColumns.length; i++) { dishColumns[i].style.display = 'table-row'; }
    } else {
        for (let i = 0; i < dishColumns.length; i++) {
            const input = dishColumns[i].querySelector('input');
            const inputValue = input.value.toLowerCase();
            if (inputValue.includes(filter)) {
                dishColumns[i].style.display = 'table-row';
            } else {
                dishColumns[i].style.display = 'none';
            }
        }
    }
}

var DishToDelete = 0;

function cancelDishDelete() {
    IngredientToDelete = 0;
    document.getElementById("accept_dish_delete_conteiner").style.display = 'none';
}

function DeleteDishConfirmationDialog(id) {
    DishToDelete = id;
    document.getElementById("accept_dish_delete_conteiner").style.display = 'block';
}

function DeleteDish() {
    document.getElementById("accept_dish_delete_conteiner").style.display = 'none';
    socket.emit("DeleteDish", DishToDelete);
    DishToDelete = 0;
}

function Recipe(id) { socket.emit("GetRecipe", id); }

socket.on('Recipe', function (data) {
    const recipeTable = document.getElementById('recipe_table');
    const addIngredientsContainer = document.getElementById('add_ingredients_conteiner');
    document.getElementById("recipeName").innerText = data['Name'];

    const recipeKeys = Object.keys(data['Recipe']);
    const ingridientKeys = Object.keys(data['ingridients']);

    var ingredientToAdd;
    ingridientKeys.forEach((key) => {
        if (!recipeKeys.includes(key)) {
            ingredientToAdd += `<option value="${key}">${data['ingridients'][key]['name']}</option>`;
        }
    });

    var addIngredientMenu = `
        <div class="add_ingredient_select">
            <select id="newIngredient">
                <option value=''></option>
                ${ingredientToAdd}
            </select>
        </div>
        <input id="newRecipeIngredientVolume" class="add_ingredient_volume" type="number" placeholder="Объем">
        <button class="add_ingredient" onclick="addIngredient(${data['id']})">Добавить</button>
    `;
    addIngredientsContainer.innerHTML = addIngredientMenu;

    recipeTable.innerHTML = '';

    var ItogPrice = 0;

    recipeKeys.forEach((key) => {
        var ingredient = data['Recipe'][key];

        console.log(data);

        var recipeRow = `
            <tr class="">
                <td class="padding_4">${data['ingridients'][key]['name']}</td>
                <td style="width: 140px;">
                    <div class="input_ingridient_per_volume_unit_price">
                        <input class="input" type="number" value="${data['ingridients'][key]['price']}" onblur="IngredientPriceEditFromRecipe(${key}, this.value, ${data['id']})">
                        <div>
                            грн/${data['ingridients'][key]['volume']}
                        </div>
                    </div>
                </td>
                <td class="input_volume">
                    <input id="set_ingridient_volume${key}" class="input" type="number" value="${ingredient}" onblur="EditVolume(${data['id']}, ${key}, this.value)"> ${data['ingridients'][key]['volume']}
                </td>
                <td style="width: 100px;">${(data['ingridients'][key]['price'] * ingredient).toFixed(2)} грн</td>
                <td class="delete_btn_column"><button class="delete_btn" onclick="DeleteIngredientFromRecipe(${data['id']}, ${key})">Удалить</button></td>
            </tr>
        `;

        ItogPrice += data['ingridients'][key]['price'] * ingredient;

        recipeTable.insertAdjacentHTML('beforeend', recipeRow);
    });

    document.getElementById("recipe_result").innerText = 'Цена всех ингридиентов: ' + ItogPrice.toFixed(2) + ' грн | Итоговая цена: ' + (ItogPrice * 1.11).toFixed(2) + ' грн';

    document.getElementById("recipeWindow").style.display = 'block';
});

function IngredientPriceEditFromRecipe(id, newPrice, DishID) {
    if (newPrice == '') { newPrice = 0 }
    socket.emit('IngredientPriceEditFromRecipe', {
        ingredientID: id, newPrice: newPrice, DishID: DishID
    });
}

function СloseRecipeWindow() { socket.emit('getDishList'); document.getElementById('recipeWindow').style.display = 'none'; }

function addIngredient(id) {

    var IngredientID = document.getElementById('newIngredient').value;
    if (IngredientID === '') { alert("Необходимо выбрать ингридиент для добавления в рецепт."); return; }

    var newIngredientVolume = document.getElementById('newRecipeIngredientVolume').value;
    if (newIngredientVolume == '') { newIngredientVolume = 0 }

    var IngredientName = document.getElementById('newIngredient').options[document.getElementById('newIngredient').selectedIndex].text;

    socket.emit("AddIngredientToRecipe", { 'DishID': id, 'IngredientID': IngredientID, 'IngredientName': IngredientName, 'volume': newIngredientVolume })
}

function DeleteIngredientFromRecipe(DishID, IngredientID) { socket.emit("DeleteIngredientFromRecipe", { 'DishID': DishID, 'IngredientID': IngredientID }) }

function EditVolume(DishID, IngredientID, newVolume) {
    if (newVolume == '') { newVolume = 0 }
    socket.emit("EditVolume", { 'DishID': DishID, 'IngredientID': IngredientID, 'Volume': newVolume })
}

/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=* JS для reports  *=*=*=*=*=*=*/

var ActiveReportData;
var ActiveReportUser = 0;

socket.on('Reports', function (data) {
    ActiveReportData = data[2];
    document.getElementById('ReportMonth').value = data[0];

    document.getElementById('UserNameToReport').innerHTML = '<option value="0">Все пользователи</option>';

    data[1].forEach((user) => {

        const newOption = new Option(user[1], user[0].toString());

        if (ActiveReportUser == user[0]) {
            newOption.selected = true;
        }

        document.getElementById('UserNameToReport').add(newOption);

    });

    MonthReport()
});

function MonthReport() {
    const daysOfWeek = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];
    const shortmonths = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"];

    const dict_result = ActiveReportData.reduce((acc, item) => {

        if (ActiveReportUser != 0 && ActiveReportUser != item[4]) { return acc; }

        const date = new Date(item[1]);
        const dayOfWeek = daysOfWeek[date.getUTCDay()];
        const day = date.getUTCDate();
        const month = shortmonths[date.getUTCMonth()];
        const formattedDate = `${dayOfWeek}, ${day} ${month}`;
        const total = Number(item[6]);

        if (!acc[date]) {
            acc[date] = [item[1], formattedDate, total];
        } else {
            acc[date][2] = (parseFloat(acc[date][2]) + total).toFixed(2);
        }

        return acc;
    }, {});

    if (dict_result == undefined) {
        const users_table = document.getElementById('report_table_body');
        users_table.innerHTML = '';
        return;
    }

    const result = Object.values(dict_result);

    document.getElementById('month_cost').innerText = result.reduce((acc, item) => acc + parseFloat(item[2]), 0).toFixed(2) + " грн.";

    const users_table = document.getElementById('report_table_body');
    users_table.innerHTML = '';

    result.forEach((day) => {
        var row = `
            <tr id="${day[0]}" class="">
                <td>
                    <div class="display_flex">
                        <div class="report_day">${day[1]}</div><div class="report_day_price">${day[2]} грн.</div>
                    </div>
                </td>
                <td style="width: 120px;"><button onclick="DayReportDetails('${day[0]}')">Подробности</button></td>
                <td style="width: 131px;"><button onclick="DownloadReport('${day[0]}')">Скачать отчёт</button></td>
                <td class="delete_btn_column"><button class="delete_btn" onclick="deleteDayReport('${day[0]}')">Очистить</button></td>
            </tr>
        `;
        users_table.insertAdjacentHTML('beforeend', row);

    });
}

function ReportsMonthUpdate() {socket.emit('getReports', document.getElementById('ReportMonth').value);}

function ReportsFilterUpdate() {
    ActiveReportUser = document.getElementById('UserNameToReport').value;
    MonthReport()
}

function DownloadReport(Day = document.getElementById('ReportMonth').value) {socket.emit('DownloadReport', [Day, ActiveReportUser]);}
socket.on('DownloadReport', function (data) {window.open("reports/" + data, '_blank');});

var details_date = "";
function DayReportDetails(Day) { details_date = Day; socket.emit('DayReportDetails', [Day, ActiveReportUser])}

function DeleteOrder(OrderID) { socket.emit('DeleteOrder', [OrderID, [details_date, document.getElementById('UserNameToReport').value]]); }

function deleteDayReport(Day) { socket.emit('DayReportDelete', [Day, ActiveReportUser]); }

socket.on('DayReportDetails', function (data) {

    var ReportDitailsTable = document.getElementById('ReportDitailsTable');

    ReportDitailsTable.innerHTML = "";

    data.forEach((order) => {

        var bill = JSON.parse(order[5]);
        console.log(bill);

        var HTML_bill = "";
        bill.forEach((dish) => {
            function padString(text, filler, length) {
                if (text.length >= length) {
                    return text;
                }
                let fillerLength = length - text.length;
                let fillerString = filler.repeat(fillerLength);
                return text + fillerString;
            }

            HTML_bill = HTML_bill + `<div style="display: flex;">
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
                    <div style="font-family: 'Courier New', Courier, monospace;">${HTML_bill}</div>
                    <div style="display: flex;justify-content: flex-end;padding-top: 9px;">
                        <button class="delete_check_btn" onclick="DeleteOrder(${order[0]})">Удалить</button>
                        <div style="width: 80px;border-top-left-radius: 0px;border-bottom-left-radius: 0px;" class="check_div">&#129534; ${order[6]}</div>
                    </div>
                </td>

            </tr>
        `;

        ReportDitailsTable.insertAdjacentHTML('beforeend', row);
    });



    document.getElementById('ReportDitailsConteiner').style.display = 'block';
});

function СloseReportDitailsWindow() { socket.emit('getReports', document.getElementById('ReportMonth').value); document.getElementById('ReportDitailsConteiner').style.display = 'none'; }

/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=* JS для setting  *=*=*=*=*=*=*/

function OrderAutoConfirmationTimeUpdate() {
    socket.emit("updateSettings", ["OrderAutoConfirmationTime", document.getElementById('OrderAutoConfirmationTime').value])
}

function OrderConfirmationTypeUpdate(tupe) {
    socket.emit("updateSettings", ["OrderConfirmationType", tupe])
}

socket.on('Settings', function (data) {


    console.log(data);

    document.getElementById('OrderConfirmationType_on').classList.remove('choised_settings');
    document.getElementById('OrderConfirmationType_off').classList.remove('choised_settings');
    document.getElementById('OrderConfirmationType_auto').classList.remove('choised_settings');

    document.getElementById('OrderConfirmationType_' + data[0]).classList.add('choised_settings');

    document.getElementById('OrderAutoConfirmationTime').value = data[1];

});

function app_update() { socket.emit('app_update') }
