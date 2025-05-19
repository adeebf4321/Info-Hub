function lookup() {
    const value = document.getElementById("input").value.trim();
    const type = document.getElementById("type").value;
    const result = document.getElementById("result");

    if (!value) {
        result.textContent = "Please enter a value to search.";
        return;
    }

    result.textContent = "🔍 Searching...";

    fetch("/lookup", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type, value})
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            result.textContent = "❌ Error: " + data.error;
        } else {
            result.textContent = JSON.stringify(data, null, 2);
        }
    })
    .catch(err => {
        result.textContent = "⚠️ Request failed: " + err.message;
    });
}
