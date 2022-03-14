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
	$.post('/game/initial/',
			{'user_id': user_id},
			function (data) {
				//{1: 17, 2: 18, 3: 17, 4: 31, 5: 16}
               $('#healthVlaue').html(data[2]);
			    $('#sportValue').html(data[2]);
			    $('#artValue').html(data[3]);
			    $('#intelligenceValue').html(data[4]);
			    $('#luckValue').html(data[5]);
                console.log(data);
			})
}

$(document).ready(function(){

	$('#random').click(function(){
		user_id = $(this).attr('data-userid');
        console.log("user_id: "+user_id);
		$.post('/game/initial/random/',
			{'user_id': user_id},
			function (data) {
       //         $('#healthVlaue').html(data.get('healthValue'));
			    // $('#sportValue').html(data.get('sportValue'));
			    // $('#artValue').html(data.get('artValue'));
			    // $('#intelligenceValue').html(data.get('intelligenceValue'));
			    // $('#luckValue').html(data.get('luckValue'));
                console.log(data);
			})
	});


});

function minus(){

}
