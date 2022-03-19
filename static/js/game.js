var attributeMap = new Map();
var eventMap = new Map();
var attributeValueMap = new Map(Object.entries(attribute));
var option1Map = new Map();
var option2Map = new Map();
var option3Map = new Map();
var questionMap = new Map();
var isEnd = false;

$(document).ready(function(){
    $.ajax({
        url: "../../static/config/attribute.csv",
        dataType: "text",
    }).done(readAttributeSuccess);

    $.ajax({
        url: "../../static/config/event.csv",
        dataType: "text",
    }).done(readEventSuccess);

    $.ajax({
        url: "../../static/config/OptionTable.csv",
        dataType: "text",
    }).done(readOptionSuccess);

});


function readAttributeSuccess(data){
    let newData = data.split(/\r?\n|\r/)
    for(let i=1;i<newData.length;i++){
        let dataCell = newData[i].split(",");
        if(dataCell[0]!==""){
            if(parseInt(dataCell[2]) !== 1) {
                attributeMap.set(dataCell[0], dataCell[1]);
            }
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
            questionMap.set(dataCell[0], dataCell[7]);
        }
    }
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
    if(typeof eventId == "number"){
        createEvent(age, eventId);
    }
    else{
        let eventArray = Array.from(eventId);
        let year = 0;
        for(let event of eventArray){
            if(parseInt((parseInt(event)%10000) / 1000) <= 3){
                createEvent(year, event);
                year ++;
            }
        }
    }
}

function createEvent(age, eventId){
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
    document.getElementById("subMiddleBody").scrollTop = document.getElementById("subMiddleBody").scrollHeight;
}

$('#next').click(function(){
    $.post('../next/',
        {},
        function (data) {
            eventId = data.event_id;
            if(Boolean(data.is_end) === true){
                isEnd = true;
                attribute = data.attribute;
                attributeValueMap = new Map(Object.entries(attribute));
                setAttribute();
                endPage(eventMap.get(String(eventId)));
            }
            else{
                age = data.age;
                if(parseInt((data.event_id%10000) / 1000) === 3){
                    attribute = data.attribute;
                    attributeValueMap = new Map(Object.entries(attribute));
                    setAttribute();
                    createEventTable();
                }
                else{
                    document.getElementById("question").innerHTML = questionMap.get(String(data.event_id));
                    document.getElementById("option1").innerHTML = option1Map.get(String(data.event_id));
                    document.getElementById("option2").innerHTML = option2Map.get(String(data.event_id));
                    document.getElementById("option3").innerHTML = option3Map.get(String(data.event_id));
                    document.getElementById("select").className = "select";
                    document.getElementById("downRight").className = "downRight hide";
                    showShadow();
                }
            }
        })
});

function showShadow(){
    document.getElementById("shadow").className = "shadow block";
}

function setAttribute(){
    for(let [key, value] of attributeValueMap){
        document.getElementById("value"+key).innerHTML = value;
    }
}

function choose(val){
    $.post('../option/',
        {'option': $(val).attr("id")},
        function (data) {
            eventId = data.event_id;
            attribute = data.attribute;
            attributeValueMap = new Map(Object.entries(attribute));
            setAttribute();
            createEventTable();
            document.getElementById("select").className = "select hide";
            document.getElementById("downRight").className = "downRight";
            document.getElementById("shadow").className = "shadow hide";

        })
}

function endPage(val){
    document.getElementById("content").innerHTML = val;
    document.getElementById("end").className="overshadow";
    if(isEnd){
        document.getElementById("next").hidden = true;
    }
}

function clickReturn(){
    document.getElementById("end").className="overshadow hide";
    if(isEnd){
        document.getElementById("restart").hidden = false;
    }
}

function tips(){
    let tips = "<br/>Please be careful not to let any of your attributes drop to 0. <br/> Do good things, maybe good things will happen.";
    endPage(tips);
}

function teamList(){
    let teamList = "<br/>Planner: Yandan Lai. Qixuan Yang. <br/> Developer: Jinyi Li. <br/> UI: Zhihao Xing. Bianca Jones.";
    endPage(teamList);
}
