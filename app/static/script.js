const tg = window.Telegram.WebApp;
    tg.ready(); // Сообщаем Telegram, что приложение готово

    const determineButton = document.getElementById('determine_button');
    const resultsDiv = document.getElementById('results');
    const winnersListUl = document.getElementById('winners_list');
    const errorMessageDiv = document.getElementById('error_message');
    const loadingDiv = document.getElementById('loading');
    const totalParticipantsP = document.getElementById('total_participants');

    const postUrlInput = document.getElementById('post_url');
    const contestNameInput = document.getElementById('contest_name');
    const criteriaLikesCheckbox = document.getElementById('criteria_likes');
    const criteriaRepostsCheckbox = document.getElementById('criteria_reposts');
    const criteriaCommentsCheckbox = document.getElementById('criteria_comments');
    const requiredGroupsTextarea = document.getElementById('required_groups');
    const checkOwnGroupCheckbox = document.getElementById('check_own_group');
    const ownGroupIdInput = document.getElementById('own_group_id');
    const numWinnersInput = document.getElementById('num_winners');

    // Показываем/скрываем поле ID своей группы
    checkOwnGroupCheckbox.addEventListener('change', () => {
        ownGroupIdInput.style.display = checkOwnGroupCheckbox.checked ? 'block' : 'none';
        if(checkOwnGroupCheckbox.checked) {
            ownGroupIdInput.required = true; // Делаем обязательным, если выбрано
        } else {
             ownGroupIdInput.required = false;
        }
    });

    // --- Глобальная переменная для хранения данных последнего запроса ---
    let lastContestRequestData = null;
    let currentWinnersData = []; // Для хранения данных текущих победителей

    determineButton.addEventListener('click', handleDetermineWinners);

    async function handleDetermineWinners() {
        clearResults();
        showLoading(true);

        // --- Сбор данных из формы ---
        const postUrl = postUrlInput.value;
        const contestName = contestNameInput.value || null; // optional
        const criteria = {
            likes: criteriaLikesCheckbox.checked,
            reposts: criteriaRepostsCheckbox.checked,
            comments: criteriaCommentsCheckbox.checked,
        };
        const requiredGroupsRaw = requiredGroupsTextarea.value.trim();
        const requiredGroups = requiredGroupsRaw ? requiredGroupsRaw.split(',').map(url => url.trim()).filter(url => url) : [];
        const checkOwnGroup = checkOwnGroupCheckbox.checked;
        const ownGroupId = checkOwnGroup ? ownGroupIdInput.value : null;
        const numWinners = parseInt(numWinnersInput.value, 10);

        // --- Валидация базовых данных ---
        if (!postUrl || !isValidHttpUrl(postUrl)) {
            showError("Пожалуйста, введите корректную ссылку на пост.");
            showLoading(false);
            return;
        }
        if (!criteria.likes && !criteria.reposts && !criteria.comments) {
             showError("Пожалуйста, выберите хотя бы один критерий (лайки, репосты или комментарии).");
             showLoading(false);
             return;
        }
         if (checkOwnGroup && !ownGroupId) {
             showError("Пожалуйста, укажите ID или короткое имя вашей группы для проверки подписки.");
             showLoading(false);
             return;
         }
        if (isNaN(numWinners) || numWinners < 1) {
            showError("Пожалуйста, введите корректное количество победителей (минимум 1).");
            showLoading(false);
            return;
        }

        // --- Сохраняем данные запроса ---
         lastContestRequestData = {
            post_url: postUrl,
            contest_name: contestName,
            criteria: criteria,
            required_groups: requiredGroups,
            check_own_group: checkOwnGroup,
            own_group_id: ownGroupId,
            num_winners: numWinners
        };


        try {
             // !!! Укажи URL твоего РАЗВЕРНУТОГО FastAPI бэкенда !!!
            const backendUrl = 'http://localhost:8000'; // ЗАМЕНИТЬ НА РЕАЛЬНЫЙ URL ПОСЛЕ ДЕПЛОЯ!
            const response = await fetch(`${backendUrl}/get_winners`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(lastContestRequestData), // Используем сохраненные данные
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Ошибка сервера: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data.winners, data.total_participants);

        } catch (error) {
            console.error("Ошибка при определении победителей:", error);
            showError(`Ошибка: ${error.message}`);
        } finally {
            showLoading(false);
        }
    }

    async function handleRerollWinner(winnerToRerollId) {
         if (!lastContestRequestData || !currentWinnersData.length) {
             showError("Нет данных предыдущего розыгрыша для перевыбора.");
             return;
         }
         showLoading(true);
         clearResults(false); // Не очищаем полностью, только список

         const rerollRequestData = {
            contest_data: lastContestRequestData,
            current_winners: currentWinnersData, // Передаем текущих победителей
            winner_to_reroll_id: winnerToRerollId
         }

          try {
             // !!! Укажи URL твоего РАЗВЕРНУТОГО FastAPI бэкенда !!!
             const backendUrl = 'http://localhost:8000'; // ЗАМЕНИТЬ!
             const response = await fetch(`${backendUrl}/reroll_winner`, {
                 method: 'POST',
                 headers: {
                     'Content-Type': 'application/json',
                 },
                 body: JSON.stringify(rerollRequestData),
             });

             if (!response.ok) {
                 const errorData = await response.json();
                 throw new Error(errorData.detail || `Ошибка сервера: ${response.status}`);
             }

             const data = await response.json();
             // Отображаем обновленный список
             displayResults(data.winners, data.total_participants);

         } catch (error) {
             console.error("Ошибка при перевыборе победителя:", error);
             showError(`Ошибка перевыбора: ${error.message}`);
             // Можно вернуть старый список или оставить сообщение об ошибке
             // displayResults(currentWinnersData, lastContestRequestData.num_winners); // Показать старый список
         } finally {
             showLoading(false);
         }
    }

    function displayResults(winners, totalParticipants) {
        currentWinnersData = winners; // Обновляем глобальные данные
        winnersListUl.innerHTML = ''; // Очищаем предыдущий список

         if (winners && winners.length > 0) {
             totalParticipantsP.textContent = `Всего участников, выполнивших условия: ${totalParticipants}`;
             winners.forEach(winner => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <a href="<span class="math-inline">\{winner\.profile\_url\}" target\="\_blank"\></span>{winner.first_name} ${winner.last_name}</a> (ID: <span class="math-inline">\{winner\.user\_id\}\)