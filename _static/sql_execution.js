document.addEventListener('DOMContentLoaded', function() {
    var executeButtons = document.querySelectorAll('.sql-execution-button');

    executeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var codeBlock = this.previousElementSibling;
            var sqlQuery = codeBlock.textContent.trim();

            // Ваш код для выполнения запроса на сервер

            // Пример с использованием fetch API для отправки запроса на сервер
            fetch('/execute-sql', {
                method: 'POST',
                body: JSON.stringify({ query: sqlQuery }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Отображение результатов запроса рядом или под блоком кода
                var resultDiv = this.nextElementSibling;
                resultDiv.textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                console.error('Error: ахахахах, ничего не вышло, нужно писать внутрянку для сервера', error);
            });
        });
    });
});
