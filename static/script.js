function switchTab(tabId) {
    // Update tabs
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`button[onclick="switchTab('${tabId}')"]`).classList.add('active');
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    
    // Clear results
    document.getElementById('results-section').innerHTML = '';
    document.getElementById('results-section').classList.add('hidden');
    document.getElementById('error-message').classList.add('hidden');
}

async function getCollaborative() {
    const custId = document.getElementById('customer-id').value.trim();
    if (!custId) return showError('Please enter a Customer ID.');
    
    showLoader();
    try {
        const response = await fetch('/recommend/collaborative', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customer_id: custId, num_recommendations: 6 })
        });
        const data = await response.json();
        handleData(data, `Recommendations for Customer ${custId}`);
    } catch (err) {
        showError('Network error occurred.');
    }
}

async function getContent() {
    const query = document.getElementById('product-query').value.trim();
    if (!query) return showError('Please enter a Product ID or Name.');
    
    showLoader();
    try {
        const response = await fetch('/recommend/content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_query: query, num_recommendations: 6 })
        });
        const data = await response.json();
        handleData(data, `Products similar to "${query}"`);
    } catch (err) {
        showError('Network error occurred.');
    }
}

function handleData(data, titleContext) {
    hideLoader();
    
    if (data.error) {
        showError(data.error);
        return;
    }
    
    const resultsSec = document.getElementById('results-section');
    resultsSec.innerHTML = '';
    
    if (data.message && (!data.products || data.products.length === 0)) {
        showError(data.message);
        return;
    }
    
    if (data.products && data.products.length > 0) {
        data.products.forEach((prod, idx) => {
            const card = document.createElement('div');
            card.className = 'card';
            card.style.animationDelay = `${idx * 0.1}s`;
            
            card.innerHTML = `
                <div class="stock-code">${prod.id}</div>
                <h3>${prod.name}</h3>
            `;
            resultsSec.appendChild(card);
        });
        
        resultsSec.classList.remove('hidden');
    } else {
        showError('No recommendations found.');
    }
}

function showLoader() {
    document.getElementById('results-loader').classList.remove('hidden');
    document.getElementById('results-section').classList.add('hidden');
    document.getElementById('error-message').classList.add('hidden');
}

function hideLoader() {
    document.getElementById('results-loader').classList.add('hidden');
}

function showError(msg) {
    hideLoader();
    const errObj = document.getElementById('error-message');
    errObj.textContent = msg;
    errObj.classList.remove('hidden');
}
