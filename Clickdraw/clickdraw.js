(function(parent) {
    "use strict";
    
    const div = document.createElement("center");
    parent.appendChild(div);
    
    const width = 600;
    const height = 600;
    
    const canvas = document.createElement("canvas");
    div.appendChild(canvas);
    
    div.appendChild(document.createElement("br"));
    
    const buttonsDiv = document.createElement("div");
    div.appendChild(buttonsDiv);
    
    const toggleShapeButton = document.createElement("button");
    buttonsDiv.appendChild(toggleShapeButton);
    
    const toggleCoordButton = document.createElement("button");
    buttonsDiv.appendChild(toggleCoordButton);
    
    const clearButton = document.createElement("button");
    buttonsDiv.appendChild(clearButton);
    
    toggleShapeButton.innerText = "Toggle Shape and Color";
    toggleCoordButton.innerText = "Toggle Coordinate System";
    clearButton.innerText = "Clear";
    
    canvas.style.border = "1px solid black";
    
    canvas.width = width;
    canvas.height = height;
    
    const context = canvas.getContext("2d");
    context.beginPath();
    
    let shapeIndex = 0;
    let coordIndex = 0;
    
    const shapeFunctions = [
        function redCircle(x, y) {
            const radius = 20;
            context.fillStyle = context.strokeStyle = "red";
            context.arc(x, y, radius, 0, 2 * Math.PI);
            context.fill();
        },
        function blueSquare(x, y) {
            const width = 40;
            const height = 40;
            context.fillStyle = context.strokeStyle = "blue";
            context.fillRect(x - width * 0.5, y - height * 0.5, width, height);
        },
    ];
    
    const coordNames = [
        "screen",
        "offset",
        "client",
        "page",
    ];
    
    const runShapeFunction = function(x, y) {
        context.beginPath();
        shapeFunctions[shapeIndex](x, y);
        context.moveTo(x, y);
    };
    
    toggleShapeButton.addEventListener("click", e => {
        e.preventDefault();
        shapeIndex = (shapeIndex + 1) % shapeFunctions.length;
    });
    
    toggleCoordButton.addEventListener("click", e => {
        e.preventDefault();
        coordIndex = (coordIndex + 1) % coordNames.length;
    });
    
    clearButton.addEventListener("click", e => {
        e.preventDefault();
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.beginPath();
    });
    
    canvas.addEventListener("click", e => {
        e.preventDefault();
        const coordName = coordNames[coordIndex] || "offset";
        const x = e[coordName + "X"];
        const y = e[coordName + "Y"];
        context.lineTo(x, y);
        context.stroke();
        runShapeFunction(x, y);
    });
    
})(document.body);