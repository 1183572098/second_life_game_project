var random = byId("random"),
healthValue = byId("healthValue"),
sportValue = byId("sportValue"),
artValue = byId("artValue"),
intelligenceValue = byId("intelligenceValue"),
luckValue = byId("luckValue");


function byId(id){
	return typeof(id)==="string"?document.getElementById(id):id;
}

$(document).ready(function(){
	$('#random').click(function(){
		user_id = $(this).attr('data-userid');
        console.log("user_id: "+user_id);
		$.post('/game/initial/random/',
			{'user_id': user_id},
			function (data) {
                $('#healthVlaue').html(data.get('healthValue'));
			    $('#sportValue').html(data.get('sportValue'));
			    $('#artValue').html(data.get('artValue'));
			    $('#intelligenceValue').html(data.get('intelligenceValue'));
			    $('#luckValue').html(data.get('luckValue'));
			})
	});
});

function minus(){

}
