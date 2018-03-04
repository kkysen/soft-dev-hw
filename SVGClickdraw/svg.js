Element.prototype.clear = function() {
    this.innerHTML = "";
};

Element.prototype.setAttributes = function(attributes) {
    for (const attribute in attributes) {
        if (attributes.hasOwnProperty(attribute) && attributes[attribute]) {
            this.setAttribute(attribute, attributes[attribute]);
        }
    }
};

const SVGCanvas = Object.freeze({
    
    new: function() {
    
        const svgCreate = document.createElementNS.bind(document, "http://www.w3.org/2000/svg");
    
        const svg = svgCreate("svg");
    
        svg.newChild = function(elementName) {
            return svg.appendChild(svgCreate(elementName));
        };
    
        const p = {
            x: 0,
            y: 0,
            invalid: true,
        };
    
        p.set = function(x, y) {
            p.x = x;
            p.y = y;
            p.invalid = false;
        };
    
        let fillStyle;
        let strokeStyle;
    
        return Object.freeze({
        
            appendTo: function(element) {
                element.appendChild(svg);
                return this;
            },
        
            appendChild: function(element) {
                return svg.appendChild(element);
            },
        
            addEventListener: function(eventType, listener, optionsOrUseCapture) {
                svg.addEventListener(eventType, listener, optionsOrUseCapture);
            },
        
            get height() {
                return svg.getAttribute("height");
            },
        
            set height(height) {
                svg.setAttribute("height", height);
            },
        
            get width() {
                return svg.getAttribute("width");
            },
        
            set width(width) {
                svg.setAttribute("width", width);
            },
        
            get style() {
                return svg.style;
            },
        
            set fillStyle(fill) {
                fillStyle = fill;
            },
        
            set strokeStyle(stroke) {
                strokeStyle = stroke;
            },
        
            clear: function() {
                svg.clear();
                p.invalid = true;
            },
        
            fillRect: function(x, y, width, height, fill=fillStyle) {
                svg.newChild("rect").setAttributes({
                    x: x,
                    y: y,
                    width: width,
                    height: height,
                    fill: fill,
                });
                p.set(x, y);
            },
        
            fillRectCentered: function(x, y, width, height, fill=fillStyle) {
                this.fillRect(x - width * 0.5, y - height * 0.5, width, height, fill);
                p.set(x, y);
            },
        
            fillCircle: function(x, y, radius, fill=fillStyle, stroke=strokeStyle) {
                svg.newChild("circle").setAttributes({
                    cx: x,
                    cy: y,
                    r: radius,
                    fill: fill,
                    stroke: stroke,
                });
                p.set(x, y);
            },
        
            moveTo: function(x, y) {
                p.set(x, y);
            },
        
            line: function(x1, y1, x2, y2, stroke=strokeStyle) {
                svg.newChild("line").setAttributes({
                    x1: x1,
                    y1: y1,
                    x2: x2,
                    y2: y2,
                    stroke: stroke,
                });
                p.set(x2, y2);
            },
        
            lineTo: function(x, y, stroke=strokeStyle) {
                if (p.invalid === true) {
                    return;
                }
                this.line(p.x, p.y, x, y, stroke);
            },
        
        });
    
    },
    
});


(function(parent) {
    "use strict";
    
    const div = document.createElement("center");
    parent.appendChild(div);
    
    const width = 600;
    const height = 600;
    
    const canvas = SVGCanvas.new().appendTo(div);
    
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
    
    let shapeIndex = 0;
    let coordIndex = 0;
    
    const shapeFunctions = [
        function redCircle(x, y) {
            const radius = 20;
            canvas.fillStyle = canvas.strokeStyle = "red";
            canvas.fillCircle(x, y, radius);
        },
        function blueSquare(x, y) {
            const width = 40;
            const height = 40;
            canvas.fillStyle = canvas.strokeStyle = "blue";
            canvas.fillRectCentered(x, y, width, height);
        },
    ];
    
    const coordNames = [
        "offset",
        "screen",
        "client",
        "page",
    ];
    
    const runShapeFunction = function(x, y) {
        shapeFunctions[shapeIndex](x, y);
        canvas.moveTo(x, y);
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
        canvas.clear();
    });
    
    canvas.addEventListener("click", e => {
        e.preventDefault();
        const coordName = coordNames[coordIndex] || "offset";
        const x = e[coordName + "X"];
        const y = e[coordName + "Y"];
        canvas.lineTo(x, y);
        runShapeFunction(x, y);
    });
    
})(document.body);