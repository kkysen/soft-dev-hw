(function() {

    HTMLCollection.prototype.forEach = function(func) {
        const length = this.length;
        for (let i = 0; i < length; i++) {
            func(this[i], i, this);
        }
    };

    const heading = document.getElementById("h");
    const originalHeadingText = heading.innerText;

    const button = document.getElementById("b");

    const list = document.getElementById("thelist");

    const replaceHeadingText = function() {
        heading.innerText = this.innerText;
    };

    const restoreHeadingText = function() {
        heading.innerText = originalHeadingText;
    };

    const deleteSelf = function() {
        this.remove();
    };

    const registerItem = function(item) {
        item.mouseover = replaceHeadingText;
        item.mouseout = restoreHeadingText;
        item.onclick = deleteSelf;
    };

    const addItem = function() {
        const item = document.createElement('li');
        item.innerText = "item " + list.children.length;
        registerItem(item);
        list.appendChild(item);
    };

    list.children.forEach(registerItem);

    button.onclick = addItem;

})();