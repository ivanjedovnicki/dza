const earthquake_data = JSON.parse(document.getElementById('earthquake-data').textContent);

var data = [{
    type: 'scattergeo',
    mode: 'markers',
    lon: earthquake_data.longitude,
    lat: earthquake_data.latitude,
    marker: {
        size: 7,
        color: earthquake_data.color,
        line: {
            width: 1
        }
    },
    name: 'Earthquakes',
}];

var layout = {
    width: 900,
    height: 900,
    title: 'Canadian cities',
    font: {
        family: 'Droid Serif, serif',
        size: 15
    },
    titlefont: {
        size: 16
    },
    geo: {
        scope: 'europe',
        resolution: 50,
        lonaxis: {
            'range': [0, 55]
        },
        lataxis: {
            'range': [20, 50]
        },
        showrivers: true,
        rivercolor: '#fff',
        showlakes: true,
        lakecolor: '#fff',
        showland: true,
        landcolor: '#EAEAAE',
        countrycolor: '#d3d3d3',
        countrywidth: 1.5,
        subunitcolor: '#d3d3d3'
    }
};

Plotly.newPlot('myDiv', data, layout);
