import streamlit as st
import pandas as pd
import re

# 1. Page Configuration
st.set_page_config(
    page_title="Forensic Messenger Pro",
    page_icon="⚖️",
    layout="wide"
)

# 2. Advanced CSS for a High-Visibility Professional UI
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    /* Title Styling */
    h1 {
        color: #1A365D;
        font-weight: 800;
        text-shadow: 1px 1px 2px #cbd5e0;
    }

    /* Professional Card Styling for the Uploader */
    .stFileUploader {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 2px dashed #3182ce;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Metric Box Styling */
    [data-testid="stMetricValue"] {
        color: #2b6cb0;
        font-weight: bold;
    }
    
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-bottom: 5px solid #3182ce;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1A365D;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h2 {
        color: white;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #3182ce;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic: The Forensic Parser
def parse_whatsapp(text):
    # Pattern for: 25/09/22, 4:26 pm - Name: Message
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2}\s[ap]m)\s-\s([^:]+):\s(.*)$'
    data = []
    for line in text.split('\n'):
        match = re.match(pattern, line)
        if match:
            data.append(match.groups())
    return pd.DataFrame(data, columns=['Date', 'Time', 'Sender', 'Message'])

# 4. MAIN UI - FRONT PAGE
st.title("🕵️‍♂️ Forensic Chat Reconstructor")
st.subheader("Professional Evidence Investigation & Analysis System")

# Updated line: Removed "Step 1" and ensured correct spacing
st.markdown("### 📥 Upload Evidence File")
uploaded_file = st.file_uploader("Drop your .txt chat export here for reconstruction", type="txt")

if uploaded_file:
    # Process Data
    raw_text = uploaded_file.read().decode("utf-8")
    df = parse_whatsapp(raw_text)

    if not df.empty:
        st.success(f"✅ Evidence Verified: {len(df)} records found.")

        # 5. Executive Dashboard (Metrics)
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        with m1:
            # Corrected spelling here
            st.metric("Investigation Total", len(df))
        with m2:
            st.metric("Unique Senders", df['Sender'].nunique())
        with m3:
            st.metric("Case Start Date", df['Date'].iloc[0])

        # 6. Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["📑 Evidence Timeline", "🔍 Deep Search", "📊 Activity Charts"])
        
        with tab1:
            st.markdown("### Reconstructed Message Log")
            st.dataframe(df, use_container_width=True, height=450)

        with tab2:
            st.markdown("### 🔎 Forensic Keyword Search")
            search_col, filter_col = st.columns([2,1])
            with search_col:
                query = st.text_input("Enter keyword (e.g., 'deleted', 'bank', 'urgent')")
            
            if query:
                filtered = df[df['Message'].str.contains(query, case=False)]
                st.warning(f"Found {len(filtered)} matching records.")
                st.table(filtered)

        with tab3:
            st.markdown("### 📈 Behavioral Analysis")
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Message Volume per Suspect**")
                st.bar_chart(df['Sender'].value_counts())
            with c2:
                st.write("**Communication Frequency over Time**")
                st.line_chart(df['Date'].value_counts())

        # 7. Sidebar Features
        st.sidebar.title("🛠 Forensic Tools")
        st.sidebar.markdown("Case ID: #WH-2026-001")
        csv = df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📄 Export Official Report (CSV)",
            data=csv,
            file_name="Forensic_Analysis_Report.csv",
            mime="text/csv",
        )
        
    else:
        st.error("Error: Could not parse the file. Please ensure it is a valid WhatsApp .txt export.")
else:
    # Welcome message when no file is uploaded
    # Corrected spelling: "Investigator"
    st.info("👋 Welcome, Investigator. Please upload a chat log to begin the reconstruction process.")
    st.image("https://img.icons8.com/clouds/500/000000/data-configuration.png", width=300)

# --- FOOTER SECTION ---
st.markdown("---")
footer_highlight_html = """
<style>
.main .block-container {
    padding-bottom: 70px !important;
}
.highligthed-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0e1117;
    color: #fafafa;
    text-align: center;
    padding: 15px 0;
    font-size: 16px;
    font-weight: 500;
    z-index: 100;
    border-top: 2px solid #ff4b4b;
}
.highligthed-footer p {
    margin: 0;
}
</style>
<div class="highligthed-footer">
    <p>🎓 Project Developed by: <b>Janhvi Ghode</b> & <b>Gunjan Narnaware</b></p>
</div>
"""
st.markdown(footer_highlight_html, unsafe_allow_html=True)

