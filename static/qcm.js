        function logout() {
            // Supprimer les informations de session lors du logout
            localStorage.removeItem('username');
            localStorage.removeItem('userType');

            // Rediriger vers la page de login après le logout
            window.location.href = 'index.html';
        }

       function checkSession() {
            // Récupérer les informations de session depuis localStorage
            const username = localStorage.getItem('username');
            const userType = localStorage.getItem('userType');
            const menuContainer = document.getElementById('optionMenu');
            menuContainer.innerHTML = '';

                    if (userType === 'admin') {
                // Ajouter des éléments spécifiques au professeur
                const quizButton = document.createElement('a');
                quizButton.href = 'new_question.html';
                quizButton.innerHTML = '<button>Ajouter une question</button>';
                menuContainer.appendChild(quizButton);
            } else if (userType === 'joueur') {
                // Ajouter des éléments spécifiques à l'étudiant
                const quizButton = document.createElement('a');
                quizButton.href = 'quiz.html';
                quizButton.innerHTML = '<button>Jouer</button>';
                menuContainer.appendChild(quizButton);
            }

            // Vérifier si l'utilisateur est connecté
            if (username && userType) {
                // L'utilisateur est connecté, vous pouvez effectuer des actions ou afficher du contenu spécifique
                const message = `Utilisateur connecté: ${username}, Type: ${userType}`;
                console.log(message);

                // Créer un élément pour afficher le message
                const messageElement = document.createElement('div');
                messageElement.textContent = message;

                // Récupérer le conteneur où vous souhaitez ajouter le message
                const messageContainer = document.getElementById('messageContainer');

                // Ajouter l'élément dans le conteneur
                messageContainer.appendChild(messageElement);

                // Modifier le menu en fonction du type d'utilisateur
                updateMenu(userType);
            } else {
                // L'utilisateur n'est pas connecté, rediriger vers la page de login
                window.location.href = 'index.html';
            }
        }

        // Appeler la fonction de vérification lors du chargement de la page
        window.onload = checkSession;