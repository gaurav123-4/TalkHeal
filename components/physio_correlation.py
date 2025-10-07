import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import plotly.express as px


def _prepare_wearable_df(records) -> pd.DataFrame:
	if not records:
		return pd.DataFrame()
	df = pd.DataFrame(records)
	if df.empty:
		return df
	df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
	df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
	# Daily aggregation
	df["date"] = df["timestamp"].dt.date
	daily = df.groupby("date").agg({
		"hrv_ms": "mean",
		"resting_hr": "mean",
		"sleep_minutes": "sum",
		"sleep_efficiency": "mean",
		"steps": "sum",
		"active_minutes": "sum"
	}).reset_index()
	return daily


def _prepare_mood_df(mood_df: pd.DataFrame) -> pd.DataFrame:
	if mood_df is None or mood_df.empty:
		return pd.DataFrame()
	df = mood_df.copy()
	df["date"] = pd.to_datetime(df["date"]).dt.date
	return df.groupby("date").agg({"mood_numeric": "mean"}).reset_index()


def correlate_mood_with_physio(mood_df: pd.DataFrame, wearable_records: list, min_days: int = 7) -> Dict[str, Any]:
	result: Dict[str, Any] = {
		"insights": [],
		"alerts": [],
		"charts": [],
		"correlations": {}
	}
	wearable_daily = _prepare_wearable_df(wearable_records)
	mood_daily = _prepare_mood_df(mood_df)
	if wearable_daily.empty or mood_daily.empty:
		result["insights"].append("Not enough data to correlate mood with physiology yet.")
		return result
	merged = pd.merge(mood_daily, wearable_daily, on="date", how="inner")
	if len(merged) < min_days:
		result["insights"].append("Collect at least a week of wearable and mood data for reliable insights.")
		return result
	metrics = ["hrv_ms", "resting_hr", "sleep_minutes", "sleep_efficiency", "steps", "active_minutes"]
	for m in metrics:
		if m in merged.columns and merged[m].notna().sum() >= min_days // 2:
			corr = merged[["mood_numeric", m]].dropna().corr().iloc[0, 1]
			result["correlations"][m] = float(corr)
			if np.isfinite(corr):
				if m == "hrv_ms" and corr > 0.2:
					result["insights"].append("Higher HRV appears associated with better mood.")
				elif m == "resting_hr" and corr < -0.2:
					result["insights"].append("Higher resting heart rate may relate to lower mood.")
				elif m == "sleep_minutes" and corr > 0.2:
					result["insights"].append("More sleep tends to correlate with better mood.")
				elif m == "steps" and corr > 0.2:
					result["insights"].append("Higher daily steps correlate with improved mood.")
	# Alerts based on thresholds rolling window
	merged_sorted = merged.sort_values("date")
	window = min(7, len(merged_sorted))
	if window >= 5:
		recent = merged_sorted.tail(window)
		# HRV drop alert
		if recent["hrv_ms"].notna().sum() >= 3:
			baseline = recent["hrv_ms"].iloc[:-1].mean()
			latest = recent["hrv_ms"].iloc[-1]
			if pd.notna(latest) and baseline and latest < 0.8 * baseline:
				result["alerts"].append("Potential stress: HRV dropped significantly vs recent baseline.")
		# Sleep deficit alert
		if recent["sleep_minutes"].notna().sum() >= 3:
			avg_sleep = recent["sleep_minutes"].mean()
			if avg_sleep < 360:
				result["alerts"].append("Low sleep duration this week may impact mood.")
		# Activity dip
		if recent["steps"].notna().sum() >= 3:
			avg_steps = recent["steps"].mean()
			if avg_steps < 3000:
				result["alerts"].append("Low activity this week; consider light walks to support mood.")
	# Chart: scatter mood vs HRV if available
	if "hrv_ms" in merged.columns and merged["hrv_ms"].notna().sum() >= min_days // 2:
		fig = px.scatter(merged, x="hrv_ms", y="mood_numeric", trendline="ols", title="Mood vs HRV")
		result["charts"].append(fig)
	return result
