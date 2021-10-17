const csrftoken = getCookie('csrftoken');
var myMainChart;
var articlesselected = [];
var pendingqueryes = 0;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function assert(condition, message) {
    if (!condition) throw new Error(message || "Array length of data and labels must be the same");
}

function get_n_ahead_option(){
    var n_ahead = document.getElementById("AheadFormControlSelect1").value ;
    return parseInt(n_ahead);
}

function clean_graph(){
    if (typeof myMainChart !== 'undefined'){
        articlesselected.forEach(idArticulo => {
            document.getElementById(idArticulo).checked = false;
         });
        articlesselected = [];
        myMainChart.destroy();
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


function create_graph_dataset(data, labels, forecastpoint, label_title,){

    assert(data.length === labels.length);
    
    const forecastline = (ctx, value) =>  ctx.p0.parsed.x >= forecastpoint  ? value : undefined;
    const newDataset = {
        label: label_title,
        backgroundColor: random_color(),
        borderColor: random_color(),
        borderWidth: 2,
        data: data, //[23,45,5,5,],
        segment: {
            borderDash: ctx => forecastline(ctx, [6, 6]),
        }
    };

    return {newDataset, labels}
}

function create_dataset(idArticulo, n=0){
    const n_ahead = get_n_ahead_option() + 1;
    const total_points = 5;
    const labels = ['2021-01', '2021-02', '2021-03', '2021-04' ,'2021-05'];
    const data = random_list(total_points);

    return create_graph_dataset(data, labels, total_points-n_ahead, idArticulo  )

}

function add_data_to_graph_mockup(idArticulo="idArticulo"){
    if (typeof myMainChart !== 'undefined'){
        var n = myMainChart.data.datasets.length;
    }
    else{
        var n = 0;
    }
    const data = create_dataset(idArticulo, n);
    try{
        myMainChart.data.datasets.push(data.newDataset);
        myMainChart.data.labels = data.labels
        myMainChart.update();
    }catch(err){
        console.log(err);
        Drawgraphonfront();
        myMainChart.data.datasets.push(data.newDataset);
        myMainChart.data.labels = data.labels
        myMainChart.update();
    }
}

function add_data_to_graph_production(payload){
    const n_ahead = payload.ahead;
    const total_points = payload.data.labels.length;
    const labels = payload.data.labels;
    const dataset = payload.data.values;
    const nameArticle = payload.name;

    const data = create_graph_dataset(dataset, labels, total_points-n_ahead-1, nameArticle)


    try{
        myMainChart.data.datasets.push(data.newDataset);
        myMainChart.data.labels = data.labels
        myMainChart.update();
    }catch(err){
        console.log(err);
        Drawgraphonfront();
        myMainChart.data.datasets.push(data.newDataset);
        myMainChart.data.labels = data.labels
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
            labels: [],
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
                  text: "Sales Forecast - Empresa X SAC",
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                    }
                }
            },
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
    var n = 0;
    if (checkbox.checked){
        // console.log(checkbox.id);
        
        get_forecastdata(checkbox.id)
        let spinner = document.getElementById("spinner-home");
        spinner.style.display = "block";
        // articlesselected.push(checkbox.id)
        
        //add_data_to_graph(checkbox.name);
    }else{
        myMainChart.data.datasets.forEach( item => {
            if (item.label === checkbox.name ){
                myMainChart.data.datasets.splice(n,1);
                myMainChart.update();
            }
            n = n +1;
        })
    }
}

async function get_forecast_from_server(payload) {
        let spinner = document.getElementById("spinner-home");
        pendingqueryes = pendingqueryes + 1
        $.ajax({
            type: "GET",
            url: "/api/model/forecast/",
            data: payload,
            headers: { 'X-CSRFToken': csrftoken },
            dataType: "json",
            encode: true,
            statusCode: {
                200: function () {
                    console.log("Success");
                    articlesselected.push(payload.id_articulo)
                    //location.reload();
                },
            },
        }).done(function (data) {
            console.log(data);
            add_data_to_graph_production(data)
            // addentries(data);
            pendingqueryes = pendingqueryes - 1
            if (pendingqueryes == 0){
                spinner.style.display = "none";
            }
        }).fail(function (data) {
            spinner.style.display = "none";
            console.log("FAIL...");
            console.log(data);
        });
}

async function get_forecastdata(idArticulo ) {

    var payload = {
        id_articulo: idArticulo,
        t_ahead: get_n_ahead_option(),
    }
    get_forecast_from_server(payload);

}