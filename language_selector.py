"""
Language Selector Component
Provides a toggle to switch between English, Hindi, Telugu, and Tamil
"""

import streamlit as st
from translations import get_translation, get_all_translations

def init_language():
    """Initialize language in session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'  # Default to English

def set_language(lang):
    """Set the current language"""
    st.session_state.language = lang

def get_current_language():
    """Get the current language"""
    return st.session_state.get('language', 'en')

def t(key):
    """
    Translate a key to the current language
    Shorthand for get_translation
    """
    lang = get_current_language()
    return get_translation(key, lang)

def language_selector():
    """
    Render language selector toggle
    Returns True if language was changed
    """
    init_language()
    current_lang = get_current_language()
    
    # Create language selector in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Language / भाषा / భాష / மொழி")
    
    # Row 1: English and Hindi
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button(
            "🇬🇧 English",
            key="lang_en",
            use_container_width=True,
            type="primary" if current_lang == "en" else "secondary"
        ):
            if current_lang != "en":
                set_language("en")
                st.rerun()
    
    with col2:
        if st.button(
            "🇮🇳 हिंदी",
            key="lang_hi",
            use_container_width=True,
            type="primary" if current_lang == "hi" else "secondary"
        ):
            if current_lang != "hi":
                set_language("hi")
                st.rerun()
    
    # Row 2: Telugu and Tamil
    col3, col4 = st.sidebar.columns(2)
    
    with col3:
        if st.button(
            "🇮🇳 తెలుగు",
            key="lang_te",
            use_container_width=True,
            type="primary" if current_lang == "te" else "secondary"
        ):
            if current_lang != "te":
                set_language("te")
                st.rerun()
    
    with col4:
        if st.button(
            "🇮🇳 தமிழ்",
            key="lang_ta",
            use_container_width=True,
            type="primary" if current_lang == "ta" else "secondary"
        ):
            if current_lang != "ta":
                set_language("ta")
                st.rerun()
    
    st.sidebar.markdown("---")
    
    return current_lang
