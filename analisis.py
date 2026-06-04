import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv("educacion_bolivia_limpio.csv")

# Consistent color palette per department
DEPT_COLORS = {
    "Chuquisaca": "#E05C2A", "La Paz":     "#1a6faf", "Cochabamba": "#4CAF50",
    "Oruro":      "#9C27B0", "Potosí":     "#FF9800", "Tarija":     "#00BCD4",
    "Santa Cruz": "#F44336", "Beni":       "#795548", "Pando":      "#607D8B"
}

# ============================================================
# ANALYSIS 1 — National enrollment trend
# ============================================================
df1 = df[
    (df["indicator"]  == "Poblacion Matriculada") &
    (df["department"] == "BOLIVIA") &
    (df["sector"]     == "Total") &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total")
].sort_values("year")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df1["year"], df1["value"], marker="o", color="#1a6faf", linewidth=2)
ax.fill_between(df1["year"], df1["value"], alpha=0.1, color="#1a6faf")
ax.axvline(x=2020, color="gray", linestyle="--", alpha=0.6)
ax.text(2020.1, df1["value"].max() * 0.98, "COVID-19", fontsize=9, color="gray")
ax.set_title("Total Student Enrollment in Bolivia (2011–2024)", fontsize=13, pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("Students (thousands)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.set_xticks(df1["year"])
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("01_national_enrollment.png", dpi=150)
plt.show()
print("✓ Chart 1 saved")

# ============================================================
# ANALYSIS 2 — Gender gap in dropout rate
# ============================================================
df2 = df[
    (df["indicator"]  == "Tasa Abandono") &
    (df["department"] == "BOLIVIA") &
    (df["sector"]     == "Total") &
    (df["nivel"]      == "Total") &
    (df["gender"].isin(["Hombres", "Mujeres"]))
].sort_values("year")

# Rename for display
df2 = df2.copy()
df2["gender"] = df2["gender"].map({"Hombres": "Male", "Mujeres": "Female"})

fig, ax = plt.subplots(figsize=(10, 5))
gender_colors = {"Male": "#2196F3", "Female": "#E91E8C"}
for gender, color in gender_colors.items():
    d = df2[df2["gender"] == gender]
    ax.plot(d["year"], d["value"], marker="o", label=gender, color=color, linewidth=2)

ax.axvline(x=2020, color="gray", linestyle="--", alpha=0.6)
ax.text(2020.1, df2["value"].max() * 0.99, "COVID-19", fontsize=9, color="gray")
ax.set_title("School Dropout Rate by Gender — Bolivia (2012–2024)", fontsize=13, pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("Rate (%)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("02_dropout_by_gender.png", dpi=150)
plt.show()
print("✓ Chart 2 saved")

# ============================================================
# ANALYSIS 3 — Dropout by department in 2024
# ============================================================
df3 = df[
    (df["indicator"]  == "Tasa Abandono") &
    (df["department"] != "BOLIVIA") &
    (df["sector"]     == "Total") &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total") &
    (df["year"]       == 2024)
].sort_values("value", ascending=True)

bar_colors = [DEPT_COLORS.get(d, "#999") for d in df3["department"]]

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.barh(df3["department"], df3["value"], color=bar_colors)
ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=9)
ax.set_title("School Dropout Rate by Department (2024)", fontsize=13, pad=12)
ax.set_xlabel("Rate (%)")
ax.grid(axis="x", alpha=0.3)
ax.set_xlim(0, df3["value"].max() * 1.2)
plt.tight_layout()
plt.savefig("03_dropout_by_dept_2024.png", dpi=150)
plt.show()
print("✓ Chart 3 saved")

# ============================================================
# ANALYSIS 4 — COVID-19 impact across all indicators
# ============================================================
indicator_colors = {
    "Tasa Efectivos":  "#2196F3",
    "Tasa Promovidos": "#4CAF50",
    "Tasa Reprobados": "#FF9800",
    "Tasa Abandono":   "#F44336",
}
indicator_labels = {
    "Tasa Efectivos":  "Attendance Rate",
    "Tasa Promovidos": "Pass Rate",
    "Tasa Reprobados": "Failure Rate",
    "Tasa Abandono":   "Dropout Rate",
}

fig, ax = plt.subplots(figsize=(11, 6))
for indicator, color in indicator_colors.items():
    d = df[
        (df["indicator"]  == indicator) &
        (df["department"] == "BOLIVIA") &
        (df["sector"]     == "Total") &
        (df["nivel"]      == "Total") &
        (df["gender"]     == "Total")
    ].sort_values("year")
    ax.plot(d["year"], d["value"], marker="o",
            label=indicator_labels[indicator], color=color, linewidth=2)

ax.axvline(x=2020, color="gray", linestyle="--", alpha=0.7)
ax.text(2020.1, 2, "COVID-19\n2020", fontsize=9, color="gray")
ax.set_title("National Education Indicators (2012–2024)", fontsize=13, pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("Rate (%)")
ax.legend(loc="center left")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("04_covid_impact_indicators.png", dpi=150)
plt.show()
print("✓ Chart 4 saved")

# ============================================================
# ANALYSIS 5 — Improvement or deterioration by department (2012→2024)
# ============================================================
df5 = df[
    (df["indicator"]  == "Tasa Abandono") &
    (df["department"] != "BOLIVIA") &
    (df["sector"]     == "Total") &
    (df["nivel"]      == "Total") &
    (df["gender"]     == "Total") &
    (df["year"].isin([2012, 2024]))
].pivot_table(index="department", columns="year", values="value")

df5["change"] = df5[2024] - df5[2012]
df5 = df5.sort_values("change")

colors5 = ["#4CAF50" if v < 0 else "#F44336" for v in df5["change"]]

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(df5.index, df5["change"], color=colors5)
ax.bar_label(bars, fmt="%.2f pp", padding=4, fontsize=9)
ax.axvline(x=0, color="black", linewidth=0.8)
ax.set_title("Change in Dropout Rate by Department\n(2012 → 2024)", fontsize=13, pad=12)
ax.set_xlabel("Change in percentage points  (green = improved, red = worsened)")
ax.set_xlim(df5["change"].min() * 1.25, 0.3)
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("05_dropout_change_by_dept.png", dpi=150)
plt.show()
print("✓ Chart 5 saved")

# ============================================================
# SUMMARY STATISTICS
# ============================================================
print("\n" + "="*55)
print("SUMMARY FOR CONCLUSIONS")
print("="*55)

m_2011 = df1[df1["year"] == 2011]["value"].values[0]
m_2024 = df1[df1["year"] == 2024]["value"].values[0]
print(f"\nEnrollment 2011: {m_2011:,.1f}k → 2024: {m_2024:,.1f}k")
print(f"Change: {((m_2024 - m_2011) / m_2011 * 100):.1f}%")

dropout_2024 = df[
    (df["indicator"]  == "Tasa Abandono") &
    (df["department"] == "BOLIVIA") &
    (df["sector"]     == "Total") &
    (df["nivel"]      == "Total") &
    (df["year"]       == 2024)
].set_index("gender")["value"]
print(f"\nDropout 2024 — Male: {dropout_2024.get('Hombres', 'N/A'):.2f}%  Female: {dropout_2024.get('Mujeres', 'N/A'):.2f}%")

print(f"\nHighest dropout dept. 2024: {df3.iloc[-1]['department']} ({df3.iloc[-1]['value']:.1f}%)")
print(f"Lowest dropout dept. 2024:  {df3.iloc[0]['department']} ({df3.iloc[0]['value']:.1f}%)")

print(f"\nMost improved (2012→2024): {df5['change'].idxmin()} ({df5['change'].min():.2f} pp)")
print(f"Least improved (2012→2024): {df5['change'].idxmax()} ({df5['change'].max():.2f} pp)")