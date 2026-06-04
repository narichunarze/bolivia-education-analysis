import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv("educacion_bolivia_limpio.csv")

# ============================================================
# ANALYSIS A — Enrollment: Public vs Private over time
# ============================================================
df_sector = df[
    (df["indicator"]  == "Poblacion Matriculada") &
    (df["department"] == "BOLIVIA") &
    (df["sector"].isin(["Público", "Privado"])) &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total")
].sort_values("year")

# Rename sectors for display
df_sector = df_sector.copy()
df_sector["sector"] = df_sector["sector"].map({"Público": "Public", "Privado": "Private"})

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left chart: enrollment trend lines
for sector, color in [("Public", "#1a6faf"), ("Private", "#E05C2A")]:
    d = df_sector[df_sector["sector"] == sector]
    axes[0].plot(d["year"], d["value"], marker="o", label=sector, color=color, linewidth=2)

axes[0].set_title("Enrollment by Sector (2011–2024)")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Students (thousands)")
axes[0].legend()
axes[0].grid(axis="y", alpha=0.3)
axes[0].set_xticks(d["year"])
axes[0].tick_params(axis="x", rotation=45)

# Right chart: percentage share per year
pivot = df_sector.pivot_table(index="year", columns="sector", values="value")
pivot["total"]       = pivot["Public"] + pivot["Private"]
pivot["pct_public"]  = pivot["Public"]  / pivot["total"] * 100
pivot["pct_private"] = pivot["Private"] / pivot["total"] * 100

axes[1].stackplot(pivot.index,
                  pivot["pct_public"], pivot["pct_private"],
                  labels=["Public", "Private"],
                  colors=["#1a6faf", "#E05C2A"], alpha=0.8)
axes[1].set_title("Share of Enrollment: Public vs Private (%)")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("% of total enrollment")
axes[1].legend(loc="center right")
axes[1].set_xticks(pivot.index)
axes[1].tick_params(axis="x", rotation=45)
axes[1].grid(axis="y", alpha=0.3)

plt.suptitle("Bolivia Student Enrollment: Public vs Private", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig("A_enrollment_by_sector.png", dpi=150)
plt.show()
print("✓ Chart A saved")

# ============================================================
# ANALYSIS B — Dropout rate: Public vs Private over time
# ============================================================
df_b = df[
    (df["indicator"]  == "Tasa Abandono") &
    (df["department"] == "BOLIVIA") &
    (df["sector"].isin(["Público", "Privado"])) &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total")
].sort_values("year").copy()

df_b["sector"] = df_b["sector"].map({"Público": "Public", "Privado": "Private"})

fig, ax = plt.subplots(figsize=(10, 5))
for sector, color in [("Public", "#1a6faf"), ("Private", "#E05C2A")]:
    d = df_b[df_b["sector"] == sector]
    ax.plot(d["year"], d["value"], marker="o", label=sector, color=color, linewidth=2)

ax.axvline(x=2020, color="gray", linestyle="--", alpha=0.6)
ax.text(2020.1, df_b["value"].max() * 0.97, "COVID-19", fontsize=9, color="gray")
ax.set_title("Dropout Rate: Public vs Private — Bolivia (2012–2024)")
ax.set_xlabel("Year")
ax.set_ylabel("Rate (%)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("B_dropout_by_sector.png", dpi=150)
plt.show()
print("✓ Chart B saved")

# ============================================================
# ANALYSIS C — Dropout gap by department in 2024
# ============================================================
df_c = df[
    (df["indicator"]  == "Tasa Abandono") &
    (df["department"] != "BOLIVIA") &
    (df["sector"].isin(["Público", "Privado"])) &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total") &
    (df["year"]       == 2024)
].copy()

df_c["sector"] = df_c["sector"].map({"Público": "Public", "Privado": "Private"})

df_c = df_c.pivot_table(
    index="department", columns="sector", values="value"
).sort_values("Public")

x = range(len(df_c))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.barh([i - width/2 for i in x], df_c["Public"],
                height=width, label="Public", color="#1a6faf")
bars2 = ax.barh([i + width/2 for i in x], df_c["Private"],
                height=width, label="Private", color="#E05C2A")

ax.set_yticks(list(x))
ax.set_yticklabels(df_c.index)
ax.bar_label(bars1, fmt="%.1f%%", padding=3, fontsize=8)
ax.bar_label(bars2, fmt="%.1f%%", padding=3, fontsize=8)
ax.set_title("Dropout Rate: Public vs Private by Department (2024)")
ax.set_xlabel("Rate (%)")
ax.legend()
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("C_dropout_sector_by_dept.png", dpi=150)
plt.show()
print("✓ Chart C saved")

# ============================================================
# ANALYSIS D — Pass rate: Public vs Private over time
# ============================================================
df_d = df[
    (df["indicator"]  == "Tasa Promovidos") &
    (df["department"] == "BOLIVIA") &
    (df["sector"].isin(["Público", "Privado"])) &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total")
].sort_values("year").copy()

df_d["sector"] = df_d["sector"].map({"Público": "Public", "Privado": "Private"})

fig, ax = plt.subplots(figsize=(10, 5))
for sector, color in [("Public", "#1a6faf"), ("Private", "#E05C2A")]:
    d = df_d[df_d["sector"] == sector]
    ax.plot(d["year"], d["value"], marker="o", label=sector, color=color, linewidth=2)

ax.axvline(x=2020, color="gray", linestyle="--", alpha=0.6)
ax.text(2020.1, df_d["value"].max() * 0.997, "COVID-19", fontsize=9, color="gray")
ax.set_title("Pass Rate: Public vs Private — Bolivia (2012–2024)")
ax.set_xlabel("Year")
ax.set_ylabel("Rate (%)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("D_pass_rate_by_sector.png", dpi=150)
plt.show()
print("✓ Chart D saved")