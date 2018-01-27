/**
 * Team FluffyDollop
 * Tiffany Moi and Khyber Sen
 * SoftDev pd7
 * HW 16 -- Sequential Progression II: Electric Boogaloo
 * 2017-12-08
 */

(function() {
    "use strict";

    Object.prototype.print = function() {
        console.log(this);
    };

    /**
     * Turn tag names into HTML elements and append them to an HTML element.
     *
     * @param {HTMLElement} element the HTML element to append these newly created elements
     */
    Array.prototype.appendHtmlElementsTo = function(element) {
        this.map(e => document.createElement(e)).forEach(e => element.appendChild(e));
    };

    // iterate over an HTMLCollection as returned by element.children
    HTMLCollection.prototype.forEach = function(func) {
        const length = this.length;
        for (let i = 0; i < length; i++) {
            func(this[i], i, this);
        }
    };

    HTMLElement.prototype.setClass = function(className) {
        this.setAttribute("class", className);
    };

    (function firstList() {

        const heading = document.getElementById("h");
        const originalHeadingText = heading.innerText;

        const button = document.getElementById("b");

        const list = document.getElementById("thelist");

        // replace heading text w/ text of another element (a list item)
        const replaceHeadingText = function() {
            heading.innerText = this.innerText;
        };

        // restore heading text to original heading text
        const restoreHeadingText = function() {
            heading.innerText = originalHeadingText;
        };

        // remove an element (a list item)
        const deleteSelf = function() {
            this.remove();
        };

        // add all event listeners to an element (a list item)
        const registerItem = function(item) {
            item.addEventListener("mouseover", replaceHeadingText, false);
            item.addEventListener("mouseout", restoreHeadingText, false);
            item.addEventListener("click", deleteSelf, false);
        };

        // add another item to the list
        const addItem = function() {
            const item = document.createElement("li");
            item.innerText = "item " + list.children.length;
            registerItem(item);
            list.appendChild(item);
        };

        // add event listeners to each list item
        list.children.forEach(registerItem);

        // set button to add another list item
        button.addEventListener('click', addItem, false);

        ["br"].appendHtmlElementsTo(document.body);

    })();

    /**
     * A generator function that returns successive values for increasing unsigned integers.
     *
     * @callback Generator
     * @param {Number} an unsigned integer
     * @return {*}
     */

    /**
     * @callback HTMLElementCallback
     */

    /**
     * Creates a <div> containing a button that adds items to a list showing successive calls to generator.
     *
     * @param {Generator} generator a generator function that takes an unsigned integer and returns the value
     * @param {Boolean} showCall true if you want "<generator.name>(n) = " before each value
     * @param {HTMLElementCallback} itemCallback applied to the each item when created
     * @returns {HTMLDivElement} the <div>
     */
    const addSequence = function(generator, showCall, itemCallback) {
        showCall = Boolean(showCall);

        // add <br><hr><br> before new div
        ["br", "hr", "br"].appendHtmlElementsTo(document.body);

        const div = document.createElement("div");
        document.body.appendChild(div);

        const list = document.createElement("ol");
        div.appendChild(list);

        let i = 0;

        /**
         * Adds the next (i++th) value returned by generator to the <ol> list.
         */
        const addItem = function() {
            const item = document.createElement("li");
            list.appendChild(item);
            if (showCall) {
                item.innerText = generator.name + "(" + i + ") = ";
            }
            const value = generator(i++);
            if (value instanceof HTMLElement) {
                item.appendChild(value);
            } else {
                item.innerText += value.toString();
            }

            if (itemCallback) {
                itemCallback.apply(item);
            }
        };

        // create button, set text to function name, and add set onclick to addItem
        const button = document.createElement("button");
        div.appendChild(button);
        button.innerText = generator.name;
        button.addEventListener("click", addItem, false);

        return div;
    };

    const square = function(n) {
        return n * n;
    };

    const triangleNumber = function(n) {
        return (n * (n + 1)) >> 1;
    };

    const tetrahedralNumber = function(n) {
        return (n * (n + 1) * (n + 2)) / 6;
    };

    /**
     * Creates a fibonacci closure that generates successive fibonacci numbers
     * without re-computing them.
     *
     * @return {Generator} a function that generates successive fibonacci numbers
     *          based on how many times it was called.
     */
    const createFibonacciGenerator = function() {
        let a = 0;
        let b = 1;

        /**
         * @returns {Number} the next fibonacci number
         */
        return function fibonacci(n) {
            const temp = a;
            a = b;
            b = a + temp;
            return temp;
        };
    };

    const createPascalTriangleGenerator = function() {
        const pascalTriangle = [[1]];

        /**
         * @param n the row number
         * @returns {Array} nth row of the Pascal Triangle
         */
        const pascalTriangleRowHelper = function(n) {
            n |= 0;
            if (n < pascalTriangle.length) {
                return pascalTriangle[n];
            }
            if (n > pascalTriangle.length) {
                return pascalTriangleRowHelper(n - 1);
            }
            const line = Array(n);
            pascalTriangle.push(line);
            line[0] = 1;
            const prevRow = pascalTriangle[n - 1];
            for (let i = 1; i < n - 1; i++) {
                line[i] = prevRow[i - 1] + prevRow[i];
            }
            line[n - 1] = 1;
            return line;
        };

        const sum = arr => arr.reduce((a, b) => a + b);

        const formatPascalTriangleRow = false;

        return {
            triangle: function pascalTriangleRow(n) {
                if (!formatPascalTriangleRow) {
                    return pascalTriangleRowHelper(n + 1).join(" ");
                }

                const div = document.createElement("div");
                div.setClass("pascal-triangle-row");
                // noinspection CommaExpressionJS
                pascalTriangleRowHelper(n + 1)
                    .map(element => {
                        const elementDiv = document.createElement("div");
                        elementDiv.setClass("pascal-triangle-element");
                        elementDiv.innerText = element.toString();
                        return elementDiv;
                    })
                    .forEach(elementDiv => div.appendChild(elementDiv));
                return div;
            },
            formattedRows: formatPascalTriangleRow,
            powersOfTwo: function pascalTrianglePowersOfTwo(n) {
                return sum(pascalTriangleRowHelper(n + 1));
            }
        };
    };

    const pascalTriangle = createPascalTriangleGenerator();

    const createPowerTowerGenerator = function() {
        /**
         * @returns n ^ n n times in a power tower
         */
        return function powerTower(n) {
            n |= 0;
            let x = n;
            for (let i = 1; i < n; i++) {
                // noinspection JSSuspiciousNameCombination
                x = Math.pow(n, x);
            }
            return x;
        };
    };

    [
        square,
        triangleNumber,
        tetrahedralNumber,
        createFibonacciGenerator(),
        pascalTriangle.triangle,
        pascalTriangle.powersOfTwo,
        createPowerTowerGenerator(),
    ].forEach(generator => {
        if (generator === pascalTriangle.triangle) {
            const div = addSequence(generator, false, !pascalTriangle.formattedRows ? null :
                function itemCallback() {
                    this.setClass("pascal-triangle-row");
                }
            );
            div.setClass("pascal-triangle");
        } else {
            addSequence(generator, true, null);
        }
    });

    Array(5).fill("br").appendHtmlElementsTo(document.body);

})();
