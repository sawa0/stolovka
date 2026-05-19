// Модуль управления настройками

/**
 * Обработка данных настроек от сервера
 */
socket.on('Settings', function (data) {
    // OrderConfirmationType
    const orderConfirmation = data['OrderConfirmation'];

    document.getElementById('OrderConfirmationType_on').classList.remove('choised_settings');
    document.getElementById('OrderConfirmationType_off').classList.remove('choised_settings');
    document.getElementById('OrderConfirmationType_auto').classList.remove('choised_settings');

    document.getElementById('OrderConfirmationType_' + orderConfirmation[0]).classList.add('choised_settings');

    document.getElementById('OrderAutoConfirmationTime').value = orderConfirmation[1];

    // TGReportAutosendParametrs
    const tgSettings = data['TGReportAutosendParametrs'];

    document.getElementById('TG_Bot_API_Key').value = tgSettings['bot_api_key'];
    document.getElementById('TG_User_ID').value = tgSettings['tg_user_id'];

    // TGReportAutosend
    document.getElementById('TGReportAutosend').checked = data['TGReportAutosend'];
});

/**
 * Обновление времени автоподтверждения заказа
 */
function orderAutoConfirmationTimeUpdate() {
    socket.emit("updateSettings", ["OrderAutoConfirmationTime", document.getElementById('OrderAutoConfirmationTime').value]);
}

/**
 * Обновление типа подтверждения заказа
 * @param {string} type - Тип подтверждения (on/off/auto)
 */
function orderConfirmationTypeUpdate(type) {
    socket.emit("updateSettings", ["OrderConfirmationType", type]);
}

/**
 * Обновление приложения
 */
function appUpdate() {
    socket.emit('app_update');
}

/**
 * Тестирование Telegram настроек
 */
function telegramTest() {
    function telegramCheckResult(result, message = "") {
        const el = document.getElementById('telegram_check_result');

        if (result) {
            el.textContent = 'test complete';
            document.getElementById('telegram_save_button').style.display = 'block';
            document.getElementById('telegram_test_button').style.display = 'none';
        } else {
            el.textContent = 'test failed' + (message ? `: ${message}` : '');
        }
    }

    var token = document.getElementById('TG_Bot_API_Key').value;
    var chatId = document.getElementById('TG_User_ID').value;

    if (!token || !chatId) {
        alert("Значения token или chatId не могут быть пустыми.");
        return;
    }

    fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            chat_id: chatId,
            text: "test"
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.ok) {
                telegramCheckResult(true);
            } else {
                telegramCheckResult(false, data.description);
            }
        })
        .catch(error => {
            telegramCheckResult(false, error.message);
        });
}

/**
 * Сброс теста Telegram
 */
function tgTestReset() {
    document.getElementById('telegram_check_result').innerHTML = '';
    document.getElementById('telegram_save_button').style.display = 'none';
    document.getElementById('telegram_test_button').style.display = 'block';
}

/**
 * Сохранение настроек Telegram
 */
function saveTelegramSettings() {
    const botApiKey = document.getElementById('TG_Bot_API_Key').value;
    const tgUserId = document.getElementById('TG_User_ID').value;

    socket.emit("updateSettings", ["TGReportAutosendParametrs", {
        'bot_api_key': botApiKey,
        'tg_user_id': tgUserId
    }]);
}

/**
 * Обновление автоотправки в Telegram
 */
function tgAutosendUpdate() {
    socket.emit("updateSettings", ["TGReportAutosend", document.getElementById('TGReportAutosend').checked]);
}

/**
 * Инициализация модуля обновлений приложения
 */
let updateManager = null;
let updateUI = null;

function initUpdateModule() {
    updateManager = new UpdateManager();
    updateUI = new UpdateUI(updateManager, socket);

    // Рендерим UI обновлений в контейнер
    const updateContainer = document.getElementById('update-section');
    if (updateContainer) {
        updateUI.render('update-section');
    }
}

// Инициализация при загрузке страницы настроек
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUpdateModule);
} else {
    initUpdateModule();
}

