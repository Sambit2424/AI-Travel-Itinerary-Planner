import warnings

warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()  # ✅ must be FIRST

import streamlit as st
import logfire
from src.core.planner import TravelPlanner
from src.utils.logger import get_logger

# Initialize Logfire Tracing
logfire.configure()
logfire.instrument_httpx()
logfire.instrument_pydantic()

logger = get_logger(__name__)

# --- Page Config ---
st.set_page_config(page_title="Voyagr | Travel without the guesswork", layout="centered")

# --- Custom CSS (Regal Gold Tint + 20% Upscale) ---
st.markdown("""
    <style>
    /* Global Font Upscaling */
    html, body, [class*="css"]  {
        font-size: 1.2rem; 
    }
    
    .stApp {
        background: linear-gradient(rgba(26, 20, 5, 0.92), rgba(14, 17, 23, 0.95)), 
                    url('https://unsplash.com');
        background-size: cover;
        background-attachment: fixed;
        color: #FFFFFF;
        font-family: 'serif';
    }
    
    .hero-title {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 4.2rem; 
        font-weight: 400;
        margin-top: 40px;
        color: #F0E6D2;
        line-height: 1.1;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.35rem; 
        color: #C19A43;
        margin-bottom: 50px;
        letter-spacing: 1px;
    }
    .logo {
        text-align: center;
        font-size: 1.6rem;
        letter-spacing: 5px;
        margin-top: 50px;
        color: #C19A43;
        font-weight: bold;
    }

    [data-testid="stForm"] {
        background-color: rgba(26, 28, 36, 0.8) !important;
        border: 1px solid rgba(193, 154, 67, 0.3) !important; 
        border-radius: 25px !important;
        padding: 55px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }

    input, div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(38, 41, 51, 0.8) !important;
        border-radius: 10px !important;
        border: 1px solid #3A3E4A !important;
        color: white !important;
        min-height: 60px !important; 
    }

    label p {
        color: #F0E6D2 !important; 
        text-transform: uppercase;
        font-size: 0.95rem !important; 
        letter-spacing: 1.5px;
        font-weight: 600 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #C19A43 0%, #8C6F2D 100%) !important;
        color: #000 !important;
        border: none !important;
        width: 100% !important;
        padding: 22px !important; 
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 1.3rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 35px;
        box-shadow: 0 4px 15px rgba(193, 154, 67, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(193, 154, 67, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI Header ---
st.markdown('<div class="logo">🔱 VOYAGR</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Travel without<br>the guesswork</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Bespoke itineraries for the modern explorer</p>', unsafe_allow_html=True)

# --- Planner Form ---
with st.form("planner_form", border=True):
    city = st.text_input("WHERE TO?", placeholder="Paris, Kyoto, Varanasi...")
    
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("TRAVEL STYLE", ["Budget", "Mid-range", "Luxury"])
        month = st.selectbox("MONTH", ["Flexible", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    with col2:
        pace = st.selectbox("PACE", ["Relaxed", "Balanced", "Packed"])
        days = st.slider("DURATION", 1, 10, 3)

    # Replaced Dropdown with Flexible Text Input
    raw_interests = st.text_input("INTERESTS", placeholder="e.g. Fine Dining, Ancient History, Hidden Gems...")
    
    submitted = st.form_submit_button("PLAN MY JOURNEY →")

# --- Logic Section ---
if submitted:
    if city and raw_interests:
        # Convert comma-separated string to a cleaned list
        interests_list = [i.strip() for i in raw_interests.split(",") if i.strip()]
        
        planner = TravelPlanner()
        result = planner.create_itinerary(
            city=city, days=days, interests=interests_list,
            style=style, pace=pace, 
            month=None if month == "Flexible" else month
        )
        itinerary = result["itinerary"]

        st.markdown(f"## 📄 {itinerary.city}")
        st.markdown(f"**{itinerary.total_days} Day {style} Experience**")
        
        for day in itinerary.itinerary:
            with st.expander(f"Day {day.day_number}: {day.theme}", expanded=True):
                for activity in day.activities:
                    st.markdown(f"🕒 `{activity.time}` **{activity.location}**")
                    st.write(activity.description)
                st.info(f"🍴 Food: {', '.join(day.food_recommendations)}")
    else:
        st.warning("Please specify both a destination and your interests.")