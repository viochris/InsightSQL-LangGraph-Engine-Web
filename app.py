import streamlit as st

# --- LangChain & LangGraph Ecosystem ---
# Schemas for structuring conversation history (Human vs AI messages)
from langchain_core.messages import HumanMessage, AIMessage

# Utilities for establishing database connections and managing schemas
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

# Interface for the Google Gemini chat model
from langchain_google_genai import ChatGoogleGenerativeAI

# LangGraph factory function to construct the ReAct Agent architecture
from langgraph.prebuilt import create_react_agent

# --- Local Application Modules ---
# Custom helper functions for session state persistence and UI logic
from function import (
    init_state, 
    change_on_api_key, 
    reset_state, 
    reset_chat_display, 
    change_on_lan
)

# Initialize session state variables (messages, llm, toolkit) immediately 
# to prevent errors during app re-runs
init_state()

# Configure the Streamlit page settings
# This sets the browser tab title, favicon, and layout mode
st.set_page_config(
    page_title="InsightSQL | LangGraph Engine",
    page_icon="🕸️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Display the main application header
st.title("🕸️ InsightSQL: LangGraph Reasoning")

# Render the introduction text using Markdown and HTML
# unsafe_allow_html=True is used here to center the subtitle text
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 30px;">
        <b>Transparent Reasoning. Data-Driven Answers.</b>
    </div>
    
    Welcome to **InsightSQL**. Built on the modern **LangGraph Architecture**, this agent is designed for precision and transparency.
    
    Instead of just guessing, InsightSQL follows a structured **reasoning process**: validating your data schema, generating precise SQL queries, and strictly adhering to logical steps.
    
    Open the **"👁️ View Reasoning Trace"** tab below to watch the AI analyze, query, and verify results in real-time before answering you.
    
    ---
    """, 
    unsafe_allow_html=True
)

with st.sidebar:
    # Sidebar header with an emoji for better visual hierarchy
    st.header("⚙️ Page Configuration")

    st.divider()

    # Input widget for the API Key
    # 'type="password"' masks the input characters for security
    # 'on_change' triggers the cleanup function immediately if the key is modified
    st.text_input(
        "🔑 Google API Key", # Improved label with emoji
        type="password",
        key="google_api_key",
        on_change = change_on_api_key,
        help="Paste your Google Gemini API Key here. This is required to power the AI agent." # Filled help text
    )

    # Language Selection Widget
    # Allows the user to dictate the language of the final natural language response.
    # This selection is dynamically injected into the system prompt via the '{chosen_language}' variable.
    chosen_language = st.selectbox(
        "🌐 Language Preference", # Improved Label: Adds an emoji for visual cue and sounds professional.
        ["English", "Indonesian"],
        index=0,
        on_change=change_on_lan, # Callback: Forces the Agent Executor to reset/rebuild when changed.
        help="Select the language for the AI's analysis. Changing this will re-initialize the agent to apply the new persona." # Informative Help Text
    )

    st.divider()

    # Button to clear the chat history (Soft Reset)
    # This invokes 'reset_state' to clear messages without breaking the database connection
    st.button(
        "🧹 Clear Screen Only", # Improved label with emoji
        on_click=reset_chat_display,
        use_container_width=True,
        help="Clears the chat text to declutter the screen, but the AI KEEPS its memory of the conversation." # Filled help text
    )

    st.button(
        "🔄 Full System Reset", # Improved label with emoji
        on_click=reset_state,
        type="primary",
        use_container_width=True,
        help="Wipes EVERYTHING: Chat history, AI Memory, and Connections. Starts 100% fresh." # Filled help text
    )

    # Main action button to initialize the Agent
    # Changing "Load Information" to "Connect to Database" is more accurate for an SQL Agent
    connect = st.button(
        "🚀 Connect to Database", # Improved label: Clearer action
        use_container_width=True,
        help="Initializes the connection to the 'dresses.db' file and builds the AI agent." # Filled help text
    )

    st.divider()

# --- USER GUIDE & DOCUMENTATION ---
    # These sections provide self-service support, reducing the need for external explanations.
    
    # Expandable "How To Use" Guide
    # Strict linear flow: API -> Language -> Connect -> Chat.
    with st.expander("📚 How To Use"):
        st.markdown("""
        **1. 🔑 API Configuration**  
        Enter your **Google Gemini API Key** in the sidebar first. This is required to power the AI engine.
        
        **2. 🌐 Select Language**  
        Choose your preferred response language (**English** or **Indonesian**). 
        
        **3. 🚀 Connect to Database**  
        Click the **'Connect'** button to initialize the LangGraph Engine and load the default dataset.
        *(⚠️ Want to switch to your own database? Please read the **FAQ** section below for technical instructions).*
        
        **4. 💬 Start Querying**  
        Once connected, type your questions naturally in the chat.
        
        ---
        **💡 Pro Tip:**  
        *Want to switch languages mid-conversation?*  
        **Just change it in the sidebar!**  
        The graph will automatically update its instructions and answer your next question in the new language. No need to reconnect.
        """)

    # Expandable "FAQ" Section
    # Anticipates common user concerns regarding security, capabilities, and performance.
    with st.expander("❓ FAQ (Frequently Asked Questions)"):
        st.markdown("""
        **Q: Can this agent modify my database?**  
        A: **No.** The agent operates under strict **Read-Only** rules. It is explicitly instructed via system prompts to avoid DML statements like `INSERT`, `UPDATE`, or `DELETE`.
        
        **Q: How do I change the database to my own?**  
        A: Since this is a specialized prototype, the database is currently linked via code. To use your own data:
        1. **Prepare your file:** Ensure you have a valid SQLite database file (e.g., `my_data.db`).
        2. **Upload:** Place the file in the **same root directory** as `app.py`.
        3. **Modify Code:** Open `app.py` and locate the connection setup (approx. **Line 245**).
        4. **Update URI:** Change the code from:  
            `db = SQLDatabase.from_uri("sqlite:///dresses.db")`  
            to:  
            `db = SQLDatabase.from_uri("sqlite:///YOUR_FILENAME.db")`

        **Q: Why does it take a few seconds to respond?**  
        A: Unlike basic chatbots, this is a **Graph-Based Reasoning Engine (LangGraph)**. It navigates a cyclic workflow: *Thinking* (Node 1), *Action* (Node 2), and *Observation* (Node 3). It may even "loop back" to correct its own errors before answering. This ensures accuracy over speed.
        
        **Q: Is my data sent to Google?**  
        A: The LLM receives the **Table Schema** (structure) and the specific **Rows** returned by queries to generate answers. Your entire database is **not** uploaded.
        
        **Q: What happens if I change the language mid-conversation?**  
        A: The system will automatically **update the Graph State** with the new language instruction. Your chat history will be preserved, but the next answer will strictly follow the new language rules.
        """)
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; font-size: 0.85rem; color: #888;">
            © 2026 <b>Silvio Christian, Joe</b><br>
            Powered by <b>Google Gemini</b> 🚀<br><br>
            <a href="https://www.linkedin.com/in/silvio-christian-joe/" target="_blank" style="text-decoration: none; margin-right: 10px;">🔗 LinkedIn</a>
            <a href="mailto:viochristian12@gmail.com" style="text-decoration: none;">📧 Email</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- LLM INITIALIZATION LOGIC ---
# Check if the API Key has been provided by the user in the sidebar.
if st.session_state.google_api_key:
    
    # --- SINGLETON PATTERN ---
    # Only initialize the LLM if it hasn't been created yet (is None).
    # This prevents unnecessary re-initialization on every app rerun, saving memory and API calls.
    if st.session_state.llm is None:
        try:
            # 1. CONFIGURE THE MODEL
            # We initialize the ChatGoogleGenerativeAI class.
            # 'model': We use "gemini-2.5-flash" for high speed and cost efficiency.
            # 'temperature': Set to 0.3. Lower temperature = less random, more deterministic.
            # This is critical for SQL generation where precision matters more than creativity.
            st.session_state.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash", 
                google_api_key=st.session_state.google_api_key,
                temperature=0.3 
            )
            
            # 2. SUCCESS NOTIFICATION
            # Notify the user that the AI engine is ready via a toast message (non-intrusive popup).
            st.toast("AI Engine initialized successfully!", icon="🧠")
            
        # --- ERROR HANDLING FOR LLM SETUP ---
        except Exception as e:
            # Normalize error message for easier keyword matching
            error_msg = str(e).lower()
            
            # Case A: Invalid API Key
            # This catches 400 Bad Request or 403 Forbidden errors immediately upon setup.
            if "api_key" in error_msg or "403" in error_msg or "key not found" in error_msg:
                 st.error("🔑 **Authentication Failed**: The provided Google API Key is invalid. Please check the sidebar.", icon="🚫")
            
            # Case B: Model Not Found (Common with new models like 2.5-flash)
            # This happens if the user's account doesn't have access to this specific model version yet.
            elif "not found" in error_msg or "404" in error_msg or "models/" in error_msg:
                 st.error("🤖 **Model Access Error**: Could not access 'gemini-2.5-flash'. Your API Key might not support this version yet.", icon="❌")
            
            # Case C: Network/Connection Issues
            # This happens if the server cannot reach Google's API endpoints.
            elif "transport" in error_msg or "connection" in error_msg or "socket" in error_msg:
                 st.error("🌐 **Connection Error**: Unable to reach Google servers. Please check your internet connection.", icon="🔌")

            # Case D: General/Unknown Errors
            else:
                 st.error(f"❌ **Initialization Error**: {error_msg}", icon="⚠️")

else:
    # --- MISSING KEY WARNING ---
    # Display a persistent warning if the user attempts to proceed without entering an API Key.
    st.warning("Please enter your Google API Key to proceed.", icon="⚠️")

# Check if the 'Connect' button was clicked and the LLM is already initialized
if connect and st.session_state.llm is not None:
    # Ensure we don't re-initialize the toolkit if it already exists
    if st.session_state.toolkit is None:
        try:
            # Establish a connection to the SQLite database
            # -------------------------------------------------------------------------
            # 💡 TO CONNECT TO EXTERNAL DATABASES:
            # Note: For MySQL/PostgreSQL, use the format: "dialect+driver://user:pass@host/dbname"
            # Replace the URI below with the standard SQLAlchemy connection string:
            #
            # - MySQL:      "mysql+pymysql://username:password@host:port/database_name"
            # - PostgreSQL: "postgresql+psycopg2://username:password@host:port/database_name"
            # -------------------------------------------------------------------------
            db = SQLDatabase.from_uri("sqlite:///dresses.db")

            # Initialize the SQL Toolkit
            # This provides the Agent with the necessary tools to inspect the schema and execute queries
            st.session_state.toolkit = SQLDatabaseToolkit(db=db, llm=st.session_state.llm)

            # Notify the user with a Success Icon
            st.toast("✅ Database Connected! System Ready.", icon="🎉")
            
        except Exception as e:
            # Catch and display any errors during connection with an Error Icon
            # Convert error to string for analysis
            error_str = str(e).lower()

            # Check for specific error types to provide better guidance
            if "argumenterror" in error_str:
                # This usually happens if the SQLAlchemy URI string is malformed
                st.error("❌ Invalid Database URI. Please check the connection string format.", icon="📝")
            
            elif "operationalerror" in error_str:
                # This often happens if the file doesn't exist or permissions are denied
                st.error("❌ Operational Error. Is 'dresses.db' in the correct folder?", icon="📂")
            
            else:
                # Catch and display any other unexpected errors
                error_msg = f"❌ Connection Failed: {str(e)}"
                st.error(error_msg, icon="🚨")
    else:
        # Inform the user if the system is already running
        st.toast("⚡ System is already active. Ready to query!", icon="🤖")

# Handle the case where the user clicks 'Connect' without providing an API Key first
elif connect and st.session_state.llm is None:
    st.toast("⚠️ API Key Missing! Please check the sidebar.", icon="🔑")

# Check if the Database Toolkit is missing (meaning the user hasn't connected yet)
if st.session_state.toolkit is None:
    st.warning("⚠️ Database not connected. Please click **'Connect to Database'** in the sidebar.", icon="🔌")

# --- AGENT INITIALIZATION LOGIC ---
# We check if the agent exists. If not, and if we have the LLM and Toolkit ready, we build it.
# This "Lazy Loading" pattern saves resources by only creating the agent when needed.
if "agent_executor" not in st.session_state \
    and st.session_state.llm is not None \
        and st.session_state.toolkit is not None:

        # --- ADVANCED CUSTOM AGENT ARCHITECTURE ---
        try:
            # 1. RETRIEVE DATABASE TOOLS
            # Extract the raw tool functions (Schema, Query, ListTables) directly from the toolkit.
            # These are the "Hands" of the agent, allowing it to interact with the SQLite database.
            tools = st.session_state.toolkit.get_tools()

            # 2. DEFINE SYSTEM INSTRUCTIONS & PERSONA
            # This is the "Brain" customization. We use a formatted string (f-string) to inject 
            # dynamic variables (like 'chosen_language') directly into the core instructions.
            # We enforce strict rules for SQL syntax and output formatting.
            prompt = f"""
            You are an expert Data Analyst and SQL Analyst. 
            Your goal is to answer user questions by querying a database.

            RULES:
            1. ALWAYS start by checking the list of tables ('sql_db_list_tables').
            2. Then, check the schema of the relevant table ('sql_db_schema').
            3. Construct a syntactically correct SQL query.
            4. Execute the query using 'sql_db_query'.
            5. If you get an error, check your query and try again.
            6. DO NOT execute DML statements (INSERT, UPDATE, DELETE).
            
            7. CRITICAL LANGUAGE OUTPUT RULE: When you have the answer, you MUST strictly use the format: "Final Answer: [Your answer in {chosen_language}]".
               - The User's chosen output language is: "{chosen_language}".
               - IGNORE the user's language for the final output; IT MUST BE IN {chosen_language}.
               - LOGIC CHECK:
                 * IF User asks in Indonesian AND "{chosen_language}" is English -> ANSWER IN ENGLISH.
                 * IF User asks in English AND "{chosen_language}" is Indonesian -> ANSWER IN INDONESIAN.
               - You MUST perform this translation step before giving the Final Answer.
               - DO NOT mimic the user's language. STICK TO "{chosen_language}".
               - If you do not start your final response with "Final Answer:", the system will crash. 
               - Format: "Final Answer: [Your answer strictly in {chosen_language}]".
               - Provide context and reasoning in your answer, not just numbers.
            
            8. SPECIAL RULE FOR CASUAL CHAT (NO TOOL USED):
               - Even if you do not use a tool (e.g., greetings like "Halo", "Hi"), you MUST STILL translate your response to "{chosen_language}".
               - Example: If User says "Halo" (Indo) and target is English -> Final Answer: "Hello! How can I help you with the database?"
               - NEVER reply in the user's language just to be polite. Stick to the target language.
            """

            # 3. INITIALIZE THE RUNTIME EXECUTOR (THE BODY)
            # We use 'create_react_agent' from LangGraph.
            # 'model': The LLM (Gemini).
            # 'tools': The SQL functions.
            # 'state_modifier': The System Prompt defined above (Note: In LangGraph, we use state_modifier, not prompt).
            st.session_state.agent_executor = create_react_agent(
                model=st.session_state.llm,
                tools=tools,
                prompt=prompt
            )

        # --- ERROR HANDLING FOR INITIALIZATION ---
        # If the agent creation fails, we categorize the error to provide specific feedback.
        except Exception as e:
            # Normalize error message for case-insensitive matching
            error_msg = str(e).lower()
            answer = "" # Placeholder for the final user-facing message

            # Case A: Handle Database Connection/Toolkit Issues
            # This happens if 'get_tools()' fails or the database is locked/inaccessible.
            if "toolkit" in error_msg or "argument" in error_msg or "get_tools" in error_msg:
                 answer = "🛠️ **Toolkit Configuration Error**\n\nThe system could not extract necessary tools from the database connection. Please verify the database file path and permissions."

            # Case B: Handle Model/LLM Configuration Issues
            # This happens if the 'model' object passed to create_react_agent is invalid.
            elif "model" in error_msg or "llm" in error_msg or "callable" in error_msg:
                 answer = "🤖 **AI Model Error**\n\nThe Language Model was not initialized correctly. Please check your API Key and Model selection in the sidebar."

            # Case C: Handle LangGraph/Version Issues
            # This happens if 'state_modifier' is not supported (e.g., using an old version of langgraph).
            elif "unexpected keyword argument" in error_msg or "state_modifier" in error_msg:
                 answer = "📦 **Library Version Error**\n\nYour 'langgraph' library version might be outdated. Please run `pip install -U langgraph`."

            # Case D: Handle API Quota/Auth (Just in case validation happens instantly)
            elif "429" in error_msg or "quota" in error_msg or "api_key" in error_msg:
                 answer = "🔑 **API Access Error**\n\nGoogle Gemini API access was denied. Check your API Key or Quota limits."

            # Case E: Handle General/Unknown Errors (Catch-all)
            else:
                answer = f"❌ **System Initialization Failed**\n\nAn unexpected error occurred while building the Agent Engine.\n\n**Technical Details:** `{error_msg}`"

            # Finally, display the structured error message
            st.error(answer, icon="⚠️")

# Render the chat history
# We iterate through the 'messages' list in the session state to persist the conversation
# across Streamlit re-runs (which happen every time the user interacts).
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- 1. CAPTURE USER INPUT ---
# The := operator assigns the input to 'prompt_text' and returns True if input exists.
# This serves as the main entry point for the interaction loop.
if prompt_text := st.chat_input("Ask a question about your data..."):
    
    # --- 2. PRE-FLIGHT CHECKS (GUARDRAILS) ---
    # Before processing, we ensure all critical components (LLM, Toolkit, Agent) are initialized.
    # This prevents the app from crashing if the user hasn't set up the connection yet.
    
    if st.session_state.llm is None:
        st.warning("⚠️ AI Engine is not active. Please enter your API Key in the sidebar.", icon="🚫")
        
    elif st.session_state.toolkit is None:
        st.warning("⚠️ Database Toolkit is missing. Please click 'Connect to Database'.", icon="🔌")
        
    elif not st.session_state.agent_executor:
        st.warning("⚠️ Agent is not initialized. Please reload the connection.", icon="🤖")

    else:
        # --- 3. PROCESS VALID INPUT ---
        
        # A. Update Session State (User Side)
        # Store the user's query in the chat history to maintain context.
        st.session_state.messages.append({"role": "human", "content": prompt_text})
        
        # B. Render User Message
        # Immediately display the user's input in the UI for a responsive feel.
        st.chat_message("human").write(prompt_text)

        # C. Generate AI Response
        with st.chat_message("ai"):
            # Use a spinner to indicate that the backend is processing logic/SQL.
            with st.spinner("Executing reasoning workflow..."):
                try:
                    # --- D. PREPARE MESSAGE HISTORY ---
                    # LangChain requires objects (HumanMessage, AIMessage), but Streamlit uses dicts.
                    # We iterate through session_state to convert the history into the correct format.
                    messages = []
                    for msg in st.session_state.messages:
                        if msg["role"] == "human":
                            messages.append(HumanMessage(content=msg["content"]))
                        elif msg["role"] == "ai":
                            messages.append(AIMessage(content=msg["content"]))

                    # --- E. MARK THE START POINT ---
                    # We calculate the current length of the history. 
                    # Anything added *after* this point is the "new" reasoning process for the current query.
                    start_len = len(messages)

                    # --- F. INVOKE THE AGENT ---
                    # We pass the full history to the Agent Executor (LangGraph).
                    # It returns a dictionary containing the updated list of 'messages'.
                    response = st.session_state.agent_executor.invoke(
                        {"messages": messages}
                    )

                    # --- G. VISUALIZE REASONING (THE "GLASS BOX") ---
                    # We slice the list to get only the NEW messages generated in this run.
                    recent_resp = response["messages"][start_len:]
                    
                    # Create an expandable section to show the "Thought Process" without cluttering the main chat.
                    with st.expander("👁️ View Reasoning Trace"):
                        for resp in recent_resp:
                            
                            # CASE A: TOOL CALL DETECTION (ACTION)
                            # Modern LLMs (like Gemini/GPT) often have empty 'content' when calling a tool.
                            # We must check the 'tool_calls' attribute to see what action the AI is taking.
                            if hasattr(resp, 'tool_calls') and len(resp.tool_calls) > 0:
                                for tool in resp.tool_calls:
                                    st.markdown(f"🤖 **AI Action:** Invoking tool `{tool['name']}`")
                                    st.code(f"Arguments: {tool['args']}")
                            
                            # CASE B: TOOL OUTPUT DETECTION (OBSERVATION)
                            # This catches the raw data returned from the SQL Database or Python tool.
                            # We truncate it to 1000 chars to avoid flooding the UI if the data is huge.
                            elif hasattr(resp, 'type') and resp.type == "tool":
                                st.markdown(f"🛠️ **Tool Observation:**")
                                st.code(str(resp.content)[:1000])
                            
                            # CASE C: THOUGHTS & FINAL ANSWER
                            # If the message has text content, it's either an internal thought or the final reply.
                            elif hasattr(resp, 'content') and resp.content:
                                
                                # Check if this is the ABSOLUTE LAST message in the sequence.
                                # If yes, it is the "Final Answer".
                                if resp == recent_resp[-1]:
                                    st.divider() # Visual separator
                                    st.markdown("🏁 **FINAL ANSWER:**")
                                    st.success(resp.content) # Green box to highlight the conclusion
                                else:
                                    # If it's not the last message, it's an intermediate "Thought" or plan.
                                    st.markdown(f"🤔 **AI Thought:**\n{resp.content}")

                    # --- H. DISPLAY FINAL OUTPUT IN MAIN CHAT ---
                    # After the reasoning process is complete, we need to extract the final natural language answer.
                    # We check if the response dictionary is valid and contains messages.
                    if "messages" in response and len(response["messages"]) > 0:
                        # The last message in the list is always the Final Answer (or the most recent output).
                        last_response = response["messages"][-1].content.replace("Final Answer: ", "").strip()
                    else:
                        # Fallback mechanism: If the agent returns an empty response or fails, provide a default error message.
                        last_response = "I'm sorry, I couldn't generate a response."

                    # Render the final answer in the main chat interface.
                    # This ensures the user sees the clean result without needing to open the "Reasoning Trace" expander.
                    st.markdown(last_response)

                    # --- I. UPDATE SESSION STATE (AI SIDE) ---
                    # Persist the AI's final answer into the session state chat history.
                    # This is critical for maintaining 'Conversation Memory' so the agent remembers this context for the next query.
                    st.session_state.messages.append({"role": "ai", "content": last_response})

                # --- J. RUNTIME ERROR HANDLING ---
                # These errors happen *during* execution (e.g., bad SQL, API limits).
                except Exception as e:
                    # Convert error to string for keyword matching
                    error_str = str(e).lower()

                    # 1. API Quota Limits (Gemini/Google)
                    # This bubble up from the LLM Node if you hit the rate limit.
                    if "429" in error_str or "resource" in error_str:
                        st.error("⏳ API Quota Exceeded. Please wait a moment or check your Google Cloud plan.", icon="🛑")

                    # 2. Authentication Errors
                    # This happens if the API key was valid at start but rejected during the call.
                    elif "api_key" in error_str or "400" in error_str:
                        st.error("🔑 Invalid API Key. Please check your Google API Key in the sidebar.", icon="🚫")

                    # 3. Parsing/Output Errors
                    # Rare in LangGraph, but happens if the LLM generates invalid JSON for tool arguments.
                    elif "parsing" in error_str or "outputparser" in error_str:
                        st.error("🧩 Parsing Error. The model response could not be interpreted. Please try again.", icon="😵‍💫")

                    # 4. SQL Execution Errors (Tool Node)
                    # This happens if the Agent writes bad SQL (e.g., querying a column that doesn't exist).
                    # 'OperationalError' comes from the SQLite driver.
                    elif "operationalerror" in error_str:
                        st.error("🛠️ Database Error. The generated SQL query failed to execute.", icon="📉")

                    # 5. Catch-All
                    else:
                        error_msg = f"❌ An error occurred: {str(e)}"
                        st.error(error_msg, icon="🚨")