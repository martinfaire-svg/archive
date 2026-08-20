# -*- coding: utf-8 -*-
import warnings; warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
import yfinance as yf

FONT_OTF = "/tmp/NotoKR_raw.otf"
fp = font_manager.FontProperties(fname=FONT_OTF)
font_manager.fontManager.addfont(FONT_OTF)
matplotlib.rcParams["font.family"] = fp.get_name()
matplotlib.rcParams["axes.unicode_minus"] = False
PERIOD = "1mo"

def get(t):
    df = yf.download(t, period=PERIOD, interval="1d", progress=False)
    return df["Close"].dropna()

def style_axis(ax):
    for lbl in ax.get_xticklabels():
        lbl.set_fontproperties(fp); lbl.set_fontsize(8); lbl.set_rotation(20)
    for lbl in ax.get_yticklabels():
        lbl.set_fontproperties(fp); lbl.set_fontsize(8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))

def chart_kospi(outpath):
    ks, kq = get("^KS11"), get("^KQ11")
    fig, ax = plt.subplots(figsize=(7.8, 3.9), dpi=150)
    ax2 = ax.twinx()
    c1, c2 = "#0f3057", "#e63946"
    l1, = ax.plot(ks.index, ks.values, color=c1, lw=1.9, marker="o", ms=2.6, label="코스피")
    l2, = ax2.plot(kq.index, kq.values, color=c2, lw=1.9, marker="o", ms=2.6, label="코스닥")
    ax.set_ylabel("코스피", fontproperties=fp, fontsize=9, color=c1)
    ax2.set_ylabel("코스닥", fontproperties=fp, fontsize=9, color=c2)
    ax.tick_params(axis="y", colors=c1); ax2.tick_params(axis="y", colors=c2)
    for s, c, a in [(ks, c1, ax), (kq, c2, ax2)]:
        a.annotate(f"{float(s.iloc[-1]):,.0f}", xy=(s.index[-1], float(s.iloc[-1])),
                   xytext=(4, 5), textcoords="offset points", fontproperties=fp, fontsize=8, color=c)
    ax.set_title("코스피·코스닥 — 최근 1개월 (실제 지수)", fontproperties=fp, fontsize=12, color="#1a1a2e")
    ax.set_xlabel(""); ax.grid(True, alpha=0.22); style_axis(ax)
    for lbl in ax2.get_yticklabels(): lbl.set_fontproperties(fp); lbl.set_fontsize(8)
    ax.legend([l1, l2], ["코스피", "코스닥"], prop=fp, fontsize=9,
              loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False)
    fig.tight_layout(); fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)

def chart_index(outpath):
    dow, nas, sp = get("^DJI"), get("^IXIC"), get("^GSPC")
    fig, ax = plt.subplots(figsize=(7.8, 3.9), dpi=150)
    ax2 = ax.twinx(); ax3 = ax.twinx()
    ax3.spines["right"].set_position(("outward", 52))
    c1, c2, c3 = "#1f4e79", "#e63946", "#2a9d8f"
    l1, = ax.plot(dow.index, dow.values, color=c1, lw=1.8, marker="o", ms=2.4, label="다우존스30")
    l2, = ax2.plot(nas.index, nas.values, color=c2, lw=1.8, marker="o", ms=2.4, label="나스닥종합")
    l3, = ax3.plot(sp.index, sp.values, color=c3, lw=1.8, marker="o", ms=2.4, label="S&P500")
    ax.set_ylabel("다우존스30", fontproperties=fp, fontsize=9, color=c1)
    ax2.set_ylabel("나스닥종합", fontproperties=fp, fontsize=9, color=c2)
    ax3.set_ylabel("S&P500", fontproperties=fp, fontsize=9, color=c3)
    ax.tick_params(axis="y", colors=c1); ax2.tick_params(axis="y", colors=c2); ax3.tick_params(axis="y", colors=c3)
    for a, s, c in [(ax, dow, c1), (ax2, nas, c2), (ax3, sp, c3)]:
        a.annotate(f"{float(s.iloc[-1]):,.0f}", xy=(s.index[-1], float(s.iloc[-1])),
                   xytext=(3, 6), textcoords="offset points", fontproperties=fp, fontsize=7.5, color=c)
    ax.set_title("미국 3대 지수 — 최근 1개월 (실제 값)", fontproperties=fp, fontsize=12, color="#1a1a2e")
    ax.set_xlabel(""); ax.grid(True, alpha=0.22); style_axis(ax)
    for a in (ax2, ax3):
        for lbl in a.get_yticklabels(): lbl.set_fontproperties(fp); lbl.set_fontsize(8)
    ax.legend([l1, l2, l3], ["다우존스30", "나스닥종합", "S&P500"], prop=fp, fontsize=9,
              loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False)
    fig.tight_layout(); fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)

def chart_fx_oil(outpath):
    br, wti, krw = get("BZ=F"), get("CL=F"), get("KRW=X")
    fig, ax = plt.subplots(figsize=(7.8, 3.9), dpi=150)
    ax2 = ax.twinx()
    cbr, cwti, ckrw = "#e07a00", "#c9a227", "#333333"
    l1, = ax2.plot(br.index, br.values, color=cbr, lw=1.8, marker="o", ms=2.4, label="브렌트유")
    l2, = ax2.plot(wti.index, wti.values, color=cwti, lw=1.8, marker="o", ms=2.4, label="WTI")
    l3, = ax.plot(krw.index, krw.values, color=ckrw, lw=1.8, marker="o", ms=2.4, label="원/달러")
    ax.set_ylabel("원/달러 (원)", fontproperties=fp, fontsize=9, color=ckrw)
    ax2.set_ylabel("국제유가 (달러)", fontproperties=fp, fontsize=9, color="#b06a00")
    ax.tick_params(axis="y", colors=ckrw)
    for s, c, a in [(br, cbr, ax2), (wti, cwti, ax2), (krw, ckrw, ax)]:
        v = float(s.iloc[-1])
        a.annotate(f"{v:,.2f}" if v < 1000 else f"{v:,.0f}", xy=(s.index[-1], v),
                   xytext=(3, 5), textcoords="offset points", fontproperties=fp, fontsize=7.5, color=c)
    ax.set_title("국제유가·원달러 환율 — 최근 1개월 (실제 값)", fontproperties=fp, fontsize=12, color="#1a1a2e")
    ax.set_xlabel(""); ax.grid(True, alpha=0.22); style_axis(ax)
    for lbl in ax2.get_yticklabels(): lbl.set_fontproperties(fp); lbl.set_fontsize(8)
    ax.legend([l3, l1, l2], ["원/달러", "브렌트유(달러)", "WTI(달러)"], prop=fp, fontsize=9,
              loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False)
    fig.tight_layout(); fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)

def chart_vix(outpath):
    vix = get("^VIX")
    fig, ax = plt.subplots(figsize=(7.8, 3.2), dpi=150)
    c = "#8338ec"
    vals = vix.to_numpy().ravel()  # fill_between용 1-d 배열 필수
    ax.plot(vix.index, vals, color=c, lw=1.8, marker="o", ms=2.6, label="VIX 공포지수")
    ax.fill_between(vix.index, vals, vals.min() * 0.97, color=c, alpha=0.08)
    v = float(vals[-1])
    ax.annotate(f"{v:.2f}", xy=(vix.index[-1], v), xytext=(4, 4), textcoords="offset points",
                fontproperties=fp, fontsize=8, color=c)
    ax.set_title("VIX 공포지수 — 최근 1개월 (실제 값)", fontproperties=fp, fontsize=12, color="#1a1a2e")
    ax.set_ylabel("VIX (지수)", fontproperties=fp, fontsize=9, color=c)
    ax.set_xlabel(""); ax.tick_params(axis="y", colors=c)
    ax.grid(True, alpha=0.22); style_axis(ax)
    fig.tight_layout(); fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)
    print(f"VIX {v:.2f} (최저 {float(vix.min()):.2f} · 최고 {float(vix.max()):.2f})")

import pandas as pd

def _s(t):  # yfinance 단일 시리즈 (tz 제거)
    d = yf.download(t, period=PERIOD, interval="1d", progress=False)["Close"].dropna()
    s = d.squeeze(); s.index = pd.to_datetime(s.index).tz_localize(None); return s

def chart_bond(outpath, csv_path):
    m3, y2, us10, us30 = _s("^IRX"), _s("2YY=F"), _s("^TNX"), _s("^TYX")
    kr = pd.read_csv(csv_path, parse_dates=["date"])
    fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=150)
    ax.plot(m3.index, m3.values, color="#e67e22", lw=1.6, marker="o", ms=2.2, label="미 3개월")
    ax.plot(y2.index, y2.values, color="#d35400", lw=1.6, marker="o", ms=2.2, label="미 2년")
    ax.plot(us10.index, us10.values, color="#c0392b", lw=1.8, marker="o", ms=2.2, label="미 10년")
    ax.plot(us30.index, us30.values, color="#7b241c", lw=1.8, marker="o", ms=2.2, label="미 30년")
    ax.plot(kr["date"], kr["kr3y"], color="#1f4e79", lw=1.6, ls="--", marker="s", ms=2.8, label="국고 3년")
    ax.plot(kr["date"], kr["kr10y"], color="#2471a3", lw=1.6, ls="--", marker="s", ms=2.8, label="국고 10년")
    ax.plot(kr["date"], kr["kr30y"], color="#5dade2", lw=1.6, ls="--", marker="s", ms=2.8, label="국고 30년")
    for s, c in [(m3, "#e67e22"), (y2, "#d35400"), (us10, "#c0392b"), (us30, "#7b241c")]:
        ax.annotate(f"{float(s.iloc[-1]):.2f}", xy=(s.index[-1], float(s.iloc[-1])), xytext=(4, 2), textcoords="offset points", fontproperties=fp, fontsize=6.5, color=c)
    for col, c in [("kr3y", "#1f4e79"), ("kr10y", "#2471a3"), ("kr30y", "#5dade2")]:
        v = float(kr[col].iloc[-1]); ax.annotate(f"{v:.2f}", xy=(kr["date"].iloc[-1], v), xytext=(4, -8), textcoords="offset points", fontproperties=fp, fontsize=6.5, color=c)
    ax.set_title("한·미 국채 금리 — 최근 1개월 (실제 값, %)", fontproperties=fp, fontsize=12, color="#1a1a2e")
    ax.set_ylabel("금리 (%)", fontproperties=fp, fontsize=9); ax.set_xlabel("")
    ax.grid(True, alpha=0.22); style_axis(ax)
    ax.legend(prop=fp, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)
    fig.tight_layout(); fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)

def chart_spread(outpath, csv_path):
    m3, us10 = _s("^IRX"), _s("^TNX")
    kr = pd.read_csv(csv_path, parse_dates=["date"])
    df = pd.concat([m3.rename("m3"), us10.rename("us10")], axis=1).dropna()
    us_sp = df["us10"] - df["m3"]; kr_sp = kr["kr10y"] - kr["kr3y"]
    fig, ax = plt.subplots(figsize=(7.8, 3.2), dpi=150); c = "#16a085"
    ax.plot(us_sp.index, us_sp.values, color=c, lw=1.9, marker="o", ms=2.6, label="미 10년-3개월")
    ax.fill_between(us_sp.index, us_sp.values, 0, color=c, alpha=0.08)
    ax.axhline(0, color="#888", lw=0.8, ls=":")
    ax.plot(kr["date"], kr_sp, color="#2471a3", lw=1.6, ls="--", marker="s", ms=2.8, label="국고 10년-3년")
    ax.annotate(f"{float(us_sp.iloc[-1]):.2f}%p", xy=(us_sp.index[-1], float(us_sp.iloc[-1])), xytext=(4, 4), textcoords="offset points", fontproperties=fp, fontsize=7.5, color=c)
    ax.annotate(f"{float(kr_sp.iloc[-1]):.2f}%p", xy=(kr["date"].iloc[-1], float(kr_sp.iloc[-1])), xytext=(4, -9), textcoords="offset points", fontproperties=fp, fontsize=7.5, color="#2471a3")
    ax.set_title("장단기 금리차 — 최근 1개월 (%p)", fontproperties=fp, fontsize=12, color="#1a1a2e")
    ax.set_ylabel("금리차 (%p)", fontproperties=fp, fontsize=9); ax.set_xlabel("")
    ax.grid(True, alpha=0.22); style_axis(ax)
    ax.legend(prop=fp, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False)
    fig.tight_layout(); fig.savefig(outpath, bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
    csv = sys.argv[2] if len(sys.argv) > 2 else f"{out}/bond_kr.csv"
    chart_kospi(f"{out}/chart_kospi.png")
    chart_index(f"{out}/chart_index.png")
    chart_fx_oil(f"{out}/chart_fx_oil.png")
    chart_vix(f"{out}/chart_vix.png")
    chart_bond(f"{out}/chart_bond.png", csv)
    chart_spread(f"{out}/chart_spread.png", csv)
    print("DONE")
