"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const bouncingBall_1 = require("./bouncingBall");
const expandingBall_1 = require("./expandingBall");
const listener_1 = require("./listener");
var AnimationIndex;
(function (AnimationIndex) {
    AnimationIndex[AnimationIndex["EXPANDING_BALL"] = 0] = "EXPANDING_BALL";
    AnimationIndex[AnimationIndex["BOUNCING_BALL"] = 1] = "BOUNCING_BALL";
    AnimationIndex[AnimationIndex["BOUNCING_BALLS"] = 2] = "BOUNCING_BALLS";
    AnimationIndex[AnimationIndex["BOUNCING_KIRAN"] = 3] = "BOUNCING_KIRAN";
    AnimationIndex[AnimationIndex["DVD_PLAYER_SCREEN_SAVER"] = 4] = "DVD_PLAYER_SCREEN_SAVER";
    AnimationIndex[AnimationIndex["NUM_ANIMATIONS"] = 5] = "NUM_ANIMATIONS";
})(AnimationIndex = exports.AnimationIndex || (exports.AnimationIndex = {}));
const checkAnimationIndex = function (animationIndex) {
    if (animationIndex === AnimationIndex.NUM_ANIMATIONS) {
        throw new Error("animationIndex can't be NUM_ANIMATIONS");
    }
};
const renderImageAsBall = function (image) {
    return function (game, ball) {
        game.context.drawImage(image, ball.x - ball.radiusX, ball.y - ball.radiusY, ball.radiusX * 2, ball.radiusY * 2);
    };
};
const newBouncingImageGame = function (parent, imageFile, name = "Bouncing Image") {
    const maxWidth = 250;
    const maxHeight = 250;
    const img = new Image();
    img.src = imageFile;
    return new Promise((resolve, reject) => {
        img.onload = () => resolve(img);
        img.onerror = (e) => reject({
            reason: "Unable to load image \"" + imageFile + "\"",
            event: e,
        });
    })
        .then(img => createImageBitmap(img))
        .then(img => {
        const scale = 0.5 * Math.min(1, maxWidth / img.width, maxHeight / img.height);
        console.log(img);
        console.log(scale);
        return bouncingBall_1.newBouncingBallGame({
            name: name,
            parent: parent,
            gameWidth: 500,
            gameHeight: 500,
            ballRadiusX: img.width * scale,
            ballRadiusY: img.height * scale,
            initialBallSpeed: 10,
            ballRenderer: renderImageAsBall(img),
        });
    });
};
const newBouncingKiranGame = function (parent) {
    const fileName = "resources/JumpingKiran.png";
    const name = "Jumping Kiran";
    return newBouncingImageGame(parent, fileName, name);
};
const newDVDPlayerScreenSaver = function (parent) {
    const fileName = "resources/DVDPlayerLogo.jpg";
    const name = "DVD Player Screen Saver";
    return newBouncingImageGame(parent, fileName, name).then(game => {
        game.start.button.innerText = "I'm waiting for the movie to start";
        game.stop.button.innerText = "STOP";
        return game;
    });
};
const newAnimationGameUnchecked = function (animationIndex, parent) {
    switch (animationIndex) {
        case AnimationIndex.NUM_ANIMATIONS:
            checkAnimationIndex(animationIndex);
            return null;
        case AnimationIndex.EXPANDING_BALL:
            return Promise.resolve(expandingBall_1.newExpandingBallGame({
                parent: parent,
                gameWidth: 500,
                gameHeight: 500,
                initialBallRadius: 50,
                initialBallRadiusSpeed: 1,
            }));
        case AnimationIndex.BOUNCING_BALL:
            return Promise.resolve(bouncingBall_1.newBouncingBallGame({
                parent: parent,
                gameWidth: 500,
                gameHeight: 500,
                ballRadiusX: 50,
                ballRadiusY: 50,
                initialBallSpeed: 25,
            }));
        case AnimationIndex.BOUNCING_BALLS:
            const game = bouncingBall_1.newBouncingBallGame({
                name: "Bouncing Balls",
                parent: parent,
                gameWidth: 500,
                gameHeight: 500,
                ballRadiusX: 10,
                ballRadiusY: 10,
                initialBallSpeed: 15,
                numBalls: 10,
            });
            // game.ball.render = ;
            return Promise.resolve(game);
        case AnimationIndex.BOUNCING_KIRAN:
            return newBouncingKiranGame(parent);
        case AnimationIndex.DVD_PLAYER_SCREEN_SAVER:
            return newDVDPlayerScreenSaver(parent);
    }
};
const newAnimationGame = function (animationIndex, parent) {
    return new Promise(resolve => {
        newAnimationGameUnchecked(animationIndex, parent)
            .then(resolve)
            .catch(error => {
            console.log(error);
            resolve(null);
        });
    });
};
const newAnimation = function (animationIndex) {
    const div = document.body.appendDiv();
    div.hidden = true;
    return {
        index: animationIndex,
        div: div,
        game: newAnimationGame(animationIndex, div),
    };
};
exports.run = function (animationIndex) {
    checkAnimationIndex(animationIndex);
    const parent = document.body.appendNewElement("center");
    parent.appendBr();
    const switchAnimationButton = parent.appendButton("Switch Animation");
    const animationName = parent.appendNewElement("h3");
    const animations = new Array(AnimationIndex.NUM_ANIMATIONS)
        .fill(null)
        .map((e, i) => newAnimation(i));
    parent.appendBr();
    const switchAnimation = function () {
        animations[animationIndex].div.hidden = true; // hide last one
        animationIndex = (animationIndex + 1) % animations.length; // switch to next
        const animation = animations[animationIndex];
        console.log("switching to:", animation);
        animation.div.hidden = false; // show new one
        animation.game.then(game => {
            if (!game) {
                // if this game wasn't loaded, skip to next
                switchAnimation();
                return;
            }
            animationName.innerText = game.name;
        });
    };
    animationIndex = (animationIndex + animations.length - 1) % animations.length; // decrease to start with correct one
    switchAnimation();
    listener_1.newListener(switchAnimation).click(switchAnimationButton);
};
