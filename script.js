document.addEventListener("DOMContentLoaded", function () {
    let euroInput = document.getElementById("euro");
    let tomanInput = document.getElementById("toman");
    let priceDisplay = document.getElementById("price");

    function fetchPrice() {
        fetch("price.json") // Fetch from static JSON file
            .then(response => response.json())
            .then(data => {
                if (data.price) {
                    priceDisplay.textContent = data.price;
                    tomanInput.value = euroInput.value * data.price;
                }
            })
            .catch(() => {
                priceDisplay.textContent = "Error fetching price";
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
