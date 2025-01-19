document.addEventListener("DOMContentLoaded", function () {
    let euroInput = document.getElementById("euro");
    let tomanInput = document.getElementById("toman");
    let priceDisplay = document.getElementById("price");

    function fetchPrice() {
        fetch("/get_price")
            .then(response => response.json())
            .then(data => {
                if (data.price) {
                    priceDisplay.textContent = data.price;
                    tomanInput.value = euroInput.value * data.price;
                }
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
