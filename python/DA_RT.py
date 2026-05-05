import pandas as pd
import numpy as np
from pathlib import Path
import os
import matplotlib.pyplot as plt

# -------------------------
# Robust project paths
# -------------------------
SCRIPT_DIR = Path(__file__).resolve().parent      # .../EnergyMarket/scripts
ROOT_DIR   = SCRIPT_DIR.parent                    # .../EnergyMarket

DATA_PATHS_TO_TRY = [
    str(ROOT_DIR / "data" / "Fact_DA_RT.csv"),
    str(ROOT_DIR / "data" / "fact_da_rt.csv"),
]

OUTPUT_DIR = str(ROOT_DIR / "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_csv(paths):
    last_err = None
    for p in paths:
        try:
            df_ = pd.read_csv(p)
            print(f"Loaded: {p} | rows={len(df_):,} cols={len(df_.columns)}")
            return df_
        except Exception as e:
            last_err = e
    raise FileNotFoundError(
        "Could not load CSV from any of these paths:\n"
        + "\n".join(paths)
        + f"\nLast error: {last_err}"
    )

df = load_csv(DATA_PATHS_TO_TRY)

print("\nColumns found:")
print(df.columns.tolist())

def pick_col(candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

date_col = pick_col(["Date", "date"])
hour_col = pick_col(["HourEnding", "Hour Ending", "hourending"])
dt_col   = pick_col(["DateTime", "Datetime", "dateTime", "datetime"])

da_col = pick_col(["DA_OZP", "DA OZP", "DA_Price", "OntarioZonalPrice", "DA price"])
rt_col = pick_col(["RT_Price", "RT Price", "RealtimePrice", "RT price"])

demand_col = pick_col(["Ontario Demand_MW", "Market Demand", "Demand", "Demand_MW", "OntarioDemandMW"])

if da_col is None or rt_col is None:
    raise KeyError(f"Could not find DA or RT columns. Found da_col={da_col}, rt_col={rt_col}.")

if dt_col is None and (date_col is None or hour_col is None):
    raise KeyError("Could not find DateTime OR (Date + HourEnding). Export must include DateTime or Date & HourEnding.")

print("\nUsing columns:")
print(f"DA: {da_col}")
print(f"RT: {rt_col}")
print(f"Demand: {demand_col}")
print(f"DateTime: {dt_col} | Date: {date_col} | HourEnding: {hour_col}")

# -------------------------
# DateTime creation / cleanup
# -------------------------
if dt_col is None:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[hour_col] = pd.to_numeric(df[hour_col], errors="coerce")
    df["DateTime"] = df[date_col] + pd.to_timedelta(df[hour_col] - 1, unit="h")
    dt_col = "DateTime"
else:
    df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce")

df = df.dropna(subset=[dt_col]).sort_values(dt_col)

# -------------------------
# Numeric cleanup
# -------------------------
for c in [da_col, rt_col]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

if demand_col is not None:
    df[demand_col] = pd.to_numeric(df[demand_col], errors="coerce")

# -------------------------
# Features
# -------------------------
df["Hour"] = df[dt_col].dt.hour
df["DayName"] = df[dt_col].dt.day_name()
df["IsWeekend"] = df[dt_col].dt.weekday >= 5

df["DA_Roll24"] = df[da_col].rolling(window=24, min_periods=1).mean()
df["SpikePremium"] = df[da_col] - df["DA_Roll24"]

df["DA_RT_Spread"] = df[rt_col] - df[da_col]
df["SpreadAbs"] = df["DA_RT_Spread"].abs()

spread = df["DA_RT_Spread"].dropna()

print("\n=== Week 4: Spread Stats ===")
print(f"Rows (non-null spread): {len(spread):,}")
print(f"Mean spread: {spread.mean():.4f}")
print(f"Max spread : {spread.max():.4f}")
print(f"P95 spread : {spread.quantile(0.95):.4f}")

print("\n=== Weekday vs Weekend ===")
print(f"Avg spread weekday: {df.loc[~df['IsWeekend'], 'DA_RT_Spread'].mean():.4f}")
print(f"Avg spread weekend: {df.loc[df['IsWeekend'], 'DA_RT_Spread'].mean():.4f}")

cols_out = [dt_col, da_col, rt_col, "DA_RT_Spread", "SpreadAbs", "DayName", "IsWeekend"]
if demand_col is not None:
    cols_out.insert(5, demand_col)

top10 = df.dropna(subset=["DA_RT_Spread"]).sort_values("SpreadAbs", ascending=False).head(10)[cols_out]

print("\n=== Top 10 Surprise Hours (Abs Spread) ===")
print(top10.to_string(index=False))

mean_spread = spread.mean()
p95_spread = spread.quantile(0.95)
max_spread = spread.max()

wk_mean = df.loc[~df["IsWeekend"], "DA_RT_Spread"].mean()
we_mean = df.loc[df["IsWeekend"], "DA_RT_Spread"].mean()

print("\n=== Week 4 Summary ===")
print(f"DA→RT spread (RT-DA): mean={mean_spread:.2f}, p95={p95_spread:.2f}, max={max_spread:.2f}")
print(f"Weekday avg spread={wk_mean:.2f} | Weekend avg spread={we_mean:.2f}")

# -------------------------
# Plots (last 14 days) -> save to output/
# -------------------------
plot_df = df.dropna(subset=[da_col, rt_col]).tail(24 * 14)

plt.figure()
plt.plot(plot_df[dt_col], plot_df[da_col], label="DA")
plt.plot(plot_df[dt_col], plot_df[rt_col], label="RT")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/da_vs_rt_last14d.png", dpi=200, bbox_inches="tight")
plt.close()

plt.figure()
plt.plot(plot_df[dt_col], plot_df["DA_RT_Spread"], label="RT-DA")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/spread_last14d.png", dpi=200, bbox_inches="tight")
plt.close()

out_csv = str(ROOT_DIR / "output" / "week4_da_rt_features.csv")
df.to_csv(out_csv, index=False)
print(f"\nSaved: {out_csv}")
import datetime as dt

targets = [dt.date(2026, 1, 24), dt.date(2026, 1, 26), dt.date(2026, 1, 28)]

df["Date"] = pd.to_datetime(df["DateTime"]).dt.date
daily = df.groupby("Date")["DA_RT_Spread"].agg(["mean", "min", "max"])

print(daily.loc[targets])
