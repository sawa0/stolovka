var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {  // подключение к серверу
    console.log('WebSocket connection established');
    socket.emit('regestration', "order");
});

var active_page = null;

document.addEventListener('DOMContentLoaded', function () {
    openpage("menu");
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
        /* == Устанавливаем текущую дату == */
        const currentDate = new Date();
        const getWeekNumber = (date) => {
            const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
            return Math.ceil(((date - firstDayOfYear) / 86400000 + firstDayOfYear.getDay() + 1) / 7);
        };
        document.getElementById('week').value = `${currentDate.getFullYear()}-W${String(getWeekNumber(currentDate)).padStart(2, '0')}`;
        /* ================================ */
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

}
/*=*=*=*=*=*=*   JS для меню   *=*=*=*=*=*=*/
function WeekChange() {
    socket.emit('get_week_menu', document.getElementById('week').value);
}
socket.on('week_menu', function (data) {
    document.getElementById('week').value = data[0];
    document.getElementById('menu_conteiner').innerHTML = '';

    var dish_select;
    Object.keys(data[2]).forEach((dish) => {
        dish = parseInt(dish)
        if (data[2][dish]['isactive'] == 1) {
            dish_select = dish_select + `<option value='${dish}'>${data[2][dish]['name']}</option>`;
        }
    });

    let days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"];
    var table = '';

    for (var day = 0; day < 5; day++) {
        table = table + `
            <table id = "dey${day}" class="menu_filling_table">
                <tr class="table_borders_1_px">
                    <th colspan="2">${days[day]}</th>
                </tr>
        `;
        for (var pos = 1; pos < 9; pos++) {

            var DishID = data[1][day][pos];
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
        <select class="menu_filling_table_dish_name" id="name${pos}" onchange="UpdateMenu(${day}, ${pos})" style="width: 300px;">
            <option>${DishName}</option>
            ${DishName !== '' ? '<option></option>' : ''}
            ${dish_select}
        </select>
    </td>
    <td class="price" ><div id="price${pos}" class="menu_filling_table_price_input">${DishPrice}</div></td>
</tr>
`;
        }
        table = table + `</table>`;
    }
    document.getElementById('menu_conteiner').innerHTML = table;
});

function UpdateMenu(day, row) {socket.emit('menu_update', [document.getElementById('week').value, [day, row, document.querySelector(`#dey${day} #name${row}`).value]])}
/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=*   JS для users  *=*=*=*=*=*=*/
socket.on('users', function (data) {
    const users_table = document.getElementById('users_table');
    users_table.innerHTML = '';

    data.forEach((user) => {
        var users_rows = `
            <tr id="userRow${user[0]}" class="user_column">
                <td>
                    <input class="table_input_user_name" type="text" id="UserName${user[0]}" value="${user[1]}" onfocus="showEditButton(${user[0]})" onblur="hideEditButtonWithDelay(${user[0]})">
                    <button id="editButton${user[0]}" style="display: none;" title="Сохранить изменённое имя" style="hiden;" onclick="EditUserName(${user[0]})">✏️</button>
                </td>
                <td class="user_status">${user[2] ? '✔️' : '❌'}</td>
                <td class="user_actions">
                    <button style="width: 140px;" title="Деактивированный пользователь не будет отображатся в списке пользователей на странице заказов. его всегда можно будет активировать снова" onclick="ChangeUserStatus(${user[0]})">${user[2] ? 'Деактивировать' : 'Активировать'}</button>
                    <button title="Удалить пользователя (не удалит его из отчётов. если пользователь временно не будет пользоватся столовой деактивируйте его.)" class="delete_user" onclick="DeleteUser(${user[0]})">Удалить</button>
                </td>
            </tr>
        `;
        users_table.insertAdjacentHTML('beforeend', users_rows);
    });
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

function ChangeUserStatus(id) {socket.emit('ChangeUserStatus', id);}

function DeleteUser(id) {socket.emit('DeleteUser', id);}

function EditUserName(id) { socket.emit('EditUserName', [id, document.getElementById('UserName' + id).value]); }

function NewUser() {
    socket.emit('newUserName', document.getElementById('newUserName').value);
    document.getElementById('newUserName').value = '';
}

function showEditButton(userId) {var editButton = document.getElementById("editButton" + userId); editButton.style.display = "inline-block";} // Показываем кнопку
function hideEditButton(userId) {var editButton = document.getElementById("editButton" + userId); editButton.style.display = "none";} // Скрываем кнопку
function hideEditButtonWithDelay(userId) {setTimeout(function () { hideEditButton(userId); }, 300);}
/*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*/
/*=*=*=*=*=*=* JS для purchase *=*=*=*=*=*=*/
socket.on('Purchase', function (data) {
    const purchase_table = document.getElementById('purchase_table');
    purchase_table.innerHTML = '';

    data.forEach((ingredient) => {
        var purchase_rows = `
        <tr class="ingredients_column">
            <td>
                <input class="table_input_ingredient_name" type="text" id="IngredientName${ingredient[0]}" value="${ingredient[1]}" onfocus="showIngredientNameEditButton(${ingredient[0]})" onblur="hideIngredientNameEditButtonWithDelay(${ingredient[0]})">
                <button id="editIngredientNameButton${ingredient[0]}" style="display: none;" title="Сохранить изменённое название" onclick="EditIngredientName(${ingredient[0]})">✏️</button>
            </td>
            <td class="ingredient_volume" style="font-size: 18px;width: 210px;">
                <input id="newPrice${ingredient[0]}" value="${ingredient[3]}" class="price_input" type="number" max="999" onblur="editPrice(${ingredient[0]})">грн/${ingredient[2]}
            </td>
            <td class="ingredients_actions" style="width: 100px;">
                <button class="delete_ingredient" onclick="DeleteIngredientConfirmationDialog(${ingredient[0]})">Удалить</button>
            </td>
        </tr>
        `;

        purchase_table.insertAdjacentHTML('beforeend', purchase_rows);
    });
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
    if (newIngredient[0] == '' || newIngredient[1] == 'Объем') { alert('Необходимо указать название, и еденицу объема нового ингредиента'); return; }

    document.getElementById('newIngredientName').value = '';
    document.getElementById('newIngredientVolume').value = 'Объем';
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

    data.forEach((dish) => {
        var dish_rows = `
        <tr class="dish_column">
            <td>
                <input class="table_input_dish_name" type="text" id="DishName${dish[0]}" value="${dish[1]}" onfocus="showDishNameEditButton(${dish[0]})" onblur="hideDishNameEditButtonWithDelay(${dish[0]})">
                <button id="editDishNameButton${dish[0]}" style="display: none;" title="Сохранить изменённое название" style="hiden;" onclick="EditDishName(${dish[0]})">✏️</button>
            </td>
            <td class="dish_status">${dish[2] ? '✔️' : '❌'}</td>
            <td class="dish_actions">
                <button style="width: 140px;" title="Деактивированное блюдо не будет отображатся в списке блюд. Его всегда можно будет активировать снова" onclick="ChangeDishStatus(${dish[0]})">${dish[2] ? 'Деактивировать' : 'Активировать'}</button>
                <button onclick="Recipe(${dish[0]})">Рецептура</button>
                <button title="Удалить блюдо" class="delete_dish" onclick="DeleteDishConfirmationDialog(${dish[0]})">Удалить</button>
            </td>
        </tr>
        `;

        dish_table.insertAdjacentHTML('beforeend', dish_rows);
    });
});

function showDishNameEditButton(dishId) { var editButton = document.getElementById("editDishNameButton" + dishId);editButton.style.display = "inline-block";} // Показываем кнопку

function hideDishNameEditButton(dishId) { var editButton = document.getElementById("editDishNameButton" + dishId);editButton.style.display = "none";} // Скрываем кнопку

function hideDishNameEditButtonWithDelay(dishId) { setTimeout(function () { hideDishNameEditButton(dishId); }, 300);}

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
        <select id="newIngredient" class="add_ingredient_select">
            <option value=''></option>
            ${ingredientToAdd}
        </select>
        <input id="newRecipeIngredientVolume" class="add_ingredient_volume" type="number" placeholder="Объем">
        <button class="add_ingredient" onclick="addIngredient(${data['id']})">Добавить</button>
    `;
    addIngredientsContainer.innerHTML = addIngredientMenu;

    recipeTable.innerHTML = '';

    recipeKeys.forEach((key) => {
        var ingredient = data['Recipe'][key];
        var recipeRow = `
            <tr class="">
                <td class="padding_4">${data['ingridients'][key]['name']}</td>
                <td class="input_volume">
                    <input id="set_ingridient_volume${key}" class="input" type="number" value="${ingredient}" onblur="EditVolume(${data['id']}, ${key})"> ${data['ingridients'][key]['volume']}
                </td>
                <td class="ingredients_actions"><button class="delete_ingredient" onclick="DeleteIngredientFromRecipe(${data['id']}, ${key})">Удалить</button></td>
            </tr>
        `;
        recipeTable.insertAdjacentHTML('beforeend', recipeRow);
    });

    document.getElementById("recipeWindow").style.display = 'block';
});

function СloseRecipeWindow() {document.getElementById('recipeWindow').style.display = 'none';}

function addIngredient(id) {

    var IngredientID = document.getElementById('newIngredient').value;
    if (IngredientID === '') { alert("Необходимо выбрать ингридиент для добавления в рецепт."); return; }

    var newIngredientVolume = document.getElementById('newRecipeIngredientVolume').value;
    if (newIngredientVolume == '') { newIngredientVolume = 0 }

    var IngredientName = document.getElementById('newIngredient').options[document.getElementById('newIngredient').selectedIndex].text;

    socket.emit("AddIngredientToRecipe", { 'DishID': id, 'IngredientID': IngredientID, 'IngredientName': IngredientName, 'volume': newIngredientVolume})
}

function DeleteIngredientFromRecipe(DishID, IngredientID) { socket.emit("DeleteIngredientFromRecipe", { 'DishID': DishID, 'IngredientID': IngredientID }) }

function EditVolume(DishID, IngredientID) {
    socket.emit("EditVolume", { 'DishID': DishID, 'IngredientID': IngredientID, 'Volume': document.getElementById('set_ingridient_volume' + IngredientID).value })
}