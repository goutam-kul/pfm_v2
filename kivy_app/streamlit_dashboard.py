import streamlit as st
import os
import jwt
import time
from dotenv import load_dotenv

load_dotenv(override=True)

def get_metabase_embed_url(user_id, dashboard_id=4):
    METABASE_SITE_URL = "http://localhost:3000"
    METABASE_SECRET_KEY = os.getenv("METABASE_SECRET_KEY")

    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": {"id": str(user_id)},
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
    return iframeUrl

def main():
    st.set_page_config(page_title="Finance Manager", layout="wide")

    # Extract user_id from query parameters
    query_params = st.query_params
    user_id = query_params.get("user_id", [None])[0] if "user_id" in query_params else None

    if not user_id:
        st.error("User ID not provided in the URL parameter")
        return

    try:
        embed_url = get_metabase_embed_url(user_id=user_id)
        st.title("User Dashboard")
        st.components.v1.iframe(embed_url, height=1000)
    except Exception as e:
        st.error(f"Failed to load dashboard: {e}")

if __name__ == "__main__":
    main()
