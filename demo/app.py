import streamlit as st
import requests
import base64

from source.utils.log_utils import get_logger

logger = get_logger(__file__)

# API endpoint
api_url = (
    "http://localhost:8000/api/v1/image_generation"  # Update with your API endpoint
)

st.title("Multiverse Image Generator")

race = st.selectbox(
    "Race",
    ["Angel"],
)

if st.button("Generate"):
    with st.spinner("Generating..."):
        response = requests.post(
            api_url,
            json={
                "race": race,
                "sub_race": "",
                "weapon": "",
            },
        )
        data = response.json()  # lấy JSON từ API
        img_b64 = data["content"]
        logger.info(data["race"], data["sub_race"], data["weapon"], data["model_name"])
        image_bytes = base64.b64decode(img_b64)
        st.image(image_bytes, caption="Generated Image")
