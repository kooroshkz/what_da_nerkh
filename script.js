let exchangeRate = 87120; // Default value

async function fetchExchangeRate() {
    try {
        const response = await fetch('exchange_rate.json');
        const data = await response.json();

        if (Array.isArray(data) && data.length > 0) {
            let latestEntry = data[data.length - 1]; // Get the latest rate
            exchangeRate = latestEntry.rate;
            document.getElementById('lastUpdated').innerText = `Last Updated: ${latestEntry.timestamp}`;

            // Set default values
            document.getElementById('euroInput').value = 1;
            document.getElementById('tomanInput').value = formatNumber(exchangeRate);
        } else {
            document.getElementById('lastUpdated').innerText = "Last Updated: No Data";
        }
    } catch (error) {
        console.error("Error fetching exchange rate:", error);
        document.getElementById('lastUpdated').innerText = "Last Updated: Error";
    }
}

// Prevents recursion when updating inputs
let isUpdating = false;

function convertCurrency(source) {
    if (isUpdating) return;
    isUpdating = true;

    let euroInput = document.getElementById('euroInput');
    let tomanInput = document.getElementById('tomanInput');

    if (source === 'euro') {
        let euroValue = parseFloat(euroInput.value) || 0;
        tomanInput.value = formatNumber(euroValue * exchangeRate);
    } else if (source === 'toman') {
        let tomanValue = removeCommas(tomanInput.value);
        euroInput.value = (tomanValue / exchangeRate).toFixed(2);
    }

    isUpdating = false;
}

// Helper function to format numbers with commas
function formatNumber(num) {
    return num.toLocaleString('en-US');
}

// Helper function to remove commas for calculations
function removeCommas(str) {
    return parseFloat(str.replace(/,/g, '')) || 0;
}

// Event listeners for live updating
document.getElementById('euroInput').addEventListener('input', () => convertCurrency('euro'));
document.getElementById('tomanInput').addEventListener('input', () => convertCurrency('toman'));

// Fetch latest rate on page load and set default values
fetchExchangeRate();
