import streamlit as st
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Cab Fare Predictor",
    page_icon="🚖",
    layout="centered"
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 2rem; }

    .title-card {
        background: linear-gradient(135deg, #1a1f3a, #2d3561);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid #3d4577;
    }
    .title-card h1 { color: #ffffff; font-size: 2rem; margin: 0; }
    .title-card p  { color: #a0aec0; font-size: 0.95rem; margin: 0.4rem 0 0; }

    .fare-card {
        background: linear-gradient(135deg, #1e4620, #2d6a30);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        text-align: center;
        border: 1px solid #38a169;
        margin-top: 1rem;
    }
    .fare-card .label { color: #9ae6b4; font-size: 0.9rem; letter-spacing: 0.05em; text-transform: uppercase; }
    .fare-card .amount { color: #ffffff; font-size: 3rem; font-weight: 700; margin: 0.2rem 0; }
    .fare-card .note { color: #c6f6d5; font-size: 0.85rem; }

    .breakdown-card {
        background: #1a202c;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border: 1px solid #2d3748;
        margin-top: 1rem;
    }
    .breakdown-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #2d3748;
        color: #e2e8f0;
        font-size: 0.9rem;
    }
    .breakdown-row:last-child { border-bottom: none; font-weight: 600; color: #68d391; }
    .breakdown-label { color: #a0aec0; }

    .info-card {
        background: #1a202c;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: 1px solid #2d3748;
        margin-top: 0.8rem;
    }
    .info-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: space-around;
        text-align: center;
    }
    .info-item { padding: 0.4rem 0; }
    .info-item .val { color: #63b3ed; font-size: 1.2rem; font-weight: 600; }
    .info-item .lbl { color: #718096; font-size: 0.8rem; }

    .section-title {
        color: #a0aec0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 1.2rem 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FARE CONFIG  (edit these values anytime)
# ─────────────────────────────────────────────
BASE_FARE = {
    1: 90,
    2: 110,
    3: 130,
    4: 150,
    5: 170,
    6: 190
}
PER_KM_RATE     = 15     # ₹ per km
MIN_FARE        = 50     # ₹ minimum fare
PLATFORM_FEE    = 10     # ₹ fixed platform / booking fee
CURRENCY_SYMBOL = "₹"

# ─────────────────────────────────────────────
#  HAVERSINE DISTANCE
# ─────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def estimate_time_minutes(distance_km, speed_kmh=30):
    return (distance_km / speed_kmh) * 60

# ─────────────────────────────────────────────
#  TITLE
# ─────────────────────────────────────────────
st.markdown("""
<div class="title-card">
    <h1>🚖 Cab Fare Predictor</h1>
    <p>Enter pickup & dropoff coordinates to estimate your fare instantly</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT SECTION
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📍 Pickup Location</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    pickup_lat = st.number_input(
        "Pickup Latitude",
        value=40.7614,
        min_value=-90.0, max_value=90.0,
        format="%.6f",
        help="Latitude of your pickup point"
    )
with col2:
    pickup_lon = st.number_input(
        "Pickup Longitude",
        value=-73.9776,
        min_value=-180.0, max_value=180.0,
        format="%.6f",
        help="Longitude of your pickup point"
    )

st.markdown('<p class="section-title">🏁 Dropoff Location</p>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    dropoff_lat = st.number_input(
        "Dropoff Latitude",
        value=40.6413,
        min_value=-90.0, max_value=90.0,
        format="%.6f",
        help="Latitude of your dropoff point"
    )
with col4:
    dropoff_lon = st.number_input(
        "Dropoff Longitude",
        value=-73.7781,
        min_value=-180.0, max_value=180.0,
        format="%.6f",
        help="Longitude of your dropoff point"
    )

st.markdown('<p class="section-title">👥 Passengers</p>', unsafe_allow_html=True)
passengers = st.slider(
    "Number of Passengers",
    min_value=1, max_value=6, value=1,
    help="Select 1 to 6 passengers"
)

# Show base fare for selected passenger count
st.info(f"Base fare for **{passengers} passenger{'s' if passengers>1 else ''}**: ₹{BASE_FARE[passengers]}")

# ─────────────────────────────────────────────
#  PREDICT BUTTON
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("🚀 Predict Fare", use_container_width=True)

if predict_clicked:

    # ── Compute distance ─────────────────────
    distance_km = haversine(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)

    if distance_km < 0.1:
        st.warning("⚠️ Pickup and dropoff locations are too close (< 100 meters). Please check coordinates.")
        st.stop()

    # ── Fare calculation ─────────────────────
    base_fare       = BASE_FARE[passengers]
    distance_charge = round(distance_km * PER_KM_RATE, 2)
    subtotal        = base_fare + distance_charge
    total_fare      = max(subtotal + PLATFORM_FEE, MIN_FARE)
    est_time        = estimate_time_minutes(distance_km)

    # ── Fare card ────────────────────────────
    st.markdown(f"""
    <div class="fare-card">
        <div class="label">Estimated Fare</div>
        <div class="amount">{CURRENCY_SYMBOL}{total_fare:.2f}</div>
        <div class="note">Inclusive of all charges</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Trip info strip ───────────────────────
    st.markdown(f"""
    <div class="info-card">
        <div class="info-row">
            <div class="info-item">
                <div class="val">{distance_km:.2f} km</div>
                <div class="lbl">Trip Distance</div>
            </div>
            <div class="info-item">
                <div class="val">{est_time:.0f} min</div>
                <div class="lbl">Est. Travel Time</div>
            </div>
            <div class="info-item">
                <div class="val">{passengers}</div>
                <div class="lbl">Passengers</div>
            </div>
            <div class="info-item">
                <div class="val">{CURRENCY_SYMBOL}{PER_KM_RATE}/km</div>
                <div class="lbl">Rate Per KM</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fare breakdown ────────────────────────
    st.markdown('<p class="section-title">💰 Fare Breakdown</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="breakdown-card">
        <div class="breakdown-row">
            <span class="breakdown-label">👥 Base Fare ({passengers} passenger{'s' if passengers>1 else ''})</span>
            <span>{CURRENCY_SYMBOL}{base_fare:.2f}</span>
        </div>
        <div class="breakdown-row">
            <span class="breakdown-label">🛣️ Distance Charge ({distance_km:.2f} km × {CURRENCY_SYMBOL}{PER_KM_RATE})</span>
            <span>{CURRENCY_SYMBOL}{distance_charge:.2f}</span>
        </div>
        <div class="breakdown-row">
            <span class="breakdown-label">📱 Platform Fee</span>
            <span>{CURRENCY_SYMBOL}{PLATFORM_FEE:.2f}</span>
        </div>
        <div class="breakdown-row">
            <span>Total Estimated Fare</span>
            <span>{CURRENCY_SYMBOL}{total_fare:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fare table for all passenger counts ──
    st.markdown('<p class="section-title">📊 Fare Comparison — All Passenger Counts</p>', unsafe_allow_html=True)
    fare_data = []
    for p in range(1, 7):
        b  = BASE_FARE[p]
        dc = round(distance_km * PER_KM_RATE, 2)
        t  = max(b + dc + PLATFORM_FEE, MIN_FARE)
        fare_data.append({
            "Passengers": f"{'👤' * min(p,4)} {p}",
            "Base Fare (₹)": b,
            "Distance Charge (₹)": dc,
            "Platform Fee (₹)": PLATFORM_FEE,
            "Total Fare (₹)": round(t, 2)
        })
    st.dataframe(pd.DataFrame(fare_data), use_container_width=True, hide_index=True)