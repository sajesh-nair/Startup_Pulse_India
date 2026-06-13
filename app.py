import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="National Startup Registry Playbook", page_icon="🎯", layout="wide")

# 2. Premium Executive Dark-Theme UI System Injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap');
    
    .stApp { 
        background-color: #060913; 
        font-family: 'Inter', system-ui, sans-serif; 
    }
    
    .telemetry-title { 
        color: #ffffff; 
        font-size: 2.4rem; 
        font-weight: 900; 
        letter-spacing: -1.5px; 
        text-transform: uppercase;
        margin-bottom: 2px;
        line-height: 1.1;
    }
    .telemetry-subtitle { 
        color: #4b5563; 
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem; 
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 35px; 
    }
    .dynamic-insight-card {
        background: #111827;
        border-left: 4px solid #00f2fe;
        padding: 20px;
        border-radius: 4px;
        color: #e5e7eb;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 30px;
        border-top: 1px solid #1f2937;
        border-right: 1px solid #1f2937;
        border-bottom: 1px solid #1f2937;
    }
    
    div[data-testid="stMetricValue"] { 
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem !important; 
        font-weight: 700 !important; 
        color: #00f2fe !important; 
    }
    div[data-testid="stMetricLabel"] { 
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem !important; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        color: #4b5563 !important; 
    }
    
    div[data-testid="stRadio"] > label {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 10px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 20px;
    }
    
    .panel-divider { border-bottom: 1px solid #1e293b; margin: 35px 0; }
    </style>
""", unsafe_allow_html=True)

# 3. Optimized High-Throughput Data Engine
@st.cache_data
def load_national_registry_data():
    df = pd.read_csv("data/dpiit_startups_2026.csv")
    df.columns = [col.strip().replace(" ", "") for col in df.columns]
    df['state'] = df['state'].astype(str).str.strip()
    df['industry'] = df['industry'].astype(str).str.strip()
    return df

df = load_national_registry_data()

# Pre-calculate baseline metrics for pipeline operations
total_national_volume = int(df['startups_recognized'].sum())
unique_states_list = sorted(df['state'].unique())
unique_industries_list = sorted(df['industry'].unique())

# --- HEADER PRESENTATION LAYER ---
st.markdown("<div class='telemetry-title'>🎯 NATIONAL STARTUP WAVE PLAYBOOK</div>", unsafe_allow_html=True)
st.markdown("<div class='telemetry-subtitle'>Official DPIIT Registry // Dual-Perspective Field Analysis</div>", unsafe_allow_html=True)

# --- GLOBAL RADIO TOGGLE ---
view_perspective = st.radio(
    "🔄 SELECT ECOSYSTEM SEGREGATION PERSPECTIVE:",
    options=["INDUSTRY-WISE ANALYSIS", "STATE-WISE ANALYSIS"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================================
# PERSPECTIVE 1: INDUSTRY-WISE ANALYSIS (Path: Industry ➔ State)
# =====================================================================
if view_perspective == "INDUSTRY-WISE ANALYSIS":
    
    # Prepend the global "ALL INDUSTRIES" option right into the drop-down menu array
    industry_options = ["ALL INDUSTRIES"] + unique_industries_list
    
    selected_target_industry = st.selectbox(
        "🔍 CHOOSE TARGET INDUSTRY DOMAIN TO PROFILE REGIONAL LEADERS:",
        options=industry_options,
        index=0  # Defaults to the broad overview option cleanly
    )
    
    # Dynamic Calculation & Branch Selection Rules
    if selected_target_industry == "ALL INDUSTRIES":
        # Group everything nationally for a multi-grid overview presentation
        plot_df = df.groupby(['industry', 'state'])['startups_recognized'].sum().reset_index()
        # Top 25 sectors to keep it completely crisp and free of low-volume noise
        top_sectors = plot_df.groupby('industry')['startups_recognized'].sum().nlargest(25).index
        plot_df = plot_df[plot_df['industry'].isin(top_sectors)]
        
        tree_path = ['industry', 'state']
        
        total_display_volume = total_national_volume
        share_metric = 100.0
        coverage_label = f"{df['state'].nunique()} Regions"
        context_string = "ALL DOMAINS COMBINED (NATIONAL OVERVIEW)"
        card_text = "Showing a complete breakdown of the top 25 active industry sectors across India and their primary regional hub weights."
    else:
        # Isolate the one single selected domain framework
        plot_df = df[df['industry'] == selected_target_industry]
        
        tree_path = ['industry', 'state']
        
        total_display_volume = int(plot_df['startups_recognized'].sum())
        share_metric = (total_display_volume / total_national_volume) * 100
        coverage_label = f"{plot_df['state'].nunique()} Regions"
        context_string = selected_target_industry.upper()
        card_text = f"The <b>{selected_target_industry}</b> segment accounts for <b>{share_metric:.2f}%</b> of India's overall registry footprint. The map below charts its geographic distribution."

    # Dynamic Context Briefing Banner
    st.markdown(f"""
        <div class='dynamic-insight-card'>
            <b>📈 SECTOR ANALYSIS PROFILE ({context_string}):</b> 
            Total volume contains <b>{total_display_volume:,}</b> active registrations nationwide. {card_text}
        </div>
    """, unsafe_allow_html=True)
    
    # Status Metric Counter Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label=f"DISPLAYED REGISTRATIONS", value=f"{total_display_volume:,}")
    with m2:
        st.metric(label="TOTAL NATIONAL SHARE", value=f"{share_metric:.1f}%")
    with m3:
        st.metric(label="GEOGRAPHIC COVERAGE", value=coverage_label)
        
    st.markdown("<div class='panel-divider'></div>", unsafe_allow_html=True)
    
    # Generate the Industry Treemap Matrix
    fig_tree = px.treemap(
        plot_df,
        path=tree_path,
        values='startups_recognized',
        color='startups_recognized',
        color_continuous_scale=["#0a1128", "#1c2541", "#3a506b", "#00f2fe"],
        labels={"startups_recognized": "Startups Volume"}
    )


# =====================================================================
# PERSPECTIVE 2: STATE-WISE ANALYSIS (Path: State ➔ Industry)
# =====================================================================
else:
    
    # Prepend the global "ALL STATES / UTs" option right into the drop-down menu array
    state_options = ["ALL STATES / UTs"] + unique_states_list
    
    selected_target_state = st.selectbox(
        "📍 CHOOSE TARGET STATE OR UT TO DRILL DOWN INTO LOCAL SECTORS:",
        options=state_options,
        index=0  # Defaults to the broad overview option cleanly
    )
    
    # Dynamic Calculation & Branch Selection Rules
    if selected_target_state == "ALL STATES / UTs":
        # Group everything nationally for a multi-grid overview presentation
        plot_df = df.groupby(['state', 'industry'])['startups_recognized'].sum().reset_index()
        # Top 15 states to avoid clamping small territories into tiny blocks
        top_regions = plot_df.groupby('state')['startups_recognized'].sum().nlargest(15).index
        plot_df = plot_df[plot_df['state'].isin(top_regions)]
        
        tree_path = ['state', 'industry']
        
        total_display_volume = total_national_volume
        share_metric = 100.0
        coverage_label = f"{df['industry'].nunique()} Domains"
        context_string = "ALL STATES COMBINED (NATIONAL OVERVIEW)"
        card_text = "Showing a complete breakdown of the top 15 highest density state economies across India and the industry sectors built within them."
    else:
        # Isolate the one single selected geographic state footprint
        plot_df = df[df['state'] == selected_target_state]
        
        tree_path = ['state', 'industry']
        
        total_display_volume = int(plot_df['startups_recognized'].sum())
        share_metric = (total_display_volume / total_national_volume) * 100
        coverage_label = f"{plot_df['industry'].nunique()} Domains"
        context_string = selected_target_state.upper()
        card_text = f"The regional ecosystem of <b>{selected_target_state}</b> represents <b>{share_metric:.2f}%</b> of the overall national market volume. The map below outlines local sector choices."

    # Dynamic Context Briefing Banner
    st.markdown(f"""
        <div class='dynamic-insight-card'>
            <b>🦁 REGIONAL ANALYSIS PROFILE ({context_string}):</b> 
            Total volume contains <b>{total_display_volume:,}</b> active registrations. {card_text}
        </div>
    """, unsafe_allow_html=True)
    
    # Status Metric Counter Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label=f"DISPLAYED REGISTRATIONS", value=f"{total_display_volume:,}")
    with m2:
        st.metric(label="NATIONAL MARKET SHARE", value=f"{share_metric:.1f}%")
    with m3:
        st.metric(label="INDUSTRIAL DIVERSIFICATION", value=coverage_label)
        
    st.markdown("<div class='panel-divider'></div>", unsafe_allow_html=True)
    
    # Generate the State Treemap Matrix
    fig_tree = px.treemap(
        plot_df,
        path=tree_path,
        values='startups_recognized',
        color='startups_recognized',
        color_continuous_scale=["#0a1128", "#1c2541", "#00b4d8", "#00f2fe"],
        labels={"startups_recognized": "Registered Startups"}
    )


# --- UNIFIED PRESENTATION SHEET RENDERING ---
fig_tree.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=0, b=0),
    height=600
)

fig_tree.update_traces(
    textinfo="label+value",
    textfont=dict(family="JetBrains Mono, monospace", size=13, color="#ffffff"),
    hovertemplate="<b>%{label}</b><br>Active Count: %{value:,}"
)

st.plotly_chart(fig_tree, width="stretch", key="unified_perspective_treemap_plot")