(function movies() {
    
    const snakeCaseToEnglish = function(snakeCase) {
        return snakeCase
            .split("_")
            .map(word => word[0].toUpperCase() + word.slice(1))
            .join(" ");
    };
    
    fetch("/movies_queries")
        .then(response => response.json())
        .then(queries => {
            const div = document.body
                // .appendChild(document.createElement("center"))
                .appendChild(document.createElement("div"));
            const queryTable = div.appendChild(document.createElement("table"));
            
            const inputs = queries
                .filter(query => query.numArgs === 1)
                .map(query => {
                    
                    const displayName = snakeCaseToEnglish(query.name);
                    
                    const row = queryTable.appendChild(document.createElement("tr"));
                    
                    const name = row.appendChild(document.createElement("td"));
                    name.innerText = displayName;
                    
                    const input = row
                        .appendChild(document.createElement("td"))
                        .appendChild(document.createElement("label"))
                        .appendChild(document.createElement("input"));
                    input.query = query;
                    input.type = "text";
                    if (query.argTypes[0] === "int") {
                        input.type = "number";
                    }
                    
                    return input;
                });
            
            div.appendChild(document.createElement("br"));
            const submit = div.appendChild(document.createElement("button"));
            submit.innerText = "Search";
            
            div.appendChild(document.createElement("br"));
            div.appendChild(document.createElement("br"));
            div.appendChild(document.createElement("hr"));
            
            const loading = div.appendChild(document.createElement("h3"));
            loading.innerText = "Loading...";
            loading.style.display = "none";
            
            const resultDiv = div.appendChild(document.createElement("div"));
            
            submit.addEventListener("click", function(e) {
                e.preventDefault();
                const query = {};
                for (const input of inputs) {
                    let arg = input.value;
                    if (arg.length > 0) {
                        if (input.query.argTypes[0] === "int") {
                            arg = parseInt(arg);
                        }
                        query[input.query.name] = [arg];
                    }
                }
                const form = new FormData();
                form.set("query", JSON.stringify(query));
                resultDiv.innerHTML = "";
                loading.style.display = "";
                fetch("/movies", {
                    method: "POST",
                    credentials: "same-origin",
                    mode: "same-origin",
                    body: form,
                })
                    .catch(reason => resultDiv.innerText = reason)
                    .then(response => response.json())
                    .then(results => {
                        window.results = results;
                        
                        loading.style.display = "none";
                        if (results.length === 0) {
                            resultDiv.innerText = "No Results";
                            return;
                        }
                        
                        resultDiv.innerHTML = "<code>"
                            + results.map(result =>
                                JSON.stringify(result, null, 2)
                                    .replace(/\n/g, "<br>")
                                    .replace(/ /g, "&nbsp;")
                            )
                            .join("</code><br><hr><code>")
                        + "</code>";
                    });
            });
        });
    
})();