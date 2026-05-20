# 🏏 IPL Win Predictor (Machine Learning)

A web-based application that predicts the winner of an IPL match using Machine Learning.

🔗 Live App: https://ipl-win-predictor-ml.streamlit.app/

---

## Overview

This project uses historical IPL match data to predict the likely winner between two teams based on key match factors such as:

* Teams playing
* Toss winner
* Toss decision
* Venue

The model is deployed using **Streamlit** with an interactive and user-friendly interface.

---

## Tech Stack

* **Python**
* **Streamlit**
* **Scikit-learn**
* **Pandas & NumPy**
* **Machine Learning (Random Forest Classifier)**

---

## How It Works

1. Historical IPL data is used to train a machine learning model.
2. Categorical features are encoded using Label Encoding.
3. The model learns patterns between match conditions and outcomes.
4. User inputs are passed into the model to generate predictions.
5. The app displays:

   * Win probabilities
   * Predicted winner
   * Confidence level

---

## Features

*  Select any two IPL teams
*  Toss winner and decision input
*  Venue selection
*  Win probability visualization
*  Predicted winner display
*  Clean and modern UI with team logos

---

## Deployment

The app is deployed using **Streamlit Cloud**.

To run locally:

```bash
git clone [https://github.com/your-username/ipl-predictor.git]
cd ipl-predictor
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
ipl-predictor/
│
├── app.py
├── model.pkl
├── encoders.pkl
├── requirements.txt
└── images/
```

---

## Model Performance

* Model: Random Forest Classifier
* Accuracy: ~50%

> Note: Cricket match outcomes are inherently uncertain due to real-world variables like player form, pitch conditions, and match-day performance.

---

## Limitations

* Does not consider player-level data
* No real-time match conditions
* Based only on historical trends

---

## Acknowledgements

* IPL dataset (Kaggle)
* Streamlit for deployment

---

## Author

**Soumya Sengupta**

---

## If you like this project

Give it a ⭐ on GitHub and share your feedback!
