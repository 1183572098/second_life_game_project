var archiveMap = new Map();
var eventMap = new Map();
var currentSelect = 0,
    one = byId("oneBorder"),
    two = byId("twoBorder"),
    three = byId("threeBorder");


function byId(id){
    return typeof(id)==="string"?document.getElementById(id):id;
}


$(document).ready(function(){
    $.ajax({
        url: "../../static/config/event.csv",
        dataType: "text",
    }).done(readEventSuccess);

});

function readEventSuccess(data){
    let newData = data.split(/\r?\n|\r/);
    for(let i=1;i<newData.length;i++){
        let dataCell = csvToArray(newData[i]);
        if(dataCell[0]!==""){
            eventMap.set(dataCell[0], dataCell[2]);
        }
    }
    showArchive();
}


function showArchive(){
    if(state === 1){
        document.getElementById("saveBtn").disabled = false;
        document.getElementById("saveBtn").hidden = false;
        document.getElementById("gamePage").style.display = "block";
    }
    for(let i=0;i<archive.length;i++){
        if(archive[i] !== null && archive[i] !== "null"){
            archiveMap = new Map(Object.entries(archive[i]));
            document.getElementById("name" + String(i+1)).innerHTML = archiveMap.get("nickname");
            document.getElementById("portrait" + String(i+1)).innerHTML = getPortrait(archiveMap.get("portrait"));
            document.getElementById("detail" + String(i+1)).innerHTML = archiveMap.get("age") + ": " + eventMap.get(String(archiveMap.get("event")));
            document.getElementById("time" + String(i+1)).innerHTML = archiveMap.get("time");
        }
    }
}

function getPortrait(val){
    let innerHtml = "<img src='../../static/image/head/";
    innerHtml += String(val);
    innerHtml += ".png' alt='portrait' >";
    return innerHtml;
}

function save(){
    if(currentSelect === 0){
        alert("Please select a archive.");
        return;
    }

    $.post('../archive/save/',
        {'location': currentSelect},
        function (data) {
            if(Boolean(data.success) === true){
               alert("save archive success");
               archive[0] = data.archive1;
               archive[1] = data.archive2;
               archive[2] = data.archive3;
               showArchive();
            }
            else{
                if(data.reason === undefined){
                    alert("Please refresh the page and try again.");
                }
                else{
                    alert(data.reason);
                }
            }
        })
}

function read(){
    if(currentSelect === 0){
        alert("Please select a archive.");
        return;
    }

    $.post('../archive/read/',
        {'location': currentSelect},
        function (data) {
            if(Boolean(data.success) === true){
                window.location.href ="../game/";
            }
            else{
                if(data.reason === undefined){
                    alert("Please refresh the page and try again.");
                }
                else{
                    alert(data.reason);
                }
            }
        })
}

function select1(){
    currentSelect = 1;
}

function select2(){
    currentSelect = 2;
}

function select3(){
    currentSelect = 3;
}

one.onclick=function(){
    one.className = "oneBorder highlight";
    two.className = "twoBorder noLight";
    three.className = "threeBorder noLight";
} 

two.onclick=function(){
    one.className = "oneBorder noLight";
    two.className = "twoBorder highlight";
    three.className = "threeBorder noLight";
} 

three.onclick=function(){
    one.className = "oneBorder noLight";
    two.className = "twoBorder noLight";
    three.className = "threeBorder highlight";
} 

