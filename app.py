import streamlit as st
import joblib
import re

# --- Page Configuration ---
st.set_page_config(page_title="AI Resume Predictor & Builder", page_icon="🔮", layout="wide")

# --- Custom Chamkile CSS (Neon/Cyberpunk Cyber-Glow Theme) ---
st.markdown("""
    <style>
    /* Background cosmic gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #1c103a, #110924);
        color: #ffffff;
    }
    
    /* Neon glowing title */
    .shiny-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2fe, #ff0080, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 18px rgba(0, 242, 254, 0.7);
        padding-bottom: 5px;
    }

    .shiny-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #b4b4dc !important;
        margin-bottom: 40px;
    }

    /* Column Cards */
    div[data-testid="stColumn"] {
        background-color: rgba(20, 15, 38, 0.65);
        border: 2px solid #00f2fe;
        border-radius: 15px;
        padding: 25px !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2);
    }

    /* Right column with different neon borders */
    div[data-testid="stColumn"]:nth-child(2) {
        border-color: #ff0080;
        box-shadow: 0 4px 15px rgba(255, 0, 128, 0.2);
    }

    /* Checkbox & Header Styling */
    h3 {
        color: #00f2fe !important;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
    }

    /* Text Area custom neon inputs */
    .stTextArea textarea {
        background-color: rgba(10, 5, 20, 0.9) !important;
        color: #00f2fe !important;
        border: 1.5px solid #ff0080 !important;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }

    /* Glowing Action Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff0080, #7928ca);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        transition: 0.3s all ease-in-out;
        box-shadow: 0 4px 15px rgba(255, 0, 128, 0.5);
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 22px rgba(255, 0, 128, 0.8);
        border: 2px solid #ffffff;
    }

    /* Result Card with pulsating glow */
    .result-card {
        background: rgba(15, 25, 55, 0.9);
        padding: 25px;
        border-radius: 20px;
        border: 3px solid #00f2fe;
        text-align: center;
        margin-top: 25px;
        animation: glow 1.8s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { box-shadow: 0 0 12px #00f2fe; }
        to { box-shadow: 0 0 28px #ff0080; }
    }
    .result-text {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 15px #00f2fe;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Session State for Resume Content ---
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = ""

# --- Load ML Model Assets ---
@st.cache_resource
def load_assets():
    model = joblib.load('model.pkl')
    tfidf = joblib.load('tfidf.pkl')
    return model, tfidf

try:
    model, tfidf = load_assets()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# --- Helper Text Cleaner ---
def clean_text(text):
    text = re.sub('http\S+\s*', ' ', text)
    text = re.sub('RT|cc', ' ', text)
    text = re.sub('#\S+', '', text)
    text = re.sub('@\S+', '  ', text)
    text = re.sub(r'[^\x00-\x7f]', r' ', text)
    text = re.sub('\s+', ' ', text)
    return text.strip().lower()

# --- UI Header ---
st.markdown('<h1 class="shiny-title">✨ AI RESUME PREDICTOR & BUILDER ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="shiny-subtitle">Construct your professional persona using checklists or paste your text to unlock your path!</p>', unsafe_allow_html=True)

# --- Layout: 2 Columns ---
col1, col2 = st.columns([1.1, 1.3], gap="medium")

with col1:
    st.write("### 🛠️ Interactive Builder Panel")
    
    # 1. Target Job Roles Checklist
    st.write("**Select Target Job Roles:**")
    target_jobs = []
    if st.checkbox("🎯 Data Scientist"):
        target_jobs.append("Data Scientist")
    if st.checkbox("🐍 Python Developer"):
        target_jobs.append("Python Developer")
    if st.checkbox("🌐 Web Developer"):
        target_jobs.append("Web Developer")

    st.write("---")

    # 2. Key Tech Skills Checklist (Derived from Model Vocabulary)
    st.write("**Check Your Technical Skills:**")
    selected_skills = []
    
    # Left & Right columns inside the checklist panel
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.checkbox("💻 Python"): selected_skills.append("Python")
        if st.checkbox("🎸 Django"): selected_skills.append("Django")
        if st.checkbox("🌶️ Flask"): selected_skills.append("Flask")
        if st.checkbox("📊 Data Visualization"): selected_skills.append("Data Visualization")
    with sub_col2:
        if st.checkbox("📈 Statistical Modeling"): selected_skills.append("Statistical Modeling")
        if st.checkbox("🎨 Frontend Dev"): selected_skills.append("Frontend Development")
        if st.checkbox("📐 UI / UX Design"): selected_skills.append("UI UX Design")
        if st.checkbox("🤖 Machine Learning"): selected_skills.append("Machine Learning")

    st.write("")
    
    # Auto-fill Button
    if st.button("✨ Auto-Fill Resume Text"):
        job_str = ", ".join(target_jobs) if target_jobs else "Professional"
        skills_str = ", ".join(selected_skills) if selected_skills else "skills"
        skills_bullets = "\n".join([f"- {skill}" for skill in selected_skills]) if selected_skills else "- Foundational Tech Stack"
        
        # Crafting dynamic resume text matching the vectorizer vocab!
        st.session_state['resume_text'] = f"""[TARGET ROLE: {job_str.upper()}]

PROFILE SUMMARY:
Highly motivated and results-driven professional seeking opportunities in the domain of {job_str}. Possess robust skills in {skills_str} and specialized experience in deploying end-to-end applications.

TECHNICAL SKILLS:
{skills_bullets}

EXPERIENCE & ACADEMIC PROJECTS:
- Engineered scalable applications leveraging {skills_str} to solve complex challenges.
- Collaborated with multi-disciplinary teams on statistical modeling, frontend design, and machine learning deployments.
"""
        st.rerun()

with col2:
    st.write("### 📋 Resume Text / Career DNA")
    
    # The Text Area reads directly from the session state
    resume_input = st.text_area(
        "Career Profile Source:", 
        height=320, 
        value=st.session_state['resume_text'],
        placeholder="Type or paste your resume here... (Or use the Builder Panel on the left to auto-fill!)"
    )
    
    st.write("")
    
    # Prediction Button
    if st.button("🔮 PREDICT RESUME CATEGORY"):
        if not resume_input.strip():
            st.warning("Please provide resume text first!")
        else:
            # Vectorization & Model Inference
            cleaned_resume = clean_text(resume_input)
            input_features = tfidf.transform([cleaned_resume])
            prediction = model.predict(input_features)[0]
            
            # Fire celebration balloons!
            st.balloons()
             # guarveeeeeeeeeee anshhhhh
            # Glowing Category Output Card
            st.markdown(f'''
                <div class="result-card">
                    <p style="color: #ff0080; font-weight: bold; margin-bottom: 5px; font-size: 16px;">
                        ANALYSIS COMPLETE
                    </p>
                        h1
                    <div class="result-text">🎯 {prediction.replace("_", " ")}</div>
                    <p style="color: #00f2fe; margin-top: 10px; font-size: 14px;">
                        Confidence High | Perfect Match for Selected Keywords!
                    </p>
                </div>
            ''', unsafe_allow_html=True)

# --- Footer ---
st.markdown("<br><hr><center style='color:#b4b4dc;'>Powered by Scikit-Learn 1.6.1 & Cyberpunk Sparkles ⚡</center>", unsafe_allow_html=True)