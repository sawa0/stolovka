// Утилиты и общие функции

// Константы
const DAYS_OF_WEEK = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];
const DAYS_OF_WEEK_SHORT = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];
const MONTHS = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];
const MONTHS_SHORT = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"];

/**
 * Получить ISO-неделю для заданной даты
 * @param {Date} date - Дата
 * @returns {string} Строка формата "YYYY-Www"
 */
function getISOWeek(date) {
    const tmp = new Date(date);
    tmp.setDate(tmp.getDate() + 3 - (tmp.getDay() + 6) % 7);

    const firstThursday = new Date(tmp.getFullYear(), 0, 4);
    const weekNumber = 1 + Math.round(
        ((tmp - firstThursday) / 86400000 - 3 + (firstThursday.getDay() + 6) % 7) / 7
    );

    return `${tmp.getFullYear()}-W${String(weekNumber).padStart(2, '0')}`;
}

/**
 * Получить даты недели с форматированием
 * @param {string} weekString - Строка формата "YYYY-Www"
 * @returns {Array<string>} Массив отформатированных дат
 */
function getWeekDatesFormatted(weekString) {
    const [year, week] = weekString.split('-W').map(Number);

    const simpleDate = new Date(year, 0, 4);
    const dayOfWeek = (simpleDate.getDay() + 6) % 7;
    const weekStart = new Date(simpleDate);
    weekStart.setDate(simpleDate.getDate() - dayOfWeek + (week - 1) * 7);

    return Array.from({ length: 7 }, (_, i) => {
        const d = new Date(weekStart);
        d.setDate(weekStart.getDate() + i);
        return `${DAYS_OF_WEEK[i]}, ${d.getDate()} ${MONTHS[d.getMonth()]}`;
    });
}

/**
 * Форматировать месяц для отчёта
 * @param {Date} date - Дата
 * @returns {string} Строка формата "YYYY-MM"
 */
function formatReportMonth(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
}

/**
 * Дополнить строку символами до нужной длины
 * @param {string} text - Исходный текст
 * @param {string} filler - Символ-заполнитель
 * @param {number} length - Целевая длина
 * @returns {string} Дополненная строка
 */
function padString(text, filler, length) {
    if (text.length >= length) {
        return text;
    }
    const fillerLength = length - text.length;
    const fillerString = filler.repeat(fillerLength);
    return text + fillerString;
}

/**
 * Показать/скрыть кнопку редактирования с задержкой
 */
function createEditButtonHandlers(prefix) {
    return {
        show: (id) => {
            const button = document.getElementById(`${prefix}${id}`);
            if (button) button.style.display = "inline-block";
        },
        hide: (id) => {
            const button = document.getElementById(`${prefix}${id}`);
            if (button) button.style.display = "none";
        },
        hideWithDelay: (id) => {
            setTimeout(() => {
                const button = document.getElementById(`${prefix}${id}`);
                if (button) button.style.display = "none";
            }, 300);
        }
    };
}

/**
 * Фильтрация списка по значению input
 * @param {string} inputId - ID поля ввода
 * @param {string} columnClass - Класс строк для фильтрации
 * @param {string} inputSelector - Селектор input внутри строки
 */
function filterList(inputId, columnClass, inputSelector = 'input') {
    const filter = document.getElementById(inputId).value.toLowerCase();
    const columns = document.getElementsByClassName(columnClass);

    if (filter === '') {
        for (let i = 0; i < columns.length; i++) {
            columns[i].style.display = 'table-row';
        }
    } else {
        for (let i = 0; i < columns.length; i++) {
            const input = columns[i].querySelector(inputSelector);
            const text = input.value.toLowerCase();
            columns[i].style.display = text.includes(filter) ? 'table-row' : 'none';
        }
    }
}

/**
 * Валидация: проверка на пустую строку
 * @param {string} value - Значение для проверки
 * @param {string} fieldName - Название поля (для сообщения об ошибке)
 * @returns {boolean} true если валидно
 */
function validateNotEmpty(value, fieldName) {
    if (value.trim() === '') {
        alert(`${fieldName} не может быть пустым`);
        return false;
    }
    return true;
}

/**
 * Валидация: проверка на выбор значения
 * @param {string} value - Значение для проверки
 * @param {string} message - Сообщение об ошибке
 * @returns {boolean} true если валидно
 */
function validateSelected(value, message) {
    if (value === '') {
        alert(message);
        return false;
    }
    return true;
}
