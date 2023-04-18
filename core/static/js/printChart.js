Chart.defaults.color = '#fff'
Chart.defaults.borderColor = '#444'

const printCharts = () => {

    renderModelsChart()
}

const renderModelsChart = () => {
    const data = {
        labels: ['uno','dos','tres','cuatro'],
        datasets: [{
            data: [10,20,30,40],
            borderColor: getDataColors(),
            backgroundColor: getDataColors(80)
        }]
    }
    const options = {
        plugins: {
            legend: { position : 'left' , color:'black'}
        }
    }

    new Chart('modelsChart', { type: 'doughnut', data, options})
}


printCharts()