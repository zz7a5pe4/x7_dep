$(document).ready(function(){
	
	$("#addHost").click(function(){
		var macAddress = $("#macAddress").val();
		var ipAddress = $("#ipAddress").val();
		
		if(macAddress == null || macAddress == ""){
			alert("Please enter the Mac Address");
		}
		else if(ipAddress == null || ipAddress == ""){
			alert("Please enter the IP Address");
		}
		else {
			
			jQuery.ajax({ //一个Ajax过程  
	       	    type: "get",  //以post方式与后台沟通
	      	    url : "addhost?macAddress="+macAddress+"&ipAddress="+ipAddress, //与django通信
	       	    contentType: "application/x-www-form-urlencoded;charset=UTF-8",
	      	    dataType: "text",
	      	    success: function( data, textStatus ){
	      	    	//do something
	      	    	alert(data);
	      	    },
	       		error: function(){
	       			alert("Connection error!")
	       			return;
	       		}
			});
		}
		
	});
	
	$("#installCompNode").click(function(){
		var compIpAddress = $("#compIpAddress").val();
		
		if(compIpAddress == null || compIpAddress == ""){
			alert("Please enter the IP Address");
		}
		else{
			
			jQuery.ajax({ //一个Ajax过程  
	       	    type: "get",  //以post方式与后台沟通
	      	    url : "installComputeNode?compIpAddress="+compIpAddress, //与django通信
	       	    contentType: "application/x-www-form-urlencoded;charset=UTF-8",
	      	    dataType: "text",
	      	    success: function( data, textStatus ){
	      	    	//do something
	      	    	alert(data);
	      	    },
	       		error: function(){
	       			alert("Connection error!")
	       			return;
	       		}
			});
		}
	});
});