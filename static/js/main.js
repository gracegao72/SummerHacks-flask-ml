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
    $('#imageElement')[0].src = '/video_feed'

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
  });
  setTimeout(checkPosition, 1000);
}

checkPosition();
