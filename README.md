# AI-Powered Commentary for Lower-Tier Cricket Leagues

## Overview
This project leverages AI to provide professional-level commentary for lower-tier cricket leagues. By addressing the lack of affordable commentary solutions, this project aims to enhance viewer engagement, boost sponsorship opportunities, and improve the visibility of smaller leagues.

---

## Problem Statement
Lower-tier cricket leagues often lack the funds for professional commentary, which:
- Limits viewer engagement and fan interaction.
- Reduces sponsorship opportunities and revenue generation.
- Hinders league growth and visibility.

---

## Solution
Our AI-powered commentary system offers:
- **Cost-effective commentary** for leagues with limited budgets.
- **Multilingual capabilities** to reach broader demographics.
- **Consistent quality** to enhance broadcast standards.

---

## Industry Context
- Cricket has 3.5 billion global fans, but smaller leagues struggle with professional broadcasting.
- Emerging cricket markets (e.g., USA, Nepal, UAE) face budget and infrastructure challenges.
- Traditional commentary is expensive, creating barriers for smaller leagues.

---

## Key Benefits
1. **Broadened Audience Reach**: Professional commentary attracts global fans, increasing streaming and broadcasting revenue.
2. **Enhanced Fan Engagement**: AI-powered commentary enriches the viewing experience, boosting viewership and ticket sales.
3. **Cost Savings**: AI replaces expensive human commentators, reducing operational costs.

---

## Features
- **Real-Time Commentary**: AI generates live commentary during matches.
- **Scenario-Based Commentary**: Tailored commentary for specific match situations.
- **Multilingual Support**: Commentary in multiple languages to cater to diverse audiences.
- **Highlight Generation**: Automated creation of match highlights.

---

## Technical Overview

### Technologies Used
1. **Llama LLM**:
   - Used to generate text commentary in a conversational style.
   - Supports multilingual output and customizable commentator styles.
2. **Cartesia LLM**:
   - Converts the generated text commentary into speech (text-to-speech functionality).
   - Ensures natural and engaging audio commentary.
3. **YOLO (You Only Look Once)**:
   - Real-time object detection system used to monitor the game and detect events.
4. **Python**:
   - Core programming language for the project.
   - Modules used:
     - [`http.server`]: For implementing the API.
     - [`pandas`]: For data ingestion and preprocessing.
     - [`re`]: For text extraction and formatting.

---

### How It Works
1. **Data Ingestion**:
   - Historical cricket commentary data is loaded from `.csv` files such as `IPL_Match_Highlights_Commentary.csv` and `IPL_SCHEDULE_2008_2020.csv`.
   - This data is preprocessed and used as examples to guide the Llama LLM in generating commentary.

2. **Text Commentary Generation**:
   - The **Llama LLM** generates text commentary in real-time.
   - It is provided with:
     - Historical commentary examples.
     - Match-specific details (e.g., teams, venue, toss decision, weather).
     - The current event (e.g., a six, a wicket) detected during the game.
   - The output is a conversational-style commentary between two commentators.

3. **Real-Time Event Detection**:
   - A **YOLO-based image processing system** monitors the cricket game in real-time.
   - When an event occurs (e.g., a boundary, a wicket), YOLO triggers a **POST request** to the API implemented in `main.py`.

4. **API Workflow**:
   - The API, implemented using Python's `http.server` module, receives the event details via a POST request.
   - The event is passed to the Llama LLM along with match context and historical examples.
   - The Llama LLM generates text commentary for the event, which is then returned as a response to the API call.

5. **Text-to-Speech Conversion**:
   - The generated text commentary is sent to the **Cartesia LLM**, which converts it into speech.
   - This allows for natural and engaging audio commentary playback.

---

## How to Run the Project

### Prerequisites
1. Install Python 3.12 or higher.
2. Install the required dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file with your API keys and configurations:
   ```
   LLAMA_API_KEY=your_llama_api_key
   CARTESIA_API_KEY=your_cartesia_api_key
   ```

### Steps to Run
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. Start the YOLO-based event detection system to send POST requests to the API.

4. Monitor the API responses for real-time commentary generation.

---

## Contributors
- Tamir Polyakov
- Branavan Jegatheeswaran
- Krish Rangwani
- Amarveer Gill
- Rupesh Rangwani