import streamlit as st
import joblib
import base64

# -------------------- LOAD MODEL & ENCODERS --------------------
model = joblib.load("model.pkl")
encoders = joblib.load("encoders.pkl")

# -------------------- BASE64 IMAGE HELPER --------------------
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# -------------------- CURRENT IPL TEAMS --------------------
current_teams = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Delhi Capitals",
    "Sunrisers Hyderabad",
    "Rajasthan Royals",
    "Punjab Kings",
    "Lucknow Super Giants",
    "Gujarat Titans"
]

teams = ["Select Team"] + current_teams

# -------------------- TEAM NAME FIX --------------------
team_name_map = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Deccan Chargers": "Sunrisers Hyderabad"
}

# -------------------- TEAM LOGOS --------------------
team_logos = {
    "Mumbai Indians": "images/mi.png",
    "Chennai Super Kings": "images/csk.png",
    "Royal Challengers Bangalore": "images/rcb.png",
    "Kolkata Knight Riders": "images/kkr.png",
    "Delhi Capitals": "images/dc.png",
    "Sunrisers Hyderabad": "images/srh.png",
    "Rajasthan Royals": "images/rr.png",
    "Punjab Kings": "images/pbks.png",
    "Lucknow Super Giants": "images/lsg.png",
    "Gujarat Titans": "images/gt.png"
}

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="IPL Predictor", page_icon="🏏", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- IPL LOGO --------------------
img = get_image_base64("images/ipl.png")
st.markdown(f"""
<div style='text-align:center; margin-top:-5px;'>
    <img src='data:image/png;base64,{img}' width='120'/>
</div>
""", unsafe_allow_html=True)

# -------------------- GRADIENT HEADER --------------------
st.markdown("""
<div style="
    text-align:center;
    padding: 10px;
    margin-top: 15px;
    background: linear-gradient(90deg, #0e1117, #1f4e79);
    border-radius: 10px;
">
    <h1>🏏 IPL Match Winner Predictor</h1>
    <p style='color:lightgray;'>
        Predict IPL match outcomes using Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------- INPUT SECTION --------------------
st.markdown("### Enter Match Details")

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team 1", teams)

with col2:
    team2 = st.selectbox("Team 2", teams)

col3, col4 = st.columns(2)

with col3:
    if team1 != "Select Team" and team2 != "Select Team":
        toss_winner = st.selectbox("Toss Winner", [team1, team2])
    else:
        toss_winner = st.selectbox("Toss Winner", ["Select Team"])

with col4:
    toss_decision = st.selectbox("Toss Decision", ["Bat", "Field"])

venue = st.selectbox("Venue", list(encoders['venue'].classes_))

# -------------------- VS DISPLAY --------------------
if team1 != "Select Team" and team2 != "Select Team":

    colA, colB, colC = st.columns([1,1,1])

    with colA:
        img = get_image_base64(team_logos.get(team1, ""))
        st.markdown(f"<div style='text-align:center'><img src='data:image/png;base64,{img}' width='110'/><p>{team1}</p></div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<h2 style='text-align:center; margin-top:40px;'>VS</h2>", unsafe_allow_html=True)

    with colC:
        img = get_image_base64(team_logos.get(team2, ""))
        st.markdown(f"<div style='text-align:center'><img src='data:image/png;base64,{img}' width='110'/><p>{team2}</p></div>", unsafe_allow_html=True)

# -------------------- BUTTON --------------------
st.markdown("---")
predict = st.button("Predict Winner", use_container_width=True)

# -------------------- PREDICTION --------------------
if predict:

    with st.spinner("Analyzing match..."):

        if team1 == "Select Team" or team2 == "Select Team":
            st.warning("⚠️ Please select both teams")

        elif team1 == team2:
            st.error("⚠️ Please select two different teams")

        else:
            input_data = [
                encoders['team1'].transform([team1])[0],
                encoders['team2'].transform([team2])[0],
                encoders['toss_winner'].transform([toss_winner])[0],
                encoders['toss_decision'].transform([toss_decision.lower()])[0],
                encoders['venue'].transform([venue])[0]
            ]

            # -------------------- PROBABILITY --------------------
            proba = model.predict_proba([input_data])[0]
            all_teams = encoders['winner'].classes_
            team_probs = dict(zip(all_teams, proba))

            team1_prob = team_probs.get(team1, 0)
            team2_prob = team_probs.get(team2, 0)

            total = team1_prob + team2_prob
            if total != 0:
                team1_prob /= total
                team2_prob /= total

            # -------------------- WINNER --------------------
            winner = team1 if team1_prob > team2_prob else team2

            # -------------------- DISPLAY --------------------
            st.markdown("### 📊 Win Probability")

            st.progress(float(team1_prob))
            st.write(f"**{team1}**: {team1_prob*100:.2f}%")

            st.progress(float(team2_prob))
            st.write(f"**{team2}**: {team2_prob*100:.2f}%")

            st.markdown("<br>", unsafe_allow_html=True)

            # -------------------- RESULT CARD --------------------
            img = get_image_base64(team_logos.get(winner, ""))

            st.markdown(f"""
            <div style="
                text-align:center;
                padding:20px;
                border-radius:15px;
                background: linear-gradient(135deg, #1f4e79, #0e1117);
                box-shadow: 0 0 15px rgba(0,0,0,0.5);
            ">
                <img src="data:image/png;base64,{img}" width="120"/>
                <h2 style="color:#00ffcc;">{winner}</h2>
                <p style="color:lightgray;">Predicted Winner</p>
            </div>
            """, unsafe_allow_html=True)

            confidence = max(team1_prob, team2_prob)
            st.progress(float(confidence))
            st.caption(f"Confidence: {confidence*100:.2f}%")

            st.balloons()

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Built by Soumya Sengupta. Email: soumya.ckd2005@gmail.com</p>",
    unsafe_allow_html=True
)