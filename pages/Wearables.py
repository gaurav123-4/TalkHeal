import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime
from core.utils import require_authentication
from core.wearable_store import (
	load_user_wearables,
	save_user_wearables,
	set_consent,
	append_records,
	set_provider_connection,
	clear_user_wearables,
)


# Auth gate
if "authenticated" not in st.session_state:
	st.session_state.authenticated = False
if "user_profile" not in st.session_state:
	st.session_state.user_profile = {}

require_authentication()

st.set_page_config(page_title="Wearables & Physiology", page_icon="⌚", layout="wide")

st.title("⌚ Wearables & Physiology")

email = st.session_state.user_profile.get("email")
user_data = load_user_wearables(email)

with st.expander("Consent & Privacy", expanded=not user_data.get("consent", False)):
	st.markdown("""
	- Data is collected passively from your wearable provider only after you consent.
	- You can revoke consent anytime; data will stop syncing and you can delete stored data.
	- We store: timestamp, HRV, resting HR, sleep duration/efficiency, steps, active minutes.
	- This is not medical advice. Contact professionals for clinical concerns.
	""")
	consented = st.toggle("I consent to passive wearable data collection", value=user_data.get("consent", False))
	if consented != user_data.get("consent", False):
		user_data = set_consent(email, consented)
		st.success("Consent updated")

colA, colB, colC = st.columns(3)
with colA:
	st.subheader("Connect Providers")
	st.caption("Placeholders — full OAuth to be added later.")
	fitbit_connected = user_data.get("providers", {}).get("fitbit", {}).get("connected", False)
	google_fit_connected = user_data.get("providers", {}).get("google_fit", {}).get("connected", False)
	oura_connected = user_data.get("providers", {}).get("oura", {}).get("connected", False)
	
	if st.button(("Disconnect Fitbit" if fitbit_connected else "Connect Fitbit")):
		user_data = set_provider_connection(email, "fitbit", not fitbit_connected)
		st.rerun()
	if st.button(("Disconnect Google Fit" if google_fit_connected else "Connect Google Fit")):
		user_data = set_provider_connection(email, "google_fit", not google_fit_connected)
		st.rerun()
	if st.button(("Disconnect Oura" if oura_connected else "Connect Oura")):
		user_data = set_provider_connection(email, "oura", not oura_connected)
		st.rerun()

with colB:
	st.subheader("Import CSV")
	st.caption("Upload exported CSV with columns: timestamp, hrv_ms, resting_hr, sleep_minutes, sleep_efficiency, steps, active_minutes")
	uploaded = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=False)
	provider_guess = st.selectbox("Provider", ["fitbit", "google_fit", "oura", "unknown"], index=0)
	if uploaded is not None:
		try:
			df = pd.read_csv(uploaded)
			# Normalize columns
			colmap = {c.lower().strip(): c for c in df.columns}
			req = ["timestamp"]
			if not all(c in colmap for c in req):
				st.error("CSV must include a 'timestamp' column")
			else:
				records = []
				for _, row in df.iterrows():
					rec = {
						"timestamp": row[colmap["timestamp"]],
						"hrv_ms": row.get(colmap.get("hrv_ms")),
						"resting_hr": row.get(colmap.get("resting_hr")),
						"sleep_minutes": row.get(colmap.get("sleep_minutes")),
						"sleep_efficiency": row.get(colmap.get("sleep_efficiency")),
						"steps": row.get(colmap.get("steps")),
						"active_minutes": row.get(colmap.get("active_minutes")),
					}
					records.append(rec)
				if not user_data.get("consent"):
					st.warning("Please provide consent before importing data.")
				else:
					user_data = append_records(email, records, provider_guess)
					st.success(f"Imported {len(records)} records")
		except Exception as e:
			st.error(f"Failed to parse CSV: {e}")

with colC:
	st.subheader("Data Controls")
	if st.button("Delete all stored wearable data", type="secondary"):
		clear_user_wearables(email)
		st.success("All wearable data deleted")
		st.rerun()

st.markdown("---")

st.subheader("Recent Records")
user_data = load_user_wearables(email)
records = user_data.get("records", [])
if not records:
	st.info("No wearable records yet.")
else:
	# Show last 20
	recent = sorted(records, key=lambda r: r.get("timestamp", ""), reverse=True)[:20]
	df_view = pd.DataFrame(recent)
	st.dataframe(df_view, use_container_width=True)

	# Simple summaries
	st.markdown("### Summaries (last 7 days)")
	try:
		df_view["ts"] = pd.to_datetime(df_view["timestamp"], errors="coerce")
		cutoff = pd.Timestamp.utcnow() - pd.Timedelta(days=7)
		last7 = df_view[df_view["ts"] >= cutoff]
		if last7.empty:
			st.info("No data in the last 7 days.")
		else:
			col1, col2, col3, col4 = st.columns(4)
			with col1:
				st.metric("Avg HRV (ms)", f"{last7['hrv_ms'].dropna().astype(float).mean():.0f}" if last7['hrv_ms'].notna().any() else "-")
			with col2:
				st.metric("Avg Resting HR", f"{last7['resting_hr'].dropna().astype(float).mean():.0f}" if last7['resting_hr'].notna().any() else "-")
			with col3:
				st.metric("Total Sleep (min)", f"{last7['sleep_minutes'].dropna().astype(float).sum():.0f}" if last7['sleep_minutes'].notna().any() else "-")
			with col4:
				st.metric("Steps (sum)", f"{last7['steps'].dropna().astype(float).sum():.0f}" if last7['steps'].notna().any() else "-")
	except Exception as e:
		st.warning(f"Summary unavailable: {e}")
