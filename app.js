// app.js

function contactUs(service) {
    const botApi = '7540557414:AAEqUjCnuerTAjRolMTk_pOdRZjct42r8Yw';
    const chatId = '-1001234567890';  // Замените на свой chat_id Telegram группы или пользователя
    const message = `Пользователь заинтересован в услуге: ${service}. Контакт для связи: [Телефон/Email].`;

    const url = `https://api.telegram.org/bot${botApi}/sendMessage?chat_id=${chatId}&text=${encodeURIComponent(message)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                alert('Сообщение отправлено! Мы свяжемся с вами в ближайшее время.');
            } else {
                alert('Произошла ошибка при отправке сообщения.');
            }
        })
        .catch(error => {
            alert('Ошибка сети. Попробуйте позже.');
            console.error('Error:', error);
        });
}
