import streamlit as st
import openai
import requests
import random
from datetime import datetime
from PIL import Image
import io
import tempfile
import os

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# === 🔑 API KEYS from environment ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

if not OPENAI_API_KEY or not STABILITY_API_KEY:
    st.error("API keys are not set. Please set OPENAI_API_KEY and STABILITY_API_KEY in your environment.")
    st.stop()

# === 🔧 Setup OpenAI Client ===
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# === 🔗 LangChain Prompt Enhancer ===
template = PromptTemplate(
    input_variables=["user_input", "style"],
    template="Enhance the following prompt for an AI image generator. Style: {style}. Prompt: {user_input}"
)
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4")
prompt_chain = LLMChain(llm=llm, prompt=template)

def enhance_prompt(prompt, style):
    return prompt_chain.run(user_input=prompt, style=style)

def generate_image_sd(prompt, steps, seed, aspect_ratio, negative_prompt=None):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*"
    }
    data = {
        "prompt": (None, prompt),
        "model": (None, "stable-diffusion-xl-1024-v1-0"),
        "output_format": (None, "png"),
        "aspect_ratio": (None, aspect_ratio),
        "seed": (None, str(seed)),
        "steps": (None, str(steps))
    }
    if negative_prompt:
        data["negative_prompt"] = (None, negative_prompt)
    response = requests.post(url, headers=headers, files=data)
    if response.status_code != 200:
        raise Exception(f"Image generation failed: {response.status_code} - {response.text}")
    return response.content

def upscale_image(image_bytes):
    return image_bytes

def generate_gif(images, duration=300):
    import imageio
    gif_path = os.path.join(tempfile.gettempdir(), "variation_loop.gif")
    imageio.mimsave(gif_path, images, duration=duration/1000)
    return gif_path

# === MAIN UI ===
st.set_page_config(page_title="Studio AI - Text to Image", layout="centered")
st.title("🎨 Studio AI - Text to Image Generator")

backend = "Stable Diffusion XL"
user_prompt = st.text_area("Enter your idea:", placeholder="e.g. a mystical forest with glowing mushrooms")
use_weights = st.checkbox("Use weighted prompt syntax (e.g. 'sunset:1.5')")
use_gpt = st.checkbox("Enhance prompt with GPT (via LangChain)", value=True)
style = st.selectbox("Choose a style:", ["None", "anime style", "photorealistic", "cyberpunk", "fantasy art", "pixel art"])
user_negative_prompt = st.text_input("What should NOT be in the image?", placeholder="e.g. blurry, text, watermark")
steps = st.slider("Steps", 10, 50, 30)
seed_option = st.radio("Seed", ["Random", "Fixed"], horizontal=True)
fixed_seed = st.number_input("Set seed (only used if 'Fixed' selected):", value=42)
aspect_ratio = st.selectbox("Aspect Ratio", ["1:1", "16:9", "9:16", "4:3", "3:2"])

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Generate Image"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        seed = random.randint(0, 999999999) if seed_option == "Random" else fixed_seed
        final_prompt = user_prompt + (f" in {style}" if style != "None" else "")
        if use_weights:
            final_prompt = final_prompt
        if use_gpt:
            with st.spinner("Enhancing prompt with LangChain..."):
                final_prompt = enhance_prompt(final_prompt, style)
            st.success("Prompt enhanced via LangChain!")
        st.markdown(f"**Final Prompt:** `{final_prompt}`")

        with st.spinner("Generating image..."):
            image_data = generate_image_sd(final_prompt, steps, seed, aspect_ratio, user_negative_prompt)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.png"
        st.image(image_data, caption=f"🖼️ Generated Image ({aspect_ratio})", use_column_width=True)
        st.download_button("📥 Download Image", image_data, file_name=filename, mime="image/png")

        if st.button("🔼 Upscale Image"):
            upscaled = upscale_image(image_data)
            st.image(upscaled, caption="🔍 Upscaled Image")

        st.session_state.history.append({
            "prompt": final_prompt,
            "image": image_data,
            "timestamp": timestamp,
            "seed": seed
        })

        if st.button("🌀 Create GIF Variation Loop"):
            variations = [Image.open(io.BytesIO(generate_image_sd(final_prompt, steps, random.randint(0, 999999), aspect_ratio, user_negative_prompt))) for _ in range(5)]
            gif_path = generate_gif(variations)
            st.image(gif_path, caption="GIF Variation Loop")
            with open(gif_path, "rb") as f:
                st.download_button("📥 Download GIF", f, file_name="variation_loop.gif", mime="image/gif")

st.subheader("🖼️ Gallery")
if st.session_state.history:
    for item in reversed(st.session_state.history[-5:]):
        st.image(item["image"], caption=f"Prompt: {item['prompt']}\nSeed: {item['seed']} ({item['timestamp']})", use_column_width=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button("Download", item["image"], file_name=f"{item['timestamp']}.png", mime="image/png")
        with col2:
            if st.button("Regenerate", key=item['timestamp']):
                st.session_state.user_prompt = item["prompt"]

st.subheader("📤 Share Prompt")
shared_prompt = st.selectbox("Select a previous prompt to share:", [h["prompt"] for h in st.session_state.history] if st.session_state.history else [])
if shared_prompt:
    st.code(shared_prompt, language="text")
    st.text("You can copy and paste this prompt to share or reuse.")
