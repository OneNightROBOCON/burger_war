
function getCSV(){
    var req = new XMLHttpRequest();
    req.open("get", "static/sim.csv", false);
    req.send(null);

    var result = convertCSVtoArray(req.responseText);
    return result
}

function convertCSVtoArray(str){
    console.log(str);
    var result = [];
    var tmp = str.split("\n");

    for(var i=0;i<tmp.length;++i){
        result[i] = tmp[i].split(',');
    }
    return result
}

function running(){
    console.log("clicked running");
    var url = 'http://' + location.host + '/warState/state';
    console.log(url);
    var post_str = JSON.stringify({"state":"running"});
    console.log(post_str);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, false);
    xhr.setRequestHeader('content-type', 'application/json');
    xhr.send(post_str);
}

function reset(){
    console.log("clicked reset");
    var url = 'http://' + location.host + '/reset';
    console.log(url);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    xhr.send();
}

function setting(){
  console.log("clicked setting");
  // get input name
  var red_name = document.getElementById("red_name").value;
  var blue_name = document.getElementById("blue_name").value;
  console.log(red_name);
  console.log(blue_name);
  var red_player = {"name":red_name, "side":"r", "id":"0000"};
  var blue_player = {"name":blue_name, "side":"b", "id":"0000"};

  //post targets setting json msg
  var url = 'http://' + location.host + '/warState/targets';
  console.log(url);
  var targets_list = getCSV();
  console.log(targets_list);
  for (var i = 0; i < targets_list.length - 1; i++) {
      var x = targets_list[i];
      var target = {"name":x[0], "id":x[2], "point":x[1]};
      var post_str = JSON.stringify(target);
      console.log(post_str);
      var xhr = new XMLHttpRequest();
      xhr.open('POST', url, false);
      xhr.setRequestHeader('content-type', 'application/json');
      xhr.send(post_str);
  }

  //post player name setting json msg
  var url = 'http://' + location.host + '/warState/players';
  console.log(url);
  // red
  var post_str_red = JSON.stringify(red_player);
  console.log(post_str_red);
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, false);
  xhr.setRequestHeader('content-type', 'application/json');
  xhr.send(post_str_red);

  // blue
  var post_str_blue = JSON.stringify(blue_player);
  var xhr = new XMLHttpRequest();
  console.log(post_str_blue);
  xhr.open('POST', url, false);
  xhr.setRequestHeader('content-type', 'application/json');
  xhr.send(post_str_blue);
  console.log("completed post answers");
}

function ready(){
    console.log("clicked ready");
    var url = 'http://' + location.host + '/submits';
    console.log(url);
    //red side
    var post_str = JSON.stringify({"name":"foo", "side": "r", "id": "0000"});
    console.log(post_str);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, false);
    xhr.setRequestHeader('content-type', 'application/json');
    xhr.send(post_str);

    // blue side
    var post_str = JSON.stringify({"name":"bar", "side": "b", "id": "0000"});
    console.log(post_str);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, false);
    xhr.setRequestHeader('content-type', 'application/json');
    xhr.send(post_str);
}

