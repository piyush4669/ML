posenet.load().then(function (net) {
    console.log("Posenet is loaded")
    const imageScaleFactor = 0.50;
    const flipHorizontal = false;
    const outputStride = 16;

    function runModel() {
        net.estimateSinglePose(video, imageScaleFactor, flipHorizontal, outputStride).then((pose) => {
            console.log(pose.keypoints[0].position)
            requestAnimationFrame(runModel);
        })
    }

    // const imageElement = document.getElementById('img1');
    video.onloadeddata = function () {
        runModel()
    };
});