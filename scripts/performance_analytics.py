from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs" / "performance_analytics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RF_ANNUAL = 0.065
TRADING_DAYS = 252


def load_data():
    nav = pd.read_csv(DATA_DIR / "clean_nav.csv", parse_dates=["date"]).sort_values(["amfi_code", "date"])
    fund_master = pd.read_csv(DATA_DIR / "clean_fund_master.csv")
    indices = pd.read_csv(DATA_DIR / "clean_indices.csv", parse_dates=["date"]).sort_values(["index_name", "date"])
    return nav, fund_master, indices


def compute_daily_returns(nav):
    nav = nav.copy()
    nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()
    summary = (
        nav.dropna(subset=["daily_return"])
        .groupby("amfi_code")
        .agg(
            start_date=("date", "min"),
            end_date=("date", "max"),
            observations=("daily_return", "size"),
            cumulative_return=("daily_return", lambda x: (1 + x).prod() - 1),
            annualised_return=("daily_return", lambda x: (1 + x).prod() ** (TRADING_DAYS / len(x)) - 1 if len(x) > 0 else np.nan),
        )
        .reset_index()
    )
    summary.to_csv(OUTPUT_DIR / "returns_computed.csv", index=False)
    nav.to_csv(OUTPUT_DIR / "daily_returns.csv", index=False)
    return nav, summary


def compute_cagr(nav, fund_master):
    latest_date = nav["date"].max()
    def cagr_for_years(group, years):
        target_date = latest_date - pd.DateOffset(years=years)
        prior = group[group["date"] <= target_date]
        if prior.empty:
            return np.nan, None
        start_nav = prior.iloc[-1]["nav"]
        end_nav = group.iloc[-1]["nav"]
        return (end_nav / start_nav) ** (1 / years) - 1, prior.iloc[-1]["date"]

    rows = []
    for amfi_code, group in nav.groupby("amfi_code"):
        group = group.sort_values("date")
        current_nav = group.iloc[-1]["nav"]
        cagr_1, start_1 = cagr_for_years(group, 1)
        cagr_3, start_3 = cagr_for_years(group, 3)
        cagr_5, start_5 = cagr_for_years(group, 5)
        rows.append(
            {
                "amfi_code": amfi_code,
                "scheme_name": fund_master.loc[fund_master["amfi_code"] == amfi_code, "scheme_name"].squeeze(),
                "category": fund_master.loc[fund_master["amfi_code"] == amfi_code, "category"].squeeze(),
                "end_date": latest_date,
                "nav_end": current_nav,
                "cagr_1yr": cagr_1,
                "cagr_3yr": cagr_3,
                "cagr_5yr": cagr_5,
                "start_1yr_date": start_1,
                "start_3yr_date": start_3,
                "start_5yr_date": start_5,
            }
        )
    cagr_df = pd.DataFrame(rows)
    cagr_df.to_csv(OUTPUT_DIR / "cagr_report.csv", index=False)
    return cagr_df


def annualise_stats(daily_returns):
    mean_daily = np.nanmean(daily_returns)
    std_daily = np.nanstd(daily_returns, ddof=1)
    annual_return = mean_daily * TRADING_DAYS
    annual_vol = std_daily * np.sqrt(TRADING_DAYS)
    return annual_return, annual_vol


def compute_risk_metrics(nav):
    rows = []
    rf_daily = (1 + RF_ANNUAL) ** (1 / TRADING_DAYS) - 1
    for amfi_code, group in nav.groupby("amfi_code"):
        returns = group["daily_return"].dropna().to_numpy()
        if len(returns) < 2:
            continue
        ann_return, ann_vol = annualise_stats(returns)
        sharpe = (ann_return - RF_ANNUAL) / ann_vol if ann_vol > 0 else np.nan
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns, ddof=1) if len(downside_returns) > 1 else np.nan
        sortino = (ann_return - RF_ANNUAL) / (downside_std * np.sqrt(TRADING_DAYS)) if downside_std > 0 else np.nan
        rows.append(
            {
                "amfi_code": amfi_code,
                "annual_return": ann_return,
                "annual_volatility": ann_vol,
                "sharpe_ratio": sharpe,
                "sortino_ratio": sortino,
                "downside_std_daily": downside_std,
            }
        )
    risk_df = pd.DataFrame(rows)
    risk_df.to_csv(OUTPUT_DIR / "sharpe_sortino_values.csv", index=False)
    return risk_df


def compute_alpha_beta(nav, indices):
    bench = indices[indices["index_name"] == "NIFTY100"].copy()
    bench["bench_return"] = bench["close_value"].pct_change()
    bench = bench[["date", "bench_return"]]
    rows = []
    merged = nav.merge(bench, on="date", how="inner")
    for amfi_code, group in merged.groupby("amfi_code"):
        fund_returns = group["daily_return"].dropna().to_numpy()
        benchmark_returns = group["bench_return"].dropna().to_numpy()
        valid = (~np.isnan(fund_returns)) & (~np.isnan(benchmark_returns))
        if valid.sum() < 10:
            continue
        fund_returns = fund_returns[valid]
        benchmark_returns = benchmark_returns[valid]
        slope, intercept = np.polyfit(benchmark_returns, fund_returns, 1)
        alpha = intercept * TRADING_DAYS
        beta = slope
        rows.append(
            {
                "amfi_code": amfi_code,
                "alpha_annualised": alpha,
                "beta": beta,
                "observations": valid.sum(),
            }
        )
    alpha_beta_df = pd.DataFrame(rows)
    alpha_beta_df.to_csv(OUTPUT_DIR / "alpha_beta.csv", index=False)
    return alpha_beta_df


def compute_max_drawdown(nav):
    rows = []
    for amfi_code, group in nav.groupby("amfi_code"):
        group = group.sort_values("date").copy()
        group["running_max"] = group["nav"].cummax()
        group["drawdown"] = group["nav"] / group["running_max"] - 1
        if group["drawdown"].isna().all():
            continue
        worst_idx = group["drawdown"].idxmin()
        trough = group.loc[worst_idx]
        peak_idx = group.loc[group["date"] <= trough["date"], "nav"].idxmax()
        peak = group.loc[peak_idx]
        rows.append(
            {
                "amfi_code": amfi_code,
                "max_drawdown_pct": float(trough["drawdown"] * 100),
                "peak_date": peak["date"],
                "trough_date": trough["date"],
                "peak_nav": peak["nav"],
                "trough_nav": trough["nav"],
            }
        )
    drawdown_df = pd.DataFrame(rows)
    drawdown_df.to_csv(OUTPUT_DIR / "max_drawdown.csv", index=False)
    return drawdown_df


def build_scorecard(cagr_df, risk_df, alpha_beta_df, fund_master, drawdown_df):
    score_df = (
        cagr_df.merge(risk_df, on="amfi_code", how="left")
        .merge(alpha_beta_df, on="amfi_code", how="left")
        .merge(fund_master[["amfi_code", "scheme_name", "expense_ratio_pct"]], on="amfi_code", how="left")
        .merge(drawdown_df[["amfi_code", "max_drawdown_pct"]], on="amfi_code", how="left")
    )
    score_df["rank_3yr"] = score_df["cagr_3yr"].rank(pct=True, ascending=False)
    score_df["rank_sharpe"] = score_df["sharpe_ratio"].rank(pct=True, ascending=False)
    score_df["rank_alpha"] = score_df["alpha_annualised"].rank(pct=True, ascending=False)
    score_df["rank_expense"] = score_df["expense_ratio_pct"].rank(pct=True, ascending=True)
    score_df["rank_drawdown"] = score_df["max_drawdown_pct"].rank(pct=True, ascending=False)
    score_df["fund_score"] = (
        score_df["rank_3yr"] * 30
        + score_df["rank_sharpe"] * 25
        + score_df["rank_alpha"] * 20
        + score_df["rank_expense"] * 15
        + score_df["rank_drawdown"] * 10
    )
    score_df["fund_score"] = score_df["fund_score"].round(2)
    score_df = score_df.sort_values("fund_score", ascending=False)
    score_df.to_csv(OUTPUT_DIR / "fund_scorecard.csv", index=False)
    return score_df


def benchmark_comparison_chart(nav, indices, cagr_df):
    latest_date = nav["date"].max()
    start_date = latest_date - pd.DateOffset(years=3)
    benchmark = indices[indices["index_name"].isin(["NIFTY50", "NIFTY100"])].copy()
    benchmark["return"] = benchmark.groupby("index_name")["close_value"].pct_change()
    benchmark = benchmark[benchmark["date"] >= start_date]

    top_funds = cagr_df.sort_values("cagr_3yr", ascending=False).head(5)["amfi_code"].tolist()
    plot_nav = nav[nav["amfi_code"].isin(top_funds) & (nav["date"] >= start_date)].copy()
    normalized = []
    for amfi_code, group in plot_nav.groupby("amfi_code"):
        group = group.sort_values("date").copy()
        base_nav = group.iloc[0]["nav"]
        group["normalized_nav"] = group["nav"] / base_nav * 100
        normalized.append(group)
    normalized = pd.concat(normalized)

    benchmark_norm = []
    for idx_name, group in benchmark.groupby("index_name"):
        group = group.sort_values("date").copy()
        base = group.iloc[0]["close_value"]
        group["normalized_nav"] = group["close_value"] / base * 100
        benchmark_norm.append(group)
    benchmark_norm = pd.concat(benchmark_norm)

    plt.figure(figsize=(14, 8))
    for amfi_code, group in normalized.groupby("amfi_code"):
        label = group["amfi_code"].iloc[0]
        plt.plot(group["date"], group["normalized_nav"], label=f"Fund {label}")
    for idx_name, group in benchmark_norm.groupby("index_name"):
        plt.plot(group["date"], group["normalized_nav"], label=idx_name, linewidth=2.5, linestyle="--")

    plt.title("Top 5 Fund NAV Comparison vs NIFTY50 and NIFTY100 (Last 3 Years)")
    plt.xlabel("Date")
    plt.ylabel("Normalized Value (Base = 100)")
    plt.legend(loc="best")
    plt.grid(True)
    plt.tight_layout()
    chart_path = OUTPUT_DIR / "benchmark_chart.png"
    plt.savefig(chart_path, dpi=200)
    plt.close()

    tracking_rows = []
    nifty100 = benchmark[benchmark["index_name"] == "NIFTY100"][['date', 'return']].set_index('date')
    for amfi_code in top_funds:
        fund_returns = nav[(nav["amfi_code"] == amfi_code) & (nav["date"] >= start_date)][["date", "daily_return"]].set_index('date')
        comp = fund_returns.join(nifty100, how='inner').dropna()
        if len(comp) < 20:
            continue
        tracking_error = np.std(comp["daily_return"] - comp["return"], ddof=1) * np.sqrt(TRADING_DAYS)
        tracking_rows.append({"amfi_code": amfi_code, "tracking_error": tracking_error})
    tracking_df = pd.DataFrame(tracking_rows)
    tracking_df.to_csv(OUTPUT_DIR / "benchmark_tracking_error.csv", index=False)
    return chart_path, tracking_df


def main():
    nav, fund_master, indices = load_data()
    nav, returns_summary = compute_daily_returns(nav)
    cagr_df = compute_cagr(nav, fund_master)
    risk_df = compute_risk_metrics(nav)
    alpha_beta_df = compute_alpha_beta(nav, indices)
    drawdown_df = compute_max_drawdown(nav)
    score_df = build_scorecard(cagr_df, risk_df, alpha_beta_df, fund_master, drawdown_df)
    chart_path, tracking_df = benchmark_comparison_chart(nav, indices, cagr_df)

    print("Outputs written to", OUTPUT_DIR)
    print("returns_computed.csv, daily_returns.csv, cagr_report.csv, sharpe_sortino_values.csv, alpha_beta.csv, max_drawdown.csv, fund_scorecard.csv, benchmark_tracking_error.csv")
    print("Chart saved to", chart_path)


if __name__ == "__main__":
    main()
