healthValue = byId("healthValue"),
sportValue = byId("sportValue"),
artValue = byId("artValue"),
intelligenceValue = byId("intelligenceValue"),
luckValue = byId("luckValue"),
initial = byId("initial");
var available = document.getElementById("available");
var attributeMap = new Map();
var random = Math.ceil(Math.random()*4);


function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

$(document).ready(function(){
	$.ajax({
		url: "../../static/config/attribute.csv",
		dataType: "text",
	}).done(readSuccess);

	function readSuccess(data){
		let newData = data.split(/\r?\n|\r/)
		for(let i=1;i<newData.length;i++){
			let dataCell = newData[i].split(",");
			if(dataCell[0]!==""){
				attributeMap.set(dataCell[0], dataCell[1]);
			}
		}

		createTable();
	}

	if(random === 0){
		random = 1;
	}
	document.getElementById("head").src = "../../static/image/head/" + String(random) + ".png";
});


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
	let user_id = $(this).attr('data-userid');
	$.post('/game/initial/random/',
		{'user_id': user_id},
		function (data) {
			let map = new Map(Object.entries(data.attribute));
			for( [key, value] of map){
				document.getElementById(key).parentNode.children[1].innerHTML = setValue(value);
			}

			available.innerHTML = String(0);
			// $('#healthValue').html(data.attribute['1']);
			// $('#sportValue').html(data.attribute['2']);
			// $('#artValue').html(data.attribute['3']);
			// $('#intelligenceValue').html(data.attribute['4']);
			// $('#luckValue').html(data.attribute['5']);
		})
});

$('#confirm').click(function(){
	let user_id = $(this).attr('data-userid');
	let first_name = $("#first_name").val();
	let last_name = $("#last_name").val();
	if(first_name === "" || last_name === ""){
		alert("Please choose a nice name");
	}
	for(let [key, value] of attributeMap){
		attributeMap.set(key, document.getElementById(key).parentNode.children[1].innerText);
	}
	alert(attributeMap);
});

