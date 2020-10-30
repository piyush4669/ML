let video;
let poseNet
let pose
let skeleton
let brain
let state = 'waiting'
let targetLabel

//DATA COLLECTION
// function keyPressed() {

//     if (key == 's') {
//         brain.saveData();
//     } else {
//         targetLabel = key;
//         console.log('waiting');
//         console.log(targetLabel);
//         setTimeout(() => {
//             console.log('collecting');
//             state = 'collecting';
//             setTimeout(() => {
//                 console.log('done');
//                 state = 'waiting';
//             }, 10000)
//         }, 10000);
//     }
// }


function setup() {
    createCanvas(640, 480);
    video = createCapture(VIDEO);
    video.hide();
    poseNet = ml5.poseNet(video, modelOnReady);
    poseNet.on('pose', gotPoses)
    let options = {
        inputs: 34,
        outputs: 3,
        task: 'classification',
        debug: true
    }
    brain = ml5.neuralNetwork(options);

    const modelInfo = {
        model: "./model.json",
        metadata: "./model_meta.json",
        weights: "./model.weights.bin"
    }

    brain.load(modelInfo, onModelLoaded)

    //MODEL TRAINING
    // brain.loadData('./mha.json', onDataReady)
}

// MODEL TRAINING
function onDataReady() {
    brain.normalizeData();
    brain.train({ epochs: 50 }, onTrainingFinished);
}

// MODEL TRAINING
function onTrainingFinished() {
    console.log("Model trained");
    brain.save();
}

//MODEL DEPLOY
function onModelLoaded() {
    console.log("Model Deployed and ready!");
    classifyPose();
}

function classifyPose() {
    if (pose) {
        let inputData = []
        for (let i = 0; i < pose.keypoints.length; i++) {
            let x = pose.keypoints[i].position.x
            let y = pose.keypoints[i].position.y
            inputData.push(x)
            inputData.push(y)
        }
        brain.classify(inputData, onResult)
    } else {
        setTimeout(classifyPose, 600);
    }
}

function onResult(error, results) {
    console.log(results[0].label);
    setTimeout(classifyPose, 600);
}


function gotPoses(poses) {
    if (poses.length > 0) {
        pose = poses[0].pose;
        skeleton = poses[0].skeleton;


        //DATA COLLECTION
        // if (state == 'collecting') {
        //     let inputData = []
        //     for (let i = 0; i < pose.keypoints.length; i++) {
        //         let x = pose.keypoints[i].position.x
        //         let y = pose.keypoints[i].position.y
        //         inputData.push(x)
        //         inputData.push(y)
        //     }
        //     brain.addData(inputData, [targetLabel])
        // }
    }
}

function modelOnReady() {
    console.log("PoseNet Model is ready!")
}

function draw() {
    translate(video.width, 0);
    scale(-1, 1);
    image(video, 0, 0, video.width, video.height);
    if (pose) {

        for (let i = 0; i < pose.keypoints.length; i++) {
            let x = pose.keypoints[i].position.x
            let y = pose.keypoints[i].position.y
            fill(0, 255, 0)
            ellipse(x, y, 4)
        }

        for (let i = 0; i < skeleton.length; i++) {
            let a = skeleton[i][0].position;
            let b = skeleton[i][1].position;
            strokeWeight(2);
            stroke(255,0,0);
            line(a.x, a.y, b.x, b.y);
        }
    }
}