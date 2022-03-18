var wholeStore = byId("wholeStore"),
	subMiddle = byId("subMiddle"),
	subMiddle2 = byId('subMiddle2'),
	flag=false;

var bagMap = new Map();
var ShopMap = new Map();
var goodsNameMap = new Map();
var goodsIconMap = new Map();


function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

$(document).ready(function(){
	$.ajax({
		url: "../../static/config/StoreTable.csv",
		dataType: "text",
	}).done(readTableSuccess);

});

function readTableSuccess(data){
	let newData = data.split(/\r?\n|\r/);
	for(let i=1;i<newData.length;i++){
		let dataCell = csvToArray(newData[i]);
		if(dataCell[0]!==""){
			goodsNameMap.set(dataCell[0], dataCell[1]);
			goodsIconMap.set(dataCell[0], dataCell[12]);
		}
	}
}


function openBag(){
	if(flag){
		wholeStore.className="store hide";
		subMiddle.className="subMiddle active";
		subMiddle2.className="subMiddle2 active"
		flag=false;
	}else{
		wholeStore.className="store active";
		subMiddle.className="subMiddle hide";
		subMiddle2.className="subMiddle2 hide";
		flag=true;
		openStore();
	}
}

function openStore(){
	$.post('../shop/',
		{},
		function (data) {
			if(data.bag !== ""){
				bagMap = new Map(Object.entries(data.bag));
			}
			ShopMap = new Map(Object.entries(data.shop));
			showStore();
		})
}

function showStore(){
	let bagBody = document.querySelectorAll("tbody")[1];
	let storeBody = document.querySelectorAll("tbody")[2];
	$("#bag tbody").html("");
	$("#store tbody").html("");
	for(let [key, value] of bagMap){
		bagBody.appendChild(createTr(key, value, 0));
	}

	for(let [key, value] of ShopMap){
		storeBody.appendChild(createTr(key, value, 1));
	}
}

function createTr(key, value, type){
	let tr = document.createElement('tr');
	let td1 = document.createElement('td');
	td1.id = key;
	td1.innerHTML = goodsNameMap.get(String(key));
	tr.appendChild(td1);

	let td2 = document.createElement('td');
	let img = document.createElement('img');
	img.src = goodsIconMap.get(String(key));
	img.alt = goodsNameMap.get(String(key));
	td2.innerHTML = setIcon(img, type);
	tr.appendChild(td2);

	let td3 = document.createElement('td');
	if(value === -1){
		td3.innerHTML = "∞";
	}
	else{
		td3.innerHTML = value;
	}
	tr.appendChild(td3);
	return tr;
}

function setIcon(val, type){
	let innerHtml;
	if(type === 0){
		innerHtml = "<a href='javascript:void(0)' ondblclick='use(this)'><img src=";
	}
	else{
		innerHtml = "<a href='javascript:void(0)' ondblclick='purchase(this)'><img src=";
	}

	innerHtml += val.src;
	innerHtml += " alt=";
	innerHtml += val.alt;
	innerHtml += "></a>"
	return innerHtml;
}

function purchase(val){
	let itemId = $(val).parent().parent().find('td').eq(0).attr("id");

	$.post('../purchase/',
		{'good_id': itemId},
		function (data) {
			if(Boolean(data.success) === true){
				if(data.bag !== ""){
					bagMap = new Map(Object.entries(data.bag));
				}
				ShopMap = new Map(Object.entries(data.shop));
				showStore();
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

function use(val){
	let itemId = $(val).parent().parent().find('td').eq(0).attr("id");

	$.post('../use/',
		{'good_id': itemId},
		function (data) {
			if(Boolean(data.success) === true){
				if(data.bag !== ""){
					bagMap = new Map(Object.entries(data.bag));
				}
				ShopMap = new Map(Object.entries(data.shop));
				showStore();
				attribute = data.attribute;
				attributeValueMap = new Map(Object.entries(attribute));
				setAttribute();
				// for rebirth especially
				if(data.event_id === 3001){
					$("#event tbody").html("");
					age = data.age;
					eventId = data.event_id;
					createEventTable();
				}
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