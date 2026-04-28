import warnings
warnings.filterwarnings("ignore")

import dotenv
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import streamlit as st
from src.core.planner import Travelplanner, plan_trip
from src.utils.custom_exception import DetailedException
from src.utils.logger import get_logger
import datetime

# Setting up our watchman
logger = get_logger(__name__)

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

# 1. Consolidated CSS: Aesthetic & Legibility
st.markdown("""
    <style>
        /* 1. Eliminate the actual Streamlit header/menu bar completely */
    header {visibility: hidden;}
    .stAppHeader {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}

    /* 2. Target the main content area to pull it up */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -5rem !important; /* Forces the content higher */
    }

    /* 3. New class for Streamlit 1.35+ compatibility */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 0rem !important;
    }

    /* 4. Remove top decoration line (the red/colored bar) */
    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Optional: Remove extra space specifically around the title */
    .stHeadingContainer {
        margin-top: -50px !important;
    }
            
    /* Theme: Midnight Alpine */
    .stApp {
        background: radial-gradient(circle at top, #1e3d59 0%, #111827 100%);
        background-attachment: fixed;
    }

    /* Glassmorphic Form Container */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(25px) saturate(150%);
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 50px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }

    /* Legibility: Labels & Spacing */
    [data-testid="stWidgetLabel"] p {
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        color: #e0f2f1 !important;
        margin-bottom: 10px !important;
    }

    /* Large Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        font-size: 1.2rem !important;
        height: 55px !important;
        color: #111827 !important;
    }

    /* Grey Placeholders */
    ::placeholder { color: #6c757d !important; opacity: 1; }
    input::placeholder { color: #6c757d !important; }

    /* Space between form elements */
    [data-testid="stVerticalBlock"] > div {
        margin-bottom: 15px !important;
    }

    /* Call to Action Button */
    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 0px !important;
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(79, 172, 254, 0.4);
    }

    /* Itinerary Output Legibility */
    .stMarkdown div {
        background: rgba(255, 255, 255, 0.98);
        padding: 30px;
        border-radius: 25px;
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
        color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍AI Travel Itinerary Planner")

with st.form("travel_form"):
    city = st.text_input("📌 City", placeholder="Enter the city you want to visit")
    days = st.slider("⌛ Number of Days", min_value=1, max_value=30, value=3)
    interests = st.text_input("🎯 Interests (enter comma-separated values)", placeholder="e.g., sightseeing, food, thrills")
    style = st.selectbox("💰 Travel Style", options=["Budget", "Luxury", "Adventure", "Cultural"], index=0)
    pace = st.selectbox("🚶‍♂️ Travel Pace", options=["Relaxed", "Moderate", "Fast"], index=1)
    month = st.selectbox("📆 Month (optional)", options=["Any"] + ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=0)
    accom_rate_per_day_inr = st.number_input("🏨 Accommodation Budget per Day (INR, optional)", min_value=500.0, step=100.0)

    submitted = st.form_submit_button("🪄 Generate Itinerary")

if submitted:
    if city and days:
        planner = Travelplanner(city=city,
            days=days,
            interests=[i.strip() for i in interests.split(",")],
            style=style,
            pace=pace,
            month=month if month != "Any" else None,
            accom_rate_per_day_inr=accom_rate_per_day_inr if accom_rate_per_day_inr > 0 else None
        )

        itinerary = plan_trip(
            data=planner
        )

        st.subheader("📜 Your AI-Generated Travel Itinerary:")
        st.markdown(itinerary)

        logger.info("Response generated")
    else:
        st.warning("Please fill in the required fields: City and Number of Days.")


