var socket = io.connect(document.domain + ':' + location.port);

socket.on('connect', function () {  // подключение к серверу
    console.log('WebSocket connection established');
});

socket.on('reboot', function (data) { setTimeout(function () { location.reload(); }, 5000); });

////////////////////////////////////////////
//          Заполнение клавиатуры
//     для выбора первой буквы фамилии
////////////////////////////////////////////
var users;
socket.on('users', function (data) {
    users = data;
    let letters = [];
    for (var i = 0; i < users.length; i++) {
        if (!letters.includes(users[i][1][0])) {
            letters.push(users[i][1][0]);
        }
    }
    const keyboardContainer = document.querySelector('.keyboard');
    letters.forEach(letter => {
        const button = document.createElement('button');
        button.className = 'last_name_key';
        button.innerHTML = letter;
        button.setAttribute('onclick', `letter('${letter}')`);
        keyboardContainer.appendChild(button);
    });
});
////////////////////////////////////////////
//  настройка страницы выбора пользователя
////////////////////////////////////////////
var selected_letter;
function letter(l) {
    selected_letter = l;
    document.querySelector('.keyboard').style.display = "none";
    document.querySelector('.choise_user').style.display = "block";

    let user_to_chose = []
    for (var i = 0; i < users.length; i++) {
        if (users[i][1][0] == selected_letter) {
            user_to_chose.push(users[i]);
        }
    }
    const usersContainer = document.querySelector('.choise_user_div');
    user_to_chose.forEach(user => {
        const button = document.createElement('button');
        button.className = 'key';
        button.innerHTML = user[1];
        button.setAttribute('onclick', `select_user('${user[0]}')`);
        usersContainer.appendChild(button);
    });
    
}
////////////////////////////////////////////
//
////////////////////////////////////////////
var user;

function select_user(id) {
    
    for (var i = 0; i < users.length; i++) {
        if (users[i][0] == id) {
            user = users[i];
            break;
        }
    }


    document.querySelector('.choise_user').style.display = "none";
    
    document.getElementById('user_name').innerText = user[1];

    document.querySelector('.wrapper').style.display = "flex";

    socket.emit('get', "menu");
}
////////////////////////////////////////////
var order;
document.addEventListener('DOMContentLoaded', function () {

    socket.emit('get', "users"); // запрос данных активных пользователей

    document.querySelector('.back').addEventListener('click', function () {
        selected_letter = "";
        document.querySelector('.keyboard').style.display = "flex";
        document.querySelector('.choise_user').style.display = "none";
        document.querySelector('.choise_user_div').innerHTML = '';
    }); //  обработчик возврата к клавиатуре

    document.querySelector('.cancel').addEventListener('click', function () {
        selected_letter = ""
        document.querySelector('.keyboard').style.display = "flex";
        document.querySelector('.choise_user').style.display = "none";
        document.querySelector('.choise_user_div').innerHTML = '';
        document.querySelector('.wrapper').style.display = "none";
        document.querySelector('.menu_table').innerHTML = '';
        total_price_resume();
    }); //  обработчик отмены заказа

    document.querySelector('.previous_dey').addEventListener('click', function () {
        if (active_dey == 0) {
            active_dey = 1;
            document.getElementById('previous_dey').innerText = 'Поточний день';
            document.getElementById("today_menu_table").style.display = "none";
            document.getElementById("previous_day_menu_table").style.display = "table";
        } else {
            active_dey = 0;
            document.getElementById('previous_dey').innerText = 'Попередній день';
            document.getElementById("today_menu_table").style.display = "table";
            document.getElementById("previous_day_menu_table").style.display = "none";
        }
    }); //  обработчик переключения дня

    document.querySelector('.full_lunch').addEventListener('click', function () {

        const tableId = active_dey === 0 ? "today_menu_table" : "previous_day_menu_table";

        for (let i = 1; i <= 8; i++) {

            const quantityElement = document.getElementById(tableId).querySelector(`#quantity${i}`);

            if (quantityElement) {
                quantityElement.value = 1;
            }
        }
        total_price_resume();
    }); //  обработчик заказа полного обеда

    document.querySelector('.buy').addEventListener('click', function () {
        let basket = [];
        function table_price_calc(table) {

            for (let i = 1; i <= 8; i++) {

                if (table.querySelector("#quantity" + i) == null) { continue; }
                if (table.querySelector("#quantity" + i).value == 0) { continue; }

                var dish_price = table.querySelector("#dish_price" + i).textContent.slice(0, -4);
                var quantity = table.querySelector("#quantity" + i).value;
                var dish_name = table.querySelector("#dish_name" + i).textContent;
                basket.push([dish_name, [dish_price, quantity]]);
            }
        }

        table_price_calc(document.getElementById("previous_day_menu_table"))
        table_price_calc(document.getElementById("today_menu_table"))

        if (basket.length == 0) { return; }

        order = { 'userName': user[1], 'userID': user[0], 'order': basket };

        document.querySelector('.form').style.display = "none";
        document.querySelector('.accept_order').style.display = "block";

        const final_order_container = document.querySelector('.final_order');

        function padString(text, filler, length) {
            if (text.length >= length) {
                return text;
            }
            let fillerLength = length - text.length;
            let fillerString = filler.repeat(fillerLength);
            return text + fillerString;
        }

        for (var i = 0; i < basket.length; i++) {
            if (basket[i][1][1] == 0) { continue; }

            const cheak_item = document.createElement('p');
            cheak_item.innerText = padString(basket[i][0], ".", 35) + " X" + basket[i][1][1] + " = " + (basket[i][1][0] * basket[i][1][1]).toFixed(2) + "грн";
            cheak_item.className = 'cheak_item';
            final_order_container.appendChild(cheak_item);
        }

        document.querySelector('.final_price').innerText = document.getElementById("total_price").textContent;
        
    });

    document.querySelector('.edit_order_btn').addEventListener('click', function () {
        document.querySelector('.final_order').innerHTML = '';
        document.querySelector('.final_price').innerHTML = '';

        document.querySelector('.form').style.display = "block";
        document.querySelector('.accept_order').style.display = "none";
    }); //  обработчик отмены заказа на странице чека

    document.querySelector('.accept_order_btn').addEventListener('click', function () {

        document.querySelector('.accept_order').style.display = "none";
        document.querySelector('.waiting_confirmation').style.display = "block";

        socket.emit('new_order', order);
    });

    let currentDate = new Date();
    if (currentDate.getDay() !== 1) {
        document.getElementById('previous_dey').style.display = "block";
    }
});
////////////////////////////////////////////
//             loading menu
////////////////////////////////////////////
var active_dey = 0;
var today_menu;
var previous_day_menu;
var regular_menu;
let dishes;

socket.on('menu', function (data) {

    dishes = data['dishes'];
    regular_menu = data['regular'];

    today_menu = data['today_data'] || { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '' };
    previous_day_menu = data['previous_dey_data'] || { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '' };

    for (let dayIndex = 1; dayIndex < 9; dayIndex++) {
        if (regular_menu[dayIndex] != "") {
            today_menu[dayIndex] = regular_menu[dayIndex];
            previous_day_menu[dayIndex] = regular_menu[dayIndex];
        }
    }

    menu_table_filling();
});

function menu_table_filling() {

    const today_menu_table = document.getElementById('today_menu_table');
    const previous_day_menu_table = document.getElementById('previous_day_menu_table');

    today_menu_table.innerHTML = '';
    previous_day_menu_table.innerHTML = '';


    function table_filling(menu, table) {

        for (var i = 1; i < 9; i++) {

            if (menu[i] == "") { continue; }

            var dish_name = dishes[menu[i]]['name'];
            var dish_price = dishes[menu[i]]['price'];

            var newRowHTML = `
        <tr class="dish_column" id="dish_column_${i}">
            <td><p class="dish_name dish_name${i}" id="dish_name${i}">${dish_name}</p></td>
            <td class="quantity-control">
                <span class="price dish_price${i}" id="dish_price${i}">${dish_price} грн</span>
                <button class="left-qua" onclick="decrement(${i})">➖</button>
                <input class="counter quantity${i}" type="value" id="quantity${i}" oninput="total_price_resume()" readonly value="0">
                <button class="right-qua" onclick="increment(${i})">➕</button>
            </td>
        </tr>
        `;

            table.insertAdjacentHTML('beforeend', newRowHTML);
        }
    }

    table_filling(today_menu, today_menu_table)
    table_filling(previous_day_menu, previous_day_menu_table)


    total_price_resume();
}

////////////////////////////////////////////
//              menu functions
////////////////////////////////////////////
function total_price_resume() {

    let total_price = 0;
    function table_price_calc(table) {

        for (let i = 1; i <= 8; i++) {

            if (table.querySelector("#quantity" + i) == null) { continue; }

            var dish_price = table.querySelector("#dish_price" + i).textContent.slice(0, -4);
            var quantity = table.querySelector("#quantity" + i).value;
            total_price += parseFloat(dish_price) * quantity;
        }
    }

    table_price_calc(document.getElementById("previous_day_menu_table"))
    table_price_calc(document.getElementById("today_menu_table"))

    document.getElementById("total_price").innerText = "Усього: " + total_price.toFixed(2) + " грн";

}
function increment(index) {

    const tableId = active_dey === 0 ? "today_menu_table" : "previous_day_menu_table";
    const inputElement = document.getElementById(tableId).querySelector(`#quantity${index}`);

    var value = parseInt(inputElement.value, 10);
    inputElement.value = value + 1;
    total_price_resume();
}

function decrement(index) {

    const tableId = active_dey === 0 ? "today_menu_table" : "previous_day_menu_table";
    const inputElement = document.getElementById(tableId).querySelector(`#quantity${index}`);

    var value = parseInt(inputElement.value, 10);
    if (value > 0) {
        inputElement.value = value - 1;
        total_price_resume();
    }
}

////////////////////////////////////////////
//             get decision
////////////////////////////////////////////
socket.on('decision', function (data) {
    console.log(data);
    if (data == 'cancel') {
        document.querySelector('.final_order').innerHTML = '';
        document.querySelector('.final_price').innerHTML = '';

        document.querySelector('.form').style.display = "block";
        document.querySelector('.waiting_confirmation').style.display = "none";
    }
    if (data == 'accept') {
        document.querySelector('.waiting_confirmation_text').style.display = 'none';
        document.querySelector('.waiting_confirmation_accept').style.display = 'block';
        
        setTimeout(() => {
            location.reload();
        }, 1000);
    }
});