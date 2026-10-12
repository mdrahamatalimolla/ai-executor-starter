async function fetchProposals() {
  const res = await fetch('/proposals');
  if (!res.ok) throw new Error('Failed to fetch proposals');
  return await res.json();
}

function el(tag, props={}, ...children){
  const e = document.createElement(tag);
  Object.entries(props).forEach(([k,v])=>{ if(k.startsWith('on')) e.addEventListener(k.slice(2).toLowerCase(), v); else e.setAttribute(k,v); });
  children.flat().forEach(c=>{ e.append(typeof c==='string'?document.createTextNode(c):c); });
  return e;
}

async function render(){
  const container = document.getElementById('list');
  container.innerHTML = 'Loading...';
  try{
    const data = await fetchProposals();
    if(!data.length){ container.innerHTML = '<em>No proposals</em>'; return }
    const table = el('table');
    table.append(el('thead',{}, el('tr',{}, el('th',{},'ID'), el('th',{},'Command'), el('th',{},'Args'), el('th',{},'Note'), el('th',{},'Status'), el('th',{},'Created'), el('th',{},'Actions'))));
    const tbody = el('tbody');
    data.forEach(p=>{
      const tr = el('tr');
      tr.append(el('td',{}, String(p.id)));
      tr.append(el('td',{}, p.command_key));
      let argsText = p.args || '';
      try{ argsText = JSON.parse(argsText); argsText = Array.isArray(argsText)? argsText.join(' '):String(argsText); }catch(e){}
      tr.append(el('td',{}, argsText));
      tr.append(el('td',{}, p.note || ''));
      tr.append(el('td',{}, el('span', { style: '', class: `status-${p.status}` }, p.status)));
      tr.append(el('td',{}, p.created_at || ''));
      const actions = el('td');
      const approveBtn = el('button',{onclick: async ()=>{ await doApprove(p.id,true); await render(); }},'Approve');
      const rejectBtn = el('button',{onclick: async ()=>{ await doApprove(p.id,false); await render(); }},'Reject');
      const viewBtn = el('button',{onclick: async ()=>{ alert('Output:\n'+(p.output||'No output yet')) } },'View');
      actions.append(approveBtn, rejectBtn, viewBtn);
      tr.append(actions);
      tbody.append(tr);
    });
    table.append(tbody);
    container.innerHTML = '';
    container.append(table);
  }catch(err){
    container.innerHTML = '<div style="color:red">Error: '+err.message+'</div>';
  }
}

async function doApprove(id, approve=true){
  const key = document.getElementById('apiKey').value;
  if(!key){ alert('API key required for approval'); return }
  const res = await fetch(`/approve/${id}`,{
    method: 'POST',
    headers: {'Content-Type':'application/json', 'X-API-KEY': key},
    body: JSON.stringify({approve})
  });
  if(!res.ok){
    const txt = await res.text();
    alert('Failed: '+res.status+' '+txt);
  } else {
    const j = await res.json();
    alert('Result: '+j.status+' (id='+j.id+')');
  }
}

document.getElementById('refresh').addEventListener('click', render);
window.addEventListener('load', render);
