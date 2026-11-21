/* 리만 가설 입문 — 단계별 복습·실험 대시보드 (외부 라이브러리 없음) */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const NS = 'http://www.w3.org/2000/svg';
  const fmt = (n, d = 0) => Number(n).toLocaleString('ko-KR', { maximumFractionDigits: d, minimumFractionDigits: d });
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const txt = (parent, x, y, s, attrs = {}) => { const t = el('text', Object.assign({ x, y, class: 'svgnote' }, attrs), parent); t.textContent = s; return t; };

  /* ---------- 소수 표 (100만까지, 처음 쓸 때 한 번 만든다) ---------- */
  const N = 1000000;
  let isP = null, piArr = null, primes = null;
  function sieve() {
    if (isP) return;
    isP = new Uint8Array(N + 1).fill(1); isP[0] = isP[1] = 0;
    for (let i = 2; i * i <= N; i++) if (isP[i]) for (let j = i * i; j <= N; j += i) isP[j] = 0;
    piArr = new Int32Array(N + 1); primes = [];
    let c = 0;
    for (let i = 0; i <= N; i++) { if (isP[i]) { c++; primes.push(i); } piArr[i] = c; }
  }
  const pi = x => { sieve(); return piArr[Math.min(N, Math.max(0, Math.floor(x)))]; };
  /* 좋은 어림: li(x) = Ei(ln x) 급수 */
  function li(x) {
    const t = Math.log(x); let s = 0, term = 1;
    for (let k = 1; k < 200; k++) { term *= t / k; s += term / k; if (term / k < 1e-12 * s) break; }
    return 0.5772156649015329 + Math.log(t) + s;
  }
  const simple = x => x / Math.log(x);
  const bound = x => Math.sqrt(x) * Math.log(x) / (8 * Math.PI);
  const isPrimeSmall = n => { if (n < 2) return false; if (n % 2 === 0) return n === 2; for (let d = 3; d * d <= n; d += 2) if (n % d === 0) return false; return true; };
  window.RH = { pi, li, simple, bound };

  /* ---------- 퀴즈 ---------- */
  $$('.quiz').forEach(q => {
    const fb = $('.fb', q);
    $$('button', q).forEach(b => b.addEventListener('click', () => {
      $$('button', q).forEach(x => x.classList.remove('ok', 'no'));
      const good = b.dataset.ok === '1';
      b.classList.add(good ? 'ok' : 'no');
      fb.textContent = good ? '맞았어요! ' + (q.dataset.why || '') : '다시 생각해 볼까요? ' + (q.dataset.hint || '');
    }));
  });

  /* ---------- 탭 ---------- */
  $$('.tabs').forEach(t => {
    const btns = $$('button[data-tab]', t), host = t.parentElement;
    btns.forEach(b => b.addEventListener('click', () => {
      btns.forEach(x => x.classList.toggle('on', x === b));
      $$('.tabpane', host).forEach(p => p.hidden = p.id !== b.dataset.tab);
    }));
  });

  /* =========================================================
     대시보드 1 — 레고 블록: 체 거르기 · 쪼개기 기계 · 소수 맞히기
     ========================================================= */
  (function d1() {
    const board = $('#d1-board'); if (!board) return;
    const cells = [];
    for (let i = 1; i <= 100; i++) { const c = document.createElement('div'); c.className = 'cell'; c.textContent = i; if (i === 1) c.classList.add('one'); board.appendChild(c); cells.push(c); }
    const crossed = new Set();
    const done = new Set();
    function upd() {
      const left = 99 - crossed.size;
      $('#d1-left').textContent = left;
      $('#d1-gone').textContent = crossed.size;
      const all = [2, 3, 5, 7].every(p => done.has(p));
      $('#d1-msg').textContent = all ? '주판봇: 다 걸렀어요! 남은 25개가 100까지의 소수예요. 따닥!' : '주판봇: 버튼을 차례로 눌러 보세요. 남는 수가 소수예요.';
      $('#d1-msg').classList.toggle('alert', all);
    }
    $$('#d1-sieve button[data-p]').forEach(b => b.addEventListener('click', () => {
      const p = +b.dataset.p; done.add(p); b.classList.add('on');
      for (let m = p * 2; m <= 100; m += p) { crossed.add(m); cells[m - 1].classList.add('x'); }
      cells[p - 1].classList.add('p');
      upd();
    }));
    $('#d1-reset').addEventListener('click', () => { crossed.clear(); done.clear(); cells.forEach(c => c.classList.remove('x', 'p')); $$('#d1-sieve button[data-p]').forEach(b => b.classList.remove('on')); upd(); });
    upd();

    const inp = $('#d1-n'), out = $('#d1-fac');
    function factor() {
      let n = Math.floor(+inp.value); if (!(n >= 2 && n <= 999999)) { out.innerHTML = '2 이상 999,999 이하의 수를 넣어 주세요.'; return; }
      const f = []; let m = n;
      for (let d = 2; d * d <= m; d++) while (m % d === 0) { f.push(d); m /= d; }
      if (m > 1) f.push(m);
      out.innerHTML = f.length === 1
        ? `<b>${fmt(n)}</b>은(는) <span class="alert">소수</span>입니다. 더 쪼갤 수 없는 블록이에요.`
        : `<b>${fmt(n)}</b> = ${f.map(x => `<span class="chip">${fmt(x)}</span>`).join(' × ')} <br><span class="hint">블록 ${f.length}개. 순서만 바꿀 수 있고, 다른 블록 조합은 없습니다.</span>`;
    }
    inp.addEventListener('input', factor); factor();

    let score = 0, tries = 0, cur = 0;
    const qn = $('#d1-qn'), qfb = $('#d1-qfb');
    function next() { cur = 2 + Math.floor(Math.random() * 199); qn.textContent = cur; }
    $$('#d1-quiz button[data-a]').forEach(b => b.addEventListener('click', () => {
      if (tries >= 5) return;
      const ans = b.dataset.a === 'p', truth = isPrimeSmall(cur);
      tries++; if (ans === truth) score++;
      qfb.textContent = (ans === truth ? '맞아요! ' : '아쉬워요. ') + (truth ? `${cur}은(는) 소수예요.` : `${cur}은(는) 소수가 아니에요.`) + ` (${score}/${tries})`;
      if (tries >= 5) { qfb.textContent += score >= 4 ? ' — 블록 감별사 합격!' : ' — 쪼개기 기계로 한 번 더 확인해 봐요.'; } else next();
    }));
    $('#d1-qreset').addEventListener('click', () => { score = 0; tries = 0; qfb.textContent = ''; next(); });
    next();
  })();

  /* =========================================================
     대시보드 2 — 쓰임: 자물쇠 · 데이터 서랍 · 매미
     ========================================================= */
  (function d2() {
    if (!$('#d2-lock')) return;
    const dig = $('#d2-dig');
    let p = 0, q = 0;
    const rec = [];
    function randPrime(d) { const lo = Math.pow(10, d - 1), hi = Math.pow(10, d) - 1; for (;;) { const n = lo + Math.floor(Math.random() * (hi - lo)); if (isPrimeSmall(n)) return n; } }
    function pick() { const d = +dig.value; p = randPrime(d); q = randPrime(d); $('#d2-p').textContent = fmt(p); $('#d2-q').textContent = fmt(q); $('#d2-n').textContent = '?'; $('#d2-mul').textContent = '—'; $('#d2-split').textContent = '—'; }
    $('#d2-pick').addEventListener('click', pick);
    dig.addEventListener('change', pick);
    $('#d2-domul').addEventListener('click', () => {
      const n = p * q; $('#d2-n').textContent = fmt(n);
      $('#d2-mul').innerHTML = `<b>곱하기 1번</b>으로 끝 (${String(n).length}자리)`;
    });
    $('#d2-dosplit').addEventListener('click', () => {
      const n = p * q; if (!n) return;
      const t0 = performance.now(); let tries = 1, f = 0;
      if (n % 2 === 0) f = 2; else for (let d = 3; d * d <= n; d += 2) { tries++; if (n % d === 0) { f = d; break; } }
      const ms = performance.now() - t0;
      $('#d2-split').innerHTML = `${fmt(n)}을(를) 작은 수부터 나눠 보기 <b>${fmt(tries)}번</b> 만에 ${fmt(f)} 발견 (${ms.toFixed(1)}ms)`;
      rec.push({ d: +dig.value, tries }); if (rec.length > 8) rec.shift();
      drawRec();
    });
    function drawRec() {
      const s = $('#d2-chart'); s.innerHTML = '';
      const W = 640, H = 200, L = 60, B = 170;
      el('line', { x1: L, y1: B, x2: W - 10, y2: B, stroke: '#9aa5b1' }, s);
      for (let e = 0; e <= 7; e++) { const y = B - e * 20; el('line', { x1: L, y1: y, x2: W - 10, y2: y, stroke: '#eef2f6' }, s); txt(s, 8, y + 4, '10^' + e); }
      const bw = (W - L - 20) / 8;
      rec.forEach((r, i) => {
        const h = Math.max(2, Math.log10(r.tries) * 20);
        el('rect', { x: L + 6 + i * bw, y: B - h, width: bw - 12, height: h, fill: '#e8731a', rx: 3 }, s);
        txt(s, L + 6 + i * bw, B + 18, `소수 ${r.d}자리`);
      });
      txt(s, L, 14, '쪼개기 시도 횟수 (세로는 10배씩 커지는 눈금) — 곱하기는 언제나 1번');
    }
    drawRec(); pick();

    /* 데이터 서랍 */
    const dr = $('#d2-drawers'), st = $('#d2-step');
    function drawers() {
      const m = +dr.value, step = +st.value; $('#d2-drv').textContent = m; $('#d2-stv').textContent = step;
      const keys = Array.from({ length: 20 }, (_, i) => (i + 1) * step);
      const cnt = new Array(m).fill(0); keys.forEach(k => cnt[k % m]++);
      const s = $('#d2-bars'); s.innerHTML = '';
      const W = 640, H = 190, L = 20, B = 160, bw = (W - 2 * L) / m, mx = Math.max(...cnt);
      cnt.forEach((c, i) => {
        const h = c / Math.max(mx, 4) * 120;
        el('rect', { x: L + i * bw + 2, y: B - h, width: bw - 4, height: Math.max(h, 1), fill: c === mx && mx > 2 ? '#c9302c' : '#0f8f84', rx: 2 }, s);
        txt(s, L + i * bw + bw / 2 - 4, B + 16, String(i));
        if (c) txt(s, L + i * bw + bw / 2 - 4, B - h - 4, String(c));
      });
      const empty = cnt.filter(c => c === 0).length;
      $('#d2-dmax').textContent = mx; $('#d2-dempty').textContent = empty;
      const pr = isPrimeSmall(m);
      $('#d2-dprime').textContent = pr ? '소수' : '소수 아님';
      $('#d2-dprime').className = pr ? 'alert' : 'warn';
      $('#d2-dmsg').textContent = mx <= 2 ? '초파리: 고르게 퍼졌네. 서랍 하나에 많아야 ' + mx + '개야.' : '초파리: 서랍 하나에 ' + mx + '개나 몰렸어. 서랍 수를 소수로 바꿔 봐.';
    }
    dr.addEventListener('input', drawers); st.addEventListener('input', drawers); drawers();

    /* 매미 */
    const cy = $('#d2-cy');
    function cicada() {
      const T = +cy.value; $('#d2-cyv').textContent = T;
      const g = (a, b) => b ? g(b, a % b) : a;
      const rows = [2, 3, 4, 5, 6].map(k => [k, T * k / g(T, k)]);
      $('#d2-cyt').innerHTML = rows.map(([k, y]) => `<tr><td>${k}년 주기 천적</td><td class="tn"><b>${y}년</b>마다 만남</td></tr>`).join('');
      const first = Math.min(...rows.map(r => r[1]));
      $('#d2-cymsg').textContent = `가장 자주 만나는 천적과도 ${first}년에 한 번. ` + (isPrimeSmall(T) ? '주기가 소수라 만남이 드물어요.' : '주기가 소수가 아니라 자주 마주쳐요.');
    }
    cy.addEventListener('input', cicada); cicada();
  })();

  /* =========================================================
     대시보드 3 — 뒤로 갈수록 드물어진다
     ========================================================= */
  (function d3() {
    const sl = $('#d3-x'); if (!sl) return;
    function draw() {
      const x = Math.round(Math.pow(10, +sl.value));
      const c = pi(x);
      $('#d3-xv').textContent = fmt(x);
      $('#d3-cnt').textContent = fmt(c);
      $('#d3-pct').textContent = (c / x * 100).toFixed(1) + '%';
      $('#d3-one').textContent = fmt(x / c, 1) + '개 중 1개';
      const s = $('#d3-chart'); s.innerHTML = '';
      const W = 640, H = 230, L = 50, R = 20, T = 20, B = 190;
      const xs = [], ys = [];
      for (let e = 2; e <= 6.0001; e += 0.05) { const xx = Math.pow(10, e); xs.push(e); ys.push(pi(xx) / xx * 100); }
      const X = e => L + (e - 2) / 4 * (W - L - R), Y = v => B - v / 30 * (B - T);
      for (let v = 0; v <= 30; v += 10) { el('line', { x1: L, y1: Y(v), x2: W - R, y2: Y(v), stroke: '#eef2f6' }, s); txt(s, 10, Y(v) + 4, v + '%'); }
      [2, 3, 4, 5, 6].forEach(e => txt(s, X(e) - 16, B + 18, fmt(Math.pow(10, e))));
      el('polyline', { points: xs.map((e, i) => X(e) + ',' + Y(ys[i])).join(' '), fill: 'none', stroke: '#0f8f84', 'stroke-width': 3 }, s);
      const e0 = +sl.value; el('circle', { cx: X(e0), cy: Y(c / x * 100), r: 7, fill: '#e8731a' }, s);
      txt(s, L + 6, T + 4, '어디까지 볼지(가로, 10배씩) — 그중 소수의 비율(세로)');
    }
    sl.addEventListener('input', draw);
    /* 표 채우기 */
    const tb = $('#d3-tbl');
    $('#d3-count').addEventListener('click', () => {
      tb.innerHTML = '';
      [100, 1000, 10000, 100000, 1000000].forEach((x, i) => setTimeout(() => {
        const c = pi(x);
        tb.insertAdjacentHTML('beforeend', `<tr><td class="tn">${fmt(x)}</td><td class="tn"><b>${fmt(c)}</b></td><td class="tn">${(c / x * 100).toFixed(1)}%</td><td class="tn">${fmt(x / c, 1)}개 중 1개</td></tr>`);
      }, i * 350));
    });
    /* 맞혀 보기 */
    let target = 0;
    function newQ() { target = [1000, 10000, 100000, 1000000][Math.floor(Math.random() * 4)]; $('#d3-gx').textContent = fmt(target); $('#d3-gfb').textContent = ''; $('#d3-g').value = ''; }
    $('#d3-gnew').addEventListener('click', newQ);
    $('#d3-gok').addEventListener('click', () => {
      const g = +$('#d3-g').value, a = pi(target);
      if (!g) return;
      const err = Math.abs(g - a) / a * 100;
      $('#d3-gfb').innerHTML = `주판봇이 센 답은 <b>${fmt(a)}개</b>. 예상과 ${err.toFixed(1)}% 차이. ` + (err < 10 ? '꽤 잘 어림했어요!' : '다음 단계의 어림 공식을 쓰면 훨씬 가까워져요.');
    });
    newQ(); draw();
  })();

  /* =========================================================
     대시보드 4 — 어림으로 맞혀 보기
     ========================================================= */
  (function d4() {
    const sl = $('#d4-x'); if (!sl) return;
    const sw = $('#d4-simple');
    function draw() {
      const Xmax = Math.round(Math.pow(10, +sl.value));
      $('#d4-xv').textContent = fmt(Xmax);
      const a = pi(Xmax), g = li(Xmax), s0 = simple(Xmax);
      $('#d4-a').textContent = fmt(a);
      $('#d4-g').textContent = fmt(g);
      $('#d4-s').textContent = fmt(s0);
      $('#d4-dg').textContent = fmt(g - a) + '개 (' + (Math.abs(g - a) / a * 100).toFixed(2) + '%)';
      $('#d4-ds').textContent = fmt(a - s0) + '개 (' + (Math.abs(a - s0) / a * 100).toFixed(2) + '%)';
      const s = $('#d4-chart'); s.innerHTML = '';
      const W = 640, H = 260, L = 64, R = 16, T = 18, B = 220;
      const top = g * 1.08;
      const X = x => L + (x - 2) / (Xmax - 2) * (W - L - R), Y = v => B - v / top * (B - T);
      for (let k = 0; k <= 4; k++) { const v = top * k / 4; el('line', { x1: L, y1: Y(v), x2: W - R, y2: Y(v), stroke: '#eef2f6' }, s); txt(s, 4, Y(v) + 4, fmt(v)); }
      txt(s, L, B + 18, '2'); txt(s, W - R, B + 18, fmt(Xmax), { 'text-anchor': 'end' });
      const n = 260, pa = [], pg = [], ps = [];
      for (let i = 0; i <= n; i++) {
        const x = 2 + (Xmax - 2) * i / n;
        pa.push(X(x) + ',' + Y(pi(x)));
        pg.push(X(x) + ',' + Y(li(Math.max(x, 2.01))));
        if (x > 2.8) ps.push(X(x) + ',' + Y(simple(x)));
      }
      el('polyline', { points: pa.join(' '), fill: 'none', stroke: '#1e2f6e', 'stroke-width': 3 }, s);
      el('polyline', { points: pg.join(' '), fill: 'none', stroke: '#0f8f84', 'stroke-width': 2, 'stroke-dasharray': '7 5' }, s);
      if (sw.checked) el('polyline', { points: ps.join(' '), fill: 'none', stroke: '#e8731a', 'stroke-width': 2, 'stroke-dasharray': '3 4' }, s);
      txt(s, L + 8, T + 6, '— 실제(주판봇)   - - 좋은 어림' + (sw.checked ? '   ··· 간단한 어림' : ''));
    }
    sl.addEventListener('input', draw); sw.addEventListener('change', draw); draw();
  })();

  /* =========================================================
     대시보드 5 — 약속: 빗나감과 약속 범위, 가운데 줄
     ========================================================= */
  (function d5() {
    const sl = $('#d5-x'); if (!sl) return;
    function draw() {
      const Xmax = Math.round(Math.pow(10, +sl.value));
      const a = pi(Xmax), miss = li(Xmax) - a, b = bound(Xmax);
      $('#d5-xv').textContent = fmt(Xmax);
      $('#d5-miss').textContent = fmt(miss) + '개';
      $('#d5-b').textContent = '± ' + fmt(b) + '개';
      $('#d5-room').textContent = (100 - miss / b * 100).toFixed(0) + '%';
      const okk = Math.abs(miss) < b;
      $('#d5-ok').textContent = okk ? '약속 지킴' : '약속 깨짐';
      $('#d5-ok').className = okk ? 'alert' : 'warn';
      const s = $('#d5-chart'); s.innerHTML = '';
      const W = 640, H = 250, L = 56, R = 16, T = 18, B = 210, M = (T + B) / 2;
      const e0 = Math.log10(3000), e1 = Math.log10(Xmax);
      const top = b * 1.15;
      const X = e => L + (e - e0) / Math.max(e1 - e0, 0.01) * (W - L - R), Y = v => M - v / top * (B - T) / 2;
      el('line', { x1: L, y1: M, x2: W - R, y2: M, stroke: '#9aa5b1' }, s);
      const up = [], dn = [], ms = [];
      for (let i = 0; i <= 200; i++) {
        const e = e0 + (e1 - e0) * i / 200, x = Math.pow(10, e);
        up.push(X(e) + ',' + Y(bound(x))); dn.push(X(e) + ',' + Y(-bound(x))); ms.push(X(e) + ',' + Y(li(x) - pi(x)));
      }
      el('polygon', { points: up.concat(dn.reverse()).join(' '), fill: 'rgba(15,143,132,.13)', stroke: '#0f8f84' }, s);
      el('polyline', { points: ms.join(' '), fill: 'none', stroke: '#e8731a', 'stroke-width': 2.5 }, s);
      txt(s, 4, Y(top * 0.85) + 4, '+' + fmt(top * 0.85)); txt(s, 4, M + 4, '0'); txt(s, 4, Y(-top * 0.85) + 4, '−' + fmt(top * 0.85));
      txt(s, L, B + 22, '3,000'); txt(s, W - R, B + 22, fmt(Xmax), { 'text-anchor': 'end' });
      txt(s, L + 6, T + 6, '초록 띠 = 약속한 범위   주황 선 = 실제 빗나간 개수');
    }
    sl.addEventListener('input', draw); draw();

    /* 가운데 줄 — 설명용 모형 */
    const zs = [14.13, 21.02, 25.01, 30.42, 32.94, 37.59, 40.92, 43.33, 48.01, 49.77];
    const sg = $('#d5-sig');
    function line() {
      const sig = +sg.value; $('#d5-sigv').textContent = sig.toFixed(2);
      const s = $('#d5-line'); s.innerHTML = '';
      const W = 320, H = 300, L = 40, R = 20, T = 14, B = 270;
      const X = v => L + v * (W - L - R), Y = h => B - h / 52 * (B - T);
      el('rect', { x: X(0), y: T, width: X(1) - X(0), height: B - T, fill: '#f6f8fa', stroke: '#d5dbe2' }, s);
      el('line', { x1: X(0.5), y1: T, x2: X(0.5), y2: B, stroke: '#0f8f84', 'stroke-width': 3 }, s);
      txt(s, X(0) - 4, B + 18, '0'); txt(s, X(0.5) - 10, B + 18, '1/2'); txt(s, X(1) - 4, B + 18, '1');
      txt(s, X(0.5) + 6, T + 14, '가운데 줄');
      zs.forEach((h, i) => {
        const moved = i === 0 ? sig : 0.5;
        el('circle', { cx: X(moved), cy: Y(h), r: 7, fill: i === 0 && sig > 0.5 ? '#c9302c' : '#e8731a', stroke: '#fff', 'stroke-width': 2 }, s);
      });
      txt(s, X(0) + 2, Y(14.13) + 4, '첫 점 →');
      /* 모형: 줄 위 점이 만드는 흔들림 ~ x^0.5, 옮긴 점 ~ x^sig. 약속 범위 = √x·ln x/(8π) */
      let msg;
      if (sig <= 0.5001) msg = '모든 점이 가운데 줄 위 → 흔들림이 약속 범위 안에 머뭅니다.';
      else {
        /* 모형: 줄 위 점들의 흔들림 크기 ~ √x·ln x, 옮긴 점의 흔들림 ~ x^sig. 옮긴 점이 더 커지는 x(로그 눈금)를 찾는다 */
        let e = 4; while (e < 5000 && (sig - 0.5) * e * Math.LN10 <= Math.log(e * Math.LN10)) e += 1;
        msg = `점 하나가 줄에서 ${(sig - 0.5).toFixed(2)}만큼 벗어남 → 그 점의 흔들림이 결국 약속 범위를 넘습니다. 이 모형으로 어림하면 10의 ${e}제곱쯤부터.` + (e > 15 ? ' 1,000조까지 확인해도 멀쩡해 보이지만, 언젠가는 깨집니다.' : ' 많이 벗어날수록 더 일찍 깨집니다.');
      }
      $('#d5-lmsg').textContent = msg;
      $('#d5-lmsg').className = sig <= 0.5001 ? 'readout alert' : 'readout warnbox';
    }
    sg.addEventListener('input', line); line();
  })();

  /* =========================================================
     대시보드 6 — 약속이 지켜지면 좋은 점
     ========================================================= */
  (function d6() {
    const xi = $('#d6-x'); if (!xi) return;
    function calc() {
      const x = Math.floor(+xi.value);
      if (!(x >= 2657 && x <= 1e15)) { $('#d6-out').innerHTML = '2,657 이상 1,000조 이하의 수를 넣어 주세요. (약속 범위 식은 2,657부터 씁니다)'; return; }
      const g = li(x), b = bound(x);
      let h = `${fmt(x)}까지 소수는 <b>${fmt(g)}개 안팎</b>, 많아야 ± <b>${fmt(b)}개</b> 빗나갑니다.<br>즉 <b>${fmt(g - b)} ~ ${fmt(g + b)}개</b> 사이.`;
      if (x <= N) { const a = pi(x); h += `<br>주판봇이 직접 센 값: <b>${fmt(a)}개</b> → ${a > g - b && a < g + b ? '<span class="alert">범위 안</span>' : '<span class="warn">범위 밖</span>'}`; }
      else h += '<br><span class="hint">100만을 넘는 수는 이 페이지에서 직접 세지 않고 범위만 보여 줍니다.</span>';
      $('#d6-out').innerHTML = h;
    }
    xi.addEventListener('input', calc); calc();

    const gx = $('#d6-gx');
    function gap() {
      sieve();
      const x = Math.round(Math.pow(10, +gx.value));
      let i = piArr[Math.min(x, N - 200)]; const pnext = primes[i] || primes[primes.length - 1], pprev = primes[i - 1] || 2;
      $('#d6-gxv').textContent = fmt(x);
      $('#d6-gp').textContent = `${fmt(pprev)} 다음 소수는 ${fmt(pnext)} (간격 ${pnext - pprev})`;
      let mg = 0, at = 2; const recs = [];
      for (let k = 1; k < primes.length && primes[k] <= x; k++) { const d = primes[k] - primes[k - 1]; if (d > mg) { mg = d; at = primes[k - 1]; recs.push([at, d]); } }
      $('#d6-gmax').textContent = `${fmt(x)}까지 가장 큰 간격: ${mg} (${fmt(at)} 다음)`;
      const s = $('#d6-gchart'); s.innerHTML = '';
      const W = 640, H = 200, L = 46, R = 14, T = 16, B = 170;
      const e1 = Math.max(Math.log10(x), 1.2), X = v => L + Math.log10(Math.max(v, 2)) / e1 * (W - L - R), Y = d => B - d / 120 * (B - T);
      for (let d = 0; d <= 120; d += 40) { el('line', { x1: L, y1: Y(d), x2: W - R, y2: Y(d), stroke: '#eef2f6' }, s); txt(s, 8, Y(d) + 4, String(d)); }
      recs.forEach(([p, d]) => el('rect', { x: X(p) - 2, y: Y(d), width: 4, height: B - Y(d), fill: '#1e2f6e' }, s));
      txt(s, L + 6, T + 4, '막대 = 지금까지 가장 큰 간격이 나온 자리 (가로는 10배씩 커지는 눈금)');
    }
    gx.addEventListener('input', gap);

    const bits = $('#d6-bits');
    function plan() {
      const b = +bits.value; const one = b * Math.LN2; const odd = one / 2;
      $('#d6-bv').textContent = b;
      $('#d6-dig').textContent = Math.floor(b * Math.log10(2)) + 1 + '자리';
      $('#d6-one').textContent = fmt(one) + '개 중 1개';
      $('#d6-odd').textContent = '평균 ' + fmt(odd) + '번';
      $('#d6-pmsg').textContent = `자물쇠용 소수(${Math.floor(b * Math.log10(2)) + 1}자리)를 찾을 때 홀수를 평균 ${fmt(odd)}번쯤 검사하면 하나가 나온다고 계획할 수 있어요. 이 "몇 개 중 1개"가 4단계의 어림 공식입니다.`;
    }
    bits.addEventListener('input', plan); plan();
    let gapDrawn = false;
    $$('button[data-tab="d6-t2"]').forEach(b => b.addEventListener('click', () => { if (!gapDrawn) { gap(); gapDrawn = true; } }));
    if (!$('#d6-t2').hidden) gap();
  })();

  /* =========================================================
     대결 — 소수 개수 맞히기
     ========================================================= */
  (function duel() {
    const sel = $('#du-x'); if (!sel) return;
    const res = {};
    function show() {
      const x = +sel.value;
      $('#du-sia').textContent = fmt(simple(x));
      $('#du-moa').textContent = fmt(li(x));
      $('#du-real').textContent = '?';
      $('#du-who').textContent = '';
    }
    $('#du-count').addEventListener('click', () => {
      const x = +sel.value, a = pi(x), ds = Math.abs(simple(x) - a), dm = Math.abs(li(x) - a);
      $('#du-real').textContent = fmt(a);
      const w = dm < ds ? '모아' : '시아';
      res[x] = w;
      $('#du-who').innerHTML = `시아 빗나감 ${fmt(ds)}개, 모아 빗나감 ${fmt(dm)}개 → <b>${w} 승</b>`;
      const done = Object.keys(res).length;
      $('#du-score').textContent = `판정한 문제 ${done}/4 · 모아 ${Object.values(res).filter(v => v === '모아').length}승`;
      if (done === 4) $('#du-end').hidden = false;
    });
    sel.addEventListener('change', show); show();
  })();

  /* ---------- 진행 막대 ---------- */
  const prog = $('#prog');
  if (prog) addEventListener('scroll', () => { const h = document.documentElement; prog.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight) * 100) + '%'; }, { passive: true });

  /* ---------- 지식 색인 검색 ---------- */
  const ks = $('#kg-q');
  if (ks) ks.addEventListener('input', () => { const v = ks.value.trim(); $$('.kg-item').forEach(k => k.hidden = v && !k.textContent.includes(v)); });
})();
