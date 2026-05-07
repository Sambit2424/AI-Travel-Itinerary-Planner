import warnings

warnings.filterwarnings(
    "ignore"
)

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

with st.form("planner_form"):
    city = st.text_input("📍 City")
    days = st.slider("🗓️ Number of days", 1, 10, 3)
    interests = st.text_input("🎯 Interests (comma-separated)")
    style = st.selectbox("💰 Travel Style", ["Budget", "Mid-range", "Luxury"])
    pace = st.selectbox("🚶 Pace", ["Relaxed", "Balanced", "Packed"])
    month = st.selectbox("📅 Month (optional)", ["Any"] + [
        "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
    ])

    submitted = st.form_submit_button("✨ Generate Itinerary")

if submitted:
    if city and interests:
        planner = TravelPlanner()

        result = planner.create_itinerary(
            city=city,
            days=days,
            interests=[i.strip() for i in interests.split(",")],
            style=style,
            pace=pace,
            month=None if month == "Any" else month
        )
        
        itinerary = result["itinerary"]

        st.subheader(f"📄 Your {itinerary.total_days}-Day Plan for {itinerary.city} is ready")
        
        # Display General Tips
        with st.expander("💡 General Travel Tips", expanded=True):
            for tip in itinerary.travel_tips:
                st.write(f"- {tip}")
        
        # Display Day-wise Itinerary
        for day in itinerary.itinerary:
            with st.expander(f"🗓️ Day {day.day_number}: {day.theme}", expanded=True):
                cols = st.columns(len(day.activities))
                for idx, activity in enumerate(day.activities):
                    with cols[idx]:
                        st.markdown(f"**{activity.time}**")
                        st.markdown(f"📍 {activity.location}")
                        st.write(activity.description)
                
                st.markdown("---")
                st.markdown("**🍴 Food Recommendations:**")
                st.write(", ".join(day.food_recommendations))

        st.success(f"Budget Category: {itinerary.estimated_budget_category}")
        
        logger.info("RESPONSE GENERATED")
    else:
        st.warning("Please enter city and interests")


