/* JS comes here */
var start_test_button=document.getElementById('start_test_button');
start_test_button.addEventListener("click", (event) => {
		console.log(start_test_button.getAttribute('test-id'))
    });
var proceed_to_exam=document.getElementById('proceed_to_exam');




(function() {

    var width = 320; // We will scale the photo width to this
    var height = 0; // This will be computed based on the input stream

    var streaming = false;

    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;

    function startup() {
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');
        photo = document.getElementById('photo');
        startbutton = document.getElementById('startbutton');

        navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            })
            .then(function(stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function(err) {
                console.log("An error occurred: " + err);
                // location.reload();
                alert('Please Make Sure Your Device have cemera or allow the permission of cemera in brower');
                // $j('#exampleModalCenter').modal('hide')
            });

        video.addEventListener('canplay', function(ev) {
            if (!streaming) {
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAttribute('width', width);
                video.setAttribute('height', height);
                canvas.setAttribute('width', width);
                canvas.setAttribute('height', height);
                streaming = true;
            }
        }, false);

        startbutton.addEventListener('click', function(ev) {
            takepicture();
            ev.preventDefault();
        }, false);

        clearphoto();
    }


    function clearphoto() {
        var context = canvas.getContext('2d');
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);

        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
    }

    function takepicture() {
        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            var data = canvas.toDataURL('image/png');
            console.log('>>>>>>>>>>>>>>ze',data)
            photo.setAttribute('src', data);
            
            proceed_to_exam.removeAttribute('disabled')
        } else {
            clearphoto();
        }
    }

    window.addEventListener('load', startup, false);



    proceed_to_exam.addEventListener("click", (event) => {
        console.log("proceed cl8ick");

        // submit_exam_fuction();

        // function submit_exam_fuction() {
        //     $j.ajax({
        //         type: "POST",

        //         url: "/submit-exam",

        //         success: function (response) {
        //             window.location.replace(
        //                 "http://localhost:8000/submit-exam/"
        //             );
        //         },
        //     });
        // }
        
    });





})();