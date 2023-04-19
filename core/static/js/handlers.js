const enableEventHandlers = characters => {

    document.querySelector('#featuresOptions').onchange = e => {

        const { value: property, text: label } = e.target.selectedOptions[0]

        const newData = characters.map(character => character[property])

        updateChartData('featuresChart', newData, label)
    }
}