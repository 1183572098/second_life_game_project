var attributeMap = new Map();
var eventMap = new Map();

$(document).ready(function(){
    $.ajax({
        url: "../../static/config/attribute.csv",
        dataType: "text",
    }).done(readSuccess);

    $.ajax({
        url: "../../static/config/event.csv",
        dataType: "text",
    }).done(readEventSuccess);

});

function readSuccess(data){
    let newData = data.split(/\r?\n|\r/)
    for(let i=1;i<newData.length;i++){
        let dataCell = newData[i].split(",");
        if(dataCell[0]!==""){
            attributeMap.set(dataCell[0], dataCell[1]);
        }
    }
    createTop();
}

function readEventSuccess(data){
    let newData = data.split(/\r?\n|\r/);
    for(let i=1;i<newData.length;i++){
        let dataCell = csvToArray(newData[i]);
        if(dataCell[0]!==""){
            eventMap.set(dataCell[0], dataCell[2]);
        }
    }
    createEventTable();
}

function csvToArray(text) {
    let p = '', row = [''], ret = [row], i = 0, r = 0, s = !0, l;
    for (l of text) {
        if ('"' === l) {
            if (s && l === p) row[i] += l;
            s = !s;
        } else if (',' === l && s) l = row[++i] = '';
        else if ('\n' === l && s) {
            if ('\r' === p) row[i] = row[i].slice(0, -1);
            row = ret[++r] = [l = '']; i = 0;
        } else row[i] += l;
        p = l;
    }
    return row;
}

function createTop(){
    let topHead = document.querySelectorAll("thead")[0];
    let topBody = document.querySelectorAll("tbody")[0];
    let map = new Map(Object.entries(attribute));
    for(let [key, value] of attributeMap){
        let td = document.createElement('td');
        td.innerHTML = value;
        td.id = key;
        topHead.appendChild(td);

        let td2 = document.createElement('td');
        td2.innerHTML = map.get(String(key));
        topBody.appendChild(td2);
    }
}

function createEventTable(){
    let eventBody = document.querySelectorAll("tbody")[3];

    let td = document.createElement('td');
    td.id = "value" + eventId;
    td.innerHTML = "The " + age + " year";
    eventBody.appendChild(td);
    let td2 = document.createElement('td');
    td2.id = "event" + eventId;
    td2.innerHTML = eventMap.get(String(eventId));
    eventBody.appendChild(td2);
}

$('#confirm').click(function(){

});