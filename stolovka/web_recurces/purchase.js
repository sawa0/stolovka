// Модуль управления ингредиентами (закупки)

const ingredientEditButtons = createEditButtonHandlers('editIngredientNameButton');
var ingredientToDelete = 0;

/**
 * Обработка данных ингредиентов от сервера
 */
socket.on('Purchase', function (data) {
    const purchaseTable = document.getElementById('purchase_table');
    purchaseTable.innerHTML = '';

    data.sort((a, b) => a[1].localeCompare(b[1], 'uk'));

    data.forEach((ingredient) => {
        var purchaseRows = `
        <tr class="ingredients_column">
            <td>
                <input class="table_input_ingredient_name" type="text" id="IngredientName${ingredient[0]}" value="${ingredient[1]}" onfocus="showIngredientNameEditButton(${ingredient[0]})" onblur="hideIngredientNameEditButtonWithDelay(${ingredient[0]})">
                <button id="editIngredientNameButton${ingredient[0]}" style="display: none;" title="Сохранить изменённое название" onclick="editIngredientName(${ingredient[0]})">✏️</button>
            </td>
            <td class="ingredient_volume">
                <div class="ingredient_volume_div">
                    <input id="newPrice${ingredient[0]}" value="${ingredient[3]}" class="price_input" type="number" max="999" onblur="editPrice(${ingredient[0]})">
                    <div class="ingredient_price_volume">грн/${ingredient[2]}</div>
                </div>
            </td>
            <td class="delete_btn_column">
                <button class="delete_btn" onclick="deleteIngredientConfirmationDialog(${ingredient[0]})">Удалить</button>
            </td>
        </tr>
        `;

        purchaseTable.insertAdjacentHTML('beforeend', purchaseRows);
    });
    filterIngredientList();
});

/**
 * Редактирование цены ингредиента
 * @param {number} id - ID ингредиента
 */
function editPrice(id) {
    var newPrice = document.getElementById('newPrice' + id).value;
    if (newPrice.trim() === '') {
        return;
    }
    socket.emit('newPrice', [id, newPrice]);
}

/**
 * Создание нового ингредиента
 */
function newIngredient() {
    var newIngredient = [
        document.getElementById('newIngredientName').value,
        document.getElementById('newIngredientVolume').value,
        document.getElementById('newIngredientPrice').value
    ];

    if (!validateNotEmpty(newIngredient[0], 'Название ингредиента')) {
        return;
    }

    document.getElementById('newIngredientName').value = '';
    document.getElementById('newIngredientVolume').value = 'кг.';
    document.getElementById('newIngredientPrice').value = '';

    if (newIngredient[2] == '') {
        newIngredient[2] = 0;
    }

    socket.emit('NewIngredient', newIngredient);
}

/**
 * Фильтрация списка ингредиентов
 */
function filterIngredientList() {
    filterList('newIngredientName', 'ingredients_column');
}

/**
 * Редактирование названия ингредиента
 * @param {number} id - ID ингредиента
 */
function editIngredientName(id) {
    var newIngredientName = document.getElementById('IngredientName' + id).value.trim();
    if (!validateNotEmpty(newIngredientName, 'Имя')) {
        return;
    }
    socket.emit("UpdateIngredientName", [id, newIngredientName]);
}

/**
 * Отмена удаления ингредиента
 */
function cancelIngredientDelete() {
    ingredientToDelete = 0;
    document.getElementById("accept_ingredient_delete_conteiner").style.display = 'none';
}

/**
 * Диалог подтверждения удаления ингредиента
 * @param {number} ingredientID - ID ингредиента
 */
function deleteIngredientConfirmationDialog(ingredientID) {
    ingredientToDelete = ingredientID;
    document.getElementById("accept_ingredient_delete_conteiner").style.display = 'block';
}

/**
 * Удаление ингредиента
 */
function deleteIngredient() {
    document.getElementById("accept_ingredient_delete_conteiner").style.display = 'none';
    socket.emit("DeleteIngredient", ingredientToDelete);
    ingredientToDelete = 0;
}

/**
 * Показать кнопку редактирования названия ингредиента
 * @param {number} ingredientId - ID ингредиента
 */
function showIngredientNameEditButton(ingredientId) {
    ingredientEditButtons.show(ingredientId);
}

/**
 * Скрыть кнопку редактирования названия ингредиента
 * @param {number} ingredientId - ID ингредиента
 */
function hideIngredientNameEditButton(ingredientId) {
    ingredientEditButtons.hide(ingredientId);
}

/**
 * Скрыть кнопку редактирования названия ингредиента с задержкой
 * @param {number} ingredientId - ID ингредиента
 */
function hideIngredientNameEditButtonWithDelay(ingredientId) {
    ingredientEditButtons.hideWithDelay(ingredientId);
}
