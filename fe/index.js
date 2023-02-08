let currentTemperature = 20;
const temp = document.getElementById('Temperature');
temp.innerText = currentTemperature + "°C";

/**
 * @param {boolean} isIncrease
 * Increase or decrease current temperature
 */
const setTemperature = (isIncrease) => {
    isIncrease ? ++currentTemperature : --currentTemperature;
    const temp = document.getElementById('Temperature');
    temp.innerText = currentTemperature + "°C";
}

const upButton = document.getElementById('up');
upButton.addEventListener('click', function() {
    setTemperature(true);
})

const downButton = document.getElementById('down');
downButton.addEventListener('click', function() {
    setTemperature(false);
})