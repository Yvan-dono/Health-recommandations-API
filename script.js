
        // URL de l'API
        const API_BASE = 'https://health-recommandations-api.onrender.com';

        // Charger toutes les recommandations/avec filtres
        async function loadRecommandations() {
            const categorie = document.getElementById('categorie').value;
            const sousCategorie = document.getElementById('sousCategorie').value;
            const publicCible = document.getElementById('public').value;

            // Construire l'URL avec paramètres (URLSearchParams) 
            const url = new URL(`${API_BASE}/api/recommandations`);
            if (categorie) url.searchParams.append('categorie', categorie);
            if (sousCategorie) url.searchParams.append('sousCategorie', sousCategorie);
            if (publicCible) url.searchParams.append('public', publicCible);

            try {
                document.getElementById('results').innerHTML = '<div class="loading">Chargement...</div>';
                
                const response = await fetch(url);  // Appel fetch() 
                if (!response.ok) throw new Error('Erreur API');
                
                const recommandations = await response.json();  
              
                displayResults(recommandations);
            } catch (error) {
                document.getElementById('results').innerHTML = 
                    `<div class="error">Erreur : ${error.message}</div>`;
            }
        }

        // Afficher toutes les recommandations
        async function loadAll() {
            document.getElementById('categorie').value = '';
            document.getElementById('sousCategorie').value = '';
            document.getElementById('public').value = '';
            loadRecommandations();
        }

        // Afficher les résultats dans la page
        function displayResults(recommandations) {
            const resultsDiv = document.getElementById('results');
            
            if (recommandations.length === 0) {
                resultsDiv.innerHTML = '<p>Aucune recommandation trouvée.</p>';
                return;
            }
            
            resultsDiv.innerHTML = recommandations.map(r => `
                <div class="recommendation">
                    <div class="categorie">${r.categorie} > ${r.sousCategorie}</div>
                    <h3>${r.titre}</h3>
                    <p><strong>Public :</strong> ${r.public}</p>
                    <p>${r.recommandation}</p>
                    <small>Source : ${r.source}</small>
                </div>
            `).join('');
        }

        // Charger au démarrage
        loadAll();
    