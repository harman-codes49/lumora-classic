import streamlit as st

from app.database.db import initialize_database
from app.database.seed import seed_if_empty

from app.ui.chat import render_chat
from app.ui.memories import render_memories
from app.ui.calendar import render_calendar
from app.ui.reflection import render_reflection
from app.ui.search import render_search
from app.ui.mood_insights import render_mood_insights
from app.ui.space import render_space
from app.ui.relationship_support import render_relationship_support

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Lumora",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

initialize_database()
seed_if_empty()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "pending_date_suggestions" not in st.session_state:
    st.session_state.pending_date_suggestions = []

# =========================================================
# LUMORA GLOBAL UI
# =========================================================

st.html("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600&display=swap'
);


/* =====================================================
   GLOBAL
   ===================================================== */

html,
body,
[class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background: #fcfafd;
}

[data-testid="stAppViewContainer"] .main .block-container {

    max-width: 1280px;

    padding-top: 0px;
    padding-bottom: 25px;

    padding-left: 38px;
    padding-right: 38px;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {

    background: #f7f1fa;

    border-right: 1px solid #e7ddec;

}

[data-testid="stSidebar"] > div {

    padding-top: 0px;

}


/* =====================================================
   SIDEBAR BRAND
   ===================================================== */

.sidebar-brand {

    padding-top: 30px;

    padding-left: 30px;
    padding-right: 30px;

    padding-bottom: 55px;

}

.sidebar-logo {

    font-size: 27px;

    margin-bottom: 8px;

}

.sidebar-title {

    font-family: "Playfair Display", serif;

    font-size: 27px;

    line-height: 1.1;

    color: #403858;

}

.sidebar-subtitle {

    color: #93889e;

    font-size: 10px;

    margin-top: 8px;

}


/* =====================================================
   SIDEBAR DIVIDER
   ===================================================== */

.sidebar-divider {

    height: 1px;

    background: #ddd3e3;

    margin-left: 39px;
    margin-right: 39px;

    margin-bottom: 46px;

}


/* =====================================================
   SIDEBAR BUTTONS
   ===================================================== */

[data-testid="stSidebar"] .stButton {

    padding-left: 28px;
    padding-right: 28px;

}


[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    height: 44px;
    min-height: 44px;

    border-radius: 11px;

    background: #ffffff;

    border: 1px solid #ded5e5;

    color: #574d62;

    font-size: 13px;

    font-weight: 400;

    text-align: left;

    padding-left: 15px;

    margin-bottom: 9px;

    box-shadow: none;

}


[data-testid="stSidebar"] .stButton > button:hover {

    background: #ffffff;

    border-color: #cdbdd8;

    color: #403858;

}


[data-testid="stSidebar"] .stButton > button:focus {

    background: #ffffff;

    border-color: #cdbdd8;

    color: #403858;

}


/* =====================================================
   SIDEBAR QUOTE
   ===================================================== */

.sidebar-quote {

    margin-top: 24px;

    margin-left: 25px;
    margin-right: 25px;

    padding: 17px;

    border-radius: 18px;

    background: #eee5f5;

    color: #766a80;

    font-size: 11px;

    line-height: 1.55;

}


/* =====================================================
   TOP AREA
   ===================================================== */

.top-area {

    display: flex;

    align-items: center;

    justify-content: space-between;

    width: 100%;

    /* REDUCED FROM 135px */
    margin-top: 25px;

    margin-bottom: 38px;

}


/* =====================================================
   MAIN BRAND
   ===================================================== */

.main-brand {

    display: flex;

    align-items: center;

    gap: 15px;

    flex-shrink: 0;

}


.main-brand-icon {

    width: 60px;
    height: 60px;

    border-radius: 18px;

    background: #eee4f7;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 31px;

}


.main-brand-name {

    font-family: "Playfair Display", serif;

    color: #403858;

    font-size: 39px;

    line-height: 1;

}


.main-brand-subtitle {

    color: #8e8398;

    font-size: 11px;

    margin-top: 6px;

}


/* =====================================================
   FEATURE STRIP
   ===================================================== */

.feature-strip {

    display: flex;

    align-items: flex-start;

    justify-content: flex-end;

    gap: 18px;

    flex: 1;

    margin-left: 35px;

}


.feature-item {

    width: 65px;

    text-align: center;

    color: #756a80;

    font-size: 9px;

    line-height: 1.25;

}


.feature-icon-box {

    width: 45px;
    height: 45px;

    margin: 0 auto 7px auto;

    border-radius: 14px;

    background: #eee6f6;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 17px;

}


/* =====================================================
   GREETING
   ===================================================== */

.greeting {

    font-family: "Playfair Display", serif;

    color: #403858;

    font-size: 29px;

    line-height: 1.2;

    margin-bottom: 7px;

}


.greeting-subtitle {

    color: #8f8499;

    font-size: 11px;

    margin-bottom: 50px;

}


/* =====================================================
   HERO ROW
   ===================================================== */

.hero-row {

    display: grid;

    grid-template-columns: 1.45fr 0.95fr;

    gap: 30px;

}


/* =====================================================
   TALK TO LUMORA
   ===================================================== */

.chat-home-card {

    background: #ead8f2;

    border-radius: 23px;

    min-height: 205px;

    padding: 28px;

}


.chat-home-title {

    font-family: "Playfair Display", serif;

    color: #403858;

    font-size: 24px;

    margin-bottom: 12px;

}


.chat-home-text {

    color: #756a7d;

    font-size: 12px;

    line-height: 1.65;

}


/* =====================================================
   START CONVERSATION BUTTON
   ===================================================== */

/*
   Streamlit renders the button separately from st.html().
   This negative margin makes it visually sit INSIDE
   the lavender Talk to Lumora card.
*/

.chat-start-wrapper {

    position: relative;

    margin-top: -65px;

    margin-left: 28px;

    margin-bottom: 22px;

    z-index: 20;

}


.chat-start-wrapper .stButton > button {

    width: 163px;

    height: 42px;

    min-height: 42px;

    border: none;

    border-radius: 11px;

    background: #8261b4;

    color: #ffffff;

    font-size: 12px;

    font-weight: 500;

    box-shadow: none;

}


.chat-start-wrapper .stButton > button:hover {

    background: #7352a4;

    color: #ffffff;

    border: none;

}


/* =====================================================
   TODAY'S REFLECTION
   ===================================================== */

.reflection-home-card {

    background: #ffffff;

    border: 1px solid #eee5f1;

    border-radius: 23px;

    min-height: 205px;

    padding: 29px;

}


.reflection-home-title {

    font-family: "Playfair Display", serif;

    color: #403858;

    font-size: 21px;

    margin-bottom: 6px;

}


.reflection-home-subtitle {

    color: #94899d;

    font-size: 10px;

    margin-bottom: 17px;

}


/* =====================================================
   MOOD EMOJIS
   ===================================================== */

.mood-row {

    display: flex;

    gap: 10px;

}


.mood-emoji {

    width: 40px;
    height: 40px;

    border-radius: 13px;

    background: #f1e8f5;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 17px;

}


/* =====================================================
   NOTE
   ===================================================== */

.home-note {

    margin-top: 15px;

    height: 43px;

    border: 1px solid #e2d8e7;

    border-radius: 11px;

    display: flex;

    align-items: center;

    padding-left: 14px;

    color: #aaa0ad;

    font-size: 10px;

}


/* =====================================================
   EXPLORE
   ===================================================== */

.explore-title {

    font-family: "Playfair Display", serif;

    color: #403858;

    font-size: 20px;

    margin-top: 38px;

    margin-bottom: 15px;

}


/* =====================================================
   QUICK CARDS
   ===================================================== */

.quick-card {

    background: #ffffff;

    border: 1px solid #eee5f1;

    border-radius: 18px;

    padding: 18px;

    min-height: 112px;

}


.quick-icon {

    font-size: 17px;

    margin-bottom: 11px;

}


.quick-title {

    color: #403858;

    font-size: 12px;

    font-weight: 600;

}


.quick-description {

    color: #94899d;

    font-size: 10px;

    margin-top: 6px;

}


/* =====================================================
   QUICK ACTION BUTTONS
   ===================================================== */

.quick-button .stButton > button {

    width: 100%;

    height: 28px;

    min-height: 28px;

    background: transparent;

    border: none;

    color: #8062a8;

    font-size: 10px;

    padding: 0;

}


/* =====================================================
   RESPONSIVE
   ===================================================== */

@media (max-width: 1050px) {

    .top-area {

        flex-direction: column;

        align-items: flex-start;

        margin-top: 25px;

    }

    .feature-strip {

        width: 100%;

        justify-content: flex-start;

        margin-left: 0;

        margin-top: 22px;

    }

}


@media (max-width: 700px) {

    .hero-row {

        grid-template-columns: 1fr;

    }

    .feature-strip {

        display: grid;

        grid-template-columns: repeat(4, 65px);

    }

}

</style>
""")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            🌿
        </div>

        <div class="sidebar-title">
            Lumora
        </div>

        <div class="sidebar-subtitle">
            Harmanpreet Kaur's space to feel, talk and grow
        </div>

    </div>

    <div class="sidebar-divider"></div>
    """)


    if st.button(
        "🏠  Home",
        key="sidebar_home",
        use_container_width=True
    ):
        st.session_state.page = "home"
        st.rerun()


    if st.button(
        "💬  Chat",
        key="sidebar_chat",
        use_container_width=True
    ):
        st.session_state.page = "chat"
        st.rerun()


    if st.button(
        "📸  Memories",
        key="sidebar_memories",
        use_container_width=True
    ):
        st.session_state.page = "memories"
        st.rerun()


    if st.button(
        "📅  Calendar",
        key="sidebar_calendar",
        use_container_width=True
    ):
        st.session_state.page = "calendar"
        st.rerun()


    if st.button(
        "🌱  Reflection",
        key="sidebar_reflection",
        use_container_width=True
    ):
        st.session_state.page = "reflection"
        st.rerun()


    if st.button(
        "🔍  Search",
        key="sidebar_search",
        use_container_width=True
    ):
        st.session_state.page = "search"
        st.rerun()


    if st.button(
        "👤  Your Space",
        key="sidebar_space",
        use_container_width=True
    ):
        st.session_state.page = "space"
        st.rerun()


    st.html("""
    <div class="sidebar-quote">

        <b>A small step</b><br>

        every day still counts. 💜

    </div>
    """)


# =========================================================
# HOME PAGE
# =========================================================

def render_home():

    # =====================================================
    # BRAND + FEATURE STRIP
    # =====================================================

    st.html("""
    <div class="top-area">

        <div class="main-brand">

            <div class="main-brand-icon">
                🌿
            </div>

            <div>

                <div class="main-brand-name">
                    Lumora
                </div>

                <div class="main-brand-subtitle">
                    Harmanpreet Kaur's space to feel, talk and grow
                </div>

            </div>

        </div>


        <div class="feature-strip">

            <div class="feature-item">

                <div class="feature-icon-box">
                    💬
                </div>

                AI<br>Companion

            </div>


            <div class="feature-item">

                <div class="feature-icon-box">
                    🌐
                </div>

                Multilingual

            </div>


            <div class="feature-item">

                <div class="feature-icon-box">
                    📅
                </div>

                Dates &<br>Reminders

            </div>


            <div class="feature-item">

                <div class="feature-icon-box">
                    ♡
                </div>

                Relationship<br>Support

            </div>


            <div class="feature-item">

                <div class="feature-icon-box">
                    🌱
                </div>

                Mood &<br>Reflection

            </div>


            <div class="feature-item">

                <div class="feature-icon-box">
                    ♢
                </div>

                Safety<br>Focused

            </div>


            <div class="feature-item">

                <div class="feature-icon-box">
                    ♟
                </div>

                Your<br>Control

            </div>

        </div>

    </div>
    """)


    # =====================================================
    # GREETING
    # =====================================================

    st.html("""
    <div class="greeting">
        Good morning, Harmanpreet Kaur 👋
    </div>

    <div class="greeting-subtitle">
        How are you feeling today?
    </div>
    """)


    # =====================================================
    # HERO ROW
    # =====================================================

    col1, col2 = st.columns(
        [1.45, 0.95],
        gap="large"
    )


    # =====================================================
    # TALK TO LUMORA
    # =====================================================

    with col1:

        st.html("""
        <div class="chat-home-card">

            <div class="chat-home-title">
                💬 Talk to Lumora
            </div>

            <div class="chat-home-text">
                Share your thoughts, feelings or just
                anything that's on your mind.
            </div>

        </div>
        """)


        # This button is visually pulled into
        # the lavender card.

        st.markdown(
            '<div class="chat-start-wrapper">',
            unsafe_allow_html=True
        )


        if st.button(
            "Start a conversation →",
            key="home_start_chat"
        ):

            st.session_state.page = "chat"

            st.rerun()


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # TODAY'S REFLECTION
    # =====================================================

    with col2:

        st.html("""
        <div class="reflection-home-card">

            <div class="reflection-home-title">
                Today's reflection
            </div>

            <div class="reflection-home-subtitle">
                How are you feeling right now?
            </div>

            <div class="mood-row">

                <div class="mood-emoji">
                    😌
                </div>

                <div class="mood-emoji">
                    😮
                </div>

                <div class="mood-emoji">
                    😀
                </div>

                <div class="mood-emoji">
                    😊
                </div>

                <div class="mood-emoji">
                    🌸
                </div>

            </div>

            <div class="home-note">
                Write a note...
            </div>

        </div>
        """)


    # =====================================================
    # EXPLORE YOUR SPACE
    # =====================================================

    st.html("""
    <div class="explore-title">
        Explore your space
    </div>
    """)


    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium"
    )


    # =====================================================
    # MEMORIES
    # =====================================================

    with col1:

        st.html("""
        <div class="quick-card">

            <div class="quick-icon">
                📸
            </div>

            <div class="quick-title">
                Memories
            </div>

            <div class="quick-description">
                24 saved moments
            </div>

        </div>
        """)


        if st.button(
            "Open →",
            key="home_memories",
            use_container_width=True
        ):

            st.session_state.page = "memories"
            st.rerun()


    # =====================================================
    # UPCOMING
    # =====================================================

    with col2:

        st.html("""
        <div class="quick-card">

            <div class="quick-icon">
                📅
            </div>

            <div class="quick-title">
                Upcoming
            </div>

            <div class="quick-description">
                2 reminders
            </div>

        </div>
        """)


        if st.button(
            "Open →",
            key="home_calendar",
            use_container_width=True
        ):

            st.session_state.page = "calendar"
            st.rerun()


    # =====================================================
    # MOOD INSIGHTS
    # =====================================================

    with col3:

        st.html("""
        <div class="quick-card">

            <div class="quick-icon">
                📊
            </div>

            <div class="quick-title">
                Mood Insights
            </div>

            <div class="quick-description">
                See your patterns
            </div>

        </div>
        """)


        if st.button(
            "Open →",
            key="home_mood",
            use_container_width=True
        ):

            st.session_state.page = "mood_insights"
            st.rerun()


    # =====================================================
    # RELATIONSHIP SUPPORT
    # =====================================================

    with col4:

        st.html("""
        <div class="quick-card">

            <div class="quick-icon">
                ♡
            </div>

            <div class="quick-title">
                Relationship Support
            </div>

            <div class="quick-description">
                Guidance for tougher days
            </div>

        </div>
        """)


        if st.button(
            "Talk to Lumora →",
            key="home_relationship",
            use_container_width=True
        ):

            st.session_state.page = "relationship"
            st.rerun()


# =========================================================
# PAGE ROUTING
# =========================================================

if st.session_state.page == "home":

    render_home()


elif st.session_state.page == "chat":

    render_chat()


elif st.session_state.page == "memories":

    render_memories()


elif st.session_state.page == "calendar":

    render_calendar()


elif st.session_state.page == "reflection":

    render_reflection()


elif st.session_state.page == "search":

    render_search()


elif st.session_state.page == "mood_insights":

    render_mood_insights()

elif st.session_state.page == "relationship":

    render_relationship_support() 
    
elif st.session_state.page == "space":

    render_space()