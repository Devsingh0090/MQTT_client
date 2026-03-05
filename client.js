document.getElementById('pubForm').addEventListener('submit', async function(e){
  e.preventDefault();
  const status = document.getElementById('status');
  const fd = new FormData(this);
  status.innerText = 'Sending...';
  try{
    const res = await fetch('/publish', { method: 'POST', body: fd });
    const js = await res.json();
    if (!res.ok) status.innerText = 'Error: ' + (js.error || res.statusText);
    else status.innerText = 'Sent 1 ID to ' + js.topic + ' @ ' + js.broker;
  }catch(err){ status.innerText = 'Network error: '+err.message }
});
