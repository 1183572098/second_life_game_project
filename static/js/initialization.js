healthValue = byId("healthValue"),
sportValue = byId("sportValue"),
artValue = byId("artValue"),
intelligenceValue = byId("intelligenceValue"),
luckValue = byId("luckValue"),
initial = byId("initial");
var available = document.getElementById("available");
var attributeMap = new Map();
var parameterMap = new Map();



function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

$(document).ready(function(){
	$.ajax({
		url: "../../static/config/attribute.csv",
		dataType: "text",
	}).done(readAttributeSuccess);

	$.ajax({
		url: "../../static/config/parameter.csv",
		dataType: "text",
	}).done(readParaSuccess);
});

function readAttributeSuccess(data){
	let newData = data.split(/\r?\n|\r/)
	for(let i=1;i<newData.length;i++){
		let dataCell = newData[i].split(",");
		if(dataCell[0]!==""){
			attributeMap.set(dataCell[0], dataCell[1]);
		}
	}

	createTable();
}

function readParaSuccess(data){
	let newData = data.split(/\r?\n|\r/)
	for(let i=1;i<newData.length;i++){
		let dataCell = newData[i].split(",");
		if(dataCell[0]!==""){
			parameterMap.set(parseInt(dataCell[0]), dataCell[1]);

		}
	}

	window.initalImg = Math.ceil(Math.random()*parseInt(parameterMap.get(2008)));
	if(window.initalImg === 0 || isNaN(window.initalImg)){
		window.initalImg = 1;
	}
	setImg(window.initalImg);
}

function setImg(img){
	document.getElementById("head").src = "../../static/image/head/" + String(img) + ".png";
}


function minus(val){
	let id = $(val).parent().parent().find('td').eq(0).attr("id");
	let value = parseInt($(val).parent().parent().find('td').eq(1).text());
	if(value > 0){
		document.getElementById(id).parentNode.children[1].innerHTML = setValue(value-1);
		available.innerHTML = String(parseInt(available.innerHTML) + 1);
	}
}

function plus(val){
	let id = $(val).parent().parent().find('td').eq(0).attr("id");
	let value = parseInt($(val).parent().parent().find('td').eq(1).text());
	if(parseInt(available.innerHTML)>0){
		document.getElementById(id).parentNode.children[1].innerHTML = setValue(value+1);
		available.innerHTML = String(parseInt(available.innerHTML) - 1);
	}
}

function createTable(){
	let tbody = document.querySelector('tbody');
	for(let [key, value] of attributeMap){
		let tr = document.createElement('tr');
		tbody.appendChild(tr);
		let td = document.createElement('td');
		td.innerHTML = value;
		td.id = key;
		tr.appendChild(td);

		let td2 = document.createElement('td');
		td2.id = "value";
		td2.innerHTML = setValue(attribute[key]);
		tr.appendChild(td2);
	}
}

function setValue(val){
	let innerHtml = "<a href='javascript:void(0)' onclick='minus(this)' class='glyphicon glyphicon-chevron-left'></a>";
	innerHtml += val;
	innerHtml += "<a href='javascript:void(0)' onclick='plus(this)' class='glyphicon glyphicon-chevron-right'></a>";
	return innerHtml;
}

$('#random').click(function(){
	$.post('../initial/random/',
		{},
		function (data) {
			let map = new Map(Object.entries(data.attribute));
			for( [key, value] of map){
				document.getElementById(key).parentNode.children[1].innerHTML = setValue(value);
			}

			available.innerHTML = String(0);
		})
});

$('#confirm').click(function(){
	let first_name = $("#first_name").val();
	let last_name = $("#last_name").val();
	if(first_name === "" || last_name === ""){
		alert("Please choose a nice name");
		return;
	}
	for(let [key, value] of attributeMap){
		let attributeValue = parseInt(document.getElementById(key).parentNode.children[1].innerText);
		if(attributeValue < parseInt(parameterMap.get(2002)) || attributeValue > parseInt(parameterMap.get(2003))){
			alert("Attribute value must be between 10 and 50");
			return;
		}
		attributeMap.set(key, attributeValue);
	}

	$.post('../initial/confirm/',
		{'attribute': JSON.stringify(Object.fromEntries(attributeMap.entries())),
		'first_name': first_name,
		'last_name': last_name,
		'head_portrait': window.initalImg},
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
});

$('#pre').click(function(){
	window.initalImg -= 1;
	if(window.initalImg <= 0){
		window.initalImg = parameterMap.get(2008);
	}
	setImg(window.initalImg);
});

$('#next').click(function(){
	window.initalImg += 1;
	if(window.initalImg > parameterMap.get(2008)){
		window.initalImg = 1;
	}
	setImg(window.initalImg);
});
