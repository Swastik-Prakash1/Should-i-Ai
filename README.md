# 🧠 Should I? – AI-Powered Chrome Extension

<p align="center">
  <b>Make smarter buying decisions using AI-driven trust analysis.</b>
</p>

<p align="center">
  🟢 Safe &nbsp;&nbsp;|&nbsp;&nbsp; 🟡 Caution &nbsp;&nbsp;|&nbsp;&nbsp; 🔴 Risk
</p>

---

## 📌 Overview
**Should I?** is an AI-powered Chrome extension that helps users decide whether they should buy a product online.  
It analyzes **reviews, ratings, and trust signals** using **Natural Language Processing (NLP)** and displays a clear, color-coded trust indicator directly on the product page.

The extension aims to reduce the impact of **fake reviews**, **misleading listings**, and **unreliable sellers**.

---

## 🎯 Trust Indicators
The extension uses intuitive visual signals for instant understanding:

- 🟢 **Green – Safe to Buy**  
  Product shows consistent reviews and strong trust signals.

- 🟡 **Yellow – Proceed with Caution**  
  Mixed or suspicious patterns detected.

- 🔴 **Red – High Risk**  
  Strong indicators of unreliable or manipulated reviews.

---

## ✨ Key Features
- 🤖 AI-based review analysis using NLP
- 🔍 Detection of suspicious or low-trust review patterns
- 🎨 Clear color-coded trust signals (🟢 🟡 🔴)
- 🧩 Seamless Chrome extension integration
- ⚙️ Lightweight backend for ML inference
- 🔁 Designed for easy expansion to other platforms

---

## 💡 Motivation
Online marketplaces often suffer from:
- Fake or manipulated reviews  
- Inconsistent seller behavior  
- Overly positive or misleading ratings  

Manual verification is unreliable and time-consuming.  
**Should I?** provides an automated trust signal to help users make informed decisions **before** purchasing.

---

## 🏗️ System Architecture

### 🧩 Frontend – Chrome Extension
- Extracts product metadata and reviews
- Sends data to the backend
- Displays trust indicator using color-coded symbols

### 🔌 Backend – API Server
- Receives product and review data
- Processes text using NLP models
- Computes an overall trust score

### 🧠 Machine Learning Layer
- Transformer-based NLP models
- Detects unnatural or manipulative review patterns
- Outputs trust classification (🟢 / 🟡 / 🔴)

---

## 🛠️ Tech Stack
- **Frontend:** JavaScript, HTML, CSS (Chrome Extension APIs)
- **Backend:** Python, Flask
- **ML / NLP:** Transformer-based models
- **Version Control:** Git & GitHub
- **Deployment:** Local or Cloud-ready backend

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/should-i-ai-chrome-extension.git
cd should-i-ai-chrome-extension
