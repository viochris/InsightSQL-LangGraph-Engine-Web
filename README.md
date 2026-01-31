# 📊 InsightSQL (LangGraph Reasoning Engine)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Reasoning-blueviolet?logo=graph&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-8E75B2?logo=google&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📌 Overview
**InsightSQL** is a next-generation AI Data Analyst powered by **Google's Gemini 2.5 Flash** and built upon the **LangGraph** architecture.

Unlike standard chatbots that guess answers, InsightSQL utilizes a **Graph-Based Reasoning Engine**. It treats data analysis as a cyclic workflow: validating schema, generating precise SQL, executing queries, and inspecting results. If an error occurs, the graph allows the agent to "loop back" and correct its own SQL syntax before presenting the final answer—providing a level of precision that linear chains cannot match.

## ✨ Key Features

### 🧠 LangGraph Reasoning Engine
Using `langgraph.prebuilt.create_react_agent`, the system navigates a structured cognitive cycle:
1.  **Plan:** Analyzes the user's intent and selects the appropriate SQL tool.
2.  **Execute:** Runs SQL queries against the SQLite database.
3.  **Verify:** Observes the output. If the query fails, the agent self-corrects and retries.
4.  **Synthesize:** Translates raw data into business insights in the requested language.

### 👁️ "Glass Box" Transparency
* **View Reasoning Trace:** Users can open an expander to watch the AI's internal monologue, tool invocations, and raw database outputs in real-time. Nothing is hidden "under the hood."

### 🌐 Multilingual Intelligence
* **Dual Language Support:** Seamlessly switch between **English** and **Indonesian** via the sidebar.
* **Strict Output Logic:** The system prompt enforces a critical logic layer. Even if you ask in Indonesian, if the setting is "English", the Agent translates the final business insight into English automatically.

### 🛡️ Robust State Management
* **Persistent Memory:** The AI remembers conversation context across Streamlit re-runs (`st.session_state`).
* **Dual Reset Modes:**
    * `🧹 Clear Screen Only`: Cleans the UI for presentation but **keeps the AI's memory** intact.
    * `🔄 Full System Reset`: Performs a "Hard Reset"—wiping memory, killing the agent executor, and resetting API connections.

## 🛠️ Tech Stack
* **LLM:** Google Gemini 2.5 Flash (via `ChatGoogleGenerativeAI`).
* **Framework:** Streamlit (Frontend).
* **Orchestration:** LangGraph (Cyclic ReAct Agent).
* **Database Tools:** SQLDatabaseToolkit (LangChain Community).
* **Database:** SQLite (via SQLAlchemy).

## ⚠️ Limitations & Data Privacy

### 1. Database Support
* Currently hardcoded for **SQLite (`.db`)** files.
* **Privacy:** The Agent does *not* upload your entire database to Google. Only the **Table Schema** and the specific **Rows** returned by queries are sent to the LLM for analysis.

### 2. Read-Only Safety
* The Agent is strictly instructed via System Prompts to avoid DML statements (`INSERT`, `UPDATE`, `DELETE`) to ensure data integrity.

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/viochris/InsightSQL-LangGraph-Engine.git
    cd InsightSQL-LangGraph-Engine
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Your Database**
    The system uses **SQLAlchemy**, making it compatible with SQLite, MySQL, PostgreSQL, and more.

    * **Option A: SQLite (Default)**
        * Place your `.db` file (e.g., `dresses.db`) in the project root folder.
        * If using a custom filename, update `app.py` (Line ~253):
            ```python
            db = SQLDatabase.from_uri("sqlite:///my_filename.db")
            ```

    * **Option B: External Databases (MySQL / PostgreSQL)**
        * Open `app.py` and replace the connection URI with your server credentials:
            ```python
            # For MySQL
            db = SQLDatabase.from_uri("mysql+pymysql://username:password@host:port/database_name")

            # For PostgreSQL
            db = SQLDatabase.from_uri("postgresql+psycopg2://username:password@host:port/database_name")
            ```
        * *Note: Ensure you have installed the necessary drivers (e.g., `pip install pymysql` or `psycopg2`) in your environment.*

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## 🚀 Usage Guide

1.  **Configuration (Sidebar):**
    * Enter your **Google Gemini API Key** (Required).
    * Select your **Language Preference** (English/Indonesian).
2.  **Connect:**
    * Click **"🚀 Connect to Database"**.
    * This initializes the `SQLDatabaseToolkit` and builds the LangGraph Agent.
3.  **Query:**
    * Type your question naturally (e.g., *"Show me the top 3 most expensive dresses"* or *"Berapa rata-rata rating untuk style casual?"*).
    * **Pro Tip:** You can switch languages in the sidebar mid-conversation, and the Agent will adapt immediately without needing a reset.
4.  **Manage:**
    * Use **"View Reasoning Trace"** to verify the SQL query used.
    * Use **"🔄 Full System Reset"** if you change API keys or want to clear the context completely.

## 📷 Gallery

### 1. Landing Interface
![Home UI](assets/home_ui.png)  
*The clean, modern landing page offering quick configuration. Users input their API key, select a language, and connect to the database securely.*

### 2. Real-Time Execution (Thinking Process)
![Thinking Process](assets/thinking_process.png)    
*Visual feedback using a spinner ("Executing reasoning workflow...") assures the user that the Graph Engine is actively planning and querying in the background.*

### 3. Transparent Reasoning (The "Glass Box")
![Reasoning Trace](assets/reasoning_thought_process.png)  
*Inside the "View Reasoning Trace" expander. Here, you can see the Agent's internal "Thought" (planning), the "Action" (invoking the SQL tool), and the "Tool Observation" (raw data returned from SQLite).*

### 4. Final Business Insight
![Result](assets/result.png)  
*The final output. The Agent synthesizes the raw SQL results into a clear, natural language answer formatted strictly according to the user's language preference.*

---
**Author:** [Silvio Christian, Joe](https://www.linkedin.com/in/silvio-christian-joe)
*"Transparent Reasoning. Data-Driven Answers."*
