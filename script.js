let exchangeRate = 87120; // Default value

async function fetchExchangeRate() {
    try {
        const response = await fetch('exchange_rate.json');
        const data = await response.json();
        exchangeRate = data.rate;
    } catch (error) {
        console.error("Error fetching exchange rate:", error);
    }
}

function convertToToman() {
    const euro = document.getElementById('euroInput').value;
    document.getElementById('tomanOutput').value = (euro * exchangeRate).toLocaleString();
}

function convertToEuro() {
    const toman = document.getElementById('tomanInput').value;
    document.getElementById('euroOutput').value = (toman / exchangeRate).toFixed(2);
}

// Fetch latest rate on page load
fetchExchangeRate();
