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

# --- Page Configuration ---
st.set_page_config(
    page_title="Wearables & Physiology",
    page_icon="⌚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Authentication ---
if not st.session_state.get("authenticated"):
    st.warning("Please log in to access this page.")
    st.stop()

require_authentication()

# --- Load User Data ---
email = st.session_state.user_profile.get("email")
if not email:
    st.error("User email not found. Please re-login.")
    st.stop()

user_data = load_user_wearables(email)

# --- Page Title ---
st.title("⌚ Wearables & Physiology")
st.markdown("Connect your wearables to track physiological data like heart rate, sleep, and activity. Gain insights into how your body responds to your mental state.")

# --- Consent & Privacy ---
with st.expander("🔒 Consent & Privacy", expanded=not user_data.get("consent", False)):
    st.markdown("""
    **Your data privacy is our priority.**
    - **Passive Data Collection:** We only collect data from your wearable provider after you grant explicit consent.
    - **Full Control:** You can revoke consent at any time. This will stop data syncing, and you can permanently delete all stored data.
    - **Data We Store:** We store timestamps, Heart Rate Variability (HRV), resting heart rate, sleep duration and efficiency, steps, and active minutes.
    - **Not Medical Advice:** This tool is for informational purposes only. Please consult a healthcare professional for any clinical concerns.
    """)
    consent_given = user_data.get("consent", False)
    consented = st.checkbox("I consent to the passive collection of my wearable data.", value=consent_given)
    if consented != consent_given:
        user_data = set_consent(email, consented)
        if consented:
            st.success("Thank you for your consent! You can now connect your providers.")
        else:
            st.warning("Consent revoked. Data syncing will be disabled.")
        st.rerun()

# --- Main Content Area ---
if user_data.get("consent"):
    col1, col2 = st.columns((1, 1))

    # --- Provider Connection ---
    with col1:
        st.subheader("🔗 Connect Providers")
        st.caption("Connect your wearable devices to automatically sync your data.")

        providers = {
            "Fitbit": "fitbit",
            "Google Fit": "google_fit",
            "Oura": "oura"
        }

        for provider_name, provider_key in providers.items():
            is_connected = user_data.get("providers", {}).get(provider_key, {}).get("connected", False)
            button_text = f"Disconnect {provider_name}" if is_connected else f"Connect {provider_name}"
            button_type = "secondary" if is_connected else "primary"
            if st.button(button_text, key=provider_key, use_container_width=True, type=button_type):
                user_data = set_provider_connection(email, provider_key, not is_connected)
                st.rerun()

    # --- Manual Data Import ---
    with col2:
        st.subheader("📄 Import CSV")
        st.caption("Manually upload a CSV file with your wearable data.")
        
        uploaded = st.file_uploader(
            "Upload a CSV file",
            type=["csv"],
            help="The CSV should have columns: timestamp, hrv_ms, resting_hr, sleep_minutes, sleep_efficiency, steps, active_minutes"
        )
        
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                colmap = {c.lower().strip().replace("_", ""): c for c in df.columns}
                
                if "timestamp" not in colmap:
                    st.error("CSV must include a 'timestamp' column.")
                else:
                    records = []
                    for _, row in df.iterrows():
                        rec = {
                            "timestamp": row[colmap["timestamp"]],
                            "hrv_ms": row.get(colmap.get("hrvms")),
                            "resting_hr": row.get(colmap.get("restinghr")),
                            "sleep_minutes": row.get(colmap.get("sleepminutes")),
                            "sleep_efficiency": row.get(colmap.get("sleepefficiency")),
                            "steps": row.get(colmap.get("steps")),
                            "active_minutes": row.get(colmap.get("activeminutes")),
                        }
                        records.append(rec)
                    
                    provider_guess = st.selectbox("Select the provider for this import:", ["fitbit", "google_fit", "oura", "unknown"])
                    if st.button("Import Data", use_container_width=True):
                        user_data = append_records(email, records, provider_guess)
                        st.success(f"Successfully imported {len(records)} records!")
            except Exception as e:
                st.error(f"Failed to parse CSV: {e}")

    st.divider()

    # --- Data Display and Summaries ---
    st.subheader("📊 Recent Records & Summaries")
    records = user_data.get("records", [])

    if not records:
        st.info("No wearable records found. Connect a provider or upload a CSV to get started.")
    else:
        df_view = pd.DataFrame(sorted(records, key=lambda r: r.get("timestamp", ""), reverse=True))
        df_view["ts"] = pd.to_datetime(df_view["timestamp"], errors="coerce")

        # --- Summaries (Last 7 Days) ---
        st.markdown("##### Last 7 Days at a Glance")
        cutoff = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=7)
        last7 = df_view[df_view["ts"] >= cutoff]

        if last7.empty:
            st.info("No data recorded in the last 7 days.")
        else:
            summary_cols = st.columns(4)
            metrics = {
                "Avg HRV (ms)": ("hrv_ms", "mean"),
                "Avg Resting HR": ("resting_hr", "mean"),
                "Total Sleep (hrs)": ("sleep_minutes", "sum"),
                "Total Steps": ("steps", "sum")
            }
            
            for i, (label, (col, agg)) in enumerate(metrics.items()):
                with summary_cols[i]:
                    series = last7[col].dropna().astype(float)
                    if not series.empty:
                        value = series.agg(agg)
                        if "sleep" in label: # Convert minutes to hours
                            value /= 60
                        st.metric(label, f"{value:.1f}")
                    else:
                        st.metric(label, "N/A")

        # --- Detailed Records ---
        st.markdown("##### All Recorded Data")
        st.dataframe(df_view.drop(columns=["ts"]), use_container_width=True, hide_index=True)

    # --- Data Controls ---
    st.divider()
    st.subheader("⚙️ Data Controls")
    st.warning("This action is irreversible and will permanently delete all your stored wearable data.")
    if st.button("Delete All Wearable Data", type="primary", use_container_width=True):
        clear_user_wearables(email)
        st.success("All your wearable data has been successfully deleted.")
        st.rerun()

else:
    st.info("Please provide consent above to begin connecting your wearable devices and tracking your physiological data.")