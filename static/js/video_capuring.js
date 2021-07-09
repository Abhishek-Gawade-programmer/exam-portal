/* JS comes here */
var proceed_to_exam = document.getElementById("proceed_to_exam");

all_start_exam_buttons = document.querySelectorAll(".start_test");

window.current_test = 0;
window.data = "";
all_start_exam_buttons.forEach((item) =>
    item.addEventListener("click", (event) => {
        window.current_test = item.getAttribute("test-id");
    })
);
var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

(function () {
    var width = 320; // We will scale the photo width to this
    var height = 0; // This will be computed based on the input stream

    var streaming = false;

    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;
    function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    function startup() {
        video = document.getElementById("video");
        canvas = document.getElementById("canvas");
        photo = document.getElementById("photo");
        startbutton = document.getElementById("startbutton");

        navigator.mediaDevices
            .getUserMedia({
                video: true,
                audio: false,
            })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (err) {
                console.log("An error occurred: " + err);
                // location.reload();
                alert('Please Make Sure Your Device have cemera or allow the permission of cemera in brsower');
                // $j('#exampleModalCenter').modal('hide')
            });

        video.addEventListener(
            "canplay",
            function (ev) {
                if (!streaming) {
                    height = video.videoHeight / (video.videoWidth / width);

                    if (isNaN(height)) {
                        height = width / (4 / 3);
                    }

                    video.setAttribute("width", width);
                    video.setAttribute("height", height);
                    canvas.setAttribute("width", width);
                    canvas.setAttribute("height", height);
                    streaming = true;
                }
            },
            false
        );

        if (window.location.href.indexOf('/test/') >-1) {
            var intervalId = setInterval(function () {
                send_picture_database();
            }, 200000);
        } else {

        startbutton.addEventListener('click', function(ev) { takepicture();
            ev.preventDefault();
        }, false);

        }

        clearphoto();
    }

    function clearphoto() {
        var context = canvas.getContext("2d");
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);

        var data = canvas.toDataURL("image/png");
        photo.setAttribute("src", data);
    }

    function takepicture() {
        var context = canvas.getContext("2d");
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            var data = canvas.toDataURL("image/png");
            window.data = data;
            photo.setAttribute("src", data);

            proceed_to_exam.removeAttribute("disabled");
        } else {
            clearphoto();
        }
    }

    function send_picture_database() {
        var context = canvas.getContext("2d");
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            data = canvas.toDataURL("image/png");

            $j.ajax({
                type: "POST",

                url: "/takingphoto-student/",
                data: {
                    csrfmiddlewaretoken: csrftoken,

                    current_test: document
                        .getElementById("test_data")
                        .getAttribute("test-id"),
                    data_img: data,
                },

                success: function (response) {
                },
            });
        } else {
            clearphoto();
        }
    }

    window.addEventListener("load", startup, false);

    proceed_to_exam.addEventListener("click", (event) => {
        // console.log("proceed cl8ick",window.current_test,window.data);

        vefication_of_student();

        function vefication_of_student() {
            $j.ajax({
                type: "POST",

                url: "/verification-student/",
                data: {
                    csrfmiddlewaretoken: csrftoken,

                    current_test: window.current_test,
                    data_img: window.data,
                },

                success: function (response) {
                    window.location.replace(
                        "http://localhost:8000/test/" +
                            window.current_test +
                            "/"
                    );
                },
            });
        }
    });
})();
