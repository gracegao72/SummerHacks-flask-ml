//var handplaytime = 0;
//var postureplaytime = 0; 

var playtime = 0;
var counterbeg = 0;

//added one indicator -- kind of like the two variables tho
var indicator = 0;

$(document).ready(function(){
  let namespace = "/test";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");
  let ctx = canvas.getContext('2d');

  var localMediaStream = null;
  

  console.log(location.protocol + '//' + document.domain + ':' + location.port + namespace)
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('input image', dataURL);
  }

  socket.on('connect', function() {
    console.log('Connected!');
  });

  var constraints = {
    video: {
      width: { min: 640 },
      height: { min: 480 }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;

    setInterval(function () {
      sendSnapshot();
    }, 50);
  }).catch(function(error) {
    console.log(error);
  });
});


///////////////////////////////////////////////////////////////////////////
// Call the ML detection route to get the results
// This code sets up a loop so that it calls the /detection_feed endpoint
// every 1000 ms (e.g. 1 second) 
///////////////////////////////////////////////////////////////////////////

function checkPosition(){
  var settings = {
    "url": "/check_position",
    "method": "GET",
    "timeout": 0,
  };
  
  $.ajax(settings).done(function (response) {
    console.log(response["posture"]);
  
    //var z = new Audio("/static/js/hands.mp3")
    var x = new Audio("/static/js/posture.mp3");
    var y = new Audio("/static/js/Cameracantsee.mp3")
    if (response["posture"] ===  "no image detected") {
        counterbeg = counterbeg + 1; 
        if (counterbeg > 10) {
          y.play();
      }
       
    }

    else if (response["posture"] !==  "You are approximatly sitting straight." 
    && response["posture"] !==  "no image detected"
    && response["hand_detection"] ===  false) {
       x.play();
       playtime = playtime +  1;
    } 
    document.querySelector('.results').innerHTML = playtime;
    console.log(indicator);
    
  });
  //added indicator if
  if (indicator == 0 ){
    setTimeout(checkPosition, 1000);
  }
  
  

}

function checkFace(){
  var settings = {
    "url": "/check_face",
    "method": "GET",
    "timeout": 0,
  };
  
  $.ajax(settings).done(function (response) {
    console.log(response["hand_detection"]);
    var hand = "Watch your hands";
    var z = new Audio("/static/js/hands.mp3")
   //var x = new Audio("/static/js/posture.mp3");
   // var y = new Audio("/static/js/Cameracantsee.mp3")
    /*
    if (response["posture"] ===  "no image detected") {
        counterbeg = counterbeg + 1; 
        if (counterbeg > 10) {
          y.play();
      }
       
    } */
   

    if (response["posture"] !==  "no image detected" &&
    response["hand_detection"] ===  true ){
      z.play();
      playtime = playtime +  1;
    }

    document.querySelector('.results').innerHTML = playtime;
    console.log(indicator);
    
  });
  //added indicator if
  if (indicator > 0 ){
    setTimeout(checkFace, 1000);
  }
  
  

}
//added function setface which calls checkface
function setFace()
{
  indicator = 1 ;
  console.log(indicator);
  checkFace();
}
//added function setposter which calls checkposition
function setPosture()
{
  indicator = 0;
  checkPosition();
}