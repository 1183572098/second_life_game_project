var store = byId("store"),
	subMiddle = byId("subMiddle"),
	subMiddle2 = byId('subMiddle2'),
	flag=false;


function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

function openBag(){
	if(flag){
		store.className="store hide";
		subMiddle.className="subMiddle active";
		subMiddle2.className="subMiddle2 active"
		flag=false;
	}else{
		store.className="store active";
		subMiddle.className="subMiddle hide";
		subMiddle2.className="subMiddle2 hide";
		flag=true;
	}
}

