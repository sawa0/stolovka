var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function () {
    console.log('WebSocket connection established');
});

//  active order
var active_order;
var order_data;
socket.on('new_order', function (order) {

    console.log(JSON.stringify(order));
    
    document.querySelector('.username').innerHTML = '';
    document.querySelector('.username').innerText = order["userName"];

    active_order = order;

    order_data = order["order"];

    const table = document.querySelector('.current_order_body');
    table.innerHTML = '';
    for (var i = 0; i < order_data.length; i++) {

        var dish_quantity = order_data[i][1][1];
        if (dish_quantity == 0) {
            continue
        }

        var dish_name = order_data[i][0];

        var newRowHTML = `
            <tr>
                <td>${dish_name}</td>
                <td>${dish_quantity}</td>
            </tr>
        `;
        table.insertAdjacentHTML('beforeend', newRowHTML);
    }

    order_status = "waiting";

    startConfirmationTimer()
})

let countdown;
function startConfirmationTimer() {

    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.display = 'block';
        btn.style.animation = 'none';
    });

    const countdownElement = document.getElementById('countdown');
    countdown = 15;
    countdownElement.textContent = countdown;

    const interval = setInterval(() => {
        if (order_status == "waiting") {
            countdown--;
            countdownElement.textContent = countdown;
            if (countdown <= 0) {
                clearInterval(interval);
                orderDecision("accept");
            }
        }
        else {
            clearInterval(interval);
        }
    }, 1000);
}

function orderDecision(decision) {

    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.display = 'none';
    });

    var decision_btn;
    if (decision == "accept") {
        decision_btn = document.querySelector('.confirm');
    } else {
        decision_btn = document.querySelector('.cancel');
    }

    decision_btn.style.animation = 'shrink-text 0.5s ease-in-out';
    decision_btn.addEventListener('animationend', () => {
        document.querySelectorAll('.btn').forEach(btn => {
            btn.style.animation = 'hide-buttons 0.5s forwards';
        });
    });

    socket.emit('decision', { 'decision': decision, 'order': active_order });

    active_order = null;
    order_status = null;
    order_data = null;
}


document.addEventListener('DOMContentLoaded', function () {
    socket.emit('get', "transactions");
});

socket.on('today_transactions', function (data) {
    console.log(data)

    const countdownElement = document.getElementById('order_history');
    countdownElement.innerHTML = '';

    data.forEach((transaction) => {
        var transaction_rows = `
            <tr>
                <td class="history_table_id">${transaction[0]}</td>
                <td>${transaction[3]}</td>
                <td class="history_table_time">${transaction[2]}</td>
            </tr>
        `;
        countdownElement.insertAdjacentHTML('beforeend', transaction_rows);
    });
});

