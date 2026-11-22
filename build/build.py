"""리만 가설 입문 — 페이지 생성기.  python3 build/build.py  →  index.html, briefing.html"""
import html, json, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
AUTHOR = '글 · 안상선 (<a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">소개</a>) · (주)M-Robo 대표'
NAME = {"sia": "시아", "moa": "모아", "haru": "하루", "doctor": "박사", "fruitfly": "초파리 연구원", "jupanbot": "주판봇", "x1": "X1", "x2": "X2", "x3": "X3"}


def face(k, e="e13", size=None):
    return f'<img src="assets/chars/{k}_{e}.webp" alt="{E(NAME[k])}" loading="lazy" width="160" height="160">'


def talk(lines):
    out = []
    for i, (k, e, t) in enumerate(lines):
        r = ' r' if k in ("sia", "moa") else ''
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
          "author": {"@type": "Person", "name": "안상선"}, "educationalLevel": "입문", "dateModified": "2026-11-22",
          "about": ["리만 가설", "소수", "소수 개수 어림", "인터넷 암호"]}
    return f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="article"><meta property="og:image" content="https://adminmrobo.github.io/riemann_hypothesis_lab/assets/thumbs/{thumb}.webp"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/lab.css"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body><div id="prog"></div>'''


def nav(links):
    a = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top"><div class="row"><a class="logo" href="index.html">하루의 <i>첫 브리핑</i></a><div class="links">{a}</div></div></nav>'


def cover(cap, img, alt):
    return f'''<div class="cover"><div class="frame"><img class="art" src="assets/img/{img}.webp" alt="{E(alt)}" width="1600" height="900"><span class="cap">{E(cap)}</span></div></div>'''


def scene(name, alt):
    return f'<figure class="scene"><img src="assets/img/{name}.webp" alt="{E(alt)}" width="1200" height="800" loading="lazy"><figcaption>{E(alt)}</figcaption></figure>'


FOOT = f'''<footer><div class="wrap"><p>{AUTHOR}</p>
<p>숫자는 모두 <code>code/check_riemann.py</code>로 검산했습니다(sympy·mpmath). 소식의 기준 시점은 2026-11-22입니다.</p>
<p>참고: Riemann(1859) · Schoenfeld(1976) 약속 범위 식 · Cramér(1920) 소수 간격 · <a href="https://www.anthropic.com/research/riemann-zeta">Anthropic, Learning more about Claude's mathematical capabilities (2026-08-10)</a> · <a href="https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/">Scientific American, 알포게 발표 기사 (2026-11-20)</a> · Lean FRO·Mathlib 공동 성명(2026-11-21, 보도로 확인 — 원문 링크는 확인 후 추가)</p>
<p class="hint">표지·장면 그림: 16비트 픽셀아트(젠스파크 제작, 캐릭터 기준 fruitfly-lab-expressions). 원자료 인포그래픽(사용자 제공)은 그대로 싣지 않고, 틀린 곳을 짚는 데만 참고했습니다.</p></div></footer>'''

STEPS = [
    ("s1", "1단계", "소수는 숫자의 레고 블록"),
    ("s2", "2단계", "소수는 어디에 쓰이나"),
    ("s3", "3단계", "뒤로 갈수록 드물어진다"),
    ("s4", "4단계", "어림으로 맞혀 보기"),
    ("s5", "5단계", "리만 가설 = 약속"),
    ("s6", "6단계", "약속이 지켜지면 좋은 점"),
]


def flow(prefix=""):
    return '<div class="flow">' + "".join(f'<a href="{prefix}#{i}"><b>{n}</b>{E(t)}</a>' for i, n, t in STEPS) + '</div>'


THREE = '''<div class="three"><h2>처음 오신 분께 — 이 페이지를 3줄로</h2><ul>
<li><b>무엇을</b>: 소수가 왜 중요한지 보고, 소수가 몇 개인지 어림으로 맞혀 봅니다.</li>
<li><b>왜 중요한가</b>: 소수는 모든 수를 만드는 블록이고, 인터넷 결제·메신저를 지키는 자물쇠의 재료입니다. 리만 가설은 소수가 "어디에 얼마나 있는지"에 대한 약속입니다.</li>
<li><b>업무에서는</b>: 암호를 만들 때 큰 소수를 찾고, 데이터를 서랍에 고르게 나눌 때도 소수를 씁니다. 리만 가설이 증명됐다고 암호가 뚫리지는 않습니다.</li></ul>
<p>코드·수식을 몰라도 됩니다. 단계마다 직접 눌러 보는 <b>복습·실험 대시보드</b>가 있습니다.</p>
<details class="abbr"><summary>더 알고 싶은 분 — 이 페이지에 나오는 이름 풀이</summary><dl>
<dt>소수</dt><dd>1과 자기 자신으로만 나눠지는 2 이상의 수 (2, 3, 5, 7, 11 …)</dd>
<dt>어림 공식</dt><dd>원래 이름은 로그 적분 li(x). 가우스가 15살 무렵 소수표를 보며 떠올린 생각에서 나왔습니다.</dd>
<dt>RH</dt><dd>Riemann Hypothesis, 리만 가설. 1859년 리만이 낸 질문</dd>
<dt>Lean</dt><dd>증명을 한 줄씩 컴퓨터가 검사하게 하는 프로그램 언어</dd>
<dt>RSA</dt><dd>큰 소수 두 개의 곱을 쓰는 인터넷 자물쇠(암호) 방식의 이름</dd></dl></details></div>'''

CAST = [("sia", "e01", "인턴 · 직관파. \"그림으로 보면요?\""), ("moa", "e09", "인턴 · 꼼꼼파. \"그럼 끝까지 맞아요?\""),
        ("haru", "e20", "조수 · 오늘 첫 브리핑을 맡아 긴장 중"), ("doctor", "e08", "박사 · 단계마다 정리"),
        ("fruitfly", "e09", "초파리 연구원 · \"이걸 눌러 봐\""), ("jupanbot", "e16", "주판봇 · 소수 세기 담당, 가끔 성급함"),
        ("x1", "e15", "방청석 · 하루가 걱정됨"), ("x2", "e09", "방청석 · 물 챙겨 주는 담당"), ("x3", "e13", "방청석 · 조용히 응원")]


def cast_grid():
    return '<div class="cast-grid">' + "".join(f'<div class="who">{face(k, e)}<b>{NAME[k]}</b><span>{E(d)}</span></div>' for k, e, d in CAST) + '</div>'


# ------------------------------------------------------------------ 목차
def build_index():
    s = head("하루의 첫 브리핑 — 리만 가설은 '약속'이다", "소수가 왜 중요한지, 소수 개수를 어떻게 어림하는지, 리만 가설이 어떤 약속인지 처음 오신 분을 위해 풀어 쓴 연구실 해설")
    s += nav([("briefing.html", "본문"), ("#dash", "대시보드 모음"), ("#cast", "등장인물")])
    s += cover("연구실 회의실 · 하루의 첫 브리핑", "cover_index", "회의실 화이트보드 앞에서 긴장한 하루가 브리핑을 시작하고, 시아·모아와 방청석 X1~X3가 지켜보는 픽셀 그림")
    s += f'''<header class="hero"><div class="wrap"><span class="kicker">연구실 해설 · 수학 특별편</span>
<h1>하루의 첫 브리핑 — 리만 가설은 '약속'이다</h1>
<p class="lead">2026년 11월, "리만 가설이 증명됐다"는 소식이 연구실에 들어왔습니다. 박사는 조수 하루에게 인턴들 앞에서 브리핑을 맡겼습니다. 하루는 떨리는 목소리로 시작합니다.</p>
<p class="byline">{AUTHOR} · 2026-11-22</p><a class="skip" href="briefing.html">브리핑 시작하기 →</a></div></header>
<section><div class="wrap">{THREE}</div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2>{cast_grid()}</div></section>
<section><div class="wrap"><h2>오늘의 흐름</h2><p>앞 단계에서 생긴 궁금증이 다음 단계의 질문이 됩니다.</p>{flow("briefing.html")}</div></section>
<section id="dash"><div class="wrap"><h2>단계별 복습·실험 대시보드</h2><p>본문을 읽은 뒤, 또는 읽기 전에 바로 눌러 봐도 됩니다.</p><div class="cards">
<a class="card" href="briefing.html#d1">{face("jupanbot", "e16")}<span class="n">1단계 대시보드</span><h3>블록 쪼개기 공방</h3><p>1~100 체 거르기, 아무 수나 소수 블록으로 쪼개기, 소수 감별 퀴즈 5문제.</p></a>
<a class="card" href="briefing.html#d2">{face("haru", "e07")}<span class="n">2단계 대시보드</span><h3>자물쇠·서랍·매미 실험실</h3><p>곱하기 1번 vs 쪼개기 수천 번, 서랍 수를 소수로 바꾸면 고르게 퍼지는지.</p></a>
<a class="card" href="briefing.html#d3">{face("moa", "e09")}<span class="n">3단계 대시보드</span><h3>소수 세기 관측소</h3><p>100에서 100만까지 소수 비율이 줄어드는 곡선, 개수 맞히기 게임.</p></a>
<a class="card" href="briefing.html#d4">{face("sia", "e19")}<span class="n">4단계 대시보드</span><h3>어림 비교판</h3><p>실제 개수와 두 가지 어림을 한 그래프에. 차이가 몇 %인지 바로.</p></a>
<a class="card" href="briefing.html#d5">{face("fruitfly", "e09")}<span class="n">5단계 대시보드</span><h3>약속 감시판</h3><p>빗나감이 약속한 범위 안에 있는지, 점 하나를 가운데 줄 밖으로 옮기면 어떻게 되는지.</p></a>
<a class="card" href="briefing.html#d6">{face("doctor", "e08")}<span class="n">6단계 대시보드</span><h3>약속 활용 센터</h3><p>개수 범위 계산기, 소수 간격 탐험, 자물쇠용 소수 찾기 계획기.</p></a>
<a class="card" href="briefing.html#duel">{face("haru", "e10")}<span class="n">대결</span><h3>소수 개수 맞히기</h3><p>시아의 간단한 어림 vs 모아의 좋은 어림. 주판봇이 직접 세어 판정.</p></a></div></div></section>
{FOOT}<script src="assets/rh.js"></script></body></html>'''
    (ROOT / "index.html").write_text(s, encoding="utf-8")


# ------------------------------------------------------------------ 본문
def step_head(i):
    sid, n, t = STEPS[i]
    return f'<span class="roomno">{n}</span><h2>{E(t)}</h2>'


def build_briefing():
    s = head("하루의 첫 브리핑 — 본문 | 리만 가설은 '약속'이다", "소수 블록, 소수의 쓰임, 소수 개수 어림, 리만 가설이라는 약속, 약속이 지켜지면 좋은 점 — 단계마다 복습·실험 대시보드", "briefing")
    s += nav([("#" + i, n) for i, n, _ in STEPS] + [("#duel", "대결"), ("#kg", "색인")])
    s += cover("회의실 화이트보드 앞 · 브리핑 시작 5분 전", "cover_briefing", "브리핑 5분 전, 긴장한 하루의 어깨를 박사가 두드리고 시아·모아·주판봇이 응원하는 픽셀 그림")
    s += f'''<header class="hero"><div class="wrap"><span class="kicker">본문 · 6단계 + 대결</span><h1>하루의 첫 브리핑</h1>
<p class="byline">{AUTHOR} · 기준 시점 2026-11-22</p>
{talk([("doctor", "e08", "리만 가설이 증명됐다는 소식, 다들 들었죠? 오늘은 하루가 인턴들에게 설명해 볼 거예요."),
       ("haru", "e20", "네, 네엣! 제, 제가요? …열심히 하겠습니다!"),
       ("sia", "e19", "하루 선배 브리핑이다! 리만 가설이 뭔지 진짜 궁금했어요."),
       ("moa", "e09", "저는 그게 왜 그렇게 대단한 일인지부터 알고 싶어요.")])}
{react([("x1", "e15", "하루 손 떨리는 거 보여…"), ("x2", "e09", "물 한 잔 갖다 둘까?"), ("x3", "e13", "(조용히 엄지 척)")])}
{THREE}<h3>오늘의 흐름</h3>{flow()}
<p class="hint">여기서 한 번 멈춰도 괜찮아요. 처음 보는 말이 많아도, 단계마다 대시보드를 눌러 보면 손에 잡힙니다.</p></div></header>'''

    # ---------------- 1단계
    s += f'''<section class="room" id="s1"><div class="wrap">{step_head(0)}
{scene("scene_s1", "주판봇이 숫자판을 걸러 소수 타일만 남기는 장면")}
<div class="tags"><span class="tag how">방법: 나눠 보기</span><span class="tag day">일상: 레고 블록</span></div>
{talk([("doctor", "e07", "택배 상자를 똑같은 크기의 작은 상자 여러 개로 나눌 수 없다면, 그게 가장 작은 블록이에요. 숫자에도 그런 블록이 있어요."),
       ("sia", "e01", "하루 선배, 소수가 정확히 뭐예요?"),
       ("haru", "e15", "소, 소수는… 1과 자기 자신으로만 나눠지는 수입니다! 2, 3, 5, 7, 11처럼요."),
       ("moa", "e09", "그럼 12는요?"),
       ("haru", "e07", "12는 2 × 2 × 3으로 쪼개져요. 쪼갤 수 있으니 소수가 아니고, 쪼개고 남은 2와 3이 블록이에요.")])}
<div class="pair"><div class="box"><h4>일상으로 치면</h4><p>레고로 무엇을 만들든 결국 기본 블록 몇 종류의 조합입니다. 숫자도 모두 소수 블록을 곱해 만듭니다.</p></div>
<div class="box ml"><h4>왜 블록이 중요한가</h4><p>어떤 수든 소수로 쪼개는 방법은 <b>딱 한 가지</b>뿐입니다(순서만 바뀔 뿐). 그래서 소수 조합은 그 수의 <b>지문</b>입니다.</p></div></div>
<div class="side"><b>모아의 질문 — 1은 왜 소수가 아니에요?</b><p>1을 블록으로 치면 12 = 2 × 2 × 3 = 1 × 2 × 2 × 3 = 1 × 1 × 2 × 2 × 3 … 처럼 쪼개는 방법이 끝없이 생깁니다. "쪼개는 방법은 한 가지뿐"이라는 규칙을 지키려고 1은 소수에서 뺍니다.</p></div>
<div class="solve"><h4>숫자로 한 번 해 보기</h4><p>12 = 2 × 2 × 3, 30 = 2 × 3 × 5, 97 = 97(더 쪼갤 수 없음 → 소수)</p><p>30까지 소수는 2, 3, 5, 7, 11, 13, 17, 19, 23, 29 — 모두 10개입니다.</p></div>
{talk([("jupanbot", "e16", "100까지는 제가 주판으로 걸러 볼게요! 2의 배수, 3의 배수… 지우고 남는 게 소수예요."),
       ("fruitfly", "e09", "정말 남는 게 다 소수일까? 아래 대시보드에서 직접 눌러 봐.")])}
<div class="dash" id="d1"><div class="dh"><span class="badge">1단계 대시보드</span><h3>블록 쪼개기 공방</h3></div>
<div class="sub">① 주판봇의 체 거르기 — 배수를 지우면 소수만 남는다</div>
<div class="ctrl" id="d1-sieve"><button data-p="2">2의 배수 지우기</button><button data-p="3">3의 배수</button><button data-p="5">5의 배수</button><button data-p="7">7의 배수</button><button id="d1-reset">처음부터</button></div>
<div class="kpis">{kpi("남은 수(1 제외)", "d1-left")}{kpi("지운 수", "d1-gone")}</div>
<div class="board" id="d1-board" aria-label="1부터 100까지 숫자판"></div>
<div class="readout" id="d1-msg" aria-live="polite"></div>
<p class="hint">왜 7까지만? 100보다 작은 수가 소수가 아니면, 10(=√100)보다 작은 블록을 꼭 하나 품고 있기 때문입니다.</p>
<div class="sub">② 쪼개기 기계 — 아무 수나 넣어 보세요</div>
<div class="ctrl"><label>수 <input type="number" id="d1-n" value="360" min="2" max="999999"></label></div>
<div class="readout" id="d1-fac" aria-live="polite"></div>
<div class="sub">③ 복습 — 소수일까, 아닐까? (5문제)</div>
<div class="ctrl" id="d1-quiz"><span>이 수는? <b id="d1-qn" class="tn" style="font-size:22px"></b></span><button data-a="p">소수</button><button data-a="n">소수 아님</button><button id="d1-qreset">다시 하기</button></div>
<div class="readout" id="d1-qfb" aria-live="polite"></div></div>
<div class="sum"><b class="t">박사 정리</b> — 소수는 더 쪼갤 수 없는 숫자 블록이고, 모든 수는 블록을 곱한 것입니다. 이 숫자는 업무에서 "그 수의 지문"이라는 뜻입니다. 다음 단계에서는 이 블록이 실제로 어디에 쓰이는지 봅니다.</div>
<div class="limit"><b>이 단계의 한계</b> — 블록이 무엇인지는 알았지만, 이게 왜 뉴스가 될 만큼 중요한지는 아직 모릅니다.</div>
{quiz("91은 소수일까요?", ["소수다", "소수가 아니다 (7 × 13)", "알 수 없다"], 1, "91 = 7 × 13으로 쪼개집니다. 홀수라고 다 소수는 아니에요.")}
{react([("x1", "e01", "오, 하루 첫 단계 무사 통과!"), ("x2", "e16", "목소리 점점 안정되는데?"), ("x3", "e01", "(박수)")])}
</div></section>'''

    # ---------------- 2단계
    s += f'''<section class="room" id="s2"><div class="wrap">{step_head(1)}
{scene("scene_s2", "블록 두 개로 자물쇠를 만들고, 주판봇이 그 자물쇠를 쪼개느라 진땀 빼는 장면")}
<div class="tags"><span class="tag how">방법: 곱하기 vs 되돌리기</span><span class="tag day">일상: 휴대폰 송금, 서랍 정리</span></div>
{talk([("doctor", "e07", "여러분 휴대폰으로 송금할 때, 그 돈은 무엇이 지켜 줄까요?"),
       ("moa", "e09", "소수가 그렇게 대단해요? 그냥 나눠지지 않는 수잖아요."),
       ("haru", "e15", "그, 그게… 바로 그 '나눠지지 않는' 성질이 쓸모예요! 세 가지로 보여 드릴게요.")])}
<div class="duo"><div class="box why"><h4>왜 소수를 쓰나</h4><ol>
<li><b>문제 상황</b>: 누구나 잠글 수 있지만, 열쇠 가진 사람만 열 수 있는 자물쇠가 필요하다.</li>
<li><b>앞 방법의 한계</b>: 비밀번호를 미리 나눠 갖는 방식은 처음 만나는 상대(쇼핑몰, 은행)와 쓸 수 없다.</li>
<li><b>해법</b>: 큰 소수 두 개를 곱한 수를 공개한다. 곱하기는 쉽지만, 그 수를 다시 두 소수로 쪼개기는 엄청나게 어렵다.</li></ol>
<div class="easy">쉽게 말하면: 물감 두 색 섞기는 쉬워도, 섞인 색에서 원래 두 색을 정확히 되찾기는 어렵습니다.</div></div>
<div class="box"><h4>숫자로 한 번 해 보기</h4><p>61 × 53 = 3,233 — 바로 나옵니다.</p><p>"3,233은 어떤 두 소수의 곱?" — 3, 5, 7, 11 … 하나씩 나눠 보다가 53에서야 찾습니다.</p>
<p>실제 인터넷 자물쇠는 <b>약 309자리</b> 소수 두 개를 곱한 <b>약 617자리</b> 수를 씁니다. 곱하기는 순식간, 쪼개기는 현재 컴퓨터로 사실상 불가능합니다.</p></div></div>
<h3>① 인터넷 자물쇠</h3><p>인터넷 결제, 메신저, 공인 인증이 이 "곱하기는 쉽고 되돌리기는 어렵다"에 기대고 있습니다.</p>
<h3>② 데이터 서랍</h3><p>컴퓨터는 자료를 "번호를 서랍 수로 나눈 나머지"로 서랍에 넣습니다. 10, 20, …, 100을 서랍 10개에 넣으면 나머지가 모두 0이라 <b>0번 서랍에 다 몰립니다</b>. 서랍을 11개(소수)로 하면 1~10번에 하나씩 <b>고르게</b> 들어갑니다.</p>
<div class="side"><b>곁가지 상자 — 13년·17년 매미</b><p>북아메리카에는 13년·17년마다 한꺼번에 땅 위로 나오는 매미가 있습니다. 12년 주기라면 2·3·4·6년 주기의 천적과 12년마다 만나지만, 17년 주기면 2년 천적과는 34년, 6년 천적과는 102년마다 만납니다.</p>
<p class="hint">"천적을 피하려고 소수 주기가 됐다"는 유력한 설명 중 하나이고, 확정된 사실은 아닙니다.</p></div>
{talk([("jupanbot", "e16", "곱하기 버튼이랑 쪼개기 버튼, 제가 시간 재 볼게요!"),
       ("fruitfly", "e09", "자릿수를 하나씩 늘려 봐. 쪼개기 횟수가 어떻게 되는지.")])}
<div class="dash" id="d2"><div class="dh"><span class="badge">2단계 대시보드</span><h3>자물쇠·서랍·매미 실험실</h3></div>
<div class="sub">① 자물쇠 — 곱하기 1번 vs 쪼개기 몇 번?</div>
<div class="ctrl" id="d2-lock"><label>소수 자릿수 <select id="d2-dig"><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option><option>7</option></select></label><button id="d2-pick">새 소수 두 개 뽑기</button><button id="d2-domul">곱하기</button><button id="d2-dosplit">곱을 다시 쪼개기</button></div>
<div class="kpis">{kpi("소수 ①", "d2-p")}{kpi("소수 ②", "d2-q")}{kpi("공개하는 곱", "d2-n", "?")}{kpi("곱하기", "d2-mul")}</div>
<div class="readout" id="d2-split" aria-live="polite">—</div>
<svg id="d2-chart" viewBox="0 0 640 200" role="img" aria-label="자릿수별 쪼개기 시도 횟수"></svg>
<p class="hint">소수의 자릿수가 하나 늘 때마다 쪼개기 횟수는 대략 10배씩 늘어납니다(나눠 볼 후보가 10배가 되므로). 309자리라면 이 방법으로는 우주의 나이를 써도 끝나지 않습니다. 실제로는 더 빠른 쪼개기 방법도 있지만, 그것으로도 현재 컴퓨터로는 사실상 불가능합니다.</p>
<div class="sub">② 데이터 서랍 — 서랍 수를 바꿔 보세요</div>
<div class="ctrl"><label>서랍 수 <input type="range" id="d2-drawers" min="5" max="20" value="10"> <b id="d2-drv"></b>개</label><label>번호 간격 <input type="range" id="d2-step" min="2" max="15" value="10"> <b id="d2-stv"></b></label></div>
<p class="hint">번호 간격 × 1, × 2, …, × 20 — 자료 20개를 넣습니다.</p>
<div class="kpis">{kpi("가장 몰린 서랍", "d2-dmax")}{kpi("빈 서랍", "d2-dempty")}{kpi("서랍 수는", "d2-dprime")}</div>
<svg id="d2-bars" viewBox="0 0 640 190" role="img" aria-label="서랍별 자료 개수"></svg>
<div class="readout" id="d2-dmsg" aria-live="polite"></div>
<div class="sub">③ 곁가지 — 매미 주기</div>
<div class="ctrl"><label>매미 주기 <input type="range" id="d2-cy" min="10" max="20" value="17"> <b id="d2-cyv"></b>년</label></div>
<div class="tbl"><table><tbody id="d2-cyt"></tbody></table></div><div class="readout" id="d2-cymsg"></div></div>
<div class="sum"><b class="t">박사 정리</b> — 소수는 ① 숫자의 지문, ② 인터넷의 자물쇠, ③ 고르게 나누는 도구입니다. 그런데 자물쇠를 만들려면 <b>309자리 소수를 실제로 찾아야</b> 해요. "그 크기에서 소수가 얼마나 자주 나오나"를 알아야 몇 번 만에 찾을지 계획할 수 있습니다. 그래서 다음 단계는 소수 세기입니다.</div>
<div class="limit"><b>이 단계의 한계</b> — 쓸모는 알았지만, 큰 수 근처에 소수가 얼마나 있는지는 아직 모릅니다.</div>
{quiz("인터넷 자물쇠가 안전한 이유는?", ["소수가 비밀이라서", "곱하기는 쉽지만 곱을 다시 소수로 쪼개기가 매우 어려워서", "소수가 무한히 많아서"], 1, "공개된 곱에서 두 소수를 되찾기 어렵다는 것이 핵심입니다.")}
{react([("x1", "e04", "송금이 소수 덕분이었어?!"), ("x2", "e01", "하루, 이제 완전 발표자네."), ("x3", "e16", "(고개 끄덕)")])}
</div></section>'''

    # ---------------- 3단계
    s += f'''<section class="room" id="s3"><div class="wrap">{step_head(2)}
{scene("scene_s3", "갈수록 간격이 멀어지는 버스 정류장 길 앞의 시아·모아·하루")}
<div class="tags"><span class="tag how">방법: 직접 세기</span><span class="tag day">일상: 버스 정류장 간격</span></div>
{talk([("doctor", "e07", "회사에서 '자물쇠용 소수를 하루에 몇 개 만들 수 있나?'라고 물으면 뭐부터 알아야 할까요?"),
       ("moa", "e09", "그 크기에 소수가 얼마나 많은지요!"),
       ("jupanbot", "e16", "그럼 세 보죠! 100까지 25개, 1,000까지 168개 … 100만까지는 78,498개!"),
       ("sia", "e19", "100까지는 4개 중 1개가 소수인데, 100만까지면 13개 중 1개 정도네요?"),
       ("moa", "e09", "그럼 결국 소수가 없어져요?"),
       ("haru", "e07", "아뇨, 소수는 끝없이 있어요. 점점 드물어질 뿐이에요. 시골로 갈수록 버스 정류장 간격이 멀어지는 것처럼요.")])}
<div class="duo"><div class="box why"><h4>왜 세어 보나</h4><ol><li><b>문제 상황</b>: 큰 소수를 찾을 때 몇 번쯤 시도해야 하는지 알고 싶다.</li><li><b>앞 단계의 한계</b>: 소수의 쓸모는 알지만 "얼마나 자주"는 모른다.</li><li><b>해법</b>: 작은 범위부터 직접 세어 규칙을 찾는다.</li></ol>
<div class="easy">쉽게 말하면: 동네마다 편의점이 몇 개인지 세어 보고, 도시와 시골의 차이를 보는 것과 같습니다.</div></div>
<div class="box"><h4>주판봇이 센 표</h4><div class="tbl"><table><thead><tr><th>어디까지</th><th>소수 개수</th><th>비율</th></tr></thead><tbody>
<tr><td>100</td><td>25</td><td>25.0%</td></tr><tr><td>1,000</td><td>168</td><td>16.8%</td></tr><tr><td>10,000</td><td>1,229</td><td>12.3%</td></tr><tr><td>100,000</td><td>9,592</td><td>9.6%</td></tr><tr><td>1,000,000</td><td>78,498</td><td>7.8%</td></tr></tbody></table></div>
<p class="hint">10배 넓힐 때마다 비율이 천천히, 규칙적으로 줄어듭니다.</p></div></div>
{talk([("fruitfly", "e09", "규칙적으로 줄어든다고? 곡선으로 그려서 확인해 봐.")])}
<div class="dash" id="d3"><div class="dh"><span class="badge">3단계 대시보드</span><h3>소수 세기 관측소</h3></div>
<div class="ctrl"><label>어디까지 셀까 <input type="range" id="d3-x" min="2" max="6" step="0.05" value="4"> <b id="d3-xv" class="tn"></b></label></div>
<div class="kpis">{kpi("소수 개수", "d3-cnt")}{kpi("비율", "d3-pct")}{kpi("몇 개 중 1개?", "d3-one")}</div>
<svg id="d3-chart" viewBox="0 0 640 230" role="img" aria-label="범위에 따른 소수 비율 곡선"></svg>
<div class="sub">② 주판봇에게 표 채우게 하기</div>
<div class="ctrl"><button id="d3-count">주판봇, 세어 줘!</button></div>
<div class="tbl"><table><thead><tr><th>어디까지</th><th>소수 개수</th><th>비율</th><th>몇 개 중 1개</th></tr></thead><tbody id="d3-tbl"></tbody></table></div>
<div class="sub">③ 복습 — 개수 맞히기</div>
<div class="ctrl"><span><b id="d3-gx"></b>까지 소수는 몇 개일까?</span><input type="number" id="d3-g" placeholder="내 예상"><button id="d3-gok">확인</button><button id="d3-gnew">다른 문제</button></div>
<div class="readout" id="d3-gfb" aria-live="polite"></div></div>
<details class="code"><summary>교안의 파이썬 코드로 보면 (몰라도 됩니다)</summary><pre>sympy.primepi(10**6)   # 78498</pre><p>100만까지의 소수 개수를 세는 한 줄입니다.</p></details>
<div class="sum"><b class="t">박사 정리</b> — 소수는 끝없이 있지만 갈수록 드물어집니다. 100만 근처에서는 13개 중 1개 정도입니다. 드물어지는 속도에 규칙이 있다는 것이 다음 단계의 출발점입니다.</div>
<div class="limit"><b>이 단계의 한계</b> — 직접 세는 건 100만까지는 금방이지만, 309자리 수까지는 영원히 셀 수 없습니다. 세지 않고 맞히는 방법이 필요합니다.</div>
{quiz("소수에 대해 맞는 말은?", ["어느 수부터는 소수가 하나도 없다", "끝없이 있지만 갈수록 드물어진다", "어디서나 같은 비율로 나온다"], 1, "소수는 끝없이 있습니다. 비율만 천천히 줄어듭니다.")}
{react([("x1", "e09", "13개 중 1개… 외워 둬야지."), ("x2", "e01", "하루 표정 이제 웃고 있다!")])}
</div></section>'''

    # ---------------- 4단계
    s += f'''<section class="room" id="s4"><div class="wrap">{step_head(3)}
{scene("scene_s4", "거의 겹쳐 올라가는 두 선 앞에서 안도하는 하루")}
<div class="tags"><span class="tag how">방법: 어림 공식</span><span class="tag day">일상: 일기예보 "내일 20도쯤"</span></div>
{talk([("doctor", "e07", "309자리 수를 일일이 셀 수 없다면, 여러분은 어떻게 개수를 짐작하겠어요?"),
       ("sia", "e19", "곡선이 규칙적이니까 공식으로 맞히면 되지 않아요?"),
       ("haru", "e10", "맞아요! 하나하나 세지 않고도 '대략 몇 개'를 맞히는 어림 공식이 있어요. 2단계 자물쇠 만들 때 쓰는 바로 그 공식이에요.")])}
<div class="duo"><div class="box why"><h4>왜 어림 공식을 쓰나</h4><ol><li><b>문제 상황</b>: 아주 큰 범위의 소수 개수를 알고 싶다.</li><li><b>앞 단계의 한계</b>: 직접 세기는 큰 수에서 불가능하다.</li><li><b>해법</b>: "그 근처에서는 몇 개 중 1개꼴"이라는 규칙을 차곡차곡 더한다.</li></ol>
<div class="easy">쉽게 말하면: 일기예보가 매 순간 온도를 재지 않고도 "내일 20도쯤"이라고 맞히는 것과 같습니다.</div></div>
<div class="box mathbox"><h4>수학 수식을 어려워하는 조수가 대신 물어봅니다</h4>
<div class="q">{face("haru", "e04")}<div><b>조수</b> 어림 공식 안에 뭐가 들어 있어요? 무서운 기호부터 나오면 어떡하죠?</div></div>
<p><b>학교 수학으로 보면</b>: 로그함수(고등학교 수학 Ⅰ). 수가 10배 커질 때마다 ln은 약 2.3씩 커집니다.</p>
<div class="tbl"><table><tr><th>조각</th><th>읽는 법</th><th>뜻</th></tr>
<tr><td class="m">ln x</td><td>엘엔 엑스</td><td>x의 자연로그 — "x가 10의 몇 제곱인가"에 약 2.3을 곱한 값 (100만 = 10⁶ → 6 × 2.3 ≈ 13.8)</td></tr>
<tr><td class="m">1 ÷ ln x</td><td>일 나누기 엘엔 엑스</td><td>x 근처에서 소수가 나올 확률 "몇 개 중 1개"</td></tr>
<tr><td>좋은 어림</td><td>—</td><td>2부터 x까지 그 확률을 차곡차곡 더한 값 (이름: li)</td></tr></table></div>
<div class="try"><div>100만 근처: ln(1,000,000) ≈ 13.8 → 13.8개 중 1개꼴</div><div>간단한 어림: 1,000,000 ÷ 13.8 ≈ 72,382개</div><div>좋은 어림(차곡차곡 더하기): ≈ 78,628개 · 실제 78,498개</div></div>
<div class="q">{face("haru", "e16")}<div><b>조수</b> 결국 "몇 개 중 1개"를 모아 더한 거네요. 3단계 표의 "13개 중 1개"가 바로 이거였어요!</div></div></div></div>
<div class="solve"><h4>풀이</h4><p>100만까지 좋은 어림 78,628개, 실제 78,498개 → <b>130개 차이(0.17%)</b>. 간단한 어림은 6,116개 차이입니다.</p><p>이 숫자는 업무에서 "100만까지 소수를 어림하면 1,000개 중 2개 정도만 틀린다"는 뜻입니다.</p></div>
{talk([("fruitfly", "e09", "0.17%라고? 범위를 바꿔도 그렇게 잘 맞는지 그래프로 봐.")])}
<div class="dash" id="d4"><div class="dh"><span class="badge">4단계 대시보드</span><h3>어림 비교판</h3></div>
<div class="ctrl"><label>어디까지 <input type="range" id="d4-x" min="2" max="6" step="0.05" value="3"> <b id="d4-xv" class="tn"></b></label><label><input type="checkbox" id="d4-simple" checked> 간단한 어림도 보기</label></div>
<div class="kpis">{kpi("실제(주판봇)", "d4-a")}{kpi("좋은 어림", "d4-g")}{kpi("좋은 어림의 차이", "d4-dg")}{kpi("간단한 어림의 차이", "d4-ds")}</div>
<div class="kpis">{kpi("간단한 어림", "d4-s")}</div>
<svg id="d4-chart" viewBox="0 0 640 260" role="img" aria-label="실제 소수 개수와 두 어림 비교"></svg>
<p class="hint">실제 개수는 소수를 만날 때마다 한 단씩 올라가는 선입니다. 좋은 어림(점선)이 거의 겹쳐 지나갑니다.</p></div>
<details class="code"><summary>교안의 파이썬 코드로 보면 (몰라도 됩니다)</summary><pre>mpmath.li(10**6)   # 78627.549…</pre><p>좋은 어림 공식을 계산하는 한 줄입니다.</p></details>
<div class="sum"><b class="t">박사 정리</b> — 소수 개수는 세지 않고도 어림으로 아주 잘 맞힐 수 있습니다. 앞 단계의 "몇 개 중 1개"를 더한 것이 어림이고, 다음 단계는 "이 어림을 끝까지 믿어도 되나?"입니다.</div>
<div class="limit"><b>이 단계의 한계</b> — 100만까지는 잘 맞았습니다. 하지만 1조, 1경, 309자리까지 가도 잘 맞는다는 <b>보장</b>은 아직 없습니다.</div>
{quiz("100만까지 좋은 어림과 실제 개수의 차이는?", ["약 13개", "약 130개", "약 6,000개"], 1, "78,628 − 78,498 = 130개, 0.17%입니다.")}
{react([("x1", "e16", "0.17%면 일기예보보다 잘 맞네."), ("x3", "e09", "그럼 큰 수에서도 맞을까…?")])}
</div></section>'''

    # ---------------- 5단계
    s += f'''<section class="room" id="s5"><div class="wrap">{step_head(4)}
{scene("scene_s5", "가운데 줄 위에 늘어선 특별한 점들을 초파리 연구원이 살펴보는 장면")}
<div class="tags"><span class="tag how">방법: 약속(보증)</span><span class="tag day">일기예보 "20도 ± 2도"</span></div>
{talk([("moa", "e09", "그래서 리만 가설이 뭐예요? 아까부터 그게 제일 궁금했어요."),
       ("haru", "e20", "(숨 고르고) 리만 가설은… '어림이 아무리 큰 수까지 가도 크게 틀리지 않는다'는 약속이에요."),
       ("doctor", "e08", "일기예보로 치면 '20도'가 어림이고, '± 2도'가 약속한 범위예요. 리만 가설은 그 ± 범위가 영원히 지켜진다는 주장이죠.")])}
<div class="duo"><div class="box why"><h4>왜 약속이 필요한가</h4><ol><li><b>문제 상황</b>: 어림을 믿고 큰 소수를 찾거나, 그 위에 다른 수학을 쌓고 싶다.</li><li><b>앞 단계의 한계</b>: 100만까지 잘 맞았다는 건 과거 기록일 뿐, 앞으로의 보장이 아니다.</li><li><b>해법</b>: "빗나감은 언제나 이 범위 안"이라는 약속을 증명한다 — 그게 리만 가설.</li></ol>
<div class="easy">쉽게 말하면: 가게가 "오늘까지 불량 0개"라고 말하는 것과, "앞으로도 불량률 0.1% 이하"를 보증서로 써 주는 것의 차이입니다.</div></div>
<div class="box mathbox"><h4>수학 수식을 어려워하는 조수가 대신 물어봅니다</h4>
<div class="q">{face("haru", "e04")}<div><b>조수</b> 약속한 범위는 얼마나 넓어요?</div></div>
<p><b>학교 수학으로 보면</b>: 제곱근과 로그함수.</p>
<div class="fx">약속 범위 = √x × ln x ÷ (8π)</div>
<div class="tbl"><table><tr><th>조각</th><th>뜻</th></tr><tr><td class="m">√x</td><td>x의 제곱근 — 100만이면 1,000</td></tr><tr><td class="m">ln x</td><td>4단계의 그 로그 — 100만이면 13.8</td></tr><tr><td class="m">8π</td><td>약 25.1, 범위를 정하는 상수</td></tr></table></div>
<div class="try"><div>100만: 1,000 × 13.8 ÷ 25.1 ≈ <b>550</b></div><div>실제 빗나감 130 → 범위 안</div></div>
<p class="hint">리만 가설이 참이면 x가 2,657 이상일 때 언제나 이 범위 안에 있습니다(쇤펠트, 1976). 거꾸로 이 범위가 늘 지켜지면 리만 가설도 참입니다. 두 말은 같은 뜻입니다.</p>
<div class="q">{face("haru", "e16")}<div><b>조수</b> 100만에서 550개까지 봐줄게, 그런데 실제로는 130개만 빗나갔다! 여유가 꽤 있네요.</div></div></div></div>
<h3>리만은 이 약속을 그림 하나로 바꿨다</h3>
<p>리만은 "약속이 지켜지나?"를 "<b>특별한 점들이 모두 가운데 줄 위에 서 있나?</b>"라는 질문으로 바꿨습니다. 점 하나하나가 어림을 조금씩 흔드는데, 모두 가운데 줄 위에 있으면 흔들림이 약속 범위 안에 머뭅니다. 한 점이라도 줄 밖에 있으면 그 점의 흔들림이 결국 범위를 넘어 약속이 깨집니다.</p>
<div class="box" style="border-color:#c9302c;background:#fff7f6"><h4>AI 판단 코너 ① — "수조 개 확인했으니 증명 끝?"</h4>
<p>어떤 AI가 이렇게 답했습니다: <i>"특별한 점을 컴퓨터로 수조 개 확인했고 모두 가운데 줄 위에 있으므로, 리만 가설은 2004년에 이미 증명되었습니다."</i></p>
{quiz("이 AI의 답은?", ["맞다 — 수조 개면 충분하다", "틀리다 — 점은 끝없이 많아서, 아무리 많이 확인해도 '모든 점'의 증명은 아니다", "반쯤 맞다 — 절반은 증명된 셈이다"], 1, "확인은 '지금까지'의 기록이고, 증명은 '끝까지'의 보증입니다. 4단계의 한계와 같은 이야기예요.", "4단계 끝의 '보장이 없다'를 떠올려 보세요.")}</div>
{talk([("jupanbot", "e16", "저도 그 AI처럼 생각했어요! 수조 개면 끝난 거 아니에요?"),
       ("doctor", "e09", "그렇게 생각하기 쉬워요. 그런데 점은 끝없이 많아서 '끝까지'는 확인으로 못 해요. 그래서 증명이 필요했죠."),
       ("fruitfly", "e09", "한 점만 줄 밖으로 옮기면 어떻게 될까? 아래에서 끌어 봐.")])}
<div class="dash" id="d5"><div class="dh"><span class="badge">5단계 대시보드</span><h3>약속 감시판</h3></div>
<div class="sub">① 실제 빗나감은 약속 범위 안에 있나</div>
<div class="ctrl"><label>어디까지 <input type="range" id="d5-x" min="3.5" max="6" step="0.05" value="6"> <b id="d5-xv" class="tn"></b></label></div>
<div class="kpis">{kpi("실제 빗나감", "d5-miss")}{kpi("약속한 범위", "d5-b")}{kpi("남은 여유", "d5-room")}{kpi("판정", "d5-ok")}</div>
<svg id="d5-chart" viewBox="0 0 640 250" role="img" aria-label="빗나감과 약속 범위"></svg>
<div class="sub">② 가운데 줄 — 첫 점을 옮겨 보기 (설명용 모형)</div>
<div class="ctrl"><label>첫 점의 가로 위치 <input type="range" id="d5-sig" min="0.5" max="0.8" step="0.01" value="0.5"> <b id="d5-sigv"></b></label></div>
<svg id="d5-line" viewBox="0 0 320 300" role="img" aria-label="가운데 줄 위의 특별한 점 10개" style="max-width:360px"></svg>
<div class="readout" id="d5-lmsg" aria-live="polite"></div>
<p class="hint">점의 높이는 실제 값(첫 점 14.13 …)입니다. 옮긴 뒤 "몇 제곱부터 넘는다"는 계산은 크기만 비교한 설명용 모형입니다.</p></div>
<div class="sum"><b class="t">박사 정리</b> — 리만 가설은 "소수 개수 어림이 영원히 약속 범위 안에 있다"는 약속이고, 리만은 이것을 "특별한 점들이 모두 가운데 줄 위에 있다"는 질문으로 바꿨습니다. 다음 단계에서는 이 약속이 지켜지면 무엇이 좋아지는지 봅니다.</div>
<details class="abbr"><summary>더 알고 싶은 분 — 특별한 점과 가운데 줄의 정체</summary><p>특별한 점은 <b>제타 함수</b> ζ(s)가 0이 되는 자리(영점)입니다. s는 가로·세로 두 좌표를 가진 수(복소수)이고, 가운데 줄은 가로 좌표가 1/2인 세로선(임계선)입니다. 가로축 위 −2, −4, −6 …에도 0이 되는 자리가 있지만 이건 쉽게 설명되는 "자명한" 자리라 약속과는 관계없습니다.</p>
<p>제타 함수는 1 + 1/2ˢ + 1/3ˢ + … 에서 출발합니다. s = 2이면 1 + 1/4 + 1/9 + … = π²/6 ≈ 1.6449 — 힐베르트 공간 해설 5번 방에서 계산한 바로 그 값입니다.</p></details>
<div class="limit"><b>이 단계의 한계</b> — 약속의 뜻은 알았지만, "그게 지켜지면 무엇이 좋은가"는 아직입니다.</div>
{quiz("리만 가설을 한 줄로 말하면?", ["소수는 끝없이 많다", "소수 개수 어림의 빗나감이 영원히 약속 범위 안에 있다", "소수는 모두 홀수다"], 1, "소수가 끝없이 많다는 건 2,300년 전 유클리드가 이미 증명했습니다. 리만 가설은 '얼마나 정확히 어림되나'에 대한 약속입니다.")}
{react([("x1", "e04", "가운데 줄 하나에 다 걸려 있었구나!"), ("x2", "e16", "하루, 핵심 설명 완벽했어."), ("x3", "e01", "(박수 크게)")])}
</div></section>'''

    # ---------------- 6단계
    s += f'''<section class="room" id="s6"><div class="wrap">{step_head(5)}
{scene("scene_s6", "기초 위에 층이 쌓이는 건물과 잠긴 채 빛나는 자물쇠")}
<div class="tags"><span class="tag how">방법: 약속을 믿고 쌓기</span><span class="tag day">일상: 건물 기초 승인</span></div>
{talk([("doctor", "e07", "회사 신입이 '그래서 이 약속이 지켜지면 뭐가 좋아요?'라고 묻는다면, 뭐라고 답하겠어요?"),
       ("sia", "e19", "음… 어림을 더 믿을 수 있다?"),
       ("haru", "e10", "맞아요. 정리하면 좋은 점이 세 가지예요.")])}
<div class="cards" style="margin:14px 0">
<div class="card"><span class="n">좋은 점 ①</span><h3>범위까지 함께 말할 수 있다</h3><p>"100만까지 소수는 78,628개 ± 550개"처럼 틀릴 수 있는 범위까지 보장합니다. 큰 수의 어느 구간에 소수가 얼마나 있는지 보증이 생기므로, 자물쇠용 소수 찾기 같은 계획의 근거가 튼튼해집니다.</p></div>
<div class="card"><span class="n">좋은 점 ②</span><h3>다음 소수가 너무 멀지 않다</h3><p>소수와 다음 소수 사이 간격이 대략 √p × ln p를 넘지 않는다고 장담할 수 있습니다(크라메르, 1920). 100만 근처라면 이 상한은 약 1만 4천으로 넉넉하고, 실제 가장 큰 간격은 114입니다. 상한은 "아무리 나빠도 이 정도"라는 보증입니다.</p></div>
<div class="card"><span class="n">좋은 점 ③</span><h3>쌓아 둔 결과가 한꺼번에 확정</h3><p>수학자들은 "이 약속이 맞다면…"으로 시작하는 결과를 많이 쌓아 왔습니다. 건물 기초가 승인되면 위층도 쓸 수 있는 것처럼, 약속이 증명되면 그 결과들도 함께 확정됩니다.</p></div></div>
<div class="box" style="border-color:#c9302c;background:#fff7f6"><h4>AI 판단 코너 ② — 이 답, 믿어도 될까?</h4>
<p>어떤 AI가 이렇게 답했습니다: <i>"리만 가설이 증명됐으므로 은행 암호가 다 뚫리게 되었습니다."</i></p>
<p>박사의 확인 질문: ① 자물쇠의 안전은 무엇에 달려 있었나? ② 리만 가설은 그 일을 빠르게 해 주나?</p>
{quiz("이 AI의 답은?", ["맞다 — 소수의 비밀이 풀렸으니까", "틀리다 — 자물쇠는 '곱을 쪼개기 어렵다'에 달려 있고, 이 약속은 쪼개기를 빠르게 해 주지 않는다", "반쯤 맞다 — 일부 은행만 뚫린다"], 1, "리만 가설은 소수가 '얼마나 있나'에 대한 약속입니다. 2단계의 '되돌리기 어렵다'는 그대로입니다.", "2단계 자물쇠 실험을 떠올려 보세요.")}
<p class="hint">원자료 인포그래픽의 "암호학에 영향"이라는 문구도 같은 이유로 조심해서 읽어야 합니다. 영향이 있다면 "소수를 찾고 판정하는 일의 확실성" 쪽입니다.</p></div>
{talk([("jupanbot", "e14", "헉, 저도 암호 다 뚫리는 줄 알았어요…"),
       ("doctor", "e16", "괜찮아요. 처음엔 다들 그렇게 생각해요. 그래서 AI 답을 볼 때 '무엇에 달려 있나'를 한 번 더 묻는 습관이 중요해요."),
       ("fruitfly", "e09", "좋은 점 세 가지, 대시보드에서 직접 계산해 봐.")])}
<div class="dash" id="d6"><div class="dh"><span class="badge">6단계 대시보드</span><h3>약속 활용 센터</h3></div>
<div class="tabs"><button class="on" data-tab="d6-t1">① 범위 계산기</button><button data-tab="d6-t2">② 소수 간격 탐험</button><button data-tab="d6-t3">③ 자물쇠 계획기</button></div>
<div class="tabpane" id="d6-t1"><div class="ctrl"><label>어디까지 <input type="number" id="d6-x" value="1000000" min="2657" max="1000000000000000"></label></div><div class="readout" id="d6-out" aria-live="polite"></div><p class="hint">1조(1000000000000)도 넣어 보세요. 약속 덕분에 세지 않고도 범위를 말할 수 있습니다.</p></div>
<div class="tabpane" id="d6-t2" hidden><div class="ctrl"><label>어디쯤 <input type="range" id="d6-gx" min="1.5" max="6" step="0.05" value="5.7"> <b id="d6-gxv" class="tn"></b></label></div>
<div class="kpis"><div class="kpi" style="grid-column:span 2"><small>그 근처</small><b id="d6-gp" style="font-size:16px"></b></div><div class="kpi" style="grid-column:span 2"><small>기록</small><b id="d6-gmax" style="font-size:16px"></b></div></div>
<svg id="d6-gchart" viewBox="0 0 640 200" role="img" aria-label="가장 큰 소수 간격 기록"></svg></div>
<div class="tabpane" id="d6-t3" hidden><div class="ctrl"><label>자물쇠 크기 <input type="range" id="d6-bits" min="256" max="4096" step="256" value="1024"> <b id="d6-bv"></b>비트</label></div>
<div class="kpis">{kpi("소수 크기", "d6-dig")}{kpi("그 근처 소수", "d6-one")}{kpi("홀수만 검사하면", "d6-odd")}</div><div class="readout" id="d6-pmsg"></div></div></div>
<h3>2026년, 무엇이 일어났나 <span class="hint">(기준 시점 2026-11-22)</span></h3>
<ul class="news"><li><b>2026-08-10</b> 앤트로픽: 공개 전 연구용 클로드가 "가운데 줄 위에 있다고 보장되는 점의 비율"을 41.6%에서 67.2%로 올렸다고 발표 — 증명은 아니었음.</li>
<li><b>2026-11-20</b> 앤트로픽 수학자 레벤트 알포게가 클로드와 함께 리만 가설(일반화된 형태 포함)의 증명을 찾았다고 발표. 증명은 Lean으로 쓴 파일 약 17만 5천 개. 같은 날 MIT 서덜랜드 등이 컴퓨터로 다시 검사해 통과를 확인.</li>
<li><b>2026-11-21</b> Lean·Mathlib 쪽 전문가들이 공동 성명으로 "리만 가설의 진술과 증명이 맞다"고 인증.</li>
<li><b>남은 일</b> 사람이 증명을 이해하는 일, 학술지 게재와 학계의 정식 인정 절차.</li></ul>
{talk([("moa", "e09", "컴퓨터가 맞다고 했으면 끝난 거 아니에요?"), ("doctor", "e08", "'맞다'와 '이해했다'는 다른 말이에요. 컴퓨터는 논리가 맞는지 검사했고, 왜 맞는지 사람이 이해하는 일은 이제 시작이에요.")])}
<div class="sum"><b class="t">박사 정리</b> — 약속이 지켜지면 ① 소수 개수를 범위까지 말하고, ② 소수 사이가 너무 멀지 않다고 장담하고, ③ 쌓아 둔 결과들이 확정됩니다. 암호가 뚫리는 일은 아닙니다. 이 숫자들은 업무에서 "큰 소수를 찾는 계획을 더 믿을 수 있다"는 뜻입니다.</div>
<div class="limit"><b>이 단계의 한계</b> — 좋은 점 대부분은 수학 안에서의 이점입니다. 내일 당장 일하는 방식이 바뀌지는 않습니다.</div>
{react([("x1", "e16", "하루, 마지막까지 완주!"), ("x2", "e01", "물 여기 있어!"), ("x3", "e16", "(기립 박수)")])}
</div></section>'''

    # ---------------- 대결
    s += f'''<section class="room" id="duel"><div class="wrap"><span class="roomno">대결</span><h2>소수 개수 맞히기 — 시아 vs 모아</h2>
{scene("scene_duel", "시아(계산기)와 모아(눈금 노트)의 대결, 가운데 심판 주판봇과 깃발 든 하루")}
{talk([("haru", "e10", "마지막은 대결이에요! 시아는 간단한 어림, 모아는 좋은 어림. 판정은 주판봇이 직접 세어서!"),
       ("sia", "e19", "간단한 게 최고죠. 나누기 한 번이면 끝!"),
       ("moa", "e09", "저는 '몇 개 중 1개'를 차곡차곡 더할게요."),
       ("jupanbot", "e16", "100만까지는 제가 다 셀 수 있습니다!")])}
<div class="dash"><div class="dh"><span class="badge">대결 대시보드</span><h3>네 문제 판정</h3></div>
<div class="ctrl"><label>문제 <select id="du-x"><option value="1000">1,000까지</option><option value="10000">1만까지</option><option value="100000">10만까지</option><option value="1000000">100만까지</option></select></label><button id="du-count">주판봇, 세어서 판정!</button></div>
<div class="kpis">{kpi("시아(간단한 어림)", "du-sia")}{kpi("모아(좋은 어림)", "du-moa")}{kpi("주판봇이 센 실제", "du-real", "?")}{kpi("점수", "du-score", "0/4")}</div>
<div class="readout" id="du-who" aria-live="polite"></div>
<div id="du-end" hidden>{talk([("haru", "e10", "판정! 네 문제 모두 모아의 승리입니다."), ("moa", "e16", "몇 개 중 1개를 더했을 뿐인데요."), ("sia", "e14", "간단한 게 최고는 아니었네요… 100만에서 6천 개나 틀렸어요."),
       ("haru", "e07", "시아 방식은 끝자리의 '몇 개 중 1개' 하나로 전체를 계산해요. 그런데 작은 수 쪽은 소수가 더 촘촘하니까 모자라게 나와요. 모아 방식은 구간마다 바뀌는 비율을 하나씩 더해서 그 차이를 메운 거예요.")])}</div></div>
</div></section>'''

    # ---------------- 아웃트로·색인
    terms = [("소수", "1과 자기 자신으로만 나눠지는 2 이상의 수. 모든 수의 블록", "s1"),
             ("소인수분해", "수를 소수 블록의 곱으로 쪼개기. 방법은 한 가지뿐", "s1"),
             ("인터넷 자물쇠(RSA)", "큰 소수 두 개의 곱을 공개하는 암호. 쪼개기가 어려워 안전", "s2"),
             ("데이터 서랍(해시)", "번호의 나머지로 자료를 나눠 넣는 방법. 서랍 수가 소수면 고르게", "s2"),
             ("소수 비율", "어디까지 중 소수가 차지하는 비율. 100만까지 7.8%", "s3"),
             ("어림 공식", "세지 않고 소수 개수를 맞히는 식. 100만에서 0.17% 차이", "s4"),
             ("약속 범위", "√x × ln x ÷ 8π. 리만 가설이 참이면 빗나감은 늘 이 안", "s5"),
             ("리만 가설", "소수 개수 어림의 빗나감이 영원히 약속 범위 안에 있다는 약속", "s5"),
             ("특별한 점·가운데 줄", "제타 함수의 영점과 임계선. 모두 줄 위면 약속이 지켜진다", "s5"),
             ("소수 간격", "소수와 다음 소수 사이 거리. 100만 아래 최대 114", "s6"),
             ("Lean", "증명을 컴퓨터가 한 줄씩 검사하게 하는 언어", "s6")]
    kg = "".join(f'<div class="kg-item"><span class="t">개념</span><b>{E(a)}</b>{E(b)}<br><a href="#{c}">본문으로</a></div>' for a, b, c in terms)
    pack = json.dumps({"title": "하루의 첫 브리핑 — 리만 가설은 '약속'이다", "author": "안상선", "date": "2026-11-22",
                       "concepts": [{"name": a, "definition": b, "anchor": c} for a, b, c in terms],
                       "order": [t for _, _, t in STEPS]}, ensure_ascii=False)
    s += f'''<section class="room" id="outro"><div class="wrap"><span class="roomno">아웃트로</span><h2>브리핑을 마치며</h2>
{scene("scene_outro", "물컵을 든 하루가 안도하고, 이긴 모아와 웃는 시아, 꽃가루를 뿌리는 X1~X3")}
{talk([("haru", "e12", "후… 끝났다! 다들 끝까지 들어 줘서 고마워요."),
       ("doctor", "e16", "첫 브리핑 치고 아주 좋았어요. 오늘의 한 줄 — 소수는 숫자의 블록이고, 리만 가설은 그 블록이 어디에 얼마나 있는지에 대한 약속입니다."),
       ("moa", "e16", "왜 대단한지 이제 알겠어요. 160년 넘게 아무도 그 약속을 증명하지 못했던 거네요."),
       ("sia", "e01", "다음엔 특별한 점들이 왜 가운데 줄에 서는지 듣고 싶어요!")])}
{react([("x1", "e01", "하루 최고!"), ("x2", "e16", "물 마셔, 물!"), ("x3", "e01", "(꽃다발 건네는 시늉)")])}
<div class="cards"><div class="card soon">{face("haru", "e19")}<span class="n">다음 편 · 준비 중</span><h3>특별한 점들은 왜 가운데 줄에 설까</h3><p>소수 개수 그래프를 여러 겹의 흔들림으로 나눠 보는 이야기. 힐베르트 공간 해설의 "물결 조각으로 나누기"와 이어집니다.</p></div>
<a class="card" href="https://adminmrobo.github.io/hilbert_space_lab/">{face("moa", "e09")}<span class="n">함께 보기</span><h3>힐베르트 공간 해설</h3><p>1 + 1/4 + 1/9 + … = π²/6 이 나오는 5번 방.</p></a></div></div></section>
<section class="room" id="kg"><div class="wrap"><h2>지식 색인</h2><input class="kg-search" id="kg-q" placeholder="찾을 말 (예: 약속)"><div class="kg-list">{kg}</div>
<h3>꾸러미</h3><p>이 페이지의 개념·순서를 JSON으로 내려받아 다른 해설과 이어 쓸 수 있습니다.</p>
<div class="exp-btns"><a class="btn" download="riemann_briefing_pack.json" href="data:application/json;charset=utf-8,{urllib.parse.quote(pack)}">꾸러미 내려받기 (JSON)</a></div>
<div class="next"><a href="index.html">← 목차로</a><a href="#s1">처음부터 다시 ↑</a></div></div></section>
{FOOT}<script src="assets/rh.js"></script></body></html>'''
    (ROOT / "briefing.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    build_briefing()
    print("built index.html, briefing.html")
