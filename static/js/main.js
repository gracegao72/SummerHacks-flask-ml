var playtime = 0;
var counterbeg = 0;
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
    console.log(response);
    // var available_voices = window.speechSynthesis.getVoices();

    // this will hold an english voice
    // var english_voice = '';

    // find voice by language locale "en-US"
    // if not then select the first voice
    //for(var i=0; i<available_voices.length; i++) {
    //if(available_voices[i].lang === 'en-US') {
    //    english_voice = available_voices[i];
    //    break;
    //}
    //}
    // if(english_voice === '')
    //english_voice = available_voices[0];

    // new SpeechSynthesisUtterance object
    //var utter = new SpeechSynthesisUtterance();
    //utter.rate = 1;
    // utter.pitch = 0.5;
    //utter.text = response[posture] + "hand present" + response[hand_detection];
    //utter.voice = english_voice;

    // event after text has been spoken
    //utter.onend = function() {
    //alert('Speech has finished');
    //}

    // speak
    //window.speechSynthesis.speak(utter);
    var str = "Watch your posture";
    var hand = "Watch your hands";
    var z = new Audio("/static/js/hands.mp3")
    var x = new Audio("/static/js/posture.mp3");
    var y = new Audio("/static/js/Cameracantsee.mp3")
    if (response["posture"] ===  "no image detected") {
        counterbeg = counterbeg + 1; 
        if (counterbeg > 10) {
          y.play();
      }
       
    }
   

    else if (response["posture"] !==  "no image detected" &&
    response["hand_detection"] ===  true ){
      z.play();
      playtime = playtime +  1;
    }
    else if (response["posture"] !==  "sitting straight" 
    && response["posture"] !==  "no image detected"
    && response["hand_detection"] ===  false) {
       x.play();
       playtime = playtime +  1;
    } 
    document.querySelector('.results').innerHTML = playtime;

    
  });
  setTimeout(checkPosition, 10000);
  

}

function callcheck(){
  checkPosition();
}



