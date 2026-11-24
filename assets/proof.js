/* 2부 — 주판봇의 증명 나무: 채점기 체험(#pa) · 증명 나무(#pb). 외부 라이브러리 없음 */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const NS = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------------- A. 채점기 체험 ---------------- */
  const LINES = [
    { t: 'a는 짝수이므로 a = 2 × m', why: '짝수의 뜻(이미 정해 둔 정의)을 그대로 씀', w: 'a는 짝수이므로 a = 2 + m', ww: '짝수의 뜻은 "2 × 무엇"이지 "2 + 무엇"이 아님' },
    { t: 'b는 짝수이므로 b = 2 × n', why: '짝수의 뜻을 그대로 씀', w: 'b는 짝수이므로 b = n × n', ww: '짝수의 뜻에서 "n × n"은 나오지 않음' },
    { t: 'a + b = 2 × m + 2 × n', why: '1·2번 줄의 a, b를 그대로 바꿔 넣음', w: 'a + b = 2 × m × n', ww: '1·2번 줄을 바꿔 넣으면 더하기가 나와야 하는데 곱하기가 나옴' },
    { t: '2 × m + 2 × n = 2 × (m + n)', why: '분배법칙 — 이미 증명된 정리를 빌려 씀', w: '2 × m + 2 × n = 2 × m + n', ww: '분배법칙과 맞지 않음(n 앞의 2가 사라짐)' },
    { t: '그러므로 a + b = 2 × (m + n), 곧 짝수', why: '3·4번 줄을 이어 붙이고 짝수의 뜻에 맞춤', w: '그러므로 a + b는 홀수', ww: '앞 줄에서 나온 "2 × (m + n)"은 홀수가 아님' }
  ];
  const pa = $('#pa');
  if (pa) {
    const box = $('#pa-lines'), msg = $('#pa-msg'), goal = $('#pa-goal');
    let timer = null;
    function draw() {
      box.innerHTML = LINES.map((L, i) => `<div class="pl" data-i="${i}"><span class="pn">${i + 1}</span><span class="pt" id="pa-t${i}">${esc(L.t)}</span>
        <select id="pa-s${i}" aria-label="${i + 1}번 줄 바꾸기"><option value="ok">그대로</option><option value="blank">비워 두기</option><option value="wrong">틀린 줄로</option></select>
        <span class="pm" id="pa-m${i}"></span></div>`).join('');
      LINES.forEach((L, i) => $('#pa-s' + i).addEventListener('change', e => {
        const v = e.target.value;
        $('#pa-t' + i).textContent = v === 'ok' ? L.t : v === 'blank' ? '(빈자리 — 나중에 채울게요)' : L.w;
        $('#pa-t' + i).className = 'pt ' + v;
        clearMarks();
      }));
    }
    function clearMarks() {
      clearInterval(timer);
      LINES.forEach((_, i) => { $('#pa-m' + i).textContent = ''; $('#pa-m' + i).className = 'pm'; });
      $('#pa-checked').textContent = '0줄'; $('#pa-ok').textContent = '—'; $('#pa-verdict').textContent = '—'; msg.innerHTML = '';
    }
    function run() {
      clearMarks();
      const easy = goal.value === 'easy';
      if (easy) {
        $('#pa-verdict').textContent = '통과';
        $('#pa-checked').textContent = '1줄'; $('#pa-ok').textContent = '1 / 1';
        msg.innerHTML = '<b>통과!</b> "a + b = a + b"는 같은 것끼리 같다는 한 줄이면 끝납니다. <b>그런데 이건 원래 질문("짝수 + 짝수는 짝수")이 아니에요.</b> 채점기는 "적힌 문장"을 검사할 뿐, 그 문장이 우리가 묻고 싶던 문제인지는 모릅니다. 그래서 꼭대기 문장은 사람이 따로 확인합니다.';
        return;
      }
      let i = 0, good = 0;
      timer = setInterval(() => {
        const v = $('#pa-s' + i).value, L = LINES[i], m = $('#pa-m' + i);
        if (v === 'ok') { good++; m.textContent = '✓ ' + L.why; m.className = 'pm ok'; }
        else if (v === 'blank') { m.textContent = '✗ 빈자리 — 증명이 비어 있어 통과 못 함'; m.className = 'pm no'; }
        else { m.textContent = '✗ ' + L.ww; m.className = 'pm no'; }
        i++;
        $('#pa-checked').textContent = i + '줄'; $('#pa-ok').textContent = good + ' / ' + i;
        if (i === LINES.length) {
          clearInterval(timer);
          const pass = good === LINES.length;
          $('#pa-verdict').textContent = pass ? '통과' : '불합격';
          msg.innerHTML = pass
            ? '<b>통과!</b> 다섯 줄 모두 앞 줄에서 나왔고 빈자리도 없습니다. 꼭대기 문장 "짝수 + 짝수는 짝수"까지 빈틈이 없어요. 주판봇: "5줄 검사, 5줄 통과! …근데 저는 센 것뿐이고, 채점기는 <b>앞 줄에서 나오는지</b>를 봤네요."'
            : `<b>불합격.</b> ${LINES.length}줄 가운데 ${LINES.length - good}줄에서 걸렸습니다. 한 줄이라도 빠지거나 틀리면 꼭대기 문장은 통과하지 못합니다. 1,700만 줄짜리 증명도 똑같은 규칙으로 검사했어요.`;
        }
      }, 420);
    }
    draw();
    $('#pa-run').addEventListener('click', run);
    $('#pa-reset').addEventListener('click', () => { draw(); clearMarks(); goal.value = 'real'; });
    goal.addEventListener('change', clearMarks);
    clearMarks();
  }

  /* ---------------- B. 증명 나무 (설명용 모형) ---------------- */
  const pb = $('#pb');
  if (pb) {
    const svg = $('#pb-svg'), msg = $('#pb-msg'), size = $('#pb-size'), dustOn = $('#pb-dust');
    const W = 640, H = 520;
    function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
    let trunk = [], leaves = [], dusts = [];
    function build() {
      const k = +size.value, T = [6, 12, 24, 48][k - 1], B = [2, 3, 4, 5][k - 1], D = [30, 70, 140, 260][k - 1];
      const r = rng(7 + k);
      trunk = []; leaves = []; dusts = [];
      for (let i = 0; i < T; i++) {
        const y = H - 40 - (H - 90) * i / (T - 1);
        const x = W / 2 + Math.sin(i * 0.9) * 18 * (1 - i / T) + (r() - 0.5) * 10;
        trunk.push({ x, y });
      }
      trunk.forEach((p, i) => {
        if (i === T - 1) return;
        for (let b = 0; b < B; b++) {
          const side = (b % 2 ? 1 : -1), len = 40 + r() * (90 + 30 * k);
          leaves.push({ from: i, x: p.x + side * len, y: p.y + (r() - 0.3) * 40, cx: p.x + side * len * 0.5, cy: p.y - 25 * r() });
        }
      });
      for (let d = 0; d < D; d++) { const x = r() * W, y = r() * H, a = r() * Math.PI, l = 8 + r() * 18; dusts.push([x, y, x + Math.cos(a) * l, y + Math.sin(a) * l]); }
      $('#pb-trunk').textContent = T + '단계'; $('#pb-branch').textContent = leaves.length + '개'; $('#pb-dustn').textContent = D + '개';
      draw();
      msg.innerHTML = k === 1
        ? '줄기·가지·먼지를 하나씩 눌러 보세요. <b>크기</b>를 키워도 모양은 그대로입니다 — 줄기 하나, 가지 여럿, 바깥 먼지.'
        : `크기 ${k}: 줄기 ${T}단계, 가지 ${leaves.length}개. 숫자만 커졌을 뿐 <b>모양은 같습니다</b>. 리만 가설의 실제 증명도 이 모양을 아주 크게 키운 것이에요.`;
    }
    function draw(hiTrunkFrom = -1, hiLeaf = -1) {
      svg.innerHTML = '';
      const gd = el('g', { opacity: dustOn.checked ? 1 : 0 }, svg);
      dusts.forEach((d, i) => {
        el('line', { x1: d[0], y1: d[1], x2: d[2], y2: d[3], stroke: '#c8ccd6', 'stroke-width': 1.5 }, gd);
        const hit = el('line', { x1: d[0], y1: d[1], x2: d[2], y2: d[3], stroke: 'transparent', 'stroke-width': 9, style: 'cursor:pointer' }, gd);
        hit.addEventListener('click', () => { if (!dustOn.checked) return; draw(); msg.innerHTML = '<b>먼지</b> — 끝내 쓰이지 않은 파일입니다. 길을 찾다 버린 시도들이에요. 초파리: "버린 길이 이렇게 많았다고?" 박사: "그게 바로 세기의 몫이에요. 많이 시도해 봐야 맞는 길이 보이거든요."'; });
      });
      leaves.forEach((L, i) => {
        const p = trunk[L.from], hi = i === hiLeaf;
        el('path', { d: `M${p.x},${p.y} Q${L.cx},${L.cy} ${L.x},${L.y}`, fill: 'none', stroke: hi ? '#0f8f84' : '#b9a6e8', 'stroke-width': hi ? 4 : 2 }, svg);
        const c = el('circle', { cx: L.x, cy: L.y, r: hi ? 7 : 5, fill: hi ? '#0f8f84' : '#8f72d6', style: 'cursor:pointer' }, svg);
        c.addEventListener('click', () => {
          draw(-1, i);
          const above = trunk.length - 1 - L.from;
          msg.innerHTML = `<b>가지</b> — 빌려 온 정리입니다. 이미 누군가 증명해 수학 도서관(Mathlib)에 넣어 둔 정리를 가져다 썼어요. 이 정리는 줄기 ${L.from + 1}단계에 붙어, 위로 ${above}단계를 거쳐 꼭대기 문장을 받칩니다(청록 선).`;
        });
      });
      for (let i = 0; i < trunk.length - 1; i++) {
        const a = trunk[i], b = trunk[i + 1];
        const broken = hiTrunkFrom >= 0 && i >= hiTrunkFrom;
        const lit = hiLeaf >= 0 && i >= leaves[hiLeaf].from;
        el('line', { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: broken ? '#c9302c' : lit ? '#0f8f84' : '#1e2f6e', 'stroke-width': 6, 'stroke-linecap': 'round', 'stroke-dasharray': broken ? '6 6' : 'none' }, svg);
      }
      trunk.forEach((p, i) => {
        const top = i === trunk.length - 1, broken = hiTrunkFrom >= 0 && i >= hiTrunkFrom;
        const c = el('circle', { cx: p.x, cy: p.y, r: top ? 13 : 7, fill: broken ? '#c9302c' : top ? '#e8731a' : '#1e2f6e', stroke: '#fff', 'stroke-width': 2, style: 'cursor:pointer' }, svg);
        if (!top) c.addEventListener('click', () => {
          draw(i);
          msg.innerHTML = `<b>줄기 ${i + 1}단계</b>를 뺐습니다. 그 위 ${trunk.length - 2 - i}단계와 꼭대기 문장이 <b>모두 무너집니다</b>(빨간 점선). 줄기는 증명의 뼈대라서, 한 단계만 빠져도 채점기를 통과하지 못해요.`;
        });
      });
      const t = trunk[trunk.length - 1];
      const lb = el('text', { x: t.x + 20, y: t.y + 5, 'font-size': 15, 'font-weight': 700, fill: '#e8731a' }, svg); lb.textContent = '꼭대기 문장';
      const b0 = trunk[0];
      const lb2 = el('text', { x: b0.x + 14, y: b0.y + 5, 'font-size': 13, fill: '#1e2f6e' }, svg); lb2.textContent = '줄기 1단계';
    }
    size.addEventListener('input', build);
    dustOn.addEventListener('change', () => draw());
    $('#pb-reset').addEventListener('click', () => { draw(); msg.innerHTML = '다시 눌러 보세요.'; });
    build();
  }
})();
