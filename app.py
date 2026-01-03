"""
Cafe AI - Production Release v2.0
Self-learning stock prediction system with Mobile Optimization, 
Reinforcement Learning, and Context Intelligence.
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import os
import secrets
import json
import hashlib
from autogluon.tabular import TabularPredictor
import numpy as np
import streamlit.components.v1 as components
from nz_calendar import get_public_holiday_status, is_school_holiday
from dotenv import load_dotenv
from dateutil import parser as dateutil_parser
import random
import time
import traceback

# Load environment variables
load_dotenv()

# Get API keys
api_key = os.getenv('TICKETMASTER_KEY')
lightspeed_client_id = os.getenv('LIGHTSPEED_CLIENT_ID')
lightspeed_client_secret = os.getenv('LIGHTSPEED_CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:8501')

# ============================================================================
# PAGE CONFIGURATION - Mobile Optimized
# ============================================================================
st.set_page_config(
    page_title="Cafe AI",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"  # Mobile: start collapsed
)

# ============================================================================
# MOBILE-FIRST CSS - Hide Streamlit UI, Large Touch Targets
# ============================================================================
st.markdown("""
<style>
    /* Import distinctive fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Instrument+Serif:ital@0;1&display=swap');
    
    /* CSS Variables - Warm Coffee Theme */
    :root {
        --primary-bg: #1a1612;
        --secondary-bg: #2d251f;
        --card-bg: #3d322a;
        --accent-gold: #d4a574;
        --accent-cream: #f5e6d3;
        --accent-espresso: #8b6914;
        --text-primary: #f5e6d3;
        --text-secondary: #b8a089;
        --success-green: #7cb342;
        --warning-orange: #ff9800;
        --danger-red: #e53935;
        --info-blue: #29b6f6;
    }
    
    /* Hide Streamlit hamburger menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit branding */
    .stDeployButton {display: none;}
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, var(--primary-bg) 0%, #2a1f17 50%, var(--secondary-bg) 100%);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Large touch targets for mobile */
    .stButton > button {
        min-height: 56px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 16px !important;
        border: none !important;
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-espresso) 100%) !important;
        color: var(--primary-bg) !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 165, 116, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 165, 116, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: var(--card-bg) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1px solid rgba(212, 165, 116, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    div[data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--accent-cream) !important;
        font-family: 'Instrument Serif', serif !important;
        font-size: 2rem !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Instrument Serif', serif !important;
        color: var(--accent-cream) !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Cards and containers */
    .css-1r6slb0, .css-12oz5g7 {
        background: var(--card-bg) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(212, 165, 116, 0.15) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--secondary-bg) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Sidebar - dark coffee theme */
    section[data-testid="stSidebar"] {
        background: var(--secondary-bg) !important;
        border-right: 1px solid rgba(212, 165, 116, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* Feedback buttons special styling */
    .feedback-btn-green button {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%) !important;
    }
    
    .feedback-btn-orange button {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%) !important;
    }
    
    .feedback-btn-red button {
        background: linear-gradient(135deg, #f44336 0%, #c62828 100%) !important;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    
    .hero-title {
        font-family: 'Instrument Serif', serif;
        font-size: 3rem;
        color: var(--accent-cream);
        margin: 0;
        text-shadow: 0 4px 20px rgba(212, 165, 116, 0.3);
    }
    
    .hero-subtitle {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-top: 8px;
    }
    
    /* Big metric cards for dashboard */
    .big-metric-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--secondary-bg) 100%);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        border: 1px solid rgba(212, 165, 116, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        margin: 8px 0;
    }
    
    .big-metric-icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }
    
    .big-metric-value {
        font-family: 'Instrument Serif', serif;
        font-size: 2.2rem;
        color: var(--accent-cream);
        font-weight: 700;
    }
    
    .big-metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 4px;
    }
    
    /* 7-day outlook list */
    .outlook-row {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-left: 4px solid var(--accent-gold);
        transition: all 0.2s ease;
    }
    
    .outlook-row:hover {
        transform: translateX(4px);
        background: var(--secondary-bg);
    }
    
    .outlook-date {
        font-weight: 600;
        color: var(--accent-cream);
    }
    
    .outlook-event {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .outlook-forecast {
        font-family: 'Instrument Serif', serif;
        font-size: 1.3rem;
        color: var(--accent-gold);
    }
    
    /* Morning review container */
    .morning-review {
        background: linear-gradient(135deg, #2d3a2d 0%, #1a2518 100%);
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        border: 2px solid rgba(124, 179, 66, 0.3);
        box-shadow: 0 8px 32px rgba(124, 179, 66, 0.1);
    }
    
    .morning-review h3 {
        color: #a5d6a7 !important;
        margin-bottom: 16px;
    }
    
    /* Install button */
    .install-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    /* Toggle switch styling */
    .stToggle > label {
        color: var(--text-primary) !important;
    }
    
    /* Pitch mode indicator */
    .pitch-mode-active {
        background: linear-gradient(135deg, #7c4dff 0%, #536dfe 100%);
        border-radius: 12px;
        padding: 8px 16px;
        color: white;
        font-weight: 600;
        text-align: center;
        margin: 8px 0;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .big-metric-value {
            font-size: 1.8rem;
        }
        
        .stButton > button {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA PERSISTENCE - The Brain (JSON Storage)
# ============================================================================
LEARNING_DATA_FILE = "shop_learning_data.json"


def get_user_id():
    """
    Generate a unique user ID based on session or IP.
    For production, this could use actual login credentials.
    """
    # Use session-based ID for simplicity
    if 'user_id' not in st.session_state:
        # Create a hash from timestamp + random for unique ID
        raw_id = f"{datetime.now().isoformat()}-{secrets.token_hex(8)}"
        st.session_state.user_id = hashlib.sha256(raw_id.encode()).hexdigest()[:16]
    return st.session_state.user_id


def load_shop_data():
    """
    Load learning data for the current user from JSON file.
    
    Returns:
    - Dictionary with user's adjustment history
    """
    try:
        if os.path.exists(LEARNING_DATA_FILE):
            with open(LEARNING_DATA_FILE, 'r') as f:
                all_data = json.load(f)
            
            user_id = get_user_id()
            return all_data.get(user_id, {
                "adjustments": [],
                "last_review_date": None,
                "total_reviews": 0,
                "created_at": datetime.now().isoformat()
            })
        else:
            return {
                "adjustments": [],
                "last_review_date": None,
                "total_reviews": 0,
                "created_at": datetime.now().isoformat()
            }
    except Exception as e:
        st.error(f"Error loading shop data: {e}")
        return {"adjustments": [], "last_review_date": None, "total_reviews": 0}


def save_shop_data(user_data):
    """
    Save learning data for the current user to JSON file.
    
    Parameters:
    - user_data: Dictionary with user's adjustment history
    """
    try:
        # Load existing data or create new
        all_data = {}
        if os.path.exists(LEARNING_DATA_FILE):
            with open(LEARNING_DATA_FILE, 'r') as f:
                all_data = json.load(f)
        
        # Update with user's data
        user_id = get_user_id()
        all_data[user_id] = user_data
        
        # Save back to file
        with open(LEARNING_DATA_FILE, 'w') as f:
            json.dump(all_data, f, indent=2, default=str)
        
        return True
    except Exception as e:
        st.error(f"Error saving shop data: {e}")
        return False


def record_adjustment(item_name, date_str, feedback_type, original_sales, true_demand):
    """
    Record a user's feedback adjustment for learning.
    
    Parameters:
    - item_name: Name of the item
    - date_str: Date of the sale (YYYY-MM-DD)
    - feedback_type: One of 'too_much', 'bit_more', 'perfect', 'bit_less', 'too_less'
    - original_sales: Original quantity sold
    - true_demand: Adjusted true demand value
    """
    user_data = load_shop_data()
    
    adjustment = {
        "item_name": item_name,
        "date": date_str,
        "feedback_type": feedback_type,
        "original_sales": original_sales,
        "true_demand": true_demand,
        "recorded_at": datetime.now().isoformat()
    }
    
    user_data["adjustments"].append(adjustment)
    user_data["last_review_date"] = datetime.now().strftime('%Y-%m-%d')
    user_data["total_reviews"] = user_data.get("total_reviews", 0) + 1
    
    save_shop_data(user_data)
    return True


def get_adjustments_for_date(date_str):
    """
    Get all adjustments recorded for a specific date.
    
    Returns:
    - Dictionary mapping item names to their true_demand values
    """
    user_data = load_shop_data()
    adjustments = {}
    
    for adj in user_data.get("adjustments", []):
        if adj.get("date") == date_str:
            adjustments[adj["item_name"]] = adj["true_demand"]
    
    return adjustments


def apply_learning_to_data(sales_df):
    """
    Apply learned adjustments to historical sales data.
    Merges user feedback with raw sales data for improved training.
    
    Parameters:
    - sales_df: DataFrame with Date, Item Name, Quantity Sold
    
    Returns:
    - DataFrame with adjusted Quantity Sold based on user feedback
    """
    user_data = load_shop_data()
    adjustments = user_data.get("adjustments", [])
    
    if not adjustments:
        return sales_df
    
    # Create a copy to modify
    adjusted_df = sales_df.copy()
    
    # Create adjustment lookup
    adj_lookup = {}
    for adj in adjustments:
        key = (adj["date"], adj["item_name"])
        adj_lookup[key] = adj["true_demand"]
    
    # Apply adjustments
    for idx, row in adjusted_df.iterrows():
        key = (row["Date"], row["Item Name"])
        if key in adj_lookup:
            adjusted_df.at[idx, "Quantity Sold"] = adj_lookup[key]
    
    return adjusted_df


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'predictor' not in st.session_state:
    st.session_state.predictor = None
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'item_names' not in st.session_state:
    st.session_state.item_names = []
if 'detected_lat' not in st.session_state:
    st.session_state.detected_lat = None
if 'detected_lon' not in st.session_state:
    st.session_state.detected_lon = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'refresh_token' not in st.session_state:
    st.session_state.refresh_token = None
if 'oauth_state' not in st.session_state:
    st.session_state.oauth_state = None
if 'product_recipes' not in st.session_state:
    st.session_state.product_recipes = {}
if 'lightspeed_data' not in st.session_state:
    st.session_state.lightspeed_data = None
if 'lightspeed_data_info' not in st.session_state:
    st.session_state.lightspeed_data_info = None
if 'pitch_mode' not in st.session_state:
    st.session_state.pitch_mode = False
if 'morning_review_done' not in st.session_state:
    st.session_state.morning_review_done = False
if 'show_install_guide' not in st.session_state:
    st.session_state.show_install_guide = False


# ============================================================================
# WEATHER & EVENTS API FUNCTIONS
# ============================================================================
def get_weather_data(lat, lon, start_date, end_date, forecast=False):
    """
    Fetch weather data from Open-Meteo API.
    """
    try:
        if forecast:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,precipitation_sum,weathercode",
                "timezone": "auto",
                "start_date": start_date,
                "end_date": end_date
            }
        else:
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,precipitation_sum",
                "start_date": start_date,
                "end_date": end_date
            }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'daily' not in data:
            raise ValueError("Invalid API response")
        
        weather_df = pd.DataFrame({
            'Date': pd.to_datetime(data['daily']['time']),
            'Max Temp': data['daily']['temperature_2m_max'],
            'Precipitation': data['daily']['precipitation_sum']
        })
        
        # Add weather code for forecast
        if forecast and 'weathercode' in data['daily']:
            weather_df['Weather Code'] = data['daily']['weathercode']
        
        weather_df['Date'] = weather_df['Date'].dt.strftime('%Y-%m-%d')
        return weather_df
    
    except Exception as e:
        return None


def get_weather_description(code):
    """Convert weather code to human-readable description."""
    weather_codes = {
        0: "☀️ Clear",
        1: "🌤️ Mostly Clear",
        2: "⛅ Partly Cloudy",
        3: "☁️ Overcast",
        45: "🌫️ Foggy",
        48: "🌫️ Icy Fog",
        51: "🌧️ Light Drizzle",
        53: "🌧️ Drizzle",
        55: "🌧️ Heavy Drizzle",
        61: "🌧️ Light Rain",
        63: "🌧️ Rain",
        65: "🌧️ Heavy Rain",
        71: "🌨️ Light Snow",
        73: "🌨️ Snow",
        75: "🌨️ Heavy Snow",
        80: "🌦️ Rain Showers",
        81: "🌧️ Rain Showers",
        82: "⛈️ Heavy Showers",
        95: "⛈️ Thunderstorm",
        96: "⛈️ Thunderstorm + Hail",
        99: "⛈️ Severe Thunderstorm"
    }
    return weather_codes.get(code, "🌡️ Unknown")


def get_nearby_events(lat, lon, days_ahead=7):
    """
    Get nearby events from Ticketmaster Discovery API for the next N days.
    
    Returns:
    - List of event dictionaries with date, name, venue, and type
    """
    try:
        if not api_key:
            return []
        
        start_datetime = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
        end_datetime = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%dT23:59:59Z')
        
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            'apikey': api_key,
            'latlong': f"{lat},{lon}",
            'radius': 10,
            'unit': 'km',
            'size': 50,
            'startDateTime': start_datetime,
            'endDateTime': end_datetime,
            'sort': 'date,asc'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        events = []
        if '_embedded' in data and 'events' in data['_embedded']:
            for event in data['_embedded']['events']:
                event_date = event.get('dates', {}).get('start', {}).get('localDate', '')
                events.append({
                    'date': event_date,
                    'name': event.get('name', 'Unknown Event'),
                    'venue': event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'Unknown Venue'),
                    'type': event.get('classifications', [{}])[0].get('segment', {}).get('name', 'Event'),
                    'is_high_traffic': len(event.get('priceRanges', [])) > 0  # Has tickets = likely big event
                })
        
        return events
    
    except Exception as e:
        return []


def get_events_for_date(events_list, target_date):
    """Get events happening on a specific date."""
    return [e for e in events_list if e.get('date') == target_date]


# ============================================================================
# HYBRID PREDICTION ENGINE
# ============================================================================
def get_forecast(lat, lon, sales_df=None, forecast_days=7):
    """
    The Hybrid Prediction Engine.
    
    Step A (History): Load sales data, merge with user adjustments, train model
    Step B (Context): Apply weather/events/holidays modifiers
    
    Returns predictions with context-aware adjustments.
    """
    # Step A: Get historical data with learning adjustments
    if sales_df is None:
        if st.session_state.lightspeed_data is not None:
            sales_df = st.session_state.lightspeed_data.copy()
        else:
            return None
    
    # Apply learned adjustments from user feedback
    adjusted_sales = apply_learning_to_data(sales_df)
    
    # Aggregate and process
    aggregated = aggregate_sales(adjusted_sales)
    if aggregated is None or aggregated.empty:
        return None
    
    # Get date range for weather
    min_date = aggregated['Date'].min()
    max_date = aggregated['Date'].max()
    
    # Fetch historical weather
    weather_df = get_weather_data(lat, lon, min_date, max_date, forecast=False)
    if weather_df is None:
        return None
    
    # Engineer features
    sales_with_features = engineer_features(aggregated)
    
    # Merge with weather
    training_data = merge_sales_weather(sales_with_features, weather_df, lat, lon)
    if training_data is None:
        return None
    
    # Train model
    predictor = train_model(training_data)
    if predictor is None:
        return None
    
    st.session_state.predictor = predictor
    st.session_state.model_trained = True
    
    # Step B: Generate predictions with context
    predictions = predict_with_context(
        predictor,
        st.session_state.item_names or adjusted_sales['Item Name'].unique().tolist(),
        lat, lon,
        forecast_days
    )
    
    return predictions


def predict_with_context(predictor, item_names, lat, lon, forecast_days=7):
    """
    Generate predictions with context-aware adjustments.
    
    Context modifiers:
    - High Traffic Event: +20% boost
    - Rain: -30% on cold drinks
    - Hot weather (>25°C): +20% on cold drinks
    - Public Holiday: +15% overall
    - School Holiday: +10% overall
    """
    if predictor is None or not item_names:
        return None
    
    tomorrow = datetime.now() + timedelta(days=1)
    end_date = tomorrow + timedelta(days=forecast_days - 1)
    
    # Get forecast weather
    weather_forecast = get_weather_data(
        lat, lon,
        tomorrow.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        forecast=True
    )
    
    if weather_forecast is None:
        return None
    
    # Get events for the forecast period
    events = get_nearby_events(lat, lon, days_ahead=forecast_days)
    
    predictions = []
    
    for _, weather_row in weather_forecast.iterrows():
        forecast_date = weather_row['Date']
        forecast_dt = datetime.strptime(forecast_date, '%Y-%m-%d')
        
        # Feature engineering for this date
        day_of_week = forecast_dt.weekday()
        is_weekend_flag = 1 if day_of_week >= 5 else 0
        is_public_holiday_flag = 1 if get_public_holiday_status(forecast_dt) else 0
        is_school_holiday_flag = 1 if is_school_holiday(forecast_dt) else 0
        is_high_spend_day_flag = 1 if day_of_week in [2, 3, 4] else 0
        
        # Get events for this date
        day_events = get_events_for_date(events, forecast_date)
        has_high_traffic_event = any(e.get('is_high_traffic') for e in day_events)
        event_count = len(day_events)
        
        # Weather context
        max_temp = weather_row.get('Max Temp', 20)
        precipitation = weather_row.get('Precipitation', 0)
        weather_code = weather_row.get('Weather Code', 0)
        is_rainy = precipitation > 2 or weather_code >= 61
        is_hot = max_temp >= 25
        
        for item_name in item_names:
            # Build prediction features
            features = pd.DataFrame([{
                'Item Name': item_name,
                'Day of Week': day_of_week,
                'Is Weekend': is_weekend_flag,
                'Is_Public_Holiday': is_public_holiday_flag,
                'Is_School_Holiday': is_school_holiday_flag,
                'Is_High_Spend_Day': is_high_spend_day_flag,
                'Max Temp': max_temp,
                'Precipitation': precipitation,
                'Nearby_Events': event_count
            }])
            
            # Get base prediction
            try:
                base_pred = predictor.predict(features)[0]
            except Exception:
                base_pred = 0
            
            # Apply context modifiers
            adjusted_pred = base_pred
            modifiers = []
            
            # High Traffic Event: +20%
            if has_high_traffic_event:
                adjusted_pred *= 1.20
                modifiers.append("🎫 Event +20%")
            
            # Rain impact on cold drinks
            item_lower = item_name.lower()
            is_cold_drink = any(term in item_lower for term in 
                ['iced', 'cold', 'frappe', 'smoothie', 'shake', 'cold brew'])
            
            if is_rainy and is_cold_drink:
                adjusted_pred *= 0.70
                modifiers.append("🌧️ Rain -30%")
            
            # Hot weather boost for cold drinks
            if is_hot and is_cold_drink:
                adjusted_pred *= 1.20
                modifiers.append("☀️ Hot +20%")
            
            # Public holiday boost
            if is_public_holiday_flag:
                adjusted_pred *= 1.15
                modifiers.append("🎉 Holiday +15%")
            
            # School holiday boost
            if is_school_holiday_flag:
                adjusted_pred *= 1.10
                modifiers.append("🏫 School Break +10%")
            
            predictions.append({
                'Date': forecast_date,
                'Item Name': item_name,
                'Base Prediction': round(base_pred, 1),
                'Predicted Quantity': round(max(0, adjusted_pred), 0),
                'Max Temp': max_temp,
                'Precipitation': precipitation,
                'Weather': get_weather_description(weather_code) if weather_code else "🌡️",
                'Events': ', '.join([e['name'][:20] for e in day_events]) if day_events else "None",
                'Event Count': event_count,
                'Modifiers': ' | '.join(modifiers) if modifiers else "None",
                'Is Public Holiday': is_public_holiday_flag,
                'Is School Holiday': is_school_holiday_flag
            })
    
    return pd.DataFrame(predictions)


# ============================================================================
# CORE FUNCTIONS (From existing app)
# ============================================================================
def aggregate_sales(df):
    """Aggregate sales data by Date and Item Name."""
    try:
        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        aggregated = df.groupby(['Date', 'Item Name'], as_index=False)['Quantity Sold'].sum()
        return aggregated
    except Exception as e:
        return None


def engineer_features(df):
    """Add feature columns for ML model."""
    try:
        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df['Day of Week'] = df['Date'].dt.dayofweek
        df['Is Weekend'] = (df['Day of Week'] >= 5).astype(int)
        df['Is_Public_Holiday'] = df['Date'].apply(
            lambda x: 1 if get_public_holiday_status(x) else 0
        )
        df['Is_School_Holiday'] = df['Date'].apply(
            lambda x: 1 if is_school_holiday(x) else 0
        )
        df['Is_High_Spend_Day'] = df['Day of Week'].apply(
            lambda x: 1 if x in [2, 3, 4] else 0
        )
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        return None


def merge_sales_weather(sales_df, weather_df, lat=None, lon=None):
    """Merge sales data with weather data."""
    try:
        merged = pd.merge(sales_df, weather_df, on='Date', how='left')
        if merged['Max Temp'].isna().any():
            merged['Max Temp'].fillna(merged['Max Temp'].median(), inplace=True)
        if merged['Precipitation'].isna().any():
            merged['Precipitation'].fillna(merged['Precipitation'].median(), inplace=True)
        
        # Add event count (simplified for training)
        merged['Nearby_Events'] = 0
        return merged
    except Exception as e:
        return None


def train_model(training_data, model_path='models/stock_predictor'):
    """Train AutoGluon model on the training data."""
    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        predictor = TabularPredictor(
            label='Quantity Sold',
            path=model_path
        )
        
        training_features = training_data.drop(columns=['Date'])
        
        predictor.fit(
            training_features,
            time_limit=60,
            presets='medium_quality',
            verbosity=0
        )
        
        return predictor
    except Exception as e:
        st.error(f"Error training model: {e}")
        return None


# ============================================================================
# DEMO DATA GENERATOR (For Pitch Mode)
# ============================================================================
def generate_demo_data():
    """Generate realistic demo data for pitch presentations."""
    items = [
        "Flat White", "Long Black", "Cappuccino", "Latte", "Mocha",
        "Iced Latte", "Cold Brew", "Chai Latte", "Hot Chocolate",
        "Croissant", "Muffin", "Banana Bread", "Avocado Toast",
        "Eggs Benedict", "Acai Bowl", "Smoothie Bowl"
    ]
    
    # Generate 90 days of demo data
    dates = pd.date_range(end=datetime.now() - timedelta(days=1), periods=90)
    
    demo_sales = []
    for d in dates:
        day_of_week = d.weekday()
        is_weekend = day_of_week >= 5
        
        for item in items:
            # Base quantity varies by item type
            if 'Coffee' in item or 'White' in item or 'Black' in item:
                base = random.randint(30, 60)
            elif 'Iced' in item or 'Cold' in item:
                base = random.randint(15, 35)
            else:
                base = random.randint(10, 25)
            
            # Weekend boost
            if is_weekend:
                base = int(base * 1.3)
            
            # Add some variance
            qty = max(1, base + random.randint(-10, 10))
            
            demo_sales.append({
                'Date': d.strftime('%Y-%m-%d'),
                'Item Name': item,
                'Quantity Sold': qty
            })
    
    return pd.DataFrame(demo_sales)


# ============================================================================
# LIGHTSPEED OAUTH FUNCTIONS (Preserved from original)
# ============================================================================
def get_lightspeed_auth_url():
    """Generate the Lightspeed OAuth authorization URL."""
    from urllib.parse import quote_plus
    
    state = secrets.token_urlsafe(16)
    st.session_state.oauth_state = state
    
    scope = "products:read sales:read customers:read inventory:read register_sales:read"
    auth_url = (
        f"https://secure.retail.lightspeed.app/connect"
        f"?response_type=code"
        f"&client_id={lightspeed_client_id}"
        f"&redirect_uri={quote_plus(redirect_uri)}"
        f"&scope={quote_plus(scope)}"
        f"&state={quote_plus(state)}"
    )
    return auth_url


def get_lightspeed_api_base():
    """Get the base API URL using the stored domain prefix."""
    domain_prefix = st.session_state.get('lightspeed_domain_prefix')
    if not domain_prefix:
        return None
    return f"https://{domain_prefix}.retail.lightspeed.app"


def exchange_code_for_token(code, domain_prefix=None):
    """Exchange authorization code for access token."""
    try:
        if not domain_prefix:
            return None
        
        token_url = f"https://{domain_prefix}.retail.lightspeed.app/api/1.0/token"
        
        data = {
            'client_id': lightspeed_client_id,
            'client_secret': lightspeed_client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.post(token_url, data=data, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
        
        token_data = response.json()
        
        if 'error' in token_data:
            return None
        
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        
        if access_token:
            st.session_state.access_token = access_token
        if refresh_token:
            st.session_state.refresh_token = refresh_token
        if domain_prefix:
            st.session_state.lightspeed_domain_prefix = domain_prefix
        
        return access_token
    
    except Exception as e:
        return None


def fetch_historical_sales(days=365):
    """Fetch historical sales data from Lightspeed."""
    try:
        if not st.session_state.access_token:
            return None
        
        api_base = get_lightspeed_api_base()
        if not api_base:
            return None
        
        # Fetch product map first
        product_map = fetch_product_map()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        all_sales = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{api_base}/api/2.0/sales"
            params = {
                'created_at': f">={start_date.strftime('%Y-%m-%d')}",
                'page': page,
                'per_page': per_page
            }
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code != 200:
                break
            
            data = response.json()
            sales = data.get('data', [])
            
            if not sales:
                break
            
            for sale in sales:
                sale_date = sale.get('createdAt') or sale.get('created_at') or ''
                if not sale_date:
                    continue
                
                try:
                    if 'T' in sale_date:
                        sale_date_parsed = dateutil_parser.isoparse(sale_date).date()
                    else:
                        sale_date_parsed = pd.to_datetime(sale_date, utc=True).date()
                except:
                    continue
                
                line_items = sale.get('line_items') or sale.get('register_sale_products') or []
                
                for item in line_items:
                    product_id = item.get('product_id') or item.get('productID')
                    product_name = product_map.get(str(product_id), 'Unknown') if product_id else 'Unknown'
                    qty = float(item.get('quantity', 0))
                    
                    if qty > 0:
                        all_sales.append({
                            'Date': sale_date_parsed.strftime('%Y-%m-%d'),
                            'Item Name': product_name,
                            'Quantity Sold': qty
                        })
            
            if len(sales) < per_page:
                break
            
            page += 1
        
        if not all_sales:
            return None
        
        df = pd.DataFrame(all_sales)
        return df.groupby(['Date', 'Item Name'], as_index=False)['Quantity Sold'].sum()
    
    except Exception as e:
        return None


def fetch_product_map():
    """Fetch product ID to name mapping from Lightspeed."""
    try:
        if not st.session_state.access_token:
            return {}
        
        api_base = get_lightspeed_api_base()
        if not api_base:
            return {}
        
        product_map = {}
        page = 1
        
        while True:
            url = f"{api_base}/api/2.0/products"
            params = {'page': page, 'per_page': 100}
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code != 200:
                break
            
            data = response.json()
            products = data.get('data', [])
            
            for product in products:
                pid = product.get('id')
                pname = product.get('description') or product.get('name')
                if pid and pname:
                    product_map[str(pid)] = str(pname)
            
            if len(products) < 100:
                break
            
            page += 1
        
        return product_map
    
    except Exception:
        return {}


# ============================================================================
# MORNING REVIEW WORKFLOW (Reinforcement Learning)
# ============================================================================
def check_if_new_day():
    """Check if we should show the morning review."""
    user_data = load_shop_data()
    last_review = user_data.get("last_review_date")
    
    if last_review is None:
        return True
    
    today = datetime.now().strftime('%Y-%m-%d')
    return last_review != today


def get_yesterdays_top_items(n=5):
    """Get yesterday's top selling items for review."""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Use Lightspeed data or demo data
    if st.session_state.pitch_mode:
        sales_df = generate_demo_data()
    elif st.session_state.lightspeed_data is not None:
        sales_df = st.session_state.lightspeed_data.copy()
    else:
        return []
    
    # Filter to yesterday
    yesterday_sales = sales_df[sales_df['Date'] == yesterday]
    
    if yesterday_sales.empty:
        # Try the most recent date
        latest_date = sales_df['Date'].max()
        yesterday_sales = sales_df[sales_df['Date'] == latest_date]
    
    if yesterday_sales.empty:
        return []
    
    # Get top items
    top_items = (
        yesterday_sales
        .groupby('Item Name')['Quantity Sold']
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )
    
    return [
        {'item': item, 'qty': qty, 'date': yesterday_sales['Date'].iloc[0]}
        for item, qty in top_items.items()
    ]


def render_morning_review():
    """Render the Morning Review UI component."""
    if st.session_state.morning_review_done:
        return False
    
    if not check_if_new_day():
        return False
    
    top_items = get_yesterdays_top_items(5)
    
    if not top_items:
        return False
    
    st.markdown("""
    <div class="morning-review">
        <h3>☀️ Good Morning! Yesterday's Stock Review</h3>
        <p style="color: #b8d4b8; margin-bottom: 16px;">
            Help the AI learn by reviewing how well you were stocked yesterday.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    review_date = top_items[0]['date']
    st.caption(f"📅 Reviewing: {review_date}")
    
    feedback_submitted = False
    
    for i, item_data in enumerate(top_items):
        item_name = item_data['item']
        original_qty = item_data['qty']
        
        with st.container():
            st.markdown(f"**{item_name}** — Sold: **{int(original_qty)}**")
            
            cols = st.columns(5)
            
            with cols[0]:
                if st.button("🟢 Too Much", key=f"too_much_{i}", use_container_width=True):
                    record_adjustment(item_name, review_date, 'too_much', original_qty, original_qty)
                    feedback_submitted = True
            
            with cols[1]:
                if st.button("🟢 Bit More", key=f"bit_more_{i}", use_container_width=True):
                    record_adjustment(item_name, review_date, 'bit_more', original_qty, original_qty)
                    feedback_submitted = True
            
            with cols[2]:
                if st.button("✅ Perfect", key=f"perfect_{i}", use_container_width=True):
                    record_adjustment(item_name, review_date, 'perfect', original_qty, original_qty)
                    feedback_submitted = True
            
            with cols[3]:
                if st.button("🟠 Bit Less", key=f"bit_less_{i}", use_container_width=True):
                    # A Bit Less means we sold out early, true demand was higher
                    true_demand = original_qty * 1.2
                    record_adjustment(item_name, review_date, 'bit_less', original_qty, true_demand)
                    feedback_submitted = True
            
            with cols[4]:
                if st.button("🔴 Too Less", key=f"too_less_{i}", use_container_width=True):
                    # Too Less means we definitely sold out, true demand much higher
                    true_demand = original_qty * 1.5
                    record_adjustment(item_name, review_date, 'too_less', original_qty, true_demand)
                    feedback_submitted = True
            
            st.markdown("---")
    
    # Skip button
    if st.button("⏭️ Skip Review for Today", use_container_width=True):
        st.session_state.morning_review_done = True
        st.rerun()
    
    if feedback_submitted:
        st.success("✅ Feedback recorded! The AI will learn from this.")
        time.sleep(0.5)
        st.rerun()
    
    return True


# ============================================================================
# 7-DAY OUTLOOK COMPONENT
# ============================================================================
def render_7day_outlook(predictions_df, lat, lon):
    """Render the 7-Day Outlook list with events and weather."""
    if predictions_df is None or predictions_df.empty:
        st.info("Generate a forecast to see your 7-day outlook.")
        return
    
    # Get unique dates
    dates = predictions_df['Date'].unique()
    
    # Get events
    events = get_nearby_events(lat, lon, days_ahead=7)
    
    st.markdown("### 📅 7-Day Outlook")
    
    for date_str in dates:
        day_data = predictions_df[predictions_df['Date'] == date_str].iloc[0]
        day_events = get_events_for_date(events, date_str)
        
        # Format date nicely
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        day_name = dt.strftime('%A')
        date_display = dt.strftime('%b %d')
        
        # Total forecast for the day
        day_total = predictions_df[predictions_df['Date'] == date_str]['Predicted Quantity'].sum()
        
        # Build event string
        event_str = day_events[0]['name'][:30] if day_events else "No major events"
        
        # Weather emoji
        weather = day_data.get('Weather', '🌡️')
        
        # Check for holidays
        is_holiday = day_data.get('Is Public Holiday', 0) == 1
        is_school_hol = day_data.get('Is School Holiday', 0) == 1
        
        holiday_badge = ""
        if is_holiday:
            holiday_badge = "🎉 Public Holiday"
        elif is_school_hol:
            holiday_badge = "🏫 School Holidays"
        
        # Render row
        with st.container():
            cols = st.columns([2, 3, 2])
            
            with cols[0]:
                st.markdown(f"**{day_name}**")
                st.caption(date_display)
            
            with cols[1]:
                st.markdown(f"{weather} {event_str}")
                if holiday_badge:
                    st.caption(holiday_badge)
            
            with cols[2]:
                st.markdown(f"**{int(day_total)} items**")
                st.caption(f"{day_data.get('Max Temp', 20):.0f}°C")
        
        st.markdown("---")


# ============================================================================
# INSTALL GUIDE (Add to Home Screen)
# ============================================================================
def render_install_guide():
    """Show install instructions for Add to Home Screen."""
    st.markdown("""
    ### 📱 Install Cafe AI on Your iPad
    
    **For Safari (iOS/iPadOS):**
    1. Tap the **Share** button (square with arrow)
    2. Scroll down and tap **"Add to Home Screen"**
    3. Name it "Cafe AI" and tap **Add**
    4. Open from your home screen - it runs like a native app!
    
    **For Chrome (Android):**
    1. Tap the **three dots** menu (⋮)
    2. Tap **"Add to Home screen"**
    3. Tap **Add**
    
    ---
    
    **Pro Tips:**
    - 📌 Pin the tab for instant access
    - 🔄 The app syncs your data across sessions
    - 📊 Check in each morning to train the AI
    """)


# ============================================================================
# MAIN APP UI
# ============================================================================

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">☕ Cafe AI</div>
    <div class="hero-subtitle">Your Self-Learning Stock Prediction System</div>
</div>
""", unsafe_allow_html=True)

# Handle OAuth callback
query_params = st.query_params
if 'code' in query_params:
    code = query_params.get('code')
    domain_prefix = query_params.get('domain_prefix')
    returned_state = query_params.get('state')
    
    if returned_state == st.session_state.oauth_state:
        token = exchange_code_for_token(code, domain_prefix)
        if token:
            st.success("✅ Connected to Lightspeed!")
            # Fetch sales data
            with st.spinner("Fetching your sales data..."):
                sales_df = fetch_historical_sales(days=365)
                if sales_df is not None:
                    st.session_state.lightspeed_data = sales_df
                    st.session_state.item_names = sales_df['Item Name'].unique().tolist()
            st.query_params.clear()
            st.rerun()

# Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Pitch Mode Toggle
    st.session_state.pitch_mode = st.toggle(
        "🎭 Pitch Mode (Demo Data)",
        value=st.session_state.pitch_mode,
        help="Switch between real data and demo data for presentations"
    )
    
    if st.session_state.pitch_mode:
        st.markdown('<div class="pitch-mode-active">📊 DEMO MODE ACTIVE</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Location Settings
    st.markdown("### 📍 Location")
    lat_input = st.text_input("Latitude", value="-36.8509")
    lon_input = st.text_input("Longitude", value="174.7645")
    
    try:
        lat_float = float(lat_input)
        lon_float = float(lon_input)
    except:
        lat_float, lon_float = -36.8509, 174.7645
    
    st.markdown("---")
    
    # Connection Status
    st.markdown("### 🔗 Data Source")
    
    if st.session_state.pitch_mode:
        st.success("Using Demo Data")
    elif st.session_state.access_token:
        st.success("✅ Connected to Lightspeed")
        if st.button("🔌 Disconnect", use_container_width=True):
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.lightspeed_data = None
            st.rerun()
    else:
        st.info("Connect to Lightspeed for real data")
        if lightspeed_client_id:
            auth_url = get_lightspeed_auth_url()
            st.link_button("🔗 Connect to Lightspeed", auth_url, use_container_width=True)
        else:
            st.warning("Set LIGHTSPEED_CLIENT_ID in .env")
    
    st.markdown("---")
    
    # Install Guide
    if st.button("ℹ️ Install on iPad", use_container_width=True):
        st.session_state.show_install_guide = not st.session_state.show_install_guide
    
    # Learning Stats
    st.markdown("### 🧠 AI Learning")
    user_data = load_shop_data()
    st.metric("Reviews Recorded", user_data.get("total_reviews", 0))
    st.metric("Adjustments Learned", len(user_data.get("adjustments", [])))

# Main Content Area
if st.session_state.show_install_guide:
    render_install_guide()
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.show_install_guide = False
        st.rerun()
else:
    # Morning Review (if applicable)
    show_review = render_morning_review()
    
    if not show_review:
        # Main Dashboard
        
        # Quick Actions Bar (visible in main view for easy access)
        quick_cols = st.columns([1, 1, 1])
        with quick_cols[0]:
            if st.button("🎭 Try Demo Mode", use_container_width=True):
                st.session_state.pitch_mode = True
                demo_df = generate_demo_data()
                st.session_state.lightspeed_data = demo_df
                st.session_state.item_names = demo_df['Item Name'].unique().tolist()
                st.rerun()
        
        with quick_cols[1]:
            if lightspeed_client_id and not st.session_state.access_token:
                auth_url = get_lightspeed_auth_url()
                st.link_button("🔗 Connect Lightspeed", auth_url, use_container_width=True)
            elif st.session_state.access_token:
                st.success("✅ Connected")
            else:
                st.info("⚙️ Set up .env")
        
        with quick_cols[2]:
            if st.button("⚙️ Settings", use_container_width=True):
                st.info("👈 Open sidebar for settings (swipe or tap hamburger menu)")
        
        # Show pitch mode indicator
        if st.session_state.pitch_mode:
            st.markdown('<div class="pitch-mode-active">🎭 DEMO MODE - Using simulated cafe data</div>', unsafe_allow_html=True)
        
        # Load data based on mode
        if st.session_state.pitch_mode:
            if st.session_state.lightspeed_data is None or 'demo' not in str(type(st.session_state.lightspeed_data)):
                demo_df = generate_demo_data()
                st.session_state.lightspeed_data = demo_df
                st.session_state.item_names = demo_df['Item Name'].unique().tolist()
        
        # Check if we have data
        has_data = st.session_state.lightspeed_data is not None
        
        st.markdown("---")
        
        # Generate Forecast Button
        col_action = st.columns([1, 2, 1])
        with col_action[1]:
            if st.button("🚀 Generate AI Forecast", use_container_width=True, type="primary"):
                if has_data:
                    with st.spinner("🧠 Training AI and generating forecast..."):
                        predictions = get_forecast(lat_float, lon_float, forecast_days=7)
                        if predictions is not None:
                            st.session_state.predictions = predictions
                            st.success("✅ Forecast ready!")
                            st.rerun()
                        else:
                            st.error("Failed to generate forecast. Check your data.")
                else:
                    st.warning("Please click 'Try Demo Mode' or connect to Lightspeed to get data.")
        
        # Dashboard Metrics
        if 'predictions' in st.session_state and st.session_state.predictions is not None:
            predictions_df = st.session_state.predictions
            
            st.markdown("---")
            
            # Top 3 Big Metrics
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            tomorrow_preds = predictions_df[predictions_df['Date'] == tomorrow]
            
            if not tomorrow_preds.empty:
                total_forecast = tomorrow_preds['Predicted Quantity'].sum()
                weather_info = tomorrow_preds['Weather'].iloc[0]
                top_item = tomorrow_preds.loc[tomorrow_preds['Predicted Quantity'].idxmax()]
                
                # Get any modifiers/advice
                modifiers = tomorrow_preds['Modifiers'].unique()
                advice_list = [m for m in modifiers if m != "None"]
                advice = advice_list[0] if advice_list else "Steady day predicted"
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="big-metric-card">
                        <div class="big-metric-icon">☕</div>
                        <div class="big-metric-value">{}</div>
                        <div class="big-metric-label">Tomorrow's Total Forecast</div>
                    </div>
                    """.format(int(total_forecast)), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="big-metric-card">
                        <div class="big-metric-icon">{}</div>
                        <div class="big-metric-value">{}°C</div>
                        <div class="big-metric-label">Tomorrow's Weather</div>
                    </div>
                    """.format(weather_info.split()[0] if weather_info else "🌡️", 
                              int(top_item['Max Temp'])), unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="big-metric-card">
                        <div class="big-metric-icon">⚠️</div>
                        <div class="big-metric-value" style="font-size: 1.2rem;">{}</div>
                        <div class="big-metric-label">AI Advice</div>
                    </div>
                    """.format(advice[:30]), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 7-Day Outlook
            render_7day_outlook(predictions_df, lat_float, lon_float)
            
            st.markdown("---")
            
            # Detailed Predictions Table
            with st.expander("📊 Detailed Item Predictions", expanded=False):
                # Group by date and show top items
                for date_str in predictions_df['Date'].unique():
                    day_data = predictions_df[predictions_df['Date'] == date_str].copy()
                    day_data = day_data.sort_values('Predicted Quantity', ascending=False)
                    
                    dt = datetime.strptime(date_str, '%Y-%m-%d')
                    st.markdown(f"**{dt.strftime('%A, %B %d')}** — {day_data['Weather'].iloc[0]}")
                    
                    display_df = day_data[['Item Name', 'Predicted Quantity', 'Modifiers']].head(10)
                    display_df.columns = ['Item', 'Qty', 'Adjustments']
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    st.markdown("---")
        
        elif has_data:
            # Show data preview if we have data but no predictions yet
            st.info("👆 Click 'Generate AI Forecast' to see predictions")
            
            with st.expander("📊 Your Sales Data Preview", expanded=False):
                st.dataframe(st.session_state.lightspeed_data.head(20), use_container_width=True)
                st.caption(f"Total records: {len(st.session_state.lightspeed_data)}")
        
        else:
            # No data state
            st.markdown("""
            <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
                <h3>Welcome to Cafe AI! 👋</h3>
                <p>Get started by connecting your Lightspeed account or enabling Pitch Mode for a demo.</p>
            </div>
            """, unsafe_allow_html=True)

# Footer with version
st.markdown("---")
st.caption("Cafe AI v2.0 • Production Release • Self-Learning Stock Prediction")
