document.getElementById('generate').addEventListener('click', async () => {
  const prefix = document.getElementById('prefix').value;
  const suffix = document.getElementById('suffix').value;
  document.getElementById('result').innerText = 'Generating...';
  try {
    const resp = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prefix, suffix })
    });
    const data = await resp.json();
    if (data.error) throw new Error(data.error);
    document.getElementById('result').innerHTML =
      `<p><strong>Address:</strong> ${data.address}</p>` +
      `<p><strong>Private Key:</strong> <code>${data.private_key}</code></p>`;
  } catch (err) {
    document.getElementById('result').innerText = 'Error: ' + err.message;
  }
});
