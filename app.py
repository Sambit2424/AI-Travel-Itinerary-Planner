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


st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("🛩️ AI Travel Itinerary Planner 🌍")



with st.form("planner_form"):
    city = st.text_input("📍 City")
    days = st.slider("🗓️ Number of days", 1, 10, 3)
    interests = st.text_input("🎯 Interests (comma-separated)")
    style = st.selectbox("💸 Travel Style", ["Budget", "Mid-range", "Luxury"])
    pace = st.selectbox("🏃‍♂️ Pace", ["Relaxed", "Balanced", "Packed"])
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