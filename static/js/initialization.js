var random = byId("random"),
healthValue = byId("healthValue"),
sportValue = byId("sportValue"),
artValue = byId("artValue"),
intelligenceValue = byId("intelligenceValue"),
luckValue = byId("luckValue"),
initial = byId("initial");


function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}




window.onload = function(){
	user_id = $('#initial').attr('data-userid');
	console.log("user_id:"+user_id);
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "/game/initial/", true);
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlHttp.send(user_id);
    xmlHttp.onreadystatechange = function () {
      if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
        console.log(xmlHttp.responseText);
      }
	}
}

// window.onload = function(){
// 	$.ajax({
// 		url: "/game/initial/",
// 		type: "post",
// 		data: "user_id",
// 		success:function(data) {
// 			$('#healthVlaue').html(data);
// 			    $('#sportValue').html(data[2]);
// 			    $('#artValue').html(data[2]);
// 			    $('#intelligenceValue').html(data[2]);
// 			    $('#luckValue').html(data[5]);
//                 console.log("L"+data+"RRRRRRRRRRRRRRRRRr");
// 		}
// 	})
// }

$(document).ready(function(){

	$('#random').click(function(){
		user_id = $(this).attr('data-userid');
        console.log("user_id: "+user_id);
		$.post('/game/initial/random/',
			{'user_id': user_id},
			function (data) {
                $('#healthValue').html(data.attribute['1']);
			    $('#sportValue').html(data.attribute['2']);
			    $('#artValue').html(data.attribute['3']);
			    $('#intelligenceValue').html(data.attribute['4']);
			    $('#luckValue').html(data.attribute['5']);
			})
	});

	document.getElementById("healthValue").innerHTML = attribute["1"];
	document.getElementById("sportValue").innerHTML = attribute["2"];
	document.getElementById("artValue").innerHTML = attribute["3"];
	document.getElementById("intelligenceValue").innerHTML = attribute["4"];
	document.getElementById("luckValue").innerHTML = attribute["5"];
});

function minus(){

}



