var myMainChart;
var datasets = [];
function clean_graph(){
    if (typeof myMainChart !== 'undefined'){
        myMainChart.destroy();
        datasets = [];
    }
}

function random_list(total){
    return Array.from({length: total}, () => Math.floor(Math.random() * 20));
}

function random_color(){
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    var gamma = Math.random() * 0.4 + 0.8;
    return "rgb(" + r + "," + g + "," + b + ","+ gamma+ ")";
}

function create_dataset(idArticulo, n=0){
    const newDataset = {
        label: idArticulo + ' ' + (n + 1) ,
        backgroundColor: random_color(),
        borderColor: random_color(),
        borderWidth: 2,
        data: random_list(5), //[23,45,5,5,],
    };
    return newDataset
}

function add_data_to_graph(idArticulo="idArticulo"){
    if (typeof myMainChart !== 'undefined'){
        var n = myMainChart.data.datasets.length;
    }
    else{
        var n = 0;
    }
    const newDataset = create_dataset(idArticulo, n);
    try{
        datasets.push(newDataset);
        myMainChart.data.datasets.push(newDataset);
        myMainChart.update();
    }catch(err){
        console.log(err);
        Drawgraphonfront();
        datasets.push(newDataset);
        myMainChart.data.datasets.push(newDataset);
        myMainChart.update();
    }
}

function Drawgraphonfront(){

    var canvas = document.getElementById('myChart')
    var ctx = canvas.getContext('2d');
    if (typeof myMainChart !== 'undefined'){
        myMainChart.destroy();
    }
    // var dataset0 = create_dataset("Base")

    myMainChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Magenta'],
            datasets: []
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                  display: true,
                  text: "Sales Forecast - Empesa X SAC",
                }
              }
        }
    });


}

document.addEventListener('readystatechange', event => { 

    // When HTML/DOM elements are ready:
    // if (event.target.readyState === "interactive") {   //does same as:  ..addEventListener("DOMContentLoaded"..
    //     alert("hi 1");
    //     Drawgraphonfront();
    // }

    // When window loaded ( external resources are loaded too- `css`,`src`, etc...) 
    if (event.target.readyState === "complete") {
        Drawgraphonfront();
    }
});

function play_checkbox(checkbox){
    if (checkbox.checked){
        console.log(checkbox.id);
        add_data_to_graph(checkbox.name);
    }else{

    }
    
}