var attributeMap = new Map();
var eventMap = new Map();
var attributeValueMap = new Map(Object.entries(attribute));
var option1Map = new Map();
var option2Map = new Map();
var option3Map = new Map();

$(document).ready(function(){
    $.ajax({
        url: "../../static/config/attribute.csv",
        dataType: "text",
    }).done(readSuccess);

    $.ajax({
        url: "../../static/config/event.csv",
        dataType: "text",
    }).done(readEventSuccess);

    $.ajax({
        url: "../../static/config/OptionTable.csv",
        dataType: "text",
    }).done(readOptionSuccess);
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

function readOptionSuccess(data){
    let newData = data.split(/\r?\n|\r/)
    for(let i=1;i<newData.length;i++){
        let dataCell = csvToArray(newData[i]);
        if(dataCell[0]!==""){
            option1Map.set(dataCell[0], dataCell[1]);
            option2Map.set(dataCell[0], dataCell[3]);
            option3Map.set(dataCell[0], dataCell[5]);
        }
    }
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

    for(let [key, value] of attributeMap){
        let td = document.createElement('td');
        td.innerHTML = value;
        td.id = key;
        topHead.appendChild(td);

        let td2 = document.createElement('td');
        td2.id = "value" + key;
        td2.innerHTML = attributeValueMap.get(String(key));
        topBody.appendChild(td2);
    }
}

function createEventTable(){
    let eventBody = document.querySelectorAll("tbody")[3];

    let tr = document.createElement('tr');
    eventBody.appendChild(tr);
    let td = document.createElement('td');
    td.id = "value" + eventId;
    td.innerHTML = "The " + age + " year";
    tr.appendChild(td);
    let td2 = document.createElement('td');
    td2.id = "event" + eventId;
    td2.innerHTML = eventMap.get(String(eventId));
    tr.appendChild(td2);
}

$('#next').click(function(){
    $.post('../next/',
        {'user_id': userId},
        function (data) {
            if(Boolean(data.is_end) === true){
                alert("game over.")
            }
            else{
                age = data.age;
                if(parseInt((data.event_id%10000) / 1000) === 3){
                    eventId = data.event_id;
                    attribute = data.attribute;
                    attributeValueMap = new Map(Object.entries(attribute));
                    setAttribute();
                    createEventTable();
                }
                else{
                    document.getElementById("option1").innerHTML = option1Map.get(String(data.event_id));
                    document.getElementById("option2").innerHTML = option2Map.get(String(data.event_id));
                    document.getElementById("option3").innerHTML = option3Map.get(String(data.event_id));
                    document.getElementById("select").className = "select";
                    document.getElementById("downRight").className = "downRight hide";
                }
            }
        })
});

function setAttribute(){
    for(let [key, value] of attributeValueMap){
        document.getElementById("value"+key).innerHTML = value;
    }
}

function choose(val){
    $.post('../option/',
        {'user_id': userId,
        'option': $(val).attr("id")},
        function (data) {
            eventId = data.event_id;
            attribute = data.attribute;
            attributeValueMap = new Map(Object.entries(attribute));
            setAttribute();
            createEventTable();
            document.getElementById("select").className = "select hide";
            document.getElementById("downRight").className = "downRight";
        })
}

document.onkeydown = function ()
{
    if (event.keyCode === 116) {
        event.keyCode = 0;
        event.cancelBubble = true;
        return false;
    }
}

document.oncontextmenu = function () {
    return false;
}