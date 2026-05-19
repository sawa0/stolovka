// Модуль управления пользователями

const userEditButtons = createEditButtonHandlers('editButton');

/**
 * Обработка данных пользователей от сервера
 */
socket.on('users', function (data) {
    const usersTable = document.getElementById('users_table');
    usersTable.innerHTML = '';

    data.sort((a, b) => a[1].localeCompare(b[1], 'uk'));

    data.forEach((user) => {
        var usersRows = `
            <tr id="userRow${user[0]}" class="user_column">
                <td>
                    <input class="table_input_user_name" type="text" id="UserName${user[0]}" value="${user[1]}" onfocus="showEditButton(${user[0]})" onblur="hideEditButtonWithDelay(${user[0]})">
                    <button id="editButton${user[0]}" style="display: none;" title="Сохранить изменённое имя" onclick="editUserName(${user[0]})">✏️</button>
                </td>
                <td class="dish_status">
                    <div style="display: flex;">
                        <div class="user_status_div">${user[2] ? '✔️' : '❌'}</div>
                        <div>
                            <button class="change_user_status_btn" title="Деактивированный пользователь не будет отображатся в списке пользователей на странице заказов. его всегда можно будет активировать снова" onclick="changeUserStatus(${user[0]})">
                                ${user[2] ? 'Деактивировать' : 'Активировать'}
                            </button>
                        </div>
                    </div>
                </td>
                <td class="delete_btn_column">
                    <button title="Удалить пользователя (не удалит его из отчётов. если пользователь временно не будет пользоватся столовой деактивируйте его.)" class="delete_btn" onclick="deleteUser(${user[0]})">Удалить</button>
                </td>
            </tr>
        `;
        usersTable.insertAdjacentHTML('beforeend', usersRows);
    });
    filterUserList();
});

/**
 * Фильтрация списка пользователей
 */
function filterUserList() {
    filterList('newUserName', 'user_column');
}

/**
 * Изменение статуса пользователя
 * @param {number} id - ID пользователя
 */
function changeUserStatus(id) {
    socket.emit('ChangeUserStatus', id);
}

/**
 * Удаление пользователя
 * @param {number} id - ID пользователя
 */
function deleteUser(id) {
    socket.emit('DeleteUser', id);
}

/**
 * Редактирование имени пользователя
 * @param {number} id - ID пользователя
 */
function editUserName(id) {
    socket.emit('EditUserName', [id, document.getElementById('UserName' + id).value]);
}

/**
 * Создание нового пользователя
 */
function newUser() {
    socket.emit('newUserName', document.getElementById('newUserName').value);
    document.getElementById('newUserName').value = '';
}

/**
 * Показать кнопку редактирования
 * @param {number} userId - ID пользователя
 */
function showEditButton(userId) {
    userEditButtons.show(userId);
}

/**
 * Скрыть кнопку редактирования
 * @param {number} userId - ID пользователя
 */
function hideEditButton(userId) {
    userEditButtons.hide(userId);
}

/**
 * Скрыть кнопку редактирования с задержкой
 * @param {number} userId - ID пользователя
 */
function hideEditButtonWithDelay(userId) {
    userEditButtons.hideWithDelay(userId);
}
