var archiveMap = new Map();
var eventMap = new Map();
var currentSelect = 0;

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
        if(archive[i] !== null){
            archiveMap = Object.entries(archive[i]);
            document.getElementById("name" + String(i+1)).innerHTML = archiveMap.get("nickname");
            document.getElementById("portrait" + String(i+1)).innerHTML = archiveMap.get("portrait");
            document.getElementById("detail" + String(i+1)).innerHTML = archiveMap.get("age") + ": " + eventMap.get(String(archiveMap.get("event")));
            document.getElementById("time" + String(i+1)).innerHTML = archiveMap.get("time");
        }
    }
}

function save(){
    if(currentSelect === 0){
        alert("Please select a archive.");
        return;
    }

    $.post('../archive/save/',
        {'location': currentSelect},
        function (data) {

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
                window.location.href ="../reload/";
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