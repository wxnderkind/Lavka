function openProductDetails(product) {
    let title = '';
    let description = '';

    // Описание товаров
    if (product === 'chatgpt') {
        title = 'ChatGPT Plus';
        description = 'Подписка на ChatGPT Plus — полный доступ к функциям, включая улучшенную версию GPT-4.';
    } else if (product === 'windows') {
        title = 'Ключ Windows 10/11 Home';
        description = 'Лицензионный ключ для активации Windows 10 или 11. Один ключ для одного устройства.';
    } else if (product === 'office') {
        title = 'Office 365';
        description = 'Полный пакет Microsoft Office, включая Word, Excel, PowerPoint, OneNote и другие приложения.';
    }

    // Наполнение модального окна
    document.getElementById('product-title').innerText = title;
    document.getElementById('product-description').innerText = description;

    // Показываем модальное окно
    document.getElementById('product-details').style.display = 'flex';
}

function closeProductDetails() {
    document.getElementById('product-details').style.display = 'none';
}
