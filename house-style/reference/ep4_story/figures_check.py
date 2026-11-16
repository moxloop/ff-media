"""Figures check for Episode 04, first ~3 minutes (script + storyboard). Run: python3 figures_check.py"""
P, YEARS, RATE, EXTRA = 200_000.0, 25, 0.05, 100.0
N, r = YEARS * 12, RATE / 12

# --- the mortgage (Episodes 01/03) ---
PAY = round(P * r / (1 - (1 + r) ** -N), 2)
assert PAY == 1169.18
assert round(P * r, 2) == 833.33                      # month-one interest
INT0 = PAY * N - P                                    # interest with no overpayment
assert round(INT0, -1) == 150_750                     # "about £150,750" (Episode 03 wording)

# --- Option A: overpay £100 a month ---
def overpay():
    bal, m, interest, last = P, 0, 0.0, 0.0
    while bal > 0.005:
        m += 1; i = bal * r; interest += i
        last = min(PAY + EXTRA, bal + i); bal = bal + i - last
    return m, interest, last
END_M, INT_A, LAST = overpay()
assert END_M == 258                                   # mortgage ends month 258
assert N - END_M == 42 and (N - END_M) / 12 == 3.5    # 3½ years early
SAVED = INT0 - INT_A
assert 24_500 <= SAVED < 24_600, SAVED                # "about £24,500 less interest" (Episode 03)
FREED = round(PAY + EXTRA, 2)
assert FREED == 1269.18

# --- guaranteed-return scene: £100 off a 5% debt ---
assert round(100 * RATE, 2) == 5.00                   # "about five pounds a year" per £100 overpaid
assert round(100 * RATE / 12, 2) == 0.42              # 42p less interest the very next month

# --- same money out of pocket either way ---
assert round(EXTRA * N) == 30_000                     # £100 x 300 months
out_B = FREED * N                                     # B: £1,169.18 mortgage + £100 invested, 300 months
out_A = FREED * (END_M - 1) + LAST + (FREED - LAST) + FREED * (N - END_M)
assert abs(out_A - out_B) < 0.01                      # A and B spend identical amounts every month

# --- head-to-head pots at month 300 (nominal monthly compounding, paid in at month end) ---
def pot_B(g):
    k = g / 12; return EXTRA * ((1 + k) ** N - 1) / k
def pot_A(g):
    k, pot = g / 12, 0.0
    for m in range(END_M, N + 1):                     # month 258: what is left of £1,269.18 after the final payment
        pot = pot * (1 + k) + (FREED - LAST if m == END_M else FREED)
    return pot
# The brief's table. Its B column is right. Its A column is NOT like-for-like: it invests only months 259-300
# and drops the £1,199.70 left over in month 258 (the final mortgage payment is only £69.48), so A pays in
# £1,199.70 less than B. Corrected A invests that leftover in month 258, so both spend £1,269.18 every month.
BRIEF = {0.04: (57_115, 51_413), 0.05: (58_122, 59_551), 0.06: (59_152, 69_299), 0.07: (60_205, 81_007)}
CORRECT_A = {0.04: 58_495, 0.05: 59_551, 0.06: 60_631, 0.07: 61_737}
assert round(LAST, 2) == 69.48 and round(FREED - LAST, 2) == 1199.70
for g, (a_brief, b) in BRIEF.items():
    k = g / 12
    assert round(FREED * ((1 + k) ** 42 - 1) / k) == a_brief      # reproduces the brief's A (leftover dropped)
    assert round(pot_B(g)) == b                                   # brief's B confirmed
    assert round(pot_A(g)) == CORRECT_A[g], (g, pot_A(g))         # like-for-like A
    assert round(pot_A(g)) - a_brief > 1_300                      # brief understates A by £1,380-£1,532

# --- figures voiced / shown in the first three minutes (corrected) ---
A4, A5, A6, A7 = (CORRECT_A[g] for g in (0.04, 0.05, 0.06, 0.07))
B4, B5, B6, B7 = (BRIEF[g][1] for g in (0.04, 0.05, 0.06, 0.07))
assert B6 - A6 == 8_668                               # hook: investing ahead "about eight thousand, seven hundred pounds" (brief: £10,147)
assert A4 - B4 == 7_082                               # hook: overpaying ahead "about seven thousand" (brief: £5,702)
assert abs(pot_A(0.05) - pot_B(0.05)) < 1.00          # dead level at 5%: the deciding number IS the mortgage rate (brief: B ahead £1,429)
assert B7 - B6 == 11_708                              # fees scene: "nearly twelve thousand pounds, gone to fees"
assert (B7, B6) == (81_007, 69_299)                   # "about eighty-one thousand" / "about sixty-nine thousand, three hundred"
assert round(0.07 - 0.01, 4) == 0.06                  # 7% growth, 1% charges, keep 6%
print("fees bars: 7%% 1.000  6%% %.3f of full width" % (B6 / B7))

# --- break-even return (brief says "about 4.9%") ---
lo, hi = 0.04, 0.06
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if pot_A(mid) > pot_B(mid) else (lo, mid)
assert abs(lo - 0.05) < 1e-5, lo                      # exactly 5.00% (brief says "about 4.9%", an artefact of the dropped leftover)
print(f"PAY {PAY}  end month {END_M}  last payment {LAST:.2f}  interest saved {SAVED:,.2f}  break-even {lo*100:.2f}%")

# --- narration length ---
import os
sp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script.txt")
if os.path.exists(sp):
    tot = 0
    for line in open(sp, encoding="utf-8"):
        if "|" not in line: continue
        k, t = line.strip().split("|", 1); n = len(t.split()); tot += n
        print(f"{k:10s} {n:4d} words  ~{n / 155 * 60:5.1f} s")
        for bad in ("ISA", "SIPP", "401", "Moxloop", "£"): assert bad not in t, (k, bad)
    print(f"total {tot} words  ~{tot / 155 * 60:.0f} s narration")
    assert 165 <= tot / 155 * 60 <= 195
print("ALL FIGURES OK")
