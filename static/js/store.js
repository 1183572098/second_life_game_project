var store = byId("store"),
	process = document.getElementsByClassName("subMiddle"),
	flag;


function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

function openBag(){
	if(flag){
		store.className="store hide";
		process.className="subMiddle active";
		flag=false;
	}else{
		store.className="store active";
		process.className="subMiddle hide";
		flag=true;
	}
}

