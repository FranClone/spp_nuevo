Chart.defaults.color = '#fff'
Chart.defaults.borderColor = '#444'

const printCharts = () => {

    renderModelsChart(),
    renderFeaturesChart(),
    renderYearsChart()
    
}

const renderModelsChart = () => {
    const data = {
        labels: ['uno','dos','tres','cuatro'],
        datasets: [{
            data: [60,20,30,40],
            borderColor: getDataColors(),
            backgroundColor: getDataColors(70)
        }]
    }
    const options = {
        plugins: {
            legend: { position : 'bottom'}
        }
    }

    new Chart('modelsChart', { type: 'doughnut', data, options})
}

const renderFeaturesChart = () => {
    const data = {
        labels: ['uno','dos','tres','cuatro','cinco','seis','siete'],
        datasets: [{
            label: 'Altura',
            data: [74,50,68,50,70,68,56],
            borderColor: getDataColors(),
            backgroundColor: getDataColors(70)
        }]
    }
    const options = {
        plugins: {
            legend: {display : false }
        },
        scales : {
            r:{
                ticks: { display : false }
            }
        }
    }

    new Chart('featuresChart', { type: 'radar', data, options})
}

const renderYearsChart = () => {

    const years = ['2015','2016','2017','2018','2019','2020','2021','2022','2023']
    const ventas = ['5','3','57','60','43','55','49','80','169']

    const data = {
        labels: years,
        datasets: [{
            data: (years,ventas),
            tension: 1,
            borderColor: getDataColors()[1],
            backgroundColor: getDataColors(70)[1],
            fill: true,
            pointBorderWidth: 5
        }]
    }

    const options = {
        plugins: {
            legend: { display: false }
        }
    }

    new Chart('yearsChart', { type: 'bar', data, options })
}


printCharts()