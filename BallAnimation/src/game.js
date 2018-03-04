"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const listener_1 = require("./listener");
const newGameAction = function (action) {
    const gameAction = action;
    gameAction.listener = listener_1.newListener(action);
    gameAction.button = document.createElement("button");
    gameAction.listener.click(gameAction.button);
    return gameAction;
};
exports.newGame = function () {
    return (function () {
        const fields = {
            name: null,
            canvas: null,
            width: null,
            height: null,
        };
        const checkFieldsInitialized = function () {
            for (const field in fields) {
                if (fields.hasOwnProperty(field)) {
                    if (!fields[field]) {
                        throw new Error(field + " not set");
                    }
                }
            }
        };
        const builder = {
            name: function (name) {
                fields.name = name;
                return builder;
            },
            canvas: function (canvas) {
                fields.canvas = canvas;
                return builder;
            },
            newCanvas: function (canvasParent) {
                fields.canvas = document.createElement("canvas");
                canvasParent.appendChild(fields.canvas);
                return builder;
            },
            width: function (width) {
                fields.width = width;
                return builder;
            },
            height: function (height) {
                fields.height = height;
                return builder;
            },
            size: function (widthOrSize, height) {
                let width;
                if (height === undefined) {
                    const size = widthOrSize;
                    width = size.x;
                    height = size.y;
                }
                else {
                    width = widthOrSize;
                }
                return builder.width(width).height(height);
            },
            build: function () {
                checkFieldsInitialized();
                const canvas = fields.canvas;
                const context = canvas.getContext("2d");
                const parent = canvas.parentElement;
                canvas.width = fields.width;
                canvas.height = fields.height;
                const actors = [];
                canvas.style.border = "1px solid black";
                const game = {
                    name: fields.name,
                    canvas: canvas,
                    context: context,
                    parent: parent,
                    tick: 0,
                    time: null,
                    delta: 0,
                    prevId: null,
                    clearFrame: true,
                    clear: function () {
                        context.clearRect(0, 0, canvas.width, canvas.height);
                    },
                    start: newGameAction(() => {
                        resume(true);
                    }),
                    stop: newGameAction(() => {
                        window.cancelAnimationFrame(game.prevId);
                        frame.prevId = null;
                        frame.time = null;
                    }),
                    resume: newGameAction(() => {
                        resume(false);
                    }),
                    reset: newGameAction(() => {
                        actors.forEach(actor => actor.reset(game));
                    }),
                    restart: newGameAction(() => {
                        game.stop();
                        game.reset();
                        game.start();
                    }),
                    actors: actors,
                    addActor: function (actor) {
                        actors.push(actor);
                        const privateGame = actor;
                        privateGame.game = game;
                        privateGame.id = actors.length;
                        privateGame.remove = function () {
                            this.game.removeActor(this);
                        };
                    },
                    removeActor: function (actor) {
                        actors.splice(actor.id, 1);
                        const privateGame = actor;
                        privateGame.game = null;
                        privateGame.id = null;
                    },
                };
                const frame = game;
                const update = function (game) {
                    actors.forEach(actor => actor.update(game));
                };
                const render = function (game) {
                    if (game.clearFrame) {
                        game.clear();
                    }
                    actors.forEach(actor => actor.render(game));
                };
                const gameLoop = function (time) {
                    frame.tick++;
                    frame.delta = game.time === null ? 0 : time - game.time;
                    frame.time = time;
                    update(game);
                    render(game);
                    frame.prevId = window.requestAnimationFrame(gameLoop);
                };
                const resume = function (reset) {
                    if (reset) {
                        game.reset();
                    }
                    if (!frame.prevId) {
                        // if not already stopped
                        frame.prevId = window.requestAnimationFrame(gameLoop);
                        console.log("starting");
                    }
                };
                return game;
            },
        };
        return builder;
    }).call({});
};
