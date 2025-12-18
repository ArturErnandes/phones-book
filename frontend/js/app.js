const API = 'http://127.0.0.1:8000';

const colors = [
    '#67D4FF',
    '#768BFF',
    '#7ED574',

    '#43dfca',
    '#dc86f0',
    '#49b3f6',
    '#ff7862',
    '#ffba62'
];

function avatar(letter) {
    const c = colors[Math.floor(Math.random() * colors.length)];
    return `<span class="avatar" style="background:${c}">${letter}</span>`;
}

async function loadAll() {
    const r = await fetch(`${API}/subscribers`);
    const data = await r.json();
    render(data.data ?? data);
}

function render(list) {
    const body = document.getElementById('table-body');
    body.innerHTML = '';

    list.forEach(s => {
        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td>${avatar(s.fam[0].toUpperCase())}${s.fam} ${s.name} ${s.surnm ?? ''}</td>
            <td>${s.street ?? ''}</td>
            <td>${s.bldng ?? ''}</td>
            <td>${s.bldng_k ?? ''}</td>
            <td>${s.appr ?? ''}</td>
            <td>${s.ph_num}</td>
            <td><span class="delete" onclick="remove(${s.subs_id})">🗑</span></td>
        `;
        body.appendChild(tr);
    });
}

async function search() {
    const params = new URLSearchParams();
    ['fam','name','surnm','street'].forEach(id => {
        const v = document.getElementById(id).value;
        if (v) params.append(id, v);
    });

    const r = await fetch(`${API}/subscribers/search?${params}`);
    const data = await r.json();
    render(data.data);
}

async function remove(id) {
    if (!confirm('Удалить абонента?')) return;
    await fetch(`${API}/subscribers/delete/${id}`, { method: 'DELETE' });
    loadAll();
}

function openModal() {
    document.getElementById('modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}

async function createSubscriber() {
    const data = {
        fam: m_fam.value,
        name: m_name.value,
        surnm: m_surnm.value,
        street: m_street.value,
        bldng: m_bldng.value,
        bldng_k: m_bldng_k.value,
        appr: m_appr.value,
        ph_num: m_ph.value
    };

    await fetch(`${API}/subscribers/new_subscriber`, {

        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    closeModal();
    loadAll();
}

loadAll();