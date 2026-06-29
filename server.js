const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');
const path = require('path');
const fs = require('fs');
const multer = require('multer');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { cors: { origin: '*' }, pingTimeout: 60000 });

const PORT = process.env.PORT || 3666;
const SNIPPETS_DIR = path.join(__dirname, 'snippets');
const ADMIN_PASS = process.env.ADMIN_PASS || 'chaos1993';

// Ensure snippets dir exists
if (!fs.existsSync(SNIPPETS_DIR)) fs.mkdirSync(SNIPPETS_DIR, { recursive: true });

app.use(express.static(path.join(__dirname)));
app.use('/snippets', express.static(SNIPPETS_DIR));
app.get('/', (_req, res) => res.sendFile(path.join(__dirname, 'index.html')));

// ════════════════ ADMIN UPLOAD ════════════════
const storage = multer.diskStorage({
  destination: SNIPPETS_DIR,
  filename: (_req, file, cb) => cb(null, file.originalname)
});
const upload = multer({
  storage,
  limits: { fileSize: 80 * 1024 * 1024 }, // 80 MB per file
  fileFilter: (_req, file, cb) => {
    const ok = /\.(mp3|wav|ogg|m4a)$/i.test(file.originalname);
    cb(null, ok);
  }
});

app.get('/admin', (req, res) => {
  if (req.query.pass !== ADMIN_PASS) {
    return res.send(`<!DOCTYPE html><html><body style="font-family:sans-serif;background:#111;color:#eee;padding:40px">
      <h2>🔒 Admin — zadej heslo</h2>
      <form><input name="pass" type="password" placeholder="heslo" style="padding:8px;margin-right:8px">
      <button type="submit" style="padding:8px 16px">Vstoupit</button></form></body></html>`);
  }
  const files = fs.readdirSync(SNIPPETS_DIR).filter(f => /\.(mp3|wav|ogg)$/i.test(f));
  res.send(`<!DOCTYPE html><html><head>
  <meta charset="UTF-8">
  <title>Chaos A.D. Admin</title>
  <style>
    body{font-family:'Segoe UI',sans-serif;background:#0a0a10;color:#e0e0e0;padding:30px;max-width:700px;margin:0 auto}
    h1{color:#d4a017;font-size:28px;margin-bottom:4px}
    h2{color:#888;font-size:14px;font-weight:400;margin-bottom:24px;letter-spacing:2px}
    .upload-box{border:2px dashed #333;border-radius:12px;padding:30px;text-align:center;cursor:pointer;transition:.2s;margin-bottom:20px}
    .upload-box:hover{border-color:#d4a017;background:rgba(212,160,23,.05)}
    input[type=file]{display:none}
    .btn{background:#d4a017;color:#000;border:none;padding:10px 24px;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;margin-top:12px}
    .btn:hover{background:#f0c040}
    .btn-del{background:#c0392b;color:#fff;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px}
    table{width:100%;border-collapse:collapse;margin-top:16px}
    th{text-align:left;color:#888;font-size:11px;letter-spacing:2px;padding:6px 8px;border-bottom:1px solid #222}
    td{padding:7px 8px;border-bottom:1px solid #1a1a22;font-size:13px;font-family:monospace}
    .prog{display:none;margin-top:12px;color:#d4a017;font-size:14px}
    .tag{display:inline-block;padding:2px 6px;border-radius:3px;font-size:10px;background:#1e3a2a;color:#27ae60;margin-left:6px}
  </style>
  </head><body>
  <h1>⚡ CHAOS A.D. BATTLE</h1>
  <h2>ADMIN · SPRÁVA AUDIO SOUBORŮ</h2>

  <div class="upload-box" onclick="document.getElementById('fi').click()">
    <div style="font-size:40px;margin-bottom:8px">📁</div>
    <div style="font-size:15px;color:#aaa">Klikni nebo přetáhni MP3/WAV soubory</div>
    <div style="font-size:11px;color:#555;margin-top:4px">Max 80 MB / soubor · MP3, WAV, OGG</div>
    <input type="file" id="fi" multiple accept=".mp3,.wav,.ogg" onchange="upload(this.files)">
  </div>
  <div class="prog" id="prog">⏳ Nahrávám...</div>
  <button class="btn" onclick="document.getElementById('fi').click()">+ Přidat soubory</button>

  <h2 style="margin-top:28px">SNIPPETY (${files.length} souborů)</h2>
  <table>
    <tr><th>Soubor</th><th>Velikost</th><th></th></tr>
    ${files.map(f => {
      const size = Math.round(fs.statSync(path.join(SNIPPETS_DIR, f)).size / 1024);
      return `<tr><td>${f}</td><td>${size} KB</td>
        <td><button class="btn-del" onclick="del('${f}',this)">🗑</button></td></tr>`;
    }).join('')}
  </table>

  <script>
  const pass = '${ADMIN_PASS}';
  async function upload(files){
    const prog = document.getElementById('prog');
    prog.style.display = 'block';
    for(const f of files){
      prog.textContent = '⏳ Nahrávám: ' + f.name;
      const fd = new FormData(); fd.append('file', f);
      await fetch('/admin/upload?pass=' + pass, {method:'POST', body: fd});
    }
    prog.textContent = '✅ Hotovo! Stránka se obnoví...';
    setTimeout(()=>location.reload(), 1000);
  }
  async function del(name, btn){
    if(!confirm('Smazat ' + name + '?')) return;
    btn.disabled = true;
    await fetch('/admin/delete?pass=' + pass + '&file=' + encodeURIComponent(name), {method:'DELETE'});
    btn.closest('tr').remove();
  }
  // Drag-drop
  document.querySelector('.upload-box').addEventListener('dragover', e=>e.preventDefault());
  document.querySelector('.upload-box').addEventListener('drop', e=>{e.preventDefault();upload(e.dataTransfer.files);});
  </script>
  </body></html>`);
});

app.post('/admin/upload', (req, res) => {
  if (req.query.pass !== ADMIN_PASS) return res.status(401).send('Unauthorized');
  upload.array('file', 50)(req, res, (err) => {
    if (err) return res.status(400).json({ error: err.message });
    res.json({ ok: true, files: (req.files || []).map(f => f.originalname) });
  });
});

app.delete('/admin/delete', (req, res) => {
  if (req.query.pass !== ADMIN_PASS) return res.status(401).send('Unauthorized');
  const name = path.basename(req.query.file || '');
  if (!name) return res.status(400).send('Bad filename');
  const fp = path.join(SNIPPETS_DIR, name);
  if (fs.existsSync(fp)) fs.unlinkSync(fp);
  res.json({ ok: true });
});

// ════════════════ ROOM SYSTEM ════════════════
const rooms = {};

function makeCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let c = '';
  for (let i = 0; i < 4; i++) c += chars[Math.floor(Math.random() * chars.length)];
  return c;
}

function cleanRoom(code) {
  const room = rooms[code];
  if (!room) return;
  if (room.players.length === 0) { delete rooms[code]; return; }
  if (!room.players.find(p => p.id === room.hostId)) {
    room.hostId = room.players[0].id;
    io.to(code).emit('host-changed', room.hostId);
  }
}

io.on('connection', (socket) => {

  // ── Create room ──
  socket.on('create-room', ({ name }) => {
    let code = makeCode();
    while (rooms[code]) code = makeCode();
    rooms[code] = {
      code, hostId: socket.id,
      players: [{ id: socket.id, name, idx: 0, ready: false }],
      gameState: null, chat: []
    };
    socket.join(code);
    socket.roomCode = code;
    socket.playerIdx = 0;
    socket.emit('room-created', { code, players: rooms[code].players, playerIdx: 0 });
    console.log(`[Room] ${code} created by ${name}`);
  });

  // ── Join room ──
  socket.on('join-room', ({ code, name }) => {
    code = code.toUpperCase().trim();
    const room = rooms[code];
    if (!room) { socket.emit('room-error', 'Místnost nenalezena 🔍'); return; }
    if (room.players.length >= 4) { socket.emit('room-error', 'Místnost je plná (max 4 hráče)'); return; }
    const idx = room.players.length;
    const player = { id: socket.id, name, idx, ready: false };
    room.players.push(player);
    socket.join(code);
    socket.roomCode = code;
    socket.playerIdx = idx;
    socket.emit('room-joined', { code, players: room.players, playerIdx: idx });
    socket.to(code).emit('players-updated', room.players);
    if (room.gameState) socket.emit('game-state', room.gameState);
    console.log(`[Room] ${name} joined ${code} (slot ${idx})`);
  });

  // ── Game state sync (host → clients) ──
  socket.on('game-state', (state) => {
    const room = rooms[socket.roomCode];
    if (!room || room.hostId !== socket.id) return;
    room.gameState = state;
    socket.to(socket.roomCode).emit('game-state', state);
  });

  // ── Game event (host → specific client or all) ──
  socket.on('game-event', ({ type, data, targetIdx }) => {
    const room = rooms[socket.roomCode];
    if (!room || room.hostId !== socket.id) return;
    if (targetIdx !== undefined) {
      const target = room.players.find(p => p.idx === targetIdx);
      if (target) io.to(target.id).emit('game-event', { type, data });
    } else {
      socket.to(socket.roomCode).emit('game-event', { type, data });
    }
  });

  // ── Player action (client → host) ──
  socket.on('player-action', (action) => {
    const room = rooms[socket.roomCode];
    if (!room) return;
    io.to(room.hostId).emit('player-action', { ...action, playerIdx: socket.playerIdx, playerId: socket.id });
  });

  // ── Chat ──
  socket.on('chat', ({ msg }) => {
    const room = rooms[socket.roomCode];
    if (!room || !msg.trim()) return;
    const player = room.players.find(p => p.id === socket.id);
    const chatMsg = { name: player?.name || '?', msg: msg.slice(0, 120), time: Date.now(), idx: socket.playerIdx };
    room.chat.push(chatMsg);
    if (room.chat.length > 80) room.chat.shift();
    io.to(socket.roomCode).emit('chat', chatMsg);
  });

  // ── Disconnect ──
  socket.on('disconnect', () => {
    const code = socket.roomCode;
    const room = rooms[code];
    if (!room) return;
    room.players = room.players.filter(p => p.id !== socket.id);
    console.log(`[Room] ${code} — player disconnected, ${room.players.length} left`);
    cleanRoom(code);
    if (rooms[code]) io.to(code).emit('players-updated', rooms[code].players);
  });
});

httpServer.listen(PORT, () => {
  console.log('\n⚡ ══════════════════════════════════════════════ ⚡');
  console.log(`   CHAOS A.D. BATTLE  ·  ONLINE SERVER`);
  console.log(`   ➜  http://localhost:${PORT}`);
  console.log('⚡ ══════════════════════════════════════════════ ⚡\n');
});
