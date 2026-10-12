// propose-send.js - ছোট browser JS উদাহরণ
async function propose(command, args=[], note="") {
  const res = await fetch("http://127.0.0.1:5000/propose", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({command, args, note})
  });
  return res.json();
}

async function approve(id, apiKey) {
  const res = await fetch(`http://127.0.0.1:5000/approve/${id}`, {
    method: "POST",
    headers: {"Content-Type": "application/json", "X-API-KEY": apiKey},
    body: JSON.stringify({approve: true})
  });
  return res.json();
}
