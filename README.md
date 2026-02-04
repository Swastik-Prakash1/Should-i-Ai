# Should I? – AI-Powered Chrome Extension

## Overview
**Should I?** is an AI-powered Chrome extension designed to help users make safer and more informed purchasing decisions. It analyzes product trust signals such as reviews, ratings, and seller behavior using Natural Language Processing (NLP) techniques and presents a clear trust assessment directly on the product page.

The project aims to reduce the impact of fake reviews, misleading product information, and unreliable sellers by providing an automated and explainable trust evaluation.

---

## Key Features
- AI-based analysis of product reviews using NLP
- Detection of suspicious or low-trust review patterns
- Trust scoring with clear visual indicators (Safe / Caution / Risk)
- Seamless integration as a Chrome extension
- Lightweight backend for model inference
- Designed to be extensible across multiple e-commerce platforms

---

## Motivation
Online marketplaces often suffer from:
- Fake or manipulated reviews  
- Inconsistent seller behavior  
- Misleading product descriptions  

Manual verification is time-consuming and unreliable.  
**Should I?** assists users by providing an automated trust signal before making a purchase decision.

---

## System Architecture
The system follows a modular and scalable architecture:

- **Chrome Extension (Frontend)**
  - Extracts product metadata and reviews from the webpage
  - Displays trust indicators and recommendations in real time

- **Backend API**
  - Receives extracted data from the extension
  - Performs review analysis and trust computation

- **Machine Learning Module**
  - Uses transformer-based NLP models for review analysis
  - Identifies potentially unreliable or manipulative review patterns

---

## Technologies Used
- **Frontend:** JavaScript, HTML, CSS (Chrome Extension APIs)
- **Backend:** Python, Flask
- **Machine Learning:** Transformer-based NLP models
- **Deployment:** Local / Cloud-ready backend
- **Version Control:** Git & GitHub

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/should-i-ai-chrome-extension.git
cd should-i-ai-chrome-extension
