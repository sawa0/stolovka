// ============================================
// Constants
// ============================================
const MENU_POSITIONS = 8;
const PRICE_SUFFIX = ' грн';
const PRICE_SUFFIX_LENGTH = 4;

// ============================================
// State
// ============================================
let socket = io.connect(document.domain + ':' + location.port);
let users = [];
let selectedLetter = '';
let selectedUser = null;
let activeDayIndex = 0; // 0 = today, 1 = previous day
let todayMenu = {};
let previousDayMenu = {};
let regularMenu = {};
let dishes = {};

// ============================================
// Socket Connection
// ============================================
socket.on('connect', function () {
    console.log('WebSocket connection established');
});

socket.on('reboot', function () {
    setTimeout(() => location.reload(), 5000);
});

// ============================================
// Users Management
// ============================================
socket.on('users', function (data) {
    users = data;
    renderLetterKeyboard();
});

function renderLetterKeyboard() {
    const letters = [...new Set(users.map(user => user[1][0]))];
    const keyboardContainer = document.querySelector('.keyboard');

    letters.forEach(letter => {
        const button = document.createElement('button');
        button.className = 'last_name_key';
        button.textContent = letter;
        button.onclick = () => selectLetter(letter);
        keyboardContainer.appendChild(button);
    });
}

function selectLetter(letter) {
    selectedLetter = letter;
    document.querySelector('.keyboard').style.display = 'none';
    document.querySelector('.choise_user').style.display = 'block';

    const filteredUsers = users.filter(user => user[1][0] === selectedLetter);
    renderUserButtons(filteredUsers);
}

function renderUserButtons(filteredUsers) {
    const usersContainer = document.querySelector('.choise_user_div');
    usersContainer.innerHTML = '';

    filteredUsers.forEach(user => {
        const button = document.createElement('button');
        button.className = 'key';
        button.textContent = user[1];
        button.onclick = () => selectUser(user[0]);
        usersContainer.appendChild(button);
    });
}

function selectUser(userId) {
    selectedUser = users.find(user => user[0] == userId);

    if (!selectedUser) return;

    document.querySelector('.choise_user').style.display = 'none';
    document.getElementById('user_name').textContent = selectedUser[1];
    document.querySelector('.wrapper').style.display = 'flex';

    socket.emit('get', 'menu');
}

function resetToLetterSelection() {
    selectedLetter = '';
    document.querySelector('.keyboard').style.display = 'flex';
    document.querySelector('.choise_user').style.display = 'none';
    document.querySelector('.choise_user_div').innerHTML = '';
}

function cancelOrder() {
    resetToLetterSelection();
    document.querySelector('.wrapper').style.display = 'none';
    document.querySelector('.menu_table').innerHTML = '';
    updateTotalPrice();
}

// ============================================
// Menu Management
// ============================================
socket.on('menu', function (data) {
    dishes = data['dishes'];
    regularMenu = data['regular'];

    todayMenu = data['today_data'] || createEmptyMenu();
    previousDayMenu = data['previous_day_data'] || createEmptyMenu();

    applyRegularMenuToDaily();
    renderMenuTables();
});

function createEmptyMenu() {
    const menu = {};
    for (let i = 1; i <= MENU_POSITIONS; i++) {
        menu[i] = '';
    }
    return menu;
}

function applyRegularMenuToDaily() {
    for (let i = 1; i <= MENU_POSITIONS; i++) {
        if (regularMenu[i] !== '') {
            todayMenu[i] = regularMenu[i];
            previousDayMenu[i] = regularMenu[i];
        }
    }
}

function renderMenuTables() {
    const todayTable = document.getElementById('today_menu_table');
    const previousDayTable = document.getElementById('previous_day_menu_table');

    todayTable.innerHTML = '';
    previousDayTable.innerHTML = '';

    fillMenuTable(todayMenu, todayTable);
    fillMenuTable(previousDayMenu, previousDayTable);

    updateTotalPrice();
}

function fillMenuTable(menu, table) {
    for (let i = 1; i <= MENU_POSITIONS; i++) {
        if (menu[i] === '') continue;

        const dish = dishes[menu[i]];
        if (!dish) continue;

        const row = createMenuRow(i, dish.name, dish.price);
        table.insertAdjacentHTML('beforeend', row);
    }
}

function createMenuRow(index, dishName, dishPrice) {
    return `
        <tr class="dish_column" id="dish_column_${index}">
            <td><p class="dish_name" id="dish_name${index}">${dishName}</p></td>
            <td class="quantity-control">
                <span class="price" id="dish_price${index}">${dishPrice}${PRICE_SUFFIX}</span>
                <button class="left-qua" onclick="decrementQuantity(${index})">➖</button>
                <input class="counter" type="text" id="quantity${index}" oninput="updateTotalPrice()" readonly value="0">
                <button class="right-qua" onclick="incrementQuantity(${index})">➕</button>
            </td>
        </tr>
    `;
}

function toggleDay() {
    activeDayIndex = activeDayIndex === 0 ? 1 : 0;

    const previousDayBtn = document.getElementById('previous_dey');
    const todayTable = document.getElementById('today_menu_table');
    const previousDayTable = document.getElementById('previous_day_menu_table');

    if (activeDayIndex === 0) {
        previousDayBtn.textContent = 'Попередній день';
        todayTable.style.display = 'table';
        previousDayTable.style.display = 'none';
    } else {
        previousDayBtn.textContent = 'Поточний день';
        todayTable.style.display = 'none';
        previousDayTable.style.display = 'table';
    }
}

function orderFullLunch() {
    const tableId = activeDayIndex === 0 ? 'today_menu_table' : 'previous_day_menu_table';
    const table = document.getElementById(tableId);

    for (let i = 1; i <= MENU_POSITIONS; i++) {
        const quantityInput = table.querySelector(`#quantity${i}`);
        if (quantityInput) {
            quantityInput.value = 1;
        }
    }

    updateTotalPrice();
}

// ============================================
// Quantity Controls
// ============================================
function incrementQuantity(index) {
    const input = getQuantityInput(index);
    if (!input) return;

    input.value = parseInt(input.value, 10) + 1;
    updateTotalPrice();
}

function decrementQuantity(index) {
    const input = getQuantityInput(index);
    if (!input) return;

    const value = parseInt(input.value, 10);
    if (value > 0) {
        input.value = value - 1;
        updateTotalPrice();
    }
}

function getQuantityInput(index) {
    const tableId = activeDayIndex === 0 ? 'today_menu_table' : 'previous_day_menu_table';
    return document.getElementById(tableId)?.querySelector(`#quantity${index}`);
}

// ============================================
// Price Calculation
// ============================================
function updateTotalPrice() {
    const total = calculateTablePrice('previous_day_menu_table') +
                  calculateTablePrice('today_menu_table');

    document.getElementById('total_price').textContent = `Усього: ${total.toFixed(2)}${PRICE_SUFFIX}`;
}

function calculateTablePrice(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return 0;

    let total = 0;

    for (let i = 1; i <= MENU_POSITIONS; i++) {
        const priceElement = table.querySelector(`#dish_price${i}`);
        const quantityElement = table.querySelector(`#quantity${i}`);

        if (!priceElement || !quantityElement) continue;

        const price = parseFloat(priceElement.textContent.slice(0, -PRICE_SUFFIX_LENGTH));
        const quantity = parseInt(quantityElement.value, 10);

        total += price * quantity;
    }

    return total;
}

// ============================================
// Order Processing
// ============================================
function collectOrderItems() {
    const basket = [];

    collectTableItems('previous_day_menu_table', basket);
    collectTableItems('today_menu_table', basket);

    return basket;
}

function collectTableItems(tableId, basket) {
    const table = document.getElementById(tableId);
    if (!table) return;

    for (let i = 1; i <= MENU_POSITIONS; i++) {
        const quantityElement = table.querySelector(`#quantity${i}`);
        if (!quantityElement || quantityElement.value == 0) continue;

        const dishName = table.querySelector(`#dish_name${i}`).textContent;
        const dishPrice = table.querySelector(`#dish_price${i}`).textContent.slice(0, -PRICE_SUFFIX_LENGTH);
        const quantity = quantityElement.value;

        basket.push([dishName, [dishPrice, quantity]]);
    }
}

function processOrder() {
    const basket = collectOrderItems();

    if (basket.length === 0) return;

    const order = {
        userName: selectedUser[1],
        userID: selectedUser[0],
        order: basket
    };

    showOrderConfirmation(basket);

    return order;
}

function showOrderConfirmation(basket) {
    document.querySelector('.form').style.display = 'none';
    document.querySelector('.accept_order').style.display = 'block';

    const finalOrderContainer = document.querySelector('.final_order');
    finalOrderContainer.innerHTML = '';

    basket.forEach(item => {
        if (item[1][1] == 0) return;

        const itemElement = document.createElement('p');
        itemElement.className = 'cheak_item';
        itemElement.textContent = formatOrderItem(item);
        finalOrderContainer.appendChild(itemElement);
    });

    document.querySelector('.final_price').textContent = document.getElementById('total_price').textContent;
}

function formatOrderItem(item) {
    const [name, [price, quantity]] = item;
    const total = (price * quantity).toFixed(2);
    return padString(name, '.', 35) + ` X${quantity} = ${total} грн`;
}

function padString(text, filler, length) {
    if (text.length >= length) return text;
    return text + filler.repeat(length - text.length);
}

function editOrder() {
    document.querySelector('.final_order').innerHTML = '';
    document.querySelector('.final_price').innerHTML = '';
    document.querySelector('.form').style.display = 'block';
    document.querySelector('.accept_order').style.display = 'none';
}

function submitOrder() {
    const order = processOrder();

    document.querySelector('.accept_order').style.display = 'none';
    document.querySelector('.waiting_confirmation').style.display = 'block';

    socket.emit('new_order', order);
}

// ============================================
// Order Decision Handling
// ============================================
socket.on('decision', function (decision) {
    console.log('Order decision:', decision);

    if (decision === 'cancel') {
        handleOrderCancellation();
    } else if (decision === 'accept') {
        handleOrderAcceptance();
    }
});

function handleOrderCancellation() {
    document.querySelector('.final_order').innerHTML = '';
    document.querySelector('.final_price').innerHTML = '';
    document.querySelector('.form').style.display = 'block';
    document.querySelector('.waiting_confirmation').style.display = 'none';
}

function handleOrderAcceptance() {
    document.querySelector('.waiting_confirmation_text').style.display = 'none';
    document.querySelector('.waiting_confirmation_accept').style.display = 'block';

    setTimeout(() => location.reload(), 1000);
}

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    socket.emit('get', 'users');

    document.querySelector('.back').addEventListener('click', resetToLetterSelection);
    document.querySelector('.cancel').addEventListener('click', cancelOrder);
    document.querySelector('.previous_dey').addEventListener('click', toggleDay);
    document.querySelector('.full_lunch').addEventListener('click', orderFullLunch);
    document.querySelector('.buy').addEventListener('click', () => processOrder());
    document.querySelector('.edit_order_btn').addEventListener('click', editOrder);
    document.querySelector('.accept_order_btn').addEventListener('click', submitOrder);

    // Show previous day button if not Monday
    const currentDate = new Date();
    if (currentDate.getDay() !== 1) {
        document.getElementById('previous_dey').style.display = 'block';
    }
});
