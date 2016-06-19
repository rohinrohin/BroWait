var boards=$("#tabcontent div div").eq(0).children().eq(1).html();
var timer=setInterval(function(){
	if (location.pathname.endsWith("mainpage.jsf")||location.pathname.endsWith("trainbetweenstns.jsf")){
		if ($("#tabcontent div div").eq(0).children().eq(1).length){
			if ($("#tabcontent div div").eq(0).children().eq(1).html()!=boards){
				boards=$("#tabcontent div div").eq(0).children().eq(1).html();
				perform();
			}
		}
	}
}, 1000);

var perform=function(){
	console.log("performed");
	var details=$(".ctab").html().trim().split("-");
	var train=details[0];
	var type=details[1];
	
	var from=$($('a:contains("'+train+'")').parent().parent().children()[2]).html();
	var to=$($('a:contains("'+train+'")').parent().parent().children()[4]).html();
	
	var date="";
	var time=$($('a:contains("'+train+'")').parent().parent().children()[3]).html();
	
	var arr=[];
	var flightomg=[];
	$("#"+$("#tabcontent div div").eq(0).children().eq(1).attr('id')+" table tbody tr").each(function(index){
		if (index<2){
			$("td", this).each(function(ind){
				if (!arr[ind]){
					arr[ind]=new Array();
				}
				arr[ind][index]=$(this).html().split("<br>")[0].trim();
				if (index==0){
					arr[ind][index]=$(arr[ind][index]).html();
					date=moment(arr[ind][index], "DD-MM-YYYY");
					arr[ind][index]=(moment(arr[ind][index]+" "+time, "DD-MM-YYYY HH:mm").diff(moment(), 'hours'))-3;
				}
			});
		}
	});
	arr.shift();
	
	console.log(arr);
	for (var i=0;i<arr.length;i++){
		if (arr[i][1].split("/").length==2&&arr[i][1].indexOf("AVAILABLE")==-1){
			$.ajax({
				type: 'POST',
				url: "http://furore.in:5000/all",
				data: JSON.stringify({
					index: i,
					date: date.format("YYYY-MM-DD"),
					conditions: [{
						train: train
					},
					{
						class: type
					},
					{
						quota: arr[i][1].split("/")[0].match(/[a-zA-Z]+/)[0]
					}],
					hours_before: ""+arr[i][0],
					waiting_list: arr[i][1].split("/")[1].match(/[0-9]+/)[0],
					to: to,
					from: from
					
				}),
				success: function(data){
					var accord="#ffffff";
					var extra="";
					if (data['probability']<41){
						accord="#ff8888";
						console.log(data);
						extra="<br /><br />Try a flight instead<br />Flight Code: "+data['flight']['results'][0]['airline']+"<br />Price: "+data['flight']['results'][0]['price'];						
					}
					else if (data['probability']>59){
						accord="#88ff88";
					}
					else if (data['probability']>40&&data['probability']<60){
						accord="#ffff88";
					}
					for (var j=1;j<$("#"+$("#tabcontent div div").eq(0).children().eq(1).attr('id')+" table tbody tr").length;j+=2){
						$("#"+$("#tabcontent div div").eq(0).children().eq(1).attr('id')+" table tbody tr").eq(j).children().eq(data['index']+1).css("background-color", accord);
						$("#"+$("#tabcontent div div").eq(0).children().eq(1).attr('id')+" table tbody tr").eq(j).children().eq(data['index']+1).append("<br /><br />"+data['probability']+"% likely to<br />be confirmed"+extra);
						boards=$("#tabcontent div div").eq(0).children().eq(1).html();
					}
					console.log(data); 
				},
				contentType: "application/json",
				dataType: 'json'
			});
		}
	}
}

window.flight=function(e, fs){
	
}