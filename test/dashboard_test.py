import streamlit as st
import jwt
import time

METABASE_SITE_URL = "http://localhost:3000"
METABASE_SECRET_KEY = "3af3064f319e8c752844869ece8be3613e88087bf219de3e984bbf7b578871df"

payload = {
  "resource": {"dashboard": 3},
  "params": {
    "user_id": "1"
  },
  "exp": round(time.time()) + (60 * 10) # 10 minute expiration
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"

st.set_page_config(layout="wide")
st.components.v1.iframe(iframeUrl)