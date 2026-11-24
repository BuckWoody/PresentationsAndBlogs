"""
Builds the chart images used in Module 04 (written to ../modules/images).
Needs: Python 3.9 or later and matplotlib. Reads lantern_clean.sqlite and supplements/anscombe.csv.
"""
import csv
import os
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "modules", "images")
os.makedirs(OUT, exist_ok=True)
con = sqlite3.connect(os.path.join(HERE, "lantern_clean.sqlite"))

BLUE, ORANGE, GRAY = "#1b20a1", "#d95f02", "#6b6b6b"

# ---- 1 and 2: average order value by acquisition channel, same data, two axes
rows = con.execute("""SELECT c.acquisition_channel, ROUND(AVG(o.order_total),2)
FROM orders o JOIN customers c USING(customer_id)
WHERE o.status='shipped' AND c.customer_type='consumer' GROUP BY 1 ORDER BY 1""").fetchall()
labels = [r[0].replace("_", " ") for r in rows]
vals = [r[1] for r in rows]

fig, ax = plt.subplots(figsize=(6.4, 4))
ax.bar(labels, vals, color=[BLUE, ORANGE, BLUE])
ax.set_ylim(min(vals) - 2, max(vals) + 1)
ax.set_title("Email customers are our big spenders!", fontsize=14, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "aov_channel_misleading.png"), dpi=130)
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.4, 4))
bars = ax.bar(labels, vals, color=BLUE)
ax.set_ylim(0, 300)
ax.set_ylabel("Average order value (US dollars)")
ax.set_title("Average order value by acquisition channel\nConsumer orders, 2023 to 2025: about $228 to $230 in every channel", fontsize=11)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 5, "$%.2f" % v, ha="center", fontsize=10)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "aov_channel_honest.png"), dpi=130)
plt.close(fig)

# ---- 3: Anscombe's quartet
data = {}
with open(os.path.join(HERE, "supplements", "anscombe.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        data.setdefault(r["dataset"], []).append((float(r["x"]), float(r["y"])))
fig, axes = plt.subplots(2, 2, figsize=(7, 5.5), sharex=True, sharey=True)
for ax, name in zip(axes.flat, ["I", "II", "III", "IV"]):
    xs, ys = zip(*data[name])
    ax.scatter(xs, ys, color=BLUE)
    ax.plot([3, 20], [3 + 0.5 * 3, 3 + 0.5 * 20], color=GRAY, linewidth=1)  # the shared fitted line, y = 3 + 0.5x
    ax.set_title("Dataset " + name, fontsize=11)
    ax.set_xlim(3, 20)
    ax.set_ylim(2, 14)
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle("Anscombe's quartet: same mean, same spread, same correlation (0.82)", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "anscombe_quartet.png"), dpi=130)
plt.close(fig)

# ---- 4: seasonality, monthly net revenue by year (finance report)
fin = {}
with open(os.path.join(HERE, "raw", "finance_monthly_revenue.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        fin[r["month"]] = float(r["net_revenue"])
fig, ax = plt.subplots(figsize=(7, 4))
for year, color in (("2023", GRAY), ("2024", ORANGE), ("2025", BLUE)):
    ys = [fin.get("%s-%02d" % (year, m), None) for m in range(1, 13)]
    ax.plot(range(1, 13), [y / 1000 if y is not None else None for y in ys], marker="o", color=color, label=year)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_ylabel("Net revenue (thousands of US dollars)")
ax.set_title("Lantern Peak net revenue by month: the holiday peak repeats every year", fontsize=11)
ax.legend(title="Year", frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "seasonality_by_year.png"), dpi=130)
plt.close(fig)
print("wrote images to", OUT, sorted(os.listdir(OUT)))
