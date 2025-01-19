document.addEventListener("DOMContentLoaded", function () {
    let euroInput = document.getElementById("euro");
    let tomanInput = document.getElementById("toman");
    let priceDisplay = document.getElementById("price");
    let refreshButton = document.createElement("button");

    refreshButton.textContent = "🔄 Update Live Price";
    refreshButton.style.marginTop = "10px";
    refreshButton.onclick = fetchLivePrice;
    document.body.appendChild(refreshButton);

    function fetchPrice() {
        fetch("price.json")
            .then(response => response.json())
            .then(data => {
                if (data.price) {
                    priceDisplay.textContent = data.price;
                    tomanInput.value = euroInput.value * data.price;
                }
            });
    }

    function fetchLivePrice() {
        fetch("https://your-api-host/trigger-update") // Replace with your deployed API URL
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert("Live price update triggered! Refresh in a few seconds.");
                }
            })
            .catch(() => {
                alert("Error triggering update. Try again later.");
            });
    }

    euroInput.addEventListener("input", () => {
        tomanInput.value = (euroInput.value * parseFloat(priceDisplay.textContent)).toFixed(2);
    });

    tomanInput.addEventListener("input", () => {
        euroInput.value = (tomanInput.value / parseFloat(priceDisplay.textContent)).toFixed(2);
    });

    fetchPrice();
});
