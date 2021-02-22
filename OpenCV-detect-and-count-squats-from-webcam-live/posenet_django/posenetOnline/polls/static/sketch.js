let video;
let poseNet
let pose
let skeleton
let squats = 0
let angles
let button
let start = false
let buffer = []



function setup() {
    createCanvas(800, 600);
    video = createCapture(VIDEO);
    video.size(width, height);
    video.hide();
    poseNet = ml5.poseNet(video, modelOnReady);
    poseNet.on('pose', gotPoses)
    button = createButton('GO!!!');
    button.position(400, 500);
    button.mousePressed(onBtnPress);
}

function onBtnPress() {
    if (start === true) {
        start = false
    } else {
        start = true
    }
    console.log(start);
}


function gotPoses(poses) {
    if (poses.length > 0) {
        pose = poses[0].pose;
        skeleton = poses[0].skeleton;
    }
}

function modelOnReady() {
    console.log("PoseNet Model is ready!")
}

function find_angle(p0, p1, c) {
    var p0c = Math.sqrt(Math.pow(c.x - p0.x, 2) +
        Math.pow(c.y - p0.y, 2)); // p0->c (b)
    var p1c = Math.sqrt(Math.pow(c.x - p1.x, 2) +
        Math.pow(c.y - p1.y, 2)); // p1->c (a)
    var p0p1 = Math.sqrt(Math.pow(p1.x - p0.x, 2) +
        Math.pow(p1.y - p0.y, 2)); // p0->p1 (c)
    return Math.acos((p1c * p1c + p0c * p0c - p0p1 * p0p1) / (2 * p1c * p0c));
}

function getAngleLeftSHK() {
    let angleLeftSHK = find_angle(pose.leftShoulder, pose.leftHip, pose.leftKnee)
    let angleRightSHK = find_angle(pose.rightShoulder, pose.rightHip, pose.rightKnee)
    let angleLeftHKA = find_angle(pose.leftHip, pose.leftKnee, pose.leftAnkle)
    let angleRightHKA = find_angle(pose.rightHip, pose.rightKnee, pose.rightAnkle)

    return ({
        "a": angleLeftSHK * 57.296,
        "b": angleLeftHKA * 57.296,
        "c": angleRightSHK * 57.296,
        "d": angleRightHKA * 57.296,
    })
}


function draw() {
    push()
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

        angles = getAngleLeftSHK()

        for (let i = 0; i < skeleton.length; i++) {
            let a = skeleton[i][0].position;
            let b = skeleton[i][1].position;
            strokeWeight(2);
            stroke(255, 0, 0);
            line(a.x, a.y, b.x, b.y);
        }
    }

    pop()
    fill(100);
    textSize(32);
    if (pose) {
        f = "ACC: " + parseInt(pose.score*100)
        text(f, 10, 10, 400, 80);
    }

    f = "FPS: " + parseInt(frameRate())
    text(f, 10, 40, 400, 80);

    textSize(32);
    f = "SQUATS: " + squats
    text(f, 10, 80, 400, 80);

    if (angles) {
        a = parseInt(angles.a)
        b = parseInt(angles.b)
        c = parseInt(angles.c)
        d = parseInt(angles.d)
        t = (a + b + c + d)

        f = "SHK: " + t
        text(f, 10, 120, 400, 80)

        // f = "HKA: " + b
        // text(f, 10, 160, 400, 80)

        // f = "SHK: " + c
        // text(f, 10, 200, 400, 80)

        // f = "HKA: " + d
        // text(f, 10, 240, 400, 80)

        if (start === true) {
            if (buffer.length < 100) {
                buffer.push(t)
            } else {
                m = Math.max(...buffer)
                if (m > 140 && m < 200) {
                    console.log(buffer, m);
                    squats = squats + 1
                }
                buffer = []
            }
        }
    }
}