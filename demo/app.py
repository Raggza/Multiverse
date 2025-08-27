import streamlit as st
import requests
import base64

# API endpoint
api_url = (
    "http://localhost:8000/api/v1/image_generation"  # Update with your API endpoint
)

st.title("Multiverse Image Generator")

dict = {
    "Human": ["Black skin", "White skin", "Yellow skin", "Blue skin"],
    "Goblin Horde": ["1 member", "10 members", "Very many members"],
    "Elf": [
        "High Elf",
        "Dark Elf",
        "Wood Elf",
        "Sea Elf",
        "Moon Elf",
        "Sun Elf",
        "Star Elf",
        "Lythari",
    ],
    "God": [
        "Zeus",
        "Hera",
        "Poseidon",
        "Demeter",
        "Apollo",
        "Artemis",
        "Ares",
        "Athena",
        "Hephaestus",
        "Aphrodite",
        "Hermes",
        "Hestia",
    ],
}

col1, col2 = st.columns(2)
with col1:
    race = st.selectbox(
        "Race",
        ("Goblin Horde", "Human", "Elf", "God"),
    )
    weapon = st.selectbox(
        "Weapon",
        ("Long Sword", "Long Bow", "Spear", "Dagger", "Shiled", "Axe"),
    )
with col2:
    sub_race = st.selectbox(
        "Sub Race",
        options=dict[race],
    )
    model_name = st.selectbox("Model", ("stable", "gemini"))

if st.button("Generate"):
    response = requests.post(
        api_url,
        json={
            "race": race,
            "sub_race": sub_race,
            "weapon": weapon,
            "model_name": model_name,
        },
    )
    data = response.json()  # lấy JSON từ API
    img_b64 = data["content"]
    image_bytes = base64.b64decode(img_b64)
    with st.expander("Prompt"):
        edited_prompt = st.text_area("Edit prompt:", value=data["prompt"], height=200)
    st.image(image_bytes, caption="Generated Image")
