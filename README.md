# 🎨 Studio AI - Text-to-Image Generator

Studio AI is a powerful Streamlit-based web app that lets users generate high-quality images using natural language prompts with the help of **Stable Diffusion XL**. It also includes GPT-powered prompt enhancement using **LangChain** for better creative control.

This project is ideal for creative professionals, artists, marketers, and developers looking to experiment with AI-generated art. It enables fine-grained control over image generation using various options like weighted prompts, style selectors, and negative prompt filtering. Users can also create animated variations in GIF format, making the app suitable for concept ideation and visual storytelling.

---

## 🚀 Live Demo

👉 [Click here to try the app](https://stable-diffusion-9kxsm49vanvnixpqq8gxce.streamlit.app)  
_(Replace the `#` with your actual Streamlit Cloud or Hugging Face Spaces URL)_

---

## ✨ Features

- 🧠 **Prompt Enhancement** using GPT-4 via LangChain
- 🎨 **AI Image Generation** using Stability AI’s Stable Diffusion XL
- 🔁 **GIF Variation Generator** for artistic looping
- 🛠️ **Prompt Options** including negative prompts, aspect ratio, and weights
- 📀 **Download Options** for both images and GIFs
- 🖼️ **Image Gallery** to view recent generations

---

## 💪 Tech Stack

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-4](https://openai.com/)
- [Stability AI (Stable Diffusion)](https://platform.stability.ai)

---

## 📁 Setup Instructions

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/Anirudh2857/Stable-Diffusion)
cd your-Stable-Diffusion
```

### 2. Install Dependencies
Make sure Python 3.8+ is installed.
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file or set the following in your system:
```bash
export OPENAI_API_KEY=your-openai-key
export STABILITY_API_KEY=your-stability-key
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📄 Example .env File
```
OPENAI_API_KEY=sk-...
STABILITY_API_KEY=sk-...
```

> Never commit your API keys to GitHub.

---

## 📈 Roadmap / Coming Soon
- Prompt template library
- Multi-image generation
- Social sharing
- Save prompt history to local storage or database

---

## ✉️ Feedback & Contributions
Pull requests and feedback are welcome! 
Feel free to open an issue or submit a PR to improve functionality or fix bugs.

---

## ✅ License
This project is licensed under the MIT License.

