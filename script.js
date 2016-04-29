$(function() {
    $('input[type="text"]').tooltip({
        position: { my: "center top+7", at: "center bottom" }
    });
          
    $('#play').tooltip({
        position: { my: "center top", at: "center+30 bottom" }
    });
          
    $('#play.code1').click(function(){
        var direction = $("textarea#direction.code1").val();
        var time = Number($("#Seconds").val())*1000;
        run_MOTOR();
        setTimeout(stop_MOTOR,time);
    })
            
    $( "input[type='text']" ).change(function() {
        var newValue = $(this).val();
        var title = $(this).attr("id");
          
        if (title == "Steering"){
            if(Number(newValue) < 0) { $(this).val("0"); newValue = "0";}
            else if(Number(newValue) > 0) { $(this).val("0"); newValue = "0";}
        }
          
        if (title == "Power"){
            if(Number(newValue) < 0) {$(this).val("0"); newValue = "0";}
            else if(Number(newValue) > 100) { $(this).val("100"); newValue = "100";}
        }
          
        if (title == "Seconds"){
            if(Number(newValue) < 0) { $(this).val("0"); newValue = "0"; }
        }
        if (title != "Steering") $(this).attr('title', title + ": " + newValue);
    });
    $( "a" ).click(function( event ) {
        event.preventDefault();
        var div = $(this).attr("class");
        $(".codingArea").hide();
        $('#' + div).show();
    });
          
});
      
function xml_http_post(url, data, callback) {
    var req = false;
    try {
        // Firefox, Opera 8.0+, Safari
        req = new XMLHttpRequest();
    }
    catch (e) {
        // Internet Explorer
        try {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }
    }
    req.open("POST", url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status==200) {
            callback(req);
        }
    }
    req.send(data);
}
      
function run_MOTOR() {
	console.log("RUN");
    var data=get_motorspeed();
    data.cmd='run';
    data=JSON.stringify(data);
    xml_http_post("index.html", data, test_handle); 
    return;
}

function stop_MOTOR() {
	console.log("STOP")
    var data=get_motorspeed();
    data.cmd='stop';
    data=JSON.stringify(data);
    xml_http_post("index.html", data, test_handle); 
    return;
}
      
function get_motorspeed(){
    var data1="0";
    var data2=$("#Power").val();
    var data3=$("#Power").val();
    var data4= "0";
    var data={device:'motor',motor0:data1,motor1:data2,motor2:data3,motor3:data4};
    console.log(data);
    return data;
}
      
function test_handle(req) {
    var elem1 = document.getElementById('test_result');
    var s=JSON.parse(req.responseText);
    console.log(s);
}