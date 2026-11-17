import datetime
import html
import requests
import streamlit as st

# 1. Configure the web page
st.set_page_config(page_title="Ingolstadt Events Finder", page_icon="📅")
st.title("📅 Ingolstadt Events Finder")
st.write("Select a date below to see what's happening in Ingolstadt.")


# 2. Fetch API data (with caching so it doesn't re-download on every click!)
@st.cache_data(ttl=3600)  # Cache data for 1 hour (3600 seconds)
def fetch_ingolstadt_events():
    url = "https://ingolstadt.live/api/v1/getAllEvents"
    headers = {
        "Accept": "application/json",
        "User-Agent": "IngolstadtWebApp/1.0",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json().get("data", [])


# 3. Interactive Date Picker Widget (Replaces terminal input())
selected_date = st.date_input("Choose a date", datetime.date.today())
target_date = selected_date.strftime("%Y-%m-%d")  # Formats as "2026-11-26"

# 4. Load and filter events
try:
    with st.spinner("Loading events..."):
        events = fetch_ingolstadt_events()

    matching_events = [
        event
        for event in events
        if str(event.get("startDate", event.get("date", ""))).startswith(
            target_date
        )
    ]

    st.divider()

    # 5. Display results on the webpage
    if matching_events:
        st.success(f"Found {len(matching_events)} event(s) for {target_date}:")

        for event in matching_events:
            name = html.unescape(event.get("name", "No Title"))
            subtitle = html.unescape(event.get("subtitle") or "")
            description = html.unescape(
                event.get("description", "No description available.")
            )
            event_url = event.get("eventURL", "")

            # Create a clean visual container for each event
            with st.container(border=True):
                st.subheader(name)
                if subtitle:
                    st.caption(subtitle)
                st.write(description)
                if event_url:
                    st.link_button("View Event Details", event_url)
    else:
        st.info(f"No events scheduled for {target_date}. Try another date!")

except Exception as err:
    st.error(f"Could not connect to the Ingolstadt API: {err}")