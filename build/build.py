"""리만 가설 해설 v2.0 — 페이지 생성기.  python3 build/build.py  →  index.html, briefing.html
플롯: 프롤로그(아침 소식·초파리의 주판 놀림) → 1장 뭐가 풀렸나 → 2장 세기와 증명 → 3장 클로드는 무엇을 했나
      → 4장 우리 일에 뭐가 바뀌나 → 에필로그(주판봇과 초파리) → 보너스 대결
"""
import html, json, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
DATE = "2026-11-23"
AUTHOR = '글 · 안상선 (<a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">소개</a>) · (주)M-Robo 대표'
NAME = {"sia": "시아", "moa": "모아", "haru": "하루", "doctor": "박사", "fruitfly": "초파리 연구원", "jupanbot": "주판봇", "x1": "X1", "x2": "X2", "x3": "X3"}
TITLE = "하루의 첫 브리핑 — 주판봇은 왜 리만 가설을 못 풀었나"
LAB = "https://adminmrobo.github.io/"


def face(k, e="e13"):
    return f'<img src="assets/chars/{k}_{e}.webp" alt="{E(NAME[k])}" loading="lazy" width="160" height="160">'


def talk(lines):
    out = []
    for k, e, t in lines:
        r = ' r' if k in ("sia", "moa") else ''
        t = t.replace("<b>", "<strong>").replace("</b>", "</strong>")
        out.append(f'<div class="line{r}">{face(k, e)}<div class="bub"><b>{E(NAME[k])}</b>{t}</div></div>')
    return '<div class="talk">' + "".join(out) + '</div>'


def react(lines):
    return '<div class="react" aria-label="방청석 반응">' + "".join(f'{face(k, e)}<span><b>{NAME[k]}</b> {t}</span>' for k, e, t in lines) + '</div>'


def quiz(q, opts, ok, why, hint="본문을 한 번 더 볼까요?"):
    b = "".join(f'<button data-ok="{1 if i == ok else 0}">{E(o)}</button>' for i, o in enumerate(opts))
    return f'<div class="quiz" data-why="{E(why)}" data-hint="{E(hint)}"><div class="qq">확인 퀴즈 · {E(q)}</div><div class="opts">{b}</div><div class="fb" aria-live="polite"></div></div>'


def kpi(label, id_, val="—"):
    return f'<div class="kpi"><small>{label}</small><b id="{id_}">{val}</b></div>'


def head(title, desc, thumb="index"):
    ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": title, "inLanguage": "ko",
          "author": {"@type": "Person", "name": "안상선", "url": "https://adminmrobo.github.io/who_am_i/who_am_i.html"},
          "educationalLevel": "입문", "dateModified": DATE,
          "about": ["리만 가설", "소수", "확인과 증명", "Lean", "AI와 수학"]}
    return f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="article"><meta property="og:image" content="https://adminmrobo.github.io/riemann_hypothesis_lab/assets/thumbs/{thumb}.webp"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/lab.css"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body><div id="prog"></div>'''


def nav(links):
    a = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top"><div class="row"><a class="logo" href="index.html">하루의 <i>첫 브리핑</i></a><div class="links">{a}</div></div></nav>'


def cover(cap, img, alt):
    if not (ROOT / "assets/img" / f"{img}.webp").exists():
        return f'<div class="cover"><div class="frame"><figure class="scene pending" style="margin:0"><div class="ph" style="aspect-ratio:16/9"><b>표지 그림 준비 중</b><span>{E(alt)}</span><small>{img}.webp</small></div></figure></div></div>'
    return f'''<div class="cover"><div class="frame"><img class="art" src="assets/img/{img}.webp" srcset="assets/img/{img}.webp 1600w, assets/img/{img}@2x.webp 3200w" sizes="(max-width:1100px) 100vw, 1080px" alt="{E(alt)}" width="1600" height="900"><span class="cap">{E(cap)}</span></div></div>'''


def scene(name, alt):
    """그림이 아직 없으면 '그림 준비 중' 자리를 낸다. 파일을 assets/img에 넣고 다시 빌드하면 바로 바뀐다."""
    if not (ROOT / "assets/img" / f"{name}.webp").exists():
        return f'<figure class="scene pending"><div class="ph"><b>그림 준비 중</b><span>{E(alt)}</span><small>{name}.webp</small></div></figure>'
    two = (ROOT / "assets/img" / f"{name}@2x.webp").exists()
    src = f' srcset="assets/img/{name}.webp 1200w, assets/img/{name}@2x.webp 2400w" sizes="(max-width:1000px) 100vw, 960px"' if two else ""
    return f'<figure class="scene"><img src="assets/img/{name}.webp"{src} alt="{E(alt)}" width="1200" height="800" loading="lazy"><figcaption>{E(alt)}</figcaption></figure>'


def labx(title, body):
    return f'<div class="labx"><h4>연구실에서 본 장면 — {title}</h4>{body}</div>'


SRC = {
    "ant": "https://www.anthropic.com/research/riemann-zeta",
    "lean": "https://leanprover-community.github.io/blog/posts/riemann-hypothesis/",
    "sa": "https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/",
}

FOOT = f'''<footer><div class="wrap"><p>{AUTHOR}</p>
<p>숫자는 모두 <code>code/check_riemann.py</code>로 검산했습니다(sympy·mpmath). 소식의 기준 시점은 {DATE}입니다. 학계의 정식 인정 절차는 아직 남아 있습니다.</p>
<p>참고: Riemann(1859) · Schoenfeld(1976) 약속 범위 식 · <a href="{SRC["ant"]}">Anthropic, Learning more about Claude's mathematical capabilities (2026-08-10)</a> · <a href="{SRC["sa"]}">Scientific American, 알포게 발표 기사 (2026-11-20)</a> · <a href="{SRC["lean"]}">Lean·Mathlib 공동 성명 (2026-11-21)</a></p>
<p class="hint">표지·장면 그림: 16비트 픽셀아트(젠스파크 제작, 캐릭터 기준 fruitfly-lab-expressions). 원자료 인포그래픽(사용자 제공)은 그대로 싣지 않고, 틀린 곳을 짚는 데만 참고했습니다.</p></div></footer>'''

STEPS = [
    ("pro", "프롤로그", "아침 연구실에 들어온 소식"),
    ("c1", "1장", "뭐가 풀렸는데? — 소수와 '몇 개 중 1개'"),
    ("c2", "2장", "세기와 증명은 다르다"),
    ("c3", "3장", "클로드는 무엇을 했나"),
    ("c4", "4장", "그래서 우리 일에 뭐가 바뀌나"),
    ("epi", "에필로그", "주판은 왜 들고 다니냐면"),
]


def flow(prefix=""):
    return '<div class="flow">' + "".join(f'<a href="{prefix}#{i}"><b>{n}</b>{E(t)}</a>' for i, n, t in STEPS) + '</div>'


THREE = '''<div class="three"><h2>처음 오신 분께 — 이 페이지를 3줄로</h2><ul>
<li><b>무엇을</b>: 2026년 11월 "수학자와 AI(클로드)가 리만 가설을 증명했다"는 소식이 무슨 뜻인지, 연구실 식구들의 대화로 따라갑니다.</li>
<li><b>왜 중요한가</b>: 리만 가설은 소수가 "어디에 얼마나 있는지"에 대한 160년 넘은 약속입니다. 컴퓨터로 수조 번 확인해도 풀리지 않던 문제를, 처음으로 AI와 함께 찾은 증명을 컴퓨터가 한 줄씩 검사해 통과시켰습니다.</li>
<li><b>업무에서는</b>: "많이 확인했다"와 "증명했다"는 다릅니다. AI가 낸 결과를 볼 때도 같은 질문을 던져야 합니다. 그리고 이 증명으로 인터넷 암호가 뚫리지는 않습니다.</li></ul>
<p>코드·수식을 몰라도 됩니다. 수식은 모두 "더 알고 싶은 분" 접기 상자에 넣었고, 장마다 직접 눌러 보는 대시보드가 있습니다.</p>
<details class="abbr"><summary>이 페이지에 나오는 이름 풀이</summary><dl>
<dt>소수</dt><dd>1과 자기 자신으로만 나눠지는 2 이상의 수 (2, 3, 5, 7, 11 …)</dd>
<dt>리만 가설(RH)</dt><dd>Riemann Hypothesis. 1859년 리만이 낸 질문. 소수 개수 어림이 영원히 크게 빗나가지 않는다는 약속</dd>
<dt>클로드</dt><dd>앤트로픽이 만든 AI 모델의 이름</dd>
<dt>Lean</dt><dd>증명을 한 줄씩 컴퓨터가 검사하게 하는 프로그램 언어. 이 페이지에서는 "증명 채점기"라고 부릅니다</dd>
<dt>보조 에이전트</dt><dd>큰일을 나눠 맡는 AI 여럿. 한 AI가 팀장처럼 일을 나눠 주고 결과를 모읍니다</dd>
<dt>RSA</dt><dd>큰 소수 두 개의 곱을 쓰는 인터넷 자물쇠(암호) 방식의 이름</dd></dl></details></div>'''

CAST = [("haru", "e20", "조수 · 오늘 오후 첫 브리핑을 맡아 긴장 중"), ("doctor", "e08", "박사 · 하루가 막히면 옆에서 거든다"),
        ("jupanbot", "e16", "주판봇 · 세는 건 연구실 최고. 확신파, 늘 주판을 들고 다닌다"), ("fruitfly", "e09", "초파리 연구원 · 확인파. 주판봇을 놀리는 게 취미"),
        ("sia", "e01", "인턴 · 직관파. \"그림으로 보면요?\""), ("moa", "e09", "인턴 · 꼼꼼파. \"그럼 끝까지 맞아요?\""),
        ("x1", "e15", "방청석 · 하루가 걱정됨"), ("x2", "e09", "방청석 · 물 챙겨 주는 담당"), ("x3", "e13", "방청석 · 조용히 응원")]


def cast_grid():
    return '<div class="cast-grid">' + "".join(f'<div class="who">{face(k, e)}<b>{NAME[k]}</b><span>{E(d)}</span></div>' for k, e, d in CAST) + '</div>'


# ------------------------------------------------------------------ 목차
def build_index():
    s = head(TITLE, "AI와 수학자가 리만 가설을 증명했다는 2026년 11월 소식을, 주판봇과 초파리의 말다툼으로 쉽게 풀어 쓴 연구실 해설. 세기와 증명은 무엇이 다른가.")
    s += nav([("briefing.html", "1부 본문"), ("part2.html", "2부"), ("#dash", "대시보드 모음"), ("#cast", "등장인물")])
    s += cover("연구실 회의실 · 하루의 첫 브리핑", "cover_index", "회의실 화이트보드 앞에서 긴장한 하루가 브리핑을 시작하고, 시아·모아와 방청석 X1~X3가 지켜보는 픽셀 그림")
    s += f'''<header class="hero"><div class="wrap"><span class="kicker">연구실 해설 · 수학 특별편 v2.0</span>
<h1>{E(TITLE)}</h1>
<p class="lead">2026년 11월 어느 아침, 주판봇이 소식을 들고 뛰어 들어옵니다. "AI가 리만 가설을 풀었대요! 우리 같은 AI가요!" 초파리 연구원은 코웃음을 칩니다. "넌 로봇 주제에 주판은 왜 들고 다니냐?" 오후 브리핑은 조수 하루가 맡았습니다.</p>
<p class="byline">{AUTHOR} · {DATE}</p><a class="skip" href="briefing.html">이야기 시작하기 →</a></div></header>
<section><div class="wrap">{THREE}</div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2>{cast_grid()}</div></section>
<section><div class="wrap"><h2>오늘의 흐름</h2><p>장 끝에서 누군가 던진 질문에 다음 장이 답합니다.</p>{flow("briefing.html")}</div></section>
<section id="parts"><div class="wrap"><h2>1부 · 2부</h2><div class="cards">
<a class="card" href="briefing.html">{face("haru", "e10")}<span class="n">1부 · 하루의 브리핑</span><h3>주판봇은 왜 리만 가설을 못 풀었나</h3><p>소수와 '몇 개 중 1개', 세기와 증명의 차이, 클로드와 수학자가 한 일, 우리 일에 바뀌는 것.</p></a>
<a class="card" href="part2.html">{face("jupanbot", "e16")}<span class="n">2부 · 주판봇의 브리핑</span><h3>주판봇의 증명 나무 — Lean은 증명을 어떻게 검사하나</h3><p>채점기는 세지 않고 따진다. 증명은 왜 나무 모양인가. 통과했으면 무조건 맞을까.</p></a></div></div></section>
<section id="dash"><div class="wrap"><h2>복습·실험 대시보드</h2><p>본문을 읽은 뒤, 또는 읽기 전에 바로 눌러 봐도 됩니다.</p><div class="cards">
<a class="card" href="briefing.html#d1">{face("jupanbot", "e16")}<span class="n">1장 대시보드 ①</span><h3>주판봇의 체 거르기</h3><p>1~100에서 배수를 지우면 소수만 남습니다. 쪼개기 기계와 소수 감별 퀴즈도.</p></a>
<a class="card" href="briefing.html#d3">{face("moa", "e09")}<span class="n">1장 대시보드 ②</span><h3>소수 세기 관측소</h3><p>100에서 100만까지 소수가 "몇 개 중 1개"로 드물어지는 곡선.</p></a>
<a class="card" href="briefing.html#d5">{face("fruitfly", "e09")}<span class="n">2장 대시보드</span><h3>약속 감시판</h3><p>빗나감이 약속 범위 안에 있는지, 점 하나를 가운데 줄 밖으로 옮기면 어떻게 되는지.</p></a>
<a class="card" href="part2.html#pa">{face("jupanbot", "e04")}<span class="n">2부 대시보드 ①</span><h3>채점기 체험</h3><p>짝수 + 짝수 증명의 줄을 비우거나 틀리게 바꾸고 채점기에 넣어 보기.</p></a>
<a class="card" href="part2.html#pb">{face("fruitfly", "e16")}<span class="n">2부 대시보드 ②</span><h3>증명 나무</h3><p>줄기·가지·먼지. 크기를 키워도 모양은 같다.</p></a>
<a class="card" href="briefing.html#duel">{face("sia", "e19")}<span class="n">보너스</span><h3>소수 개수 맞히기 대결</h3><p>시아의 간단한 어림 vs 모아의 좋은 어림. 주판봇이 직접 세어 판정.</p></a></div></div></section>
{FOOT}<script src="assets/rh.js"></script></body></html>'''
    (ROOT / "index.html").write_text(s, encoding="utf-8")


def step_head(i):
    sid, n, t = STEPS[i]
    return f'<span class="roomno">{n}</span><h2>{E(t)}</h2>'


# ------------------------------------------------------------------ 본문
def build_briefing():
    s = head(TITLE + " | 본문", "프롤로그·4장·에필로그. 소수와 '몇 개 중 1개', 세기와 증명의 차이, 클로드와 수학자가 한 일, 우리 일에 바뀌는 것", "briefing")
    s += nav([("#" + i, n) for i, n, _ in STEPS] + [("#duel", "보너스"), ("part2.html", "2부"), ("#kg", "색인")])
    s += cover("아침 소식 뒤, 오후 브리핑 5분 전", "cover_briefing", "브리핑 5분 전, 긴장한 하루의 어깨를 박사가 두드리고 시아·모아·주판봇이 응원하는 픽셀 그림")
    s += f'''<header class="hero"><div class="wrap"><span class="kicker">본문 · 프롤로그 + 4장 + 에필로그</span><h1>{E(TITLE)}</h1>
<p class="byline">{AUTHOR} · 기준 시점 {DATE}</p>
{THREE}<h3>오늘의 흐름</h3>{flow()}
<p class="hint">처음 보는 말이 많아도 괜찮아요. 등장인물들도 오늘 처음 듣는 이야기라, 모르는 건 서로 물어 가며 갑니다.</p></div></header>'''

    # ---------------- 프롤로그
    s += f'''<section class="room" id="pro"><div class="wrap">{step_head(0)}
{scene("scene_prologue", "아침 연구실 — 소식을 들고 뛰어 들어온 주판봇, 팔짱 끼고 주판을 툭 치는 초파리 연구원, 어리둥절한 시아·모아")}
{talk([("jupanbot", "e16", "큰일 났어요! AI가 리만 가설을 풀었대요! <b>우리 같은 AI가요!</b>"),
       ("fruitfly", "e09", "우리 같은? 주판봇, 넌 로봇 주제에 <b>주판은 왜 들고 다니냐?</b> 그러니까 수학 문제 하나 못 푸는 거 아니야?"),
       ("jupanbot", "e04", "주, 주판은 제 자존심이에요! 세는 건 연구실에서 제가 제일 빠르다고요!"),
       ("fruitfly", "e16", "세기만 빠르면 뭐 해. 그리고 너 8월에도 똑같이 뛰어왔잖아. \"AI가 리만 가설을 풀었대요!\" 하고."),
       ("jupanbot", "e14", "그, 그때는… 절반 조금 넘게 푼 거였죠…"),
       ("sia", "e19", "잠깐만요. 리만 가설이 뭔데요? 그걸 왜 다들 이렇게 난리예요?"),
       ("moa", "e09", "그리고 '절반 넘게 풀었다'는 건 또 무슨 말이에요? 문제를 반만 풀 수도 있어요?"),
       ("doctor", "e08", "좋은 질문들이네요. 마침 잘됐어요. 하루, 오늘 오후에 인턴들 앞에서 이 소식을 브리핑해 볼래요? 막히면 내가 옆에서 거들게요."),
       ("haru", "e20", "네, 네엣! 제가요? …주판봇이랑 초파리가 싸우기 전에 정리해 볼게요!")])}
{react([("x1", "e15", "하루 벌써 손 떨린다…"), ("x2", "e09", "물부터 갖다 놓자."), ("x3", "e13", "(주판봇 쪽을 보며 조용히 위로)")])}
<div class="side"><b>오늘 따라갈 질문 네 개</b><p>① 뭐가 풀렸는데? ② 주판봇이 끝까지 세면 되는 거 아니야? ③ 그럼 클로드는 무엇을 했나? ④ 그래서 우리 일에 뭐가 바뀌나? — 그리고 마지막에, 주판봇이 주판을 들고 다니는 이유.</p></div>
</div></section>'''

    # ---------------- 1장
    s += f'''<section class="room" id="c1"><div class="wrap">{step_head(1)}
{scene("scene_s1", "주판봇이 숫자판을 걸러 소수 타일만 남기는 장면")}
<div class="tags"><span class="tag how">방법: 직접 세기</span><span class="tag day">일상: 레고 블록, 버스 정류장</span></div>
{talk([("haru", "e15", "(화이트보드 앞에서) 그, 그럼 시작할게요. 리만 가설은 <b>소수</b> 이야기예요. 시아, 소수 기억나요?"),
       ("sia", "e01", "1과 자기 자신으로만 나눠지는 수요. 2, 3, 5, 7…"),
       ("haru", "e07", "맞아요. 소수는 숫자의 <b>레고 블록</b>이에요. 12는 2 × 2 × 3으로 쪼개지지만, 7은 더 쪼갤 수 없죠. 모든 수는 이 블록을 곱해서 만들어요."),
       ("moa", "e09", "블록이 왜 그렇게 중요해요?"),
       ("doctor", "e07", "하루 대신 하나만 보탤게요. 여러분이 휴대폰으로 송금할 때 그 돈을 지키는 자물쇠가 <b>큰 소수 두 개</b>로 만들어져요. 그 얘기는 4장에서 다시 해요."),
       ("haru", "e10", "네! 그럼 오늘의 진짜 질문은 이거예요. <b>소수는 어디에, 얼마나 있을까?</b> 주판봇, 세어 줄래요?"),
       ("jupanbot", "e16", "드디어 제 차례! 따닥따닥… 100까지 25개, 1,000까지 168개, 100만까지 <b>78,498개</b>!")])}
<details class="abbr"><summary>모아의 질문 — 1은 왜 소수가 아니에요?</summary><p>1을 블록으로 치면 12 = 2 × 2 × 3 = 1 × 2 × 2 × 3 = 1 × 1 × 2 × 2 × 3 … 처럼 쪼개는 방법이 끝없이 생깁니다. "쪼개는 방법은 한 가지뿐"이라는 규칙을 지키려고 1은 소수에서 뺍니다.</p></details>
{talk([("fruitfly", "e09", "정말 남는 게 다 소수야? 직접 걸러 봐.")])}
<div class="dash" id="d1"><div class="dh"><span class="badge">1장 대시보드 ①</span><h3>주판봇의 체 거르기</h3></div>
<div class="sub">① 배수를 지우면 소수만 남는다</div>
<div class="ctrl" id="d1-sieve"><button data-p="2">2의 배수 지우기</button><button data-p="3">3의 배수</button><button data-p="5">5의 배수</button><button data-p="7">7의 배수</button><button id="d1-reset">처음부터</button></div>
<div class="kpis">{kpi("남은 수(1 제외)", "d1-left")}{kpi("지운 수", "d1-gone")}</div>
<div class="board" id="d1-board" aria-label="1부터 100까지 숫자판"></div>
<div class="readout" id="d1-msg" aria-live="polite"></div>
<div class="sub">② 쪼개기 기계 — 아무 수나 넣어 보세요</div>
<div class="ctrl"><label>수 <input type="number" id="d1-n" value="360" min="2" max="999999"></label></div>
<div class="readout" id="d1-fac" aria-live="polite"></div>
<div class="sub">③ 복습 — 소수일까, 아닐까? (5문제)</div>
<div class="ctrl" id="d1-quiz"><span>이 수는? <b id="d1-qn" class="tn" style="font-size:22px"></b></span><button data-a="p">소수</button><button data-a="n">소수 아님</button><button id="d1-qreset">다시 하기</button></div>
<div class="readout" id="d1-qfb" aria-live="polite"></div></div>
{scene("scene_s3", "갈수록 간격이 멀어지는 버스 정류장 길 앞의 시아·모아·하루")}
{talk([("sia", "e19", "100까지는 4개 중 1개가 소수인데, 100만까지면… 13개 중 1개쯤이네요?"),
       ("haru", "e07", "맞아요. 소수는 <b>끝없이 있지만 갈수록 드물어져요</b>. 시골로 갈수록 버스 정류장 간격이 멀어지는 것처럼요."),
       ("doctor", "e07", "그리고 드물어지는 속도에 <b>규칙</b>이 있어요. 그래서 일일이 세지 않고도 '대략 몇 개'를 아주 잘 맞히는 <b>어림</b>이 있죠. 100만까지 어림하면 78,628개, 실제는 78,498개. 130개, 0.17%만 빗나가요.")])}
<div class="solve"><h4>숫자로 한 번 해 보기</h4><p>100만까지 소수 78,498개 → 1,000,000 ÷ 78,498 ≈ <b>13개 중 1개</b>.</p><p>어림 78,628개와 실제 78,498개의 차이 130개 → 이 숫자는 업무에서 "1,000개를 어림하면 2개쯤만 틀린다"는 뜻입니다.</p></div>
<div class="dash" id="d3"><div class="dh"><span class="badge">1장 대시보드 ②</span><h3>소수 세기 관측소</h3></div>
<div class="ctrl"><label>어디까지 셀까 <input type="range" id="d3-x" min="2" max="6" step="0.05" value="4"> <b id="d3-xv" class="tn"></b></label></div>
<div class="kpis">{kpi("소수 개수", "d3-cnt")}{kpi("비율", "d3-pct")}{kpi("몇 개 중 1개?", "d3-one")}</div>
<svg id="d3-chart" viewBox="0 0 640 230" role="img" aria-label="범위에 따른 소수 비율 곡선"></svg>
<div class="sub">주판봇에게 표 채우게 하기</div>
<div class="ctrl"><button id="d3-count">주판봇, 세어 줘!</button></div>
<div class="tbl"><table><thead><tr><th>어디까지</th><th>소수 개수</th><th>비율</th><th>몇 개 중 1개</th></tr></thead><tbody id="d3-tbl"></tbody></table></div>
<div class="sub">복습 — 개수 맞히기</div>
<div class="ctrl"><span><b id="d3-gx"></b>까지 소수는 몇 개일까?</span><input type="number" id="d3-g" placeholder="내 예상"><button id="d3-gok">확인</button><button id="d3-gnew">다른 문제</button></div>
<div class="readout" id="d3-gfb" aria-live="polite"></div></div>
<details class="abbr"><summary>더 알고 싶은 분 — 어림 공식의 정체</summary><p>x 근처에서 소수가 나올 확률은 대략 "ln x개 중 1개"입니다(ln은 자연로그. 100만이면 약 13.8). 2부터 x까지 이 확률을 차곡차곡 더한 것이 좋은 어림이고, 이름은 로그 적분 li(x)입니다. 가우스가 15살 무렵 소수표를 보며 떠올린 생각에서 나왔습니다. 파이썬으로는 <code>mpmath.li(10**6)</code> 한 줄이면 78,627.5…가 나옵니다.</p></details>
<div class="sum"><b class="t">박사 정리</b> — 소수는 숫자의 블록이고, 끝없이 있지만 갈수록 드물어집니다. 그 드물어지는 규칙 덕분에 어림이 아주 잘 맞습니다. 리만 가설은 바로 이 어림에 대한 이야기예요.</div>
{quiz("소수에 대해 맞는 말은?", ["어느 수부터는 소수가 하나도 없다", "끝없이 있지만 갈수록 드물어진다", "어디서나 같은 비율로 나온다"], 1, "소수는 끝없이 있습니다(2,300년 전 유클리드가 증명). 비율만 천천히 줄어듭니다.")}
{talk([("moa", "e09", "그런데요, 주판봇이 이렇게 빨리 세잖아요. 그럼 주판봇이 <b>끝까지 세면</b> 리만 가설도 끝나는 거 아니에요?"),
       ("jupanbot", "e16", "바로 그거예요! 저한테 시간만 주시면…")])}
</div></section>'''

    # ---------------- 2장
    s += f'''<section class="room" id="c2"><div class="wrap">{step_head(2)}
{scene("scene_s5", "가운데 줄 위에 늘어선 특별한 점들을 초파리 연구원이 돋보기로 살펴보는 장면")}
<div class="tags"><span class="tag how">방법: 확인 vs 증명</span><span class="tag day">일상: 일기예보 "20도 ± 2도"</span></div>
{talk([("fruitfly", "e09", "또 주판이야? '끝까지'가 어디인데? 숫자는 끝이 없잖아. 너 주판알 다 닳아도 못 끝내."),
       ("jupanbot", "e04", "…끝이 없어요?"),
       ("haru", "e07", "초파리 말이 맞아요. 그래서 리만 가설은 '세기'로는 못 끝내요. 리만 가설이 무슨 말인지부터 볼게요."),
       ("haru", "e10", "아까 어림이 130개만 빗나갔죠? 리만 가설은 <b>'어림이 아무리 큰 수까지 가도 크게 빗나가지 않는다'는 약속</b>이에요."),
       ("sia", "e19", "그림으로 보면요?"),
       ("doctor", "e07", "일기예보로 생각해 봐요. '내일 20도'가 어림이고, '± 2도'가 약속한 범위예요. 리만 가설은 소수 개수 어림의 그 ± 범위가 <b>영원히</b> 지켜진다는 주장이에요. 100만에서는 그 범위가 약 550개인데, 실제로는 130개만 빗나갔죠."),
       ("moa", "e09", "지금까지 지켜졌으면 앞으로도 지켜지는 거 아니에요?"),
       ("doctor", "e09", "그게 오늘의 핵심이에요. '지금까지 지켜졌다'는 <b>기록</b>이고, '영원히 지켜진다'는 <b>보증</b>이에요. 기록은 아무리 쌓여도 보증이 되지 않아요.")])}
{labx("머신러닝 시험 점수", f'<p>연구실 해설에서 늘 보던 장면과 같습니다. 머신러닝 모델이 시험 데이터에서 정확도 99%를 받아도, 내일 들어올 데이터에서 99%라는 <b>보장</b>은 아닙니다. 많이 맞혔다는 기록과 언제나 맞는다는 보증은 다른 말이에요. 리만 가설에서 주판봇이 하는 일은 "시험 점수 올리기"이고, 수학자들이 원한 것은 "보증서"였습니다.</p><p class="hint">함께 보기: <a href="{LAB}one_day_machine_learning/">머신러닝 서머리 노트</a></p>')}
<h3>리만은 약속을 그림 하나로 바꿨다</h3>
{talk([("haru", "e07", "1859년에 리만이 이 약속을 그림 하나로 바꿨어요. '약속이 지켜지나?'를 '<b>특별한 점들이 모두 가운데 줄 위에 서 있나?</b>'로요."),
       ("sia", "e01", "점이 줄 위에 서 있으면 약속이 지켜지는 거예요?"),
       ("haru", "e10", "네. 점 하나하나가 어림을 조금씩 흔드는데, 모두 가운데 줄 위에 있으면 흔들림이 약속 범위 안에 머물러요. 한 점이라도 줄 밖에 있으면 언젠가 약속이 깨져요."),
       ("jupanbot", "e16", "그 점이라면 컴퓨터가 <b>수조 개</b>나 확인했어요! 전부 줄 위였다고요!"),
       ("fruitfly", "e09", "그래서, 점이 모두 몇 개인데?"),
       ("jupanbot", "e14", "…끝없이요.")])}
<div class="aibox"><h4>AI 판단 코너 ① — "수조 개 확인했으니 증명 끝?"</h4>
<p>어떤 AI가 이렇게 답했습니다: <i>"특별한 점을 컴퓨터로 수조 개 확인했고 모두 가운데 줄 위에 있으므로, 리만 가설은 이미 증명되었습니다."</i></p>
{quiz("이 AI의 답은?", ["맞다 — 수조 개면 충분하다", "틀리다 — 점은 끝없이 많아서, 아무리 많이 확인해도 '모든 점'의 증명은 아니다", "반쯤 맞다 — 절반은 증명된 셈이다"], 1, "확인은 '지금까지'의 기록이고, 증명은 '끝까지'의 보증입니다. 머신러닝 시험 점수와 같은 이야기예요.", "모아의 질문 '지금까지 지켜졌으면 앞으로도?'를 떠올려 보세요.")}</div>
{talk([("fruitfly", "e16", "한 점만 줄 밖으로 옮기면 어떻게 될까? 아래에서 끌어 봐. 수조 개까지 멀쩡해도 언젠가 깨지는 걸 볼 수 있어.")])}
<div class="dash" id="d5"><div class="dh"><span class="badge">2장 대시보드</span><h3>약속 감시판</h3></div>
<div class="sub">① 실제 빗나감은 약속 범위 안에 있나</div>
<div class="ctrl"><label>어디까지 <input type="range" id="d5-x" min="3.5" max="6" step="0.05" value="6"> <b id="d5-xv" class="tn"></b></label></div>
<div class="kpis">{kpi("실제 빗나감", "d5-miss")}{kpi("약속한 범위", "d5-b")}{kpi("남은 여유", "d5-room")}{kpi("판정", "d5-ok")}</div>
<svg id="d5-chart" viewBox="0 0 640 250" role="img" aria-label="빗나감과 약속 범위"></svg>
<div class="sub">② 가운데 줄 — 첫 점을 옮겨 보기 (설명용 모형)</div>
<div class="ctrl"><label>첫 점의 가로 위치 <input type="range" id="d5-sig" min="0.5" max="0.8" step="0.01" value="0.5"> <b id="d5-sigv"></b></label></div>
<svg id="d5-line" viewBox="0 0 320 300" role="img" aria-label="가운데 줄 위의 특별한 점 10개" style="max-width:360px"></svg>
<div class="readout" id="d5-lmsg" aria-live="polite"></div>
<p class="hint">점의 높이는 실제 값(첫 점 14.13 …)입니다. 옮긴 뒤 "몇 제곱부터 넘는다"는 계산은 크기만 비교한 설명용 모형입니다.</p></div>
<details class="abbr"><summary>더 알고 싶은 분 — 약속 범위 식과 특별한 점의 정체</summary>
<p><b>약속 범위</b> = √x × ln x ÷ (8π). 100만이면 1,000 × 13.8 ÷ 25.1 ≈ 550. 리만 가설이 참이면 x가 2,657 이상일 때 빗나감은 언제나 이 범위 안에 있고, 거꾸로 이 범위가 늘 지켜지면 리만 가설도 참입니다(쇤펠트, 1976). 두 말은 같은 뜻입니다.</p>
<p><b>특별한 점</b>은 제타 함수 ζ(s)가 0이 되는 자리(영점), <b>가운데 줄</b>은 가로 좌표가 1/2인 세로선(임계선)입니다. 제타 함수는 1 + 1/2ˢ + 1/3ˢ + … 에서 출발하고, s = 2이면 π²/6 ≈ 1.6449 — <a href="{LAB}hilbert_space_lab/">힐베르트 공간 해설</a> 5번 방의 그 값입니다.</p></details>
<div class="sum"><b class="t">박사 정리</b> — 주판봇은 '확인'을, 리만 가설은 '증명'을 요구합니다. 리만 가설은 "소수 개수 어림이 영원히 약속 범위 안"이라는 보증이고, 끝없이 많은 점을 하나도 빠짐없이 다뤄야 해서 세기로는 끝나지 않습니다.</div>
{quiz("리만 가설을 한 줄로 말하면?", ["소수는 끝없이 많다", "소수 개수 어림의 빗나감이 영원히 약속 범위 안에 있다", "소수는 모두 홀수다"], 1, "소수가 끝없이 많다는 건 유클리드가 이미 증명했습니다. 리만 가설은 '얼마나 정확히 어림되나'에 대한 약속입니다.")}
{react([("x1", "e04", "주판봇 시무룩해졌어…"), ("x2", "e16", "그래도 확인 기록 덕분에 다들 참이라고 믿어 왔잖아."), ("x3", "e01", "(주판봇에게 엄지 척)")])}
{talk([("sia", "e19", "그럼 이상해요. 끝없는 점을 셀 수 없는데, <b>클로드는 그걸 어떻게 다 확인했어요?</b>")])}
</div></section>'''

    # ---------------- 3장
    s += f'''<section class="room" id="c3"><div class="wrap">{step_head(3)}
{scene("scene_claude", "수학자 한 명과 작은 도우미 로봇 여럿이 증명 종이를 쌓아 올리고, 커다란 증명 채점기가 한 줄씩 초록 체크를 찍는 장면")}
<div class="tags"><span class="tag how">방법: 증명 + 컴퓨터 채점</span><span class="tag day">일상: 시험지 채점</span></div>
{talk([("haru", "e07", "좋은 질문이에요, 시아. 답부터 말하면 클로드는 점을 <b>하나씩 확인한 게 아니에요</b>. 끝없는 점 전부에 한꺼번에 통하는 <b>논리</b>를 찾은 거예요."),
       ("moa", "e09", "한꺼번에요? 그게 어떻게 돼요?"),
       ("doctor", "e07", "이렇게 생각해 봐요. '짝수 + 짝수는 짝수'를 확인하려고 모든 짝수를 더해 볼 필요는 없죠? '짝수는 2 × 무엇'이니까 둘을 더해도 2 × 무엇이다 — 이 한 줄이 끝없는 경우를 한 번에 덮어요. 그게 증명이에요."),
       ("sia", "e01", "아, 세는 게 아니라 '왜 그런지'를 보이는 거네요!"),
       ("haru", "e10", "맞아요. 그럼 무슨 일이 있었는지 순서대로 볼게요.")])}
<ul class="tl">
<li><b>1859년</b> 리만이 질문을 냅니다. 이후 160년 넘게 아무도 증명하지 못했습니다.</li>
<li><b>2004년 무렵</b> 컴퓨터로 특별한 점 10조 개를 확인 — 모두 가운데 줄 위. 그래도 증명은 아닙니다(2장).</li>
<li><b>2026-08-10</b> 앤트로픽 발표: 공개 전 연구용 클로드가 "가운데 줄 위에 있다고 <b>보장</b>되는 점의 비율"을 41.6%에서 67.2%로 올렸습니다. 주판봇이 말한 "절반 조금 넘게"가 이것입니다. 증명은 아니었지만, 이것도 '보증'이었습니다.</li>
<li><b>2026-11-20</b> 앤트로픽 수학자 레벤트 알포게가 "클로드와 함께 리만 가설의 증명을 찾았다고 믿는다"는 4쪽짜리 글을 올렸습니다. 증명은 Lean 코드 약 1,700만 줄로 공개됐습니다.</li>
<li><b>2026-11-21</b> Lean·Mathlib 커뮤니티가 공동 성명으로 "리만 가설의 진술과 증명이 모두 맞다"고 인증했습니다.</li>
</ul>
<p class="hint">기준 시점 {DATE}. 사람 수학자들의 검토와 학술지 게재 같은 정식 인정 절차는 아직 남아 있습니다(4장).</p>
{talk([("jupanbot", "e04", "1,700만 줄이요? 그걸 사람이 어떻게 다 읽어요?"),
       ("haru", "e07", "그래서 <b>Lean</b>이 나와요. Lean은 <b>증명 채점기</b>예요. 증명을 한 줄씩 받아서, 앞 줄에서 정말 다음 줄이 나오는지 컴퓨터가 검사해요. 한 줄이라도 틀리면 통과가 안 돼요."),
       ("moa", "e09", "그럼 사람이 안 읽어도 맞는지는 알 수 있는 거네요?"),
       ("doctor", "e08", "맞아요. 그리고 '진술이 맞다'는 확인도 중요했어요. 엉뚱한 문제를 증명해 놓고 리만 가설이라고 부르면 안 되니까요. Lean 공동 성명은 증명된 문장이 공유 수학 도서관(Mathlib)에 이미 있던 리만 가설 문장과 같다는 것도 확인했어요.")])}
<div class="solve"><h4>숫자로 한 번 해 보기</h4><p>1,700만 줄을 사람이 1초에 한 줄씩, 하루 8시간 읽는다면: 17,000,000 ÷ (8 × 3,600) ≈ <b>590일</b>. 읽기만 해도 1년 반이 넘습니다.</p><p>이 숫자는 업무에서 "이 정도 크기의 결과는 사람이 다 읽는 대신 <b>기계 채점</b>으로 맞는지 확인한다"는 뜻입니다.</p></div>
<h3>그래서 왜 대단한가 — 세 가지</h3>
{talk([("sia", "e19", "결국 클로드가 대단하다는 건 뭐가 대단한 거예요?"),
       ("haru", "e10", "세 가지로 정리할게요. ① <b>160년 넘게</b> 사람이 못 푼 문제예요. ② 사람이 다 읽을 수 없는 크기의 증명을 <b>컴퓨터가 한 줄씩 검사</b>해서 통과시켰어요. ③ AI 혼자가 아니라 <b>수학자와 AI가 함께</b> 찾았어요."),
       ("doctor", "e08", "하나 덧붙이면, 8월 연구 때 클로드는 하루 반 동안 보조 에이전트 약 60개를 팀장처럼 부렸어요. 일을 나눠 주고, 결과를 모으고, 틀린 길은 버리고. 우리 연구실 해설에서 다룬 '에이전트'가 실제 연구에서 일한 장면이죠.")])}
{labx("에이전트와 스스로 고치는 AI", f'<p>보조 에이전트 여럿이 일을 나눠 맡는 구조는 <a href="{LAB}agentic_ai_crash_guide/">AI 에이전트 공식 속성 가이드</a>에서, AI가 연구 자체를 돕기 시작하면 무엇이 달라지는지는 <a href="{LAB}Recursive-Self-Improvement/">스스로 고치는 AI는 어디까지 왔나(RSI 해설)</a>에서 이어 볼 수 있습니다.</p>')}
{talk([("jupanbot", "e14", "결국 저 같은 주판은 필요 없다는 거네요…"),
       ("doctor", "e16", "그렇지 않아요. 8월 발표를 보면 보조 에이전트들은 명령을 2,400번 돌리고 파이썬 계산 코드를 수백 개 썼어요. 길을 찾는 동안 엄청나게 <b>셌다</b>는 뜻이에요. 세기는 증명의 <b>재료</b>예요. 세기만으로 끝나지 않을 뿐이죠."),
       ("jupanbot", "e16", "재료! 들었죠, 초파리? 재료래요!"),
       ("fruitfly", "e09", "…재료는 재료고.")])}
<div class="aibox"><h4>AI 판단 코너 ② — 이 말, 믿어도 될까?</h4>
<p>어떤 AI가 이렇게 답했습니다: <i>"클로드가 리만 가설을 혼자 풀었으니, 이제 수학자는 필요 없습니다."</i></p>
<p>박사의 확인 질문: ① 증명을 발표한 사람은 누구였나? ② 컴퓨터가 검사한 것은 '맞다'인가, '이해했다'인가?</p>
{quiz("이 AI의 답은?", ["맞다 — AI가 풀었으니 끝이다", "틀리다 — 수학자와 함께 찾았고, 증명을 사람이 이해하고 검토하는 일이 남아 있다", "반쯤 맞다 — 쉬운 문제만 수학자가 푼다"], 1, "알포게(사람 수학자)가 클로드와 함께 찾았다고 밝혔고, 컴퓨터는 '맞다'를 검사했을 뿐 '왜 맞는지' 이해하는 일은 이제 시작입니다.", "3장 시간표의 11월 20일을 다시 보세요.")}</div>
<div class="sum"><b class="t">박사 정리</b> — 클로드는 점을 세지 않고, 끝없는 점 전부에 통하는 논리를 수학자와 함께 찾았습니다. 그 논리는 너무 길어서 사람이 다 읽는 대신 Lean이라는 증명 채점기가 한 줄씩 검사했고, 통과했습니다. 그 과정에서 세기는 버려진 게 아니라 재료로 쓰였어요.</div>
{react([("x1", "e04", "증명 채점기라니 신기하다!"), ("x2", "e01", "하루, 이제 목소리 하나도 안 떨려."), ("x3", "e16", "(조용히 메모)")])}
{talk([("jupanbot", "e04", "그런데요… 그럼 이제 세상이 뭐가 바뀌어요? 소수 비밀이 풀렸으니 <b>은행 암호도 다 뚫리는 거</b> 아니에요?")])}
</div></section>'''

    # ---------------- 4장
    s += f'''<section class="room" id="c4"><div class="wrap">{step_head(4)}
{scene("scene_s2", "블록 두 개로 자물쇠를 만들고, 주판봇이 그 자물쇠를 쪼개느라 진땀 빼는 장면")}
<div class="tags"><span class="tag how">방법: 곱하기 vs 되돌리기</span><span class="tag day">일상: 휴대폰 송금, 허가 심사</span></div>
{talk([("haru", "e07", "주판봇, 그건 아니에요. 1장에서 박사님이 말한 자물쇠 기억나요? 인터넷 자물쇠는 <b>큰 소수 두 개를 곱한 수</b>를 공개해요."),
       ("haru", "e10", "곱하기는 쉬워요. 61 × 53 = 3,233은 바로 나오죠. 그런데 '3,233은 어떤 두 소수의 곱?'은 3, 5, 7, 11… 하나씩 나눠 보다가 53에서야 찾아요. 실제 자물쇠는 약 309자리 소수 두 개를 써서, 되돌리기가 사실상 불가능해요."),
       ("moa", "e09", "리만 가설이 증명되면 그 되돌리기가 빨라져요?"),
       ("doctor", "e07", "아니요. 리만 가설은 소수가 '어디에 얼마나 있나'에 대한 약속이지, '곱을 쪼개는 방법'이 아니에요. 자물쇠의 안전은 쪼개기가 어렵다는 데 달려 있고, 그건 그대로예요.")])}
<div class="aibox"><h4>AI 판단 코너 ③ — "리만 가설이 풀렸으니 암호가 뚫린다?"</h4>
{quiz("이 말은?", ["맞다 — 소수의 비밀이 풀렸으니까", "틀리다 — 자물쇠는 '곱을 쪼개기 어렵다'에 달려 있고, 이 증명은 쪼개기를 빠르게 해 주지 않는다", "반쯤 맞다 — 일부 은행만 뚫린다"], 1, "AI 답을 볼 때 '무엇에 달려 있나'를 한 번 더 묻는 습관이 중요합니다.", "자물쇠의 안전이 무엇에 달려 있었는지 떠올려 보세요.")}</div>
{labx("피싱 사이트 탐지", f'<p>자물쇠가 아무리 튼튼해도, 가짜 사이트에 열쇠(비밀번호)를 직접 건네면 소용이 없습니다. 실제 사고는 수학보다 사람을 노리는 쪽에서 더 자주 납니다. <a href="{LAB}catch_phishing/">피싱 사이트 탐지 연구실</a>에서 그 이야기를 이어 볼 수 있습니다.</p>')}
<h3>그럼 무엇이 좋아지나</h3>
{scene("scene_s6", "기초 위에 층이 쌓이는 건물과 잠긴 채 빛나는 자물쇠")}
{talk([("sia", "e19", "암호가 안 뚫리면… 그럼 좋은 점은 뭐예요?"),
       ("haru", "e10", "두 가지예요. ① 소수 개수를 <b>범위까지</b> 말할 수 있어요. '100만까지 78,628개 ± 550개'처럼요. 큰 소수를 찾는 계획을 더 믿을 수 있죠. ② 수학자들이 '리만 가설이 맞다면…'으로 쌓아 둔 결과들이 <b>한꺼번에 확정</b>돼요. 건물 기초가 승인되면 위층도 쓸 수 있는 것처럼요."),
       ("moa", "e09", "그럼 이제 완전히 끝난 거예요? 컴퓨터가 맞다고 했으니까요."),
       ("doctor", "e08", "'맞다'와 '이해했다'는 다른 말이에요. 컴퓨터는 논리가 맞는지 검사했고, 왜 맞는지 사람이 이해하는 일은 이제 시작이에요. 그리고 상금이 걸린 공식 인정은 학술지에 실린 뒤 2년 동안 검토를 더 거쳐야 해요.")])}
{labx("보건통계의 허가 심사", f'<p>신약도 임상시험 숫자가 좋게 나왔다고 바로 팔리지 않습니다. 정해진 심사 절차를 거쳐야 허가가 나죠. 수학의 증명도 "검사 통과"와 "학계의 정식 인정" 사이에 절차가 있습니다. <a href="{LAB}health_stats_lab/">보건통계 연구실</a> 01편과 나란히 읽어 보세요.</p>')}
<div class="sum"><b class="t">박사 정리</b> — 이 증명으로 암호가 뚫리지는 않습니다. 좋아지는 것은 ① 소수 개수를 범위까지 보증할 수 있고 ② 쌓아 둔 수학 결과들이 확정된다는 점입니다. 그리고 '컴퓨터가 맞다고 했다'와 '사람이 이해했다' 사이에는 아직 할 일이 남아 있습니다.</div>
<div class="limit"><b>이 장의 한계</b> — 좋은 점 대부분은 수학 안에서의 이점입니다. 내일 당장 일하는 방식이 바뀌지는 않습니다. 바뀌는 것은 "AI가 연구를 함께 하는 시대가 왔다"는 감각입니다.</div>
{quiz("이번 소식에 대해 맞는 말은?", ["인터넷 암호를 모두 바꿔야 한다", "컴퓨터가 증명을 검사해 통과시켰고, 사람의 이해와 정식 인정 절차는 남아 있다", "리만 가설은 이제 틀린 것으로 밝혀졌다"], 1, "Lean 검사 통과는 큰 걸음이지만, 학계의 정식 인정은 별도의 절차입니다.")}
</div></section>'''

    # ---------------- 에필로그
    s += f'''<section class="room" id="epi"><div class="wrap">{step_head(5)}
{scene("scene_reconcile", "주판봇의 주판과 초파리 연구원의 돋보기가 맞닿고, 둘이 쑥스럽게 웃는 장면")}
{talk([("haru", "e12", "후… 브리핑 끝! 다들 끝까지 들어 줘서 고마워요."),
       ("doctor", "e16", "아주 좋았어요. 오늘의 한 줄 — <b>세기는 '지금까지'를 말하고, 증명은 '끝까지'를 말한다.</b> 리만 가설은 그 차이 때문에 160년이 걸렸어요."),
       ("fruitfly", "e09", "…주판봇. 아침에 한 말 말인데."),
       ("jupanbot", "e14", "'로봇 주제에 주판은 왜 들고 다니냐'요? 괜찮아요, 사실 저도 궁금했어요."),
       ("fruitfly", "e16", "아니, 오늘 보니까 클로드도 엄청 셌더라. 세는 놈이 있어야 의심하는 놈도 뭘 의심할지 알지. 주판, 계속 들고 다녀."),
       ("jupanbot", "e16", "그럼요! 저는 세고, 초파리는 의심하고, 증명은 <b>같이</b> 하는 거죠!"),
       ("sia", "e01", "다음엔 특별한 점들이 <b>왜</b> 가운데 줄에 서는지 듣고 싶어요!"),
       ("moa", "e16", "저는 그 1,700만 줄 중에 딱 한 줄만이라도 읽어 보고 싶어요.")])}
{react([("x1", "e01", "하루 최고!"), ("x2", "e16", "물 마셔, 물!"), ("x3", "e01", "(주판봇과 초파리에게 박수)")])}
{scene("scene_outro", "물컵을 든 하루가 안도하고, 웃는 시아·모아, 꽃가루를 뿌리는 X1~X3")}
<div class="cards"><a class="card" href="part2.html">{face("jupanbot", "e16")}<span class="n">2부 · 이어서 읽기</span><h3>주판봇의 증명 나무</h3><p>다음 날 아침, 이번엔 주판봇이 브리핑합니다. Lean 채점기는 무엇을 보나, 증명은 왜 나무 모양인가.</p></a><div class="card soon">{face("haru", "e19")}<span class="n">다음 편 · 준비 중</span><h3>특별한 점들은 왜 가운데 줄에 설까</h3><p>소수 개수 그래프를 여러 겹의 흔들림으로 나눠 보는 이야기. 힐베르트 공간 해설의 "물결 조각으로 나누기"와 이어집니다.</p></div>
<a class="card" href="{LAB}hilbert_space_lab/">{face("moa", "e09")}<span class="n">함께 보기</span><h3>힐베르트 공간 해설</h3><p>1 + 1/4 + 1/9 + … = π²/6 이 나오는 5번 방.</p></a></div>
</div></section>'''

    # ---------------- 보너스 대결
    s += f'''<section class="room" id="duel"><div class="wrap"><span class="roomno">보너스</span><h2>소수 개수 맞히기 — 시아 vs 모아</h2>
{scene("scene_duel", "시아(계산기)와 모아(눈금 노트)의 대결, 가운데 심판 주판봇과 깃발 든 하루")}
{talk([("haru", "e10", "브리핑 뒤 쉬는 시간 대결! 시아는 간단한 어림, 모아는 좋은 어림. 판정은 주판봇이 직접 세어서!"),
       ("sia", "e19", "간단한 게 최고죠. 나누기 한 번이면 끝!"),
       ("moa", "e09", "저는 '몇 개 중 1개'를 차곡차곡 더할게요."),
       ("jupanbot", "e16", "100만까지는 제가 다 셀 수 있습니다! 주판 덕분에요!")])}
<div class="dash"><div class="dh"><span class="badge">보너스 대시보드</span><h3>네 문제 판정</h3></div>
<div class="ctrl"><label>문제 <select id="du-x"><option value="1000">1,000까지</option><option value="10000">1만까지</option><option value="100000">10만까지</option><option value="1000000">100만까지</option></select></label><button id="du-count">주판봇, 세어서 판정!</button></div>
<div class="kpis">{kpi("시아(간단한 어림)", "du-sia")}{kpi("모아(좋은 어림)", "du-moa")}{kpi("주판봇이 센 실제", "du-real", "?")}{kpi("점수", "du-score", "0/4")}</div>
<div class="readout" id="du-who" aria-live="polite"></div>
<div id="du-end" hidden>{talk([("haru", "e10", "판정! 네 문제 모두 모아의 승리입니다."), ("sia", "e14", "100만에서 6천 개나 틀렸어요…"),
       ("haru", "e07", "시아 방식은 끝자리의 '몇 개 중 1개' 하나로 전체를 계산해서, 소수가 더 촘촘한 작은 수 쪽을 놓쳐요. 모아 방식은 구간마다 바뀌는 비율을 하나씩 더해서 그 차이를 메운 거예요."),
       ("fruitfly", "e16", "판정은 주판이 했네. 인정.")])}</div></div>
</div></section>'''

    # ---------------- 색인
    terms = [("소수", "1과 자기 자신으로만 나눠지는 2 이상의 수. 모든 수의 블록", "c1"),
             ("소수 비율", "어디까지 중 소수가 차지하는 비율. 100만까지 13개 중 1개", "c1"),
             ("어림 공식", "세지 않고 소수 개수를 맞히는 식(li). 100만에서 0.17% 차이", "c1"),
             ("확인과 증명", "확인은 '지금까지'의 기록, 증명은 '끝까지'의 보증", "c2"),
             ("리만 가설", "소수 개수 어림의 빗나감이 영원히 약속 범위 안에 있다는 약속", "c2"),
             ("약속 범위", "√x × ln x ÷ 8π. 100만에서 약 550", "c2"),
             ("특별한 점·가운데 줄", "제타 함수의 영점과 임계선. 모두 줄 위면 약속이 지켜진다", "c2"),
             ("Lean(증명 채점기)", "증명을 컴퓨터가 한 줄씩 검사하게 하는 언어", "c3"),
             ("보조 에이전트", "큰일을 나눠 맡는 여러 AI. 클로드는 약 60개를 부렸다", "c3"),
             ("인터넷 자물쇠(RSA)", "큰 소수 두 개의 곱을 공개하는 암호. 리만 가설 증명과 무관하게 안전", "c4"),
             ("정식 인정 절차", "검사 통과 뒤 사람의 이해·학술지 게재·검토가 남아 있다", "c4")]
    kg = "".join(f'<div class="kg-item"><span class="t">개념</span><b>{E(a)}</b>{E(b)}<br><a href="#{c}">본문으로</a></div>' for a, b, c in terms)
    pack = json.dumps({"title": TITLE, "author": "안상선", "date": DATE, "version": "2.0",
                       "concepts": [{"name": a, "definition": b, "anchor": c} for a, b, c in terms],
                       "order": [t for _, _, t in STEPS]}, ensure_ascii=False)
    s += f'''<section class="room" id="kg"><div class="wrap"><h2>지식 색인</h2><input class="kg-search" id="kg-q" placeholder="찾을 말 (예: 증명)"><div class="kg-list">{kg}</div>
<h3>꾸러미</h3><p>이 페이지의 개념·순서를 JSON으로 내려받아 다른 해설과 이어 쓸 수 있습니다.</p>
<div class="exp-btns"><a class="btn" download="riemann_briefing_pack.json" href="data:application/json;charset=utf-8,{urllib.parse.quote(pack)}">꾸러미 내려받기 (JSON)</a></div>
<div class="next"><a href="index.html">← 목차로</a><a href="#pro">처음부터 다시 ↑</a></div></div></section>
{FOOT}<script src="assets/rh.js"></script></body></html>'''
    (ROOT / "briefing.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    build_briefing()
    import part2
    part2.build_part2()
    print("built index.html, briefing.html, part2.html")


# ── 지식 색인 다시 덧붙이기 (kg/pages/, ai-lab-retrofit autokg) ──
# 빌드가 페이지를 다시 쓰면 덧붙인 #kg가 사라지므로 빌드 끝에서 다시 덧붙인다. kg/reapply.py가 없으면 아무것도 하지 않는다.
if __name__ == "__main__":
    import os as _os, sys as _sys, subprocess as _sp
    _r = _os.path.dirname(_os.path.abspath(__file__))
    for _i in range(3):
        if _os.path.exists(_os.path.join(_r, "kg", "reapply.py")): break
        _r = _os.path.dirname(_r)
    if _os.path.exists(_os.path.join(_r, "kg", "reapply.py")):
        _sp.run([_sys.executable, _os.path.join(_r, "kg", "reapply.py"), _r])
