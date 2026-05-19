// ============================================
// Constants
// ============================================
const ORDER_CONFIRMATION_TYPES = {
    OFF: 'off',
    ON: 'on',
    AUTO: 'auto'
};

const ORDER_STATUS = {
    WAITING: 'waiting',
    ACCEPTED: 'accepted',
    CANCELLED: 'cancelled'
};

const DECISION_TYPES = {
    ACCEPT: 'accept',
    CANCEL: 'cancel'
};

// ============================================
// State
// ============================================
let socket = io.connect(document.domain + ':' + location.port);
let activeOrder = null;
let orderStatus = null;
let countdownTimer = null;
let countdownInterval = null;

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
// Order Management
// ============================================
socket.on('new_order', function (data) {
    const [confirmationSettings, order] = data;

    activeOrder = order;
    orderStatus = ORDER_STATUS.WAITING;

    displayOrder(order);
    handleConfirmationType(confirmationSettings);
});

function displayOrder(order) {
    document.querySelector('.username').textContent = order.userName;

    const tableBody = document.querySelector('.current_order_body');
    tableBody.innerHTML = '';

    order.order.forEach(item => {
        const [dishName, [price, quantity]] = item;

        if (quantity == 0) return;

        const row = `
            <tr>
                <td>${dishName}</td>
                <td>${quantity}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

function handleConfirmationType(settings) {
    const [type, autoConfirmTime] = settings;

    hideDecisionButtons();

    if (type === ORDER_CONFIRMATION_TYPES.OFF) {
        return;
    }

    showDecisionButtons();

    if (type === ORDER_CONFIRMATION_TYPES.AUTO) {
        startAutoConfirmationTimer(autoConfirmTime);
    }
}

function showDecisionButtons() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.display = 'block';
        btn.style.animation = 'none';
    });
}

function hideDecisionButtons() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.style.display = 'none';
    });
}

// ============================================
// Auto-Confirmation Timer
// ============================================
function startAutoConfirmationTimer(seconds) {
    const countdownElement = document.getElementById('countdown');
    countdownElement.style.display = 'block';

    countdownTimer = seconds;
    updateCountdownDisplay();

    countdownInterval = setInterval(() => {
        if (orderStatus !== ORDER_STATUS.WAITING) {
            stopCountdownTimer();
            return;
        }

        countdownTimer--;
        updateCountdownDisplay();

        if (countdownTimer <= 0) {
            stopCountdownTimer();
            processOrderDecision(DECISION_TYPES.ACCEPT);
        }
    }, 1000);
}

function updateCountdownDisplay() {
    const countdownElement = document.getElementById('countdown');
    countdownElement.textContent = `(${countdownTimer}c)`;
}

function stopCountdownTimer() {
    if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
    }

    document.getElementById('countdown').style.display = 'none';
}

// ============================================
// Order Decision
// ============================================
function orderDecision(decision) {
    processOrderDecision(decision);
}

function processOrderDecision(decision) {
    stopCountdownTimer();
    hideDecisionButtons();

    animateDecisionButton(decision);

    socket.emit('decision', {
        decision: decision,
        order: activeOrder
    });

    resetOrderState();
}

function animateDecisionButton(decision) {
    const buttonClass = decision === DECISION_TYPES.ACCEPT ? '.confirm' : '.cancel';
    const button = document.querySelector(buttonClass);

    button.style.animation = 'shrink-text 0.5s ease-in-out';

    button.addEventListener('animationend', () => {
        document.querySelectorAll('.btn').forEach(btn => {
            btn.style.animation = 'hide-buttons 0.5s forwards';
        });
    }, { once: true });
}

function resetOrderState() {
    activeOrder = null;
    orderStatus = null;
    countdownTimer = null;
}

// ============================================
// Order History
// ============================================
socket.on('today_transactions', function (transactions) {
    displayOrderHistory(transactions);
});

function displayOrderHistory(transactions) {
    const historyTable = document.getElementById('order_history');
    historyTable.innerHTML = '';

    // Show most recent first
    const reversedTransactions = [...transactions].reverse();

    reversedTransactions.forEach(transaction => {
        const [orderId, date, time, userName] = transaction;

        const row = `
            <tr>
                <td class="history_table_id">${orderId}</td>
                <td>${userName}</td>
                <td class="history_table_time">${time}</td>
            </tr>
        `;
        historyTable.insertAdjacentHTML('beforeend', row);
    });
}

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    socket.emit('get', 'transactions');
});
