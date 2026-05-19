// Модуль управления блюдами и рецептами

const dishEditButtons = createEditButtonHandlers('editDishNameButton');
var dishToDelete = 0;

/**
 * Обработка данных блюд от сервера
 */
socket.on('Dishes', function (data) {
    const dishTable = document.getElementById('dish_table');
    dishTable.innerHTML = '';
    var dishRows = '';

    data.sort((a, b) => a[1].localeCompare(b[1], 'uk'));
    data.forEach((dish) => {
        const zeroVolumeIngredients = Object.values(JSON.parse(dish[3])).some(value => value === 0);

        dishRows += `
        <tr class="dish_column">
            <td>
                <input class="table_input_dish_name" type="text" id="DishName${dish[0]}" value="${dish[1]}" onfocus="showDishNameEditButton(${dish[0]})" onblur="hideDishNameEditButtonWithDelay(${dish[0]})">
                <button id="editDishNameButton${dish[0]}" style="display: none;" title="Сохранить изменённое название" onclick="editDishName(${dish[0]})">✏️</button>
            </td>
            <td class="dish_status">
                <div style="display: flex;">
                    <div class="dish_price">${dish[4]} грн</div>
                    <div style="position: relative;">
                        <button style="border-top-left-radius: 0px; border-bottom-left-radius: 0px;" onclick="recipe(${dish[0]})">Рецептура</button>
                        <div style="display: ${zeroVolumeIngredients ? 'block' : 'none'};" class="dish_allert">Содержит ингредиенты с 0 объёмом</div>
                    </div>
                </div>
            </td>
            <td class="dish_status">
                <div style="display: flex;">
                    <div class="dish_status_div">${dish[2] ? '✔️' : '❌'}</div>
                    <div>
                        <button class="change_dish_status_btn" title="Деактивированное блюдо не будет отображатся в списке блюд. Его всегда можно будет активировать снова" onclick="changeDishStatus(${dish[0]})">
                            ${dish[2] ? 'Деактивировать' : 'Активировать'}
                        </button>
                    </div>
                </div>
            </td>
            <td class="delete_btn_column">
                <button title="Удалить блюдо" class="delete_btn" onclick="deleteDishConfirmationDialog(${dish[0]})">Удалить</button>
            </td>
        </tr>
        `;
    });

    dishTable.innerHTML = dishRows;
    filterDishList();
});

/**
 * Показать кнопку редактирования названия блюда
 * @param {number} dishId - ID блюда
 */
function showDishNameEditButton(dishId) {
    dishEditButtons.show(dishId);
}

/**
 * Скрыть кнопку редактирования названия блюда
 * @param {number} dishId - ID блюда
 */
function hideDishNameEditButton(dishId) {
    dishEditButtons.hide(dishId);
}

/**
 * Скрыть кнопку редактирования названия блюда с задержкой
 * @param {number} dishId - ID блюда
 */
function hideDishNameEditButtonWithDelay(dishId) {
    dishEditButtons.hideWithDelay(dishId);
}

/**
 * Создание нового блюда
 */
function newDish() {
    const dishName = document.getElementById("newDishName").value;
    if (!validateNotEmpty(dishName, 'Название блюда')) {
        return;
    }
    socket.emit("NewDish", dishName);
    document.getElementById("newDishName").value = "";
}

/**
 * Редактирование названия блюда
 * @param {number} id - ID блюда
 */
function editDishName(id) {
    socket.emit("EditDishName", [id, document.getElementById('DishName' + id).value]);
}

/**
 * Изменение статуса блюда
 * @param {number} id - ID блюда
 */
function changeDishStatus(id) {
    socket.emit("ChangeDishStatus", id);
}

/**
 * Фильтрация списка блюд
 */
function filterDishList() {
    filterList('newDishName', 'dish_column');
}

/**
 * Отмена удаления блюда
 */
function cancelDishDelete() {
    dishToDelete = 0;
    document.getElementById("accept_dish_delete_conteiner").style.display = 'none';
}

/**
 * Диалог подтверждения удаления блюда
 * @param {number} id - ID блюда
 */
function deleteDishConfirmationDialog(id) {
    dishToDelete = id;
    document.getElementById("accept_dish_delete_conteiner").style.display = 'block';
}

/**
 * Удаление блюда
 */
function deleteDish() {
    document.getElementById("accept_dish_delete_conteiner").style.display = 'none';
    socket.emit("DeleteDish", dishToDelete);
    dishToDelete = 0;
}

/**
 * Открыть окно рецепта
 * @param {number} id - ID блюда
 */
function recipe(id) {
    socket.emit("GetRecipe", id);
}

/**
 * Обработка данных рецепта от сервера
 */
socket.on('Recipe', function (data) {
    const recipeTable = document.getElementById('recipe_table');
    const downloadRecipeDiv = document.getElementById("download_recipe_div");
    const addIngredientsContainer = document.getElementById('add_ingredients_conteiner');
    document.getElementById("recipeName").innerText = data['Name'];

    const recipeKeys = Object.keys(data['Recipe']);
    const ingredientKeys = Object.keys(data['ingredients']);

    let ingredientToAdd = '';

    ingredientKeys.forEach((key) => {
        if (!recipeKeys.includes(key)) {
            ingredientToAdd += `<option value="${key}">${data['ingredients'][key]['name']}</option>`;
        }
    });

    var addIngredientMenu = `
        <div class="add_ingredient_select">
            <select class="add_ingredient_in_dish_select" id="newIngredient">
                <option value=''></option>
                ${ingredientToAdd}
            </select>
        </div>
        <input id="newRecipeIngredientVolume" class="add_ingredient_volume" type="number" placeholder="Объем">
        <button class="add_ingredient" onclick="addIngredient(${data['id']})">Добавить</button>
    `;
    addIngredientsContainer.innerHTML = addIngredientMenu;

    recipeTable.innerHTML = '';
    downloadRecipeDiv.innerHTML = '';

    var downloadRecipeButton = `
        <button class="download_recipe_button" onclick="downloadRecipe(${data['id']})">Скачать рецепт</button>
    `;
    downloadRecipeDiv.innerHTML = downloadRecipeButton;

    var totalPrice = 0;
    var totalWeight = 0;
    var recipeTableContent = '';

    recipeKeys.forEach((key) => {
        var ingredient = data['Recipe'][key];
        if (data['ingredients'][key]['volume'] == "кг.") {
            totalWeight += ingredient;
        }

        var recipeRow = `
            <tr class="">
                <td class="padding_4">${data['ingredients'][key]['name']}</td>
                <td style="width: 140px;">
                    <div class="input_ingredient_per_volume_unit_price">
                        <input class="input" type="number" value="${data['ingredients'][key]['price']}" onblur="ingredientPriceEditFromRecipe(${key}, this.value, ${data['id']})">
                        <div>грн/${data['ingredients'][key]['volume']}</div>
                    </div>
                </td>
                <td class="input_volume">
                    <input style="${ingredient === 0 ? 'background-color: #ffa4a4; border-color: #c83838;' : ''}" id="set_ingredient_volume${key}" class="input" type="number" value="${ingredient}" onblur="editVolume(${data['id']}, ${key}, this.value)"> ${data['ingredients'][key]['volume']}
                </td>
                <td style="width: 100px;">${(data['ingredients'][key]['price'] * ingredient).toFixed(2)} грн</td>
                <td class="delete_btn_column"><button class="delete_btn" onclick="deleteIngredientFromRecipe(${data['id']}, ${key})">Удалить</button></td>
            </tr>
        `;

        recipeTableContent += recipeRow;
        totalPrice += data['ingredients'][key]['price'] * ingredient;
    });

    recipeTable.innerHTML = recipeTableContent;

    document.getElementById("recipe_result_text").innerText = 'Цена всех ингредиентов: ' + totalPrice.toFixed(2) + ' грн | Итоговая цена: ' + (totalPrice * 1.11).toFixed(2) + ' грн';

    document.getElementById("recipeWindow").style.display = 'block';
});

/**
 * Редактирование цены ингредиента из окна рецепта
 * @param {number} id - ID ингредиента
 * @param {string} newPrice - Новая цена
 * @param {number} dishID - ID блюда
 */
function ingredientPriceEditFromRecipe(id, newPrice, dishID) {
    if (newPrice == '') {
        newPrice = 0;
    }
    socket.emit('IngredientPriceEditFromRecipe', {
        ingredientID: id,
        newPrice: newPrice,
        DishID: dishID
    });
}

/**
 * Закрыть окно рецепта
 */
function closeRecipeWindow() {
    socket.emit('getDishList');
    document.getElementById('recipeWindow').style.display = 'none';
}

/**
 * Добавить ингредиент в рецепт
 * @param {number} id - ID блюда
 */
function addIngredient(id) {
    var ingredientID = document.getElementById('newIngredient').value;
    if (!validateSelected(ingredientID, "Необходимо выбрать ингредиент для добавления в рецепт.")) {
        return;
    }

    var newIngredientVolume = document.getElementById('newRecipeIngredientVolume').value;
    if (newIngredientVolume == '') {
        newIngredientVolume = 0;
    }

    var ingredientName = document.getElementById('newIngredient').options[document.getElementById('newIngredient').selectedIndex].text;

    socket.emit("AddIngredientToRecipe", {
        'DishID': id,
        'IngredientID': ingredientID,
        'IngredientName': ingredientName,
        'volume': newIngredientVolume
    });
}

/**
 * Удалить ингредиент из рецепта
 * @param {number} dishID - ID блюда
 * @param {number} ingredientID - ID ингредиента
 */
function deleteIngredientFromRecipe(dishID, ingredientID) {
    socket.emit("DeleteIngredientFromRecipe", {
        'DishID': dishID,
        'IngredientID': ingredientID
    });
}

/**
 * Редактировать объем ингредиента в рецепте
 * @param {number} dishID - ID блюда
 * @param {number} ingredientID - ID ингредиента
 * @param {string} newVolume - Новый объем
 */
function editVolume(dishID, ingredientID, newVolume) {
    if (newVolume == '') {
        newVolume = 0;
    }
    socket.emit("EditVolume", {
        'DishID': dishID,
        'IngredientID': ingredientID,
        'Volume': newVolume
    });
}

/**
 * Скачать рецепт
 * @param {number} dishID - ID блюда
 */
function downloadRecipe(dishID) {
    socket.emit("DownloadRecipe", {
        'DishID': dishID
    });
}
