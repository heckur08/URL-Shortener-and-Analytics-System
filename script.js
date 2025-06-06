async function shorten() {
  const url = document.getElementById("longUrl").value;
  const response = await fetch("/shorten", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ long_url: url })
  });

  const data = await response.json();
  document.getElementById("shortResult").innerText = `Short URL: ${data.short_url}`;
}

async function getStats() {
  const code = document.getElementById("shortCode").value;
  const response = await fetch(`/stats/${code}`);
  const data = await response.json();
  document.getElementById("statsResult").innerText = JSON.stringify(data, null, 2);
}
