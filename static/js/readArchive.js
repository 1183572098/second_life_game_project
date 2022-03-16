var archiveMap = new Map();
var eventMap = new Map();

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