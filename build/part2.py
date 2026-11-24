"""2부 — 주판봇의 증명 나무 (Lean은 증명을 어떻게 검사하나).  build/build.py가 부른다 → part2.html
주판봇이 브리핑을 맡는다. 프롤로그 → 1장 블록처럼 쌓인다 → 2장 채점기는 한 줄씩 → 3장 1,700만 줄짜리 나무 → 4장 통과하면 무조건 맞나 → 에필로그
"""
import json, urllib.parse
import build as b
from build import E, talk, react, quiz, kpi, head, nav, cover, scene, labx, face, AUTHOR, DATE, ROOT, SRC, LAB

TITLE2 = "2부 · 주판봇의 증명 나무 — Lean은 증명을 어떻게 검사하나"
STEPS2 = [
    ("p2pro", "프롤로그", "다음 날 아침, 주판봇의 선언"),
    ("p2c1", "1장", "증명은 블록처럼 쌓인다"),
    ("p2c2", "2장", "채점기는 한 줄씩 본다"),
    ("p2c3", "3장", "1,700만 줄짜리 나무"),
    ("p2c4", "4장", "통과했으면 무조건 맞을까"),
    ("p2epi", "에필로그", "주판은 길을 찾을 때 센다"),
]

ZULIP = "https://leanprover-community.github.io/archive/stream/116395-maths/topic/Lean.20Formalization.20of.20the.20Riemann.20Hypothesis.20.E2.80.93.20Open.20for.20Test.html"
MATHLIB_PAPER = "https://arxiv.org/abs/2503.00959"

THREE2 = '''<div class="three"><h2>처음 오신 분께 — 2부를 3줄로</h2><ul>
<li><b>무엇을</b>: 1부에서 "컴퓨터가 1,700만 줄 증명을 한 줄씩 검사했다"고 했죠. 그 채점기(Lean)가 실제로 무엇을 보는지, 오늘은 주판봇이 브리핑합니다.</li>
<li><b>왜 중요한가</b>: 사람이 다 읽을 수 없는 증명을 믿을 수 있는 이유가 여기 있습니다. 그리고 "채점기를 통과했다"만으로는 부족한 이유도요.</li>
<li><b>업무에서는</b>: AI가 만든 결과를 기계로 검사할 때도 같은 두 질문이 남습니다. ① 검사한 문장이 정말 우리가 묻던 문제인가 ② 몰래 넣은 가정은 없는가.</li></ul>
<p>1부를 안 읽었어도 따라올 수 있습니다. 코드는 몰라도 되고, 짧은 예시만 "더 알고 싶은 분" 접기 상자에 있습니다.</p>
<details class="abbr"><summary>2부에 나오는 이름 풀이</summary><dl>
<dt>Lean</dt><dd>증명을 컴퓨터가 한 줄씩 검사하게 하는 프로그램 언어. 여기서는 "증명 채점기"</dd>
<dt>Mathlib</dt><dd>수학자들이 함께 쌓아 온 Lean 정리 모음. 여기서는 "수학 도서관"</dd>
<dt>꼭대기 문장</dt><dd>증명하려는 최종 문장(정리)</dd>
<dt>빈자리</dt><dd>증명을 나중에 채우겠다고 비워 둔 곳. Lean에서는 sorry라고 적는다. 하나라도 있으면 완성된 증명이 아니다</dd>
<dt>검사기 핵심</dt><dd>Lean 안에서 증명을 최종 판정하는 작은 부분(커널). 사람이 믿어야 하는 것은 이 작은 부분이다</dd>
<dt>가정(공리)</dt><dd>증명 없이 받아들이는 출발점. 증명이 어떤 가정에 기대는지 Lean이 목록으로 보여 줄 수 있다</dd></dl></details></div>'''


def flow2(prefix=""):
    return '<div class="flow">' + "".join(f'<a href="{prefix}#{i}"><b>{n}</b>{E(t)}</a>' for i, n, t in STEPS2) + '</div>'


def sh(i):
    sid, n, t = STEPS2[i]
    return f'<span class="roomno">{n}</span><h2>{E(t)}</h2>'


MINITREE = '''<svg class="minitree" viewBox="0 0 560 330" role="img" aria-label="짝수 + 짝수 증명 나무: 꼭대기 문장 아래 다섯 단계의 줄기와 빌려 온 정리 두 개">
<g font-size="14" font-family="inherit">
<line x1="280" y1="300" x2="280" y2="40" stroke="#1e2f6e" stroke-width="6" stroke-linecap="round"/>
<path d="M280,250 Q200,240 120,262" fill="none" stroke="#b9a6e8" stroke-width="3"/><circle cx="120" cy="262" r="7" fill="#8f72d6"/>
<text x="20" y="290" fill="#5a4a9a">빌려 온 것: 짝수의 뜻</text>
<path d="M280,145 Q360,135 440,155" fill="none" stroke="#b9a6e8" stroke-width="3"/><circle cx="440" cy="155" r="7" fill="#8f72d6"/>
<text x="392" y="185" fill="#5a4a9a">빌려 온 것: 분배법칙</text>
<circle cx="280" cy="300" r="8" fill="#1e2f6e"/><text x="296" y="305">1·2  a = 2×m, b = 2×n</text>
<circle cx="280" cy="210" r="8" fill="#1e2f6e"/><text x="296" y="215">3  a+b = 2×m + 2×n</text>
<circle cx="280" cy="125" r="8" fill="#1e2f6e"/><text x="296" y="118">4  = 2×(m+n)</text>
<circle cx="280" cy="40" r="13" fill="#e8731a"/><text x="300" y="45" font-weight="700" fill="#e8731a">꼭대기: 짝수 + 짝수는 짝수</text>
</g></svg>'''


def build_part2():
    s = head(TITLE2, "주판봇이 브리핑하는 2부. Lean 채점기는 증명을 어떻게 검사하나, 1,700만 줄 증명은 왜 나무 모양인가, 통과했으면 무조건 맞을까.", "index")
    s += nav([("#" + i, n) for i, n, _ in STEPS2] + [("briefing.html", "1부"), ("#kg", "색인")])
    s += cover("다음 날 아침 · 주판봇의 첫 브리핑", "cover_part2", "화이트보드 앞에서 주판을 높이 든 주판봇이 브리핑을 시작하고, 하루가 옆에서 안도하며 돕고, 초파리 연구원이 팔짱을 낀 픽셀 그림")
    s += f'''<header class="hero"><div class="wrap"><span class="kicker">연구실 해설 · 수학 특별편 2부</span><h1>{E(TITLE2)}</h1>
<p class="lead">어제는 하루가 리만 가설 소식을 브리핑했습니다. 오늘은 주판봇이 자청했습니다. "1,700만 줄을 한 줄씩 검사한다면서요? 한 줄씩! 그건 제 전문이에요!" 그런데 채점기는 정말 '세는' 기계일까요?</p>
<p class="byline">{AUTHOR} · 기준 시점 {DATE} · <a href="briefing.html">1부 하루의 첫 브리핑</a></p>
{THREE2}<h3>오늘의 흐름</h3>{flow2()}</div></header>'''

    # ---------- 프롤로그
    s += f'''<section class="room" id="p2pro"><div class="wrap">{sh(0)}
{talk([("jupanbot", "e16", "여러분, 주목! <b>오늘 브리핑은 제가 합니다!</b> (주판을 높이 들며)"),
       ("haru", "e12", "정말요? 다행이다… 저는 어제 한 번으로 충분해요. 옆에서 도울게요."),
       ("fruitfly", "e09", "로봇 주제에 주판 들고 브리핑? 또 세기만 하려고?"),
       ("jupanbot", "e16", "어젯밤에 Lean 채점기를 공부했어요. 1,700만 줄을 <b>한 줄씩</b> 검사한다면서요? 한 줄씩이면 결국 세는 거잖아요. 그건 제 전문이에요!"),
       ("sia", "e19", "그러고 보니 어제 누가 보여 준 그림이 있어요. 리만 가설의 Lean 증명을 그린 건데, 보라색 나무처럼 생겼더라고요."),
       ("moa", "e09", "증명이 왜 나무 모양이에요? 그리고 채점기가 통과시키면 무조건 맞는 거예요?"),
       ("doctor", "e08", "좋아요, 주판봇. 오늘 질문은 셋이네요. 채점기는 무엇을 보나, 증명은 왜 나무 모양인가, 통과하면 무조건 맞나. 그리고 하나 더 — 채점기가 정말 '세는' 기계인지는 주판봇이 직접 확인해 보세요."),
       ("jupanbot", "e01", "맡겨 주세요!")])}
{react([("x1", "e04", "주판봇이 브리핑을?!"), ("x2", "e16", "초파리 표정 좀 봐."), ("x3", "e13", "(주판봇에게 물 한 컵)")])}
</div></section>'''

    # ---------- 1장
    s += f'''<section class="room" id="p2c1"><div class="wrap">{sh(1)}
<div class="tags"><span class="tag how">방법: 꼭대기 문장 + 단계 + 빌려 온 정리</span><span class="tag day">일상: 레고 조립 설명서</span></div>
{talk([("jupanbot", "e16", "어제 박사님이 보여 준 증명 기억나요? <b>짝수 + 짝수는 짝수</b>. 이걸 제가 블록으로 쌓아 볼게요."),
       ("jupanbot", "e01", "맨 위에 증명하고 싶은 문장을 놓아요. 이걸 <b>꼭대기 문장</b>이라고 불러요. 그 아래에 한 단계씩 블록을 쌓고요."),
       ("haru", "e07", "중간에 남의 블록도 빌려 써요. '짝수는 2 × 무엇'이라는 뜻이나, 분배법칙 같은 것. 이미 누가 증명해 둔 거라 다시 증명하지 않아요."),
       ("jupanbot", "e16", "자, 세어 볼게요. 따닥! <b>줄기 다섯 단계, 빌려 온 것 두 개!</b>")])}
{MINITREE}
{talk([("sia", "e01", "아, 그림으로 보니까 정말 나무네요! 가운데 줄기가 있고, 옆으로 가지가 나와요."),
       ("doctor", "e07", "맞아요. 빌려 온 정리들은 <b>수학 도서관</b>에 있어요. Lean에서는 Mathlib이라고 부르는데, 전 세계 수학자들이 함께 쌓아 온 정리 모음이에요. 리만 가설이라는 '문장'도 이미 거기 들어 있었어요. 증명만 없었을 뿐이죠."),
       ("moa", "e09", "그럼 증명이 길어지면 블록이 엄청 많아지겠네요.")])}
{labx("레고 조립 설명서", '<p>조립 설명서는 완성품 사진(꼭대기 문장)에서 시작해, 한 단계씩 블록을 끼우는 순서(줄기)를 적고, 이미 조립된 부품(빌려 온 정리)은 "부품 B 사용"이라고만 씁니다. 증명도 같은 방식으로 적습니다.</p>')}
<div class="sum"><b class="t">박사 정리</b> — 증명은 꼭대기 문장을 향해 블록을 한 단계씩 쌓는 일이고, 이미 증명된 정리는 도서관에서 빌려 씁니다. 그래서 어떤 증명이든 그려 보면 줄기 하나에 가지가 붙은 나무 모양이 됩니다.</div>
{quiz("증명에서 '빌려 온 정리'란?", ["아직 증명 안 된 추측", "이미 증명돼 수학 도서관에 있어서 가져다 쓰는 정리", "주판봇이 센 숫자"], 1, "빌려 온 정리는 이미 증명이 끝난 것이라, 다시 증명하지 않고 가져다 씁니다.")}
{talk([("moa", "e09", "그런데요, 채점기는 이 다섯 줄을 어떻게 검사해요? <b>주판봇처럼 세요?</b>"),
       ("jupanbot", "e16", "당연히… 세겠죠? 아마도?")])}
</div></section>'''

    # ---------- 2장
    s += f'''<section class="room" id="p2c2"><div class="wrap">{sh(2)}
{scene("scene_claude", "수학자와 도우미 로봇들이 쌓은 증명 종이를 커다란 증명 채점기가 한 줄씩 받아 초록 체크를 찍는 장면")}
<div class="tags"><span class="tag how">방법: 줄마다 "앞에서 나오나?"</span><span class="tag day">일상: 시험 채점</span></div>
{talk([("jupanbot", "e16", "채점기는 줄 수를 세는 거예요. 다섯 줄이면 다섯!"),
       ("doctor", "e09", "직접 해 보죠. 채점기는 줄마다 딱 하나만 물어요. <b>'이 줄이 앞 줄과 규칙에서 정말 나오나?'</b> 세는 게 아니라 따져 보는 거예요."),
       ("fruitfly", "e16", "줄 하나를 틀리게 바꿔 봐. 채점기가 잡아내나 보자.")])}
<div class="dash" id="pa"><div class="dh"><span class="badge">2장 대시보드</span><h3>채점기 체험 — 짝수 + 짝수는 짝수</h3></div>
<div class="ctrl"><label>꼭대기 문장 <select id="pa-goal"><option value="real">짝수 + 짝수는 짝수다 (원래 질문)</option><option value="easy">a + b = a + b (엉뚱하게 쉬운 문장)</option></select></label></div>
<div class="sub">줄마다 "그대로 / 비워 두기 / 틀린 줄로"를 골라 본 뒤 검사를 누르세요</div>
<div id="pa-lines"></div>
<div class="ctrl"><button id="pa-run">채점기로 검사</button><button id="pa-reset">처음부터</button></div>
<div class="kpis">{kpi("검사한 줄", "pa-checked")}{kpi("통과한 줄", "pa-ok")}{kpi("판정", "pa-verdict")}</div>
<div class="readout" id="pa-msg" aria-live="polite"></div>
<p class="hint">"엉뚱하게 쉬운 문장"은 4장에서 다시 씁니다.</p></div>
{talk([("jupanbot", "e04", "어? 줄을 하나 비웠더니 다섯 줄을 다 '셌는데도' 불합격이에요!"),
       ("haru", "e07", "맞아요. 비워 둔 줄을 <b>빈자리</b>라고 해요. '나중에 채울게요'라고 표시만 한 거죠. 빈자리가 하나라도 있으면 완성된 증명이 아니에요."),
       ("doctor", "e07", "그리고 중요한 점 하나. 1,700만 줄을 사람이 다 믿을 필요는 없어요. 최종 판정은 Lean 안의 <b>작은 검사기 핵심</b>이 내리거든요. 사람은 그 작은 부분이 제대로 만들어졌는지만 믿으면 돼요. 채점 규칙 한 장만 확인하면, 시험지가 1,700만 장이어도 채점을 믿을 수 있는 것과 같아요."),
       ("jupanbot", "e14", "결국… 세는 건 제가 했는데, <b>맞는지 본 건 채점기</b>였네요."),
       ("fruitfly", "e09", "그래, 세는 거랑 따지는 건 달라. 어제부터 내가 하던 말이 그거야.")])}
<div class="solve"><h4>숫자로 한 번 해 보기</h4><p>사람이 1초에 한 줄을 읽고, 그 줄이 맞는지 따지는 데 10초가 더 걸린다고 해 봅시다. 1,700만 줄 × 11초 ÷ (하루 8시간 × 3,600초) ≈ <b>6,490일, 약 18년</b>. 채점기는 이 일을 컴퓨터 시간으로 해냅니다.</p><p>이 숫자는 업무에서 "결과물이 일정 크기를 넘으면, 사람이 다 검토하는 대신 <b>검사 규칙을 믿을 수 있게 만드는 쪽</b>이 현실적"이라는 뜻입니다.</p></div>
<details class="abbr"><summary>더 알고 싶은 분 — Lean으로 쓰면 어떻게 생겼나</summary>
<p>짝수 + 짝수 증명을 Lean 4로 쓰면 대략 이런 모양입니다(설명용으로 줄였습니다).</p>
<pre><code>theorem even_add_even (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by
  obtain ⟨m, rfl⟩ := ha      -- a = m + m
  obtain ⟨n, rfl⟩ := hb      -- b = n + n
  exact ⟨m + n, by ring⟩     -- a + b = (m+n) + (m+n)</code></pre>
<p>Mathlib에서는 짝수를 "m + m"으로 정의합니다(본문의 "2 × m"과 같은 뜻). 마지막 줄의 ring은 "더하기·곱하기 규칙으로 정리해 줘"라는 빌려 온 도구입니다. 한 줄을 sorry(빈자리)로 바꾸면 Lean은 경고를 내고, 완성된 증명으로 인정하지 않습니다.</p></details>
<div class="sum"><b class="t">박사 정리</b> — 채점기는 줄을 세지 않고, 줄마다 "앞에서 나오나?"를 따집니다. 한 줄이라도 빠지거나(빈자리) 틀리면 꼭대기 문장은 통과하지 못합니다. 사람이 믿어야 하는 건 1,700만 줄이 아니라 작은 검사기 핵심 하나입니다.</div>
{quiz("Lean 채점기가 줄마다 확인하는 것은?", ["줄의 개수", "그 줄이 앞 줄과 규칙에서 정말 나오는지", "글씨가 예쁜지"], 1, "채점기는 세는 기계가 아니라 따지는 기계입니다.")}
{talk([("sia", "e19", "그럼 1,700만 줄짜리 증명은 나무가 엄청 크겠네요? <b>어제 본 보라색 그림처럼요.</b>")])}
</div></section>'''

    # ---------- 3장
    s += f'''<section class="room" id="p2c3"><div class="wrap">{sh(3)}
{scene("scene_p2_tree", "거대한 보라빛 증명 나무 앞에서 주판봇이 줄기 단계를 세고, 초파리 연구원이 돋보기로 바닥의 먼지를 살피는 장면")}
<div class="tags"><span class="tag how">방법: 줄기 · 가지 · 먼지</span><span class="tag day">일상: 족보, 회사 조직도</span></div>
{talk([("jupanbot", "e16", "시아가 말한 그림은 리만 가설의 Lean 증명을 그린 거예요. 읽는 법은 세 가지!"),
       ("jupanbot", "e01", "① 가운데 밝은 <b>줄기</b> — 꼭대기 문장 '리만 가설'까지 가는 증명의 뼈대. ② 옆으로 뻗은 <b>가지</b> — 빌려 온 정리들 가운데 일부. ③ 바깥의 흐린 <b>먼지</b> — 끝내 쓰이지 않은 파일들."),
       ("sia", "e19", "근데 잠깐만요. 그거 <b>당연한 모양</b> 아니에요? 아까 짝수 증명도 줄기 하나에 가지 두 개였잖아요."),
       ("doctor", "e16", "바로 그거예요, 시아! 오늘의 핵심을 먼저 말했네요. <b>모양은 모든 증명이 같고, 크기만 다릅니다.</b> 리만 가설 증명이 특별한 건 모양이 아니라 크기, 그리고 160년 동안 아무도 줄기를 끝까지 잇지 못했다는 점이에요."),
       ("fruitfly", "e09", "그럼 그 먼지는 다 뭐야? 줄기보다 훨씬 많던데.")])}
<div class="dash" id="pb"><div class="dh"><span class="badge">3장 대시보드</span><h3>증명 나무 (설명용 모형)</h3></div>
<div class="ctrl"><label>증명 크기 <input type="range" id="pb-size" min="1" max="4" step="1" value="1"></label><label><input type="checkbox" id="pb-dust" checked> 먼지 보기</label><button id="pb-reset">강조 지우기</button></div>
<div class="kpis">{kpi("줄기", "pb-trunk")}{kpi("가지(빌려 온 정리)", "pb-branch")}{kpi("먼지(안 쓰인 파일)", "pb-dustn")}</div>
<svg id="pb-svg" viewBox="0 0 640 520" role="img" aria-label="줄기·가지·먼지로 된 증명 나무 모형. 줄기 점, 가지 끝 점, 먼지 선을 누를 수 있다"></svg>
<div class="readout" id="pb-msg" aria-live="polite"></div>
<p class="hint">실제 증명의 이름·단계 수를 옮긴 것이 아니라, 모양을 보여 주려고 만든 모형입니다. 줄기 점(남색)·가지 끝 점(보라)·먼지 선(회색)을 눌러 보세요.</p></div>
{talk([("jupanbot", "e04", "먼지를 세어 봤는데… 크기 4에서는 줄기보다 다섯 배나 많아요!"),
       ("fruitfly", "e16", "버린 길이 이렇게 많았다고? 클로드도 헛발질 꽤 했네."),
       ("doctor", "e07", "헛발질이 아니에요. <b>먼지는 길을 찾다 버린 시도</b>예요. 1부에서 보조 에이전트들이 계산을 엄청나게 돌렸다고 했죠? 많이 시도하고 많이 세어 봐야 맞는 줄기가 보여요. 그게 세기의 몫이에요."),
       ("jupanbot", "e16", "들었죠, 초파리? 먼지도 제 몫이래요!"),
       ("haru", "e10", "그리고 줄기 점 하나를 눌러 보세요. 그 위가 전부 빨갛게 무너지죠? 줄기는 한 단계만 빠져도 꼭대기까지 못 가요. 2장의 '빈자리 하나면 불합격'이 그림으로 보이는 거예요.")])}
{labx("회사 조직도와 결재선", '<p>결재 문서도 같은 모양입니다. 사장님 결재(꼭대기)까지 올라가는 결재선(줄기)이 있고, 각 단계에서 다른 부서 검토 의견(가지)을 붙이며, 초안 단계에서 버려진 문서들(먼지)이 쌓입니다. 결재선 중간 한 사람이 빠지면 문서는 위로 못 올라갑니다.</p>')}
<div class="sum"><b class="t">박사 정리</b> — 증명을 그리면 줄기(뼈대) · 가지(빌려 온 정리) · 먼지(버린 시도)로 된 나무가 됩니다. 이 모양은 모든 증명이 같고, 리만 가설 증명은 그것을 아주 크게 키운 것입니다. 줄기는 한 단계도 빠질 수 없고, 먼지는 길을 찾는 데 쓴 세기의 흔적입니다.</div>
{quiz("증명 나무에서 '먼지'가 뜻하는 것은?", ["증명의 뼈대", "빌려 온 정리", "길을 찾다 끝내 쓰이지 않은 시도·파일"], 2, "먼지는 최종 증명에 쓰이지 않았지만, 맞는 길을 찾는 과정에서 생긴 흔적입니다.")}
{talk([("fruitfly", "e09", "좋아, 채점기를 통과했다 치자. <b>그럼 무조건 맞는 거야?</b> 채점기를 속일 수는 없어?")])}
</div></section>'''

    # ---------- 4장
    s += f'''<section class="room" id="p2c4"><div class="wrap">{sh(4)}
<div class="tags"><span class="tag how">방법: 꼭대기 문장 확인 + 가정 목록 확인</span><span class="tag day">일상: 계약서 확인</span></div>
{talk([("jupanbot", "e14", "음… 초파리 질문이 날카로워요. 하루, 도와줄래요?"),
       ("haru", "e07", "네! 채점기가 못 보는 게 두 가지 있어요. 2장 대시보드에서 꼭대기 문장을 '엉뚱하게 쉬운 문장'으로 바꿔 봤어요?"),
       ("moa", "e16", "해 봤어요! 'a + b = a + b'는 통과했는데, 그건 원래 질문이 아니었어요."),
       ("haru", "e10", "그게 첫째예요. ① <b>꼭대기 문장이 정말 우리가 묻던 문제인가.</b> 채점기는 적힌 문장을 검사할 뿐, 그게 리만 가설인지는 몰라요."),
       ("doctor", "e08", "둘째는 ② <b>몰래 넣은 가정이 없나.</b> '리만 가설은 참이다'를 가정으로 슬쩍 넣으면, 증명은 한 줄로 끝나고 채점기도 통과시켜요. 그래서 Lean은 증명이 어떤 가정에 기대는지 목록으로 보여 줄 수 있고, 검토자들은 그 목록이 모두가 쓰는 표준 가정뿐인지 확인해요.")])}
<div class="aibox"><h4>AI 판단 코너 — 실제로 있었던 일</h4>
<p>2025년 4월, 한 사람이 Lean 커뮤니티 게시판에 "Lean 4로 리만 가설을 형식화했다"고 올렸습니다. 수학자 데이비드 뢰플러는 바로 "유효한 증명이 아니다"라고 답했습니다. 그 결론은 정리를 증명한 것이 아니라, 정리를 <b>진술만</b> 해 둔 것이었기 때문입니다. "Lean으로 썼다"와 "Lean이 증명을 인정했다"는 전혀 다른 말입니다. (<a href="{ZULIP}">게시판 기록</a>)</p>
<p>반대로 이번 증명은, 증명된 꼭대기 문장이 수학 도서관(Mathlib)에 이미 있던 리만 가설의 공식 문장과 같다는 점까지 확인받았습니다. (<a href="{SRC["lean"]}">Lean·Mathlib 공동 성명</a>, <a href="{MATHLIB_PAPER}">Mathlib의 제타 함수·리만 가설 형식화 논문</a>)</p>
{quiz("어떤 AI가 \"Lean 코드로 리만 가설을 썼으니 증명된 것\"이라고 답했다. 박사가 먼저 물을 질문은?", ["코드가 몇 줄인가?", "꼭대기 문장이 Mathlib의 리만 가설과 같은가, 빈자리나 몰래 넣은 가정은 없는가?", "어떤 컴퓨터로 돌렸나?"], 1, "줄 수나 컴퓨터는 상관없습니다. 무엇을 증명했는지(꼭대기 문장)와 무엇에 기댔는지(가정·빈자리)를 확인해야 합니다.", "2장 대시보드의 '엉뚱하게 쉬운 문장'을 떠올려 보세요.")}</div>
{labx("계약서 확인", '<p>계약서 맞춤법 검사기를 통과했다고 계약이 내게 유리한 건 아닙니다. 확인할 것은 두 가지 — 계약 대상이 정말 내가 사려던 물건인가(꼭대기 문장), 작은 글씨로 넣은 특약은 없나(몰래 넣은 가정).</p>')}
<div class="sum"><b class="t">박사 정리</b> — 채점기는 줄마다 빈틈이 없는지는 확실히 보지만, ① 꼭대기 문장이 정말 묻던 문제인지 ② 몰래 넣은 가정은 없는지는 사람이 확인합니다. 이번 리만 가설 증명은 이 두 가지까지 확인받았기 때문에 큰 소식이 된 거예요. 사람이 '왜 맞는지' 이해하는 일은 1부에서 말한 대로 남아 있습니다.</div>
<div class="limit"><b>이 장의 한계</b> — 검사기 핵심 자체에 결함이 있을 가능성은 아주 작지만 0은 아닙니다. 그래서 수학자들은 Lean 검사와 별도로 사람의 검토·학술지 게재 절차를 함께 거칩니다.</div>
</div></section>'''

    # ---------- 에필로그
    s += f'''<section class="room" id="p2epi"><div class="wrap">{sh(5)}
{scene("scene_reconcile", "주판봇의 주판과 초파리 연구원의 돋보기가 맞닿고, 연구실 식구들이 박수 치는 장면")}
{talk([("jupanbot", "e16", "정리할게요! 채점기는 <b>세지 않고 따진다.</b> 증명은 <b>나무 모양</b>이고 크기만 다르다. 통과해도 <b>꼭대기 문장과 가정</b>은 사람이 확인한다. 이상, 주판봇의 첫 브리핑 끝!"),
       ("doctor", "e16", "훌륭했어요. 처음에 '채점기는 세는 기계'라고 했다가 직접 고친 게 제일 좋았어요. 그게 확인하는 사람의 태도예요."),
       ("fruitfly", "e09", "…주판봇, 오늘은 인정. 근데 채점기가 세는 기계가 아니면, 주판은 이제 왜 들고 다녀?"),
       ("jupanbot", "e01", "채점기는 맞는지 따지고, 주판은 <b>길을 찾을 때</b> 세요. 먼지가 그렇게 많았잖아요. 둘 다 필요하다고 어제 초파리가 그랬고요!"),
       ("fruitfly", "e16", "…내가 그랬지. 주판, 계속 들고 다녀."),
       ("haru", "e12", "휴, 오늘은 제가 안 떨어도 돼서 좋았어요."),
       ("sia", "e01", "다음엔 특별한 점들이 <b>왜</b> 가운데 줄에 서는지 듣고 싶어요!")])}
{react([("x1", "e01", "주판봇 최고!"), ("x2", "e16", "초파리가 인정했다!"), ("x3", "e01", "(주판봇과 초파리에게 박수)")])}
<div class="cards"><a class="card" href="briefing.html">{face("haru", "e10")}<span class="n">1부</span><h3>하루의 첫 브리핑 — 주판봇은 왜 리만 가설을 못 풀었나</h3><p>소수와 '몇 개 중 1개', 세기와 증명, 클로드가 한 일.</p></a>
<div class="card soon">{face("sia", "e19")}<span class="n">다음 편 · 준비 중</span><h3>특별한 점들은 왜 가운데 줄에 설까</h3><p>소수 개수 그래프를 여러 겹의 흔들림으로 나눠 보는 이야기.</p></div></div>
</div></section>'''

    # ---------- 색인
    terms = [("꼭대기 문장", "증명하려는 최종 문장(정리)", "p2c1"),
             ("빌려 온 정리", "이미 증명돼 수학 도서관(Mathlib)에 있어 가져다 쓰는 정리", "p2c1"),
             ("Lean 채점기", "줄마다 '앞에서 나오나?'를 따지는 증명 검사 프로그램", "p2c2"),
             ("빈자리(sorry)", "나중에 채우겠다고 비워 둔 곳. 하나라도 있으면 완성된 증명이 아니다", "p2c2"),
             ("검사기 핵심(커널)", "최종 판정을 내리는 작은 부분. 사람이 믿어야 하는 것은 이것", "p2c2"),
             ("증명 나무", "줄기(뼈대)·가지(빌려 온 정리)·먼지(버린 시도). 모든 증명이 같은 모양", "p2c3"),
             ("진술 확인", "꼭대기 문장이 정말 묻던 문제인지 사람이 확인하는 일", "p2c4"),
             ("가정 목록", "증명이 기대는 가정. 표준 가정뿐인지 확인한다", "p2c4")]
    kg = "".join(f'<div class="kg-item"><span class="t">개념</span><b>{E(a)}</b>{E(c_)}<br><a href="#{d}">본문으로</a></div>' for a, c_, d in terms)
    pack = json.dumps({"title": TITLE2, "author": "안상선", "date": DATE, "version": "1.0", "part": 2,
                       "concepts": [{"name": a, "definition": c_, "anchor": d} for a, c_, d in terms],
                       "order": [t for _, _, t in STEPS2]}, ensure_ascii=False)
    s += f'''<section class="room" id="kg"><div class="wrap"><h2>지식 색인</h2><input class="kg-search" id="kg-q" placeholder="찾을 말 (예: 빈자리)"><div class="kg-list">{kg}</div>
<h3>꾸러미</h3><p>2부의 개념·순서를 JSON으로 내려받아 다른 해설과 이어 쓸 수 있습니다.</p>
<div class="exp-btns"><a class="btn" download="riemann_part2_pack.json" href="data:application/json;charset=utf-8,{urllib.parse.quote(pack)}">꾸러미 내려받기 (JSON)</a></div>
<div class="next"><a href="briefing.html">← 1부로</a><a href="index.html">목차</a><a href="#p2pro">처음부터 다시 ↑</a></div></div></section>'''
    foot = b.FOOT.replace("</p>\n<p class=\"hint\">", f' · <a href="{ZULIP}">Lean 커뮤니티 게시판 기록 (2025-04)</a> · <a href="{MATHLIB_PAPER}">Formalizing zeta and L-functions in Lean (arXiv 2503.00959)</a></p>\n<p class="hint">', 1)
    s += f'''{foot}<script src="assets/rh.js"></script><script src="assets/proof.js"></script></body></html>'''
    (ROOT / "part2.html").write_text(s, encoding="utf-8")
