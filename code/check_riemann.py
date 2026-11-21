"""리만 가설 입문 — 페이지에 나오는 숫자 검산.
실행: python3 code/check_riemann.py   (필요: sympy, mpmath)
모든 항목이 OK면 끝에 ALL OK를 찍는다.
"""
import math
import mpmath as mp
import sympy as sp

mp.mp.dps = 25
bad = []


def ok(name, got, want, tol=0):
    good = abs(got - want) <= tol if isinstance(want, (int, float)) else got == want
    print(("OK  " if good else "FAIL"), name, "->", got, "(기대", want, ")")
    if not good:
        bad.append(name)


# 1단계 — 레고 블록
ok("12 = 2*2*3", sp.factorint(12), {2: 2, 3: 1})
ok("30까지 소수 개수", len(list(sp.primerange(2, 31))), 10)
ok("100까지 소수 개수", int(sp.primepi(100)), 25)

# 2단계 — 쓰임
ok("61*53", 61 * 53, 3233)
ok("10,20..100 mod 10 모두 0", [k % 10 for k in range(10, 101, 10)], [0] * 10)
ok("10,20..100 mod 11 모두 다름", len({k % 11 for k in range(10, 101, 10)}), 10)
ok("2^1024 자릿수", len(str(2 ** 1024)), 309)
ok("2^2048 자릿수", len(str(2 ** 2048)), 617)
ok("1024비트 크기에서 홀수 중 소수 비율 1/x", round(1024 * math.log(2) / 2), 355)
ok("매미 17과 2..6 최소공배수", [math.lcm(17, k) for k in range(2, 7)], [34, 51, 68, 85, 102])
ok("매미 12와 2..6 최소공배수", [math.lcm(12, k) for k in range(2, 7)], [12, 12, 12, 60, 12])

# 3단계 — 드물어진다
for x, want in [(1000, 168), (10 ** 4, 1229), (10 ** 5, 9592), (10 ** 6, 78498)]:
    ok(f"pi({x})", int(sp.primepi(x)), want)
ok("100만에서 몇 개 중 1개", round(10 ** 6 / 78498), 13)

# 4단계 — 어림
ok("li(1e4)", round(float(mp.li(10 ** 4))), 1246)
ok("li(1e6)", round(float(mp.li(10 ** 6))), 78628)
ok("1e4/ln", round(10 ** 4 / math.log(10 ** 4)), 1086)
ok("1e6/ln", round(10 ** 6 / math.log(10 ** 6)), 72382)
ok("li(1e6)-pi(1e6)", round(float(mp.li(10 ** 6)) - 78498), 130)

# 5단계 — 약속 범위 (쇤펠트 1976, x >= 2657)
bound = lambda x: math.sqrt(x) * math.log(x) / (8 * math.pi)
ok("약속 범위 at 1e6", round(bound(10 ** 6)), 550)
ok("첫 특별한 점 높이", round(float(mp.zetazero(1).imag), 2), 14.13)
ok("zeta(1/2)", round(float(mp.zeta(0.5)), 2), -1.46)
# 2657..1e6 구간에서 실제로 범위 안인지 1000 간격으로 확인
pis = list(sp.primerange(2, 10 ** 6 + 1))
import bisect
inside = all(abs(float(mp.li(x)) - bisect.bisect_right(pis, x)) < bound(x) for x in range(3000, 10 ** 6 + 1, 997))
ok("2657 이후 100만까지 범위 안(표본 점검)", inside, True)

# 6단계 — 좋은 점
gaps = max((pis[i + 1] - pis[i], pis[i]) for i in range(len(pis) - 1))
ok("100만 아래 최대 간격", gaps, (114, 492113))

# 대결
ok("시아 1만", round(10 ** 4 / math.log(10 ** 4)), 1086)
ok("모아 1만", round(float(mp.li(10 ** 4))), 1246)

print("\nALL OK" if not bad else f"\nFAILED: {bad}")
