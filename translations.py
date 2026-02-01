"""
Multi-Language Translation System
Supports English and Hindi for the Grievance Management System
"""

# Translation Dictionary
TRANSLATIONS = {
    "en": {
        # Navigation & Headers
        "app_title": "Citizen Grievance & Welfare Intelligence",
        "homepage_subtitle": "Submit your concerns to help us serve you better. Your feedback is important to improving public services.",
        "submit_grievance": "Submit Grievance",
        "track_grievance": "Track Grievance",
        "admin_dashboard": "Admin Dashboard",
        "analytics_dashboard": "Analytics Dashboard",
        
        # Common
        "home": "Home",
        "submit": "Submit",
        "search": "Search",
        "save": "Save",
        "cancel": "Cancel",
        "close": "Close",
        "refresh": "Refresh",
        "loading": "Loading...",
        
        # Form Labels
        "title": "Title",
        "description": "Description",
        "location": "Location",
        "category": "Category",
        "priority": "Priority",
        "status": "Status",
        "date": "Date",
        "id": "ID",
        
        # Status Values
        "pending": "Pending",
        "in_progress": "In Progress",
        "resolved": "Resolved",
        "rejected": "Rejected",
        
        # Priority Values
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        
        # Categories
        "healthcare": "Healthcare",
        "education": "Education",
        "water_supply": "Water Supply",
        "roads_transport": "Roads & Transport",
        "electricity": "Electricity",
        "sanitation": "Sanitation",
        "unknown": "Unknown",
        
        # Submit Grievance Page
        "submit_your_grievance": "Submit Your Grievance",
        "grievance_title": "Grievance Title",
        "grievance_description": "Grievance Description",
        "your_location": "Your Location (Optional)",
        "upload_photo": "Upload Photo (Optional)",
        "submit_button": "📝 Submit Grievance",
        "title_placeholder": "Brief summary of your concern",
        "description_placeholder": "Describe your grievance in detail...",
        "location_placeholder": "e.g., Ward No. 5, Sector 4",
        
        # Success Messages
        "grievance_submitted": "Grievance Submitted Successfully!",
        "grievance_received": "Your grievance has been received and analyzed by our AI system.",
        "status_updated": "Status updated successfully!",
        
        # AI Analysis
        "ai_analysis": "AI Analysis Results",
        "confidence": "Confidence",
        "ai_confidence": "AI Confidence",
        "classification_details": "Classification Details",
        "suggested_schemes": "Recommended Government Schemes",
        "why_classification": "Why This Classification?",
        
        # Track Grievance
        "track_your_grievance": "Track Your Grievance",
        "enter_grievance_id": "Enter your grievance ID to check the current status",
        "grievance_id": "Grievance ID",
        "grievance_details": "Grievance Details",
        "status_history": "Status History",
        "official_notes": "Official Notes",
        
        # Admin Dashboard
        "admin_panel": "Admin Panel",
        "filter_by_status": "Filter by Status",
        "filter_by_category": "Filter by Category",
        "filter_by_priority": "Filter by Priority",
        "update_status": "Update Status",
        "save_changes": "💾 Save Changes",
        "view_analysis": "View Analysis",
        "view_history": "View Status History",
        
        # Analytics Dashboard
        "analytics": "Analytics Dashboard",
        "real_time_insights": "Real-time insights into citizen grievances and system performance",
        "key_indicators": "Key Performance Indicators",
        "total_grievances": "Total Grievances",
        "avg_confidence": "Avg Confidence",
        "avg_resolution_time": "Avg Resolution Time",
        "grievance_distribution": "Grievance Distribution",
        "trends_analysis": "Trends & Analysis",
        "by_category": "Grievances by Category",
        "by_priority": "Grievances by Priority Level",
        "by_status": "Grievances by Status",
        "recent_grievances": "Recent Grievances",
        "refresh_dashboard": "🔄 Refresh Dashboard",
        
        # Metrics
        "this_week": "this week",
        "days": "days",
        "excellent": "Excellent",
        "good": "Good",
        "fair": "Fair",
        
        # Help & Info
        "need_help": "Need Help?",
        "what_happens_next": "What happens next?",
        "tips_for_submission": "Tips for Your Submission",
        "be_specific": "Be specific",
        
        # Timeline
        "grievance_submitted_action": "Grievance submitted",
        "status_changed_to": "Status changed to",
        "by_citizen": "by citizen",
        "by_admin": "by admin",
        "by_system": "by system",
    },
    
    "hi": {
        # Navigation & Headers
        "app_title": "नागरिक शिकायत और कल्याण प्रणाली",
        "homepage_subtitle": "बेहतर सेवा के लिए अपनी चिंताएं दर्ज करें। आपकी प्रतिक्रिया सार्वजनिक सेवाओं में सुधार के लिए महत्वपूर्ण है।",
        "submit_grievance": "शिकायत दर्ज करें",
        "track_grievance": "शिकायत ट्रैक करें",
        "admin_dashboard": "प्रशासन डैशबोर्ड",
        "analytics_dashboard": "विश्लेषण डैशबोर्ड",
        
        # Common
        "home": "होम",
        "submit": "जमा करें",
        "search": "खोजें",
        "save": "सहेजें",
        "cancel": "रद्द करें",
        "close": "बंद करें",
        "refresh": "रीफ्रेश करें",
        "loading": "लोड हो रहा है...",
        
        # Form Labels
        "title": "शीर्षक",
        "description": "विवरण",
        "location": "स्थान",
        "category": "श्रेणी",
        "priority": "प्राथमिकता",
        "status": "स्थिति",
        "date": "तारीख",
        "id": "आईडी",
        
        # Status Values
        "pending": "लंबित",
        "in_progress": "प्रगति में",
        "resolved": "हल हो गया",
        "rejected": "अस्वीकृत",
        
        # Priority Values
        "high": "उच्च",
        "medium": "मध्यम",
        "low": "निम्न",
        
        # Categories
        "healthcare": "स्वास्थ्य सेवा",
        "education": "शिक्षा",
        "water_supply": "जल आपूर्ति",
        "roads_transport": "सड़क और परिवहन",
        "electricity": "बिजली",
        "sanitation": "स्वच्छता",
        "unknown": "अज्ञात",
        
        # Submit Grievance Page
        "submit_your_grievance": "अपनी शिकायत दर्ज करें",
        "grievance_title": "शिकायत का शीर्षक",
        "grievance_description": "शिकायत का विवरण",
        "your_location": "आपका स्थान (वैकल्पिक)",
        "upload_photo": "फोटो अपलोड करें (वैकल्पिक)",
        "submit_button": "📝 शिकायत दर्ज करें",
        "title_placeholder": "अपनी चिंता का संक्षिप्त सारांश",
        "description_placeholder": "अपनी शिकायत का विस्तार से वर्णन करें...",
        "location_placeholder": "उदा., वार्ड नं. 5, सेक्टर 4",
        
        # Success Messages
        "grievance_submitted": "शिकायत सफलतापूर्वक दर्ज की गई!",
        "grievance_received": "आपकी शिकायत प्राप्त हो गई है और हमारे AI सिस्टम द्वारा विश्लेषण किया गया है।",
        "status_updated": "स्थिति सफलतापूर्वक अपडेट की गई!",
        
        # AI Analysis
        "ai_analysis": "AI विश्लेषण परिणाम",
        "confidence": "विश्वास",
        "ai_confidence": "AI विश्वास",
        "classification_details": "वर्गीकरण विवरण",
        "suggested_schemes": "अनुशंसित सरकारी योजनाएं",
        "why_classification": "यह वर्गीकरण क्यों?",
        
        # Track Grievance
        "track_your_grievance": "अपनी शिकायत ट्रैक करें",
        "enter_grievance_id": "वर्तमान स्थिति जांचने के लिए अपनी शिकायत आईडी दर्ज करें",
        "grievance_id": "शिकायत आईडी",
        "grievance_details": "शिकायत विवरण",
        "status_history": "स्थिति इतिहास",
        "official_notes": "आधिकारिक नोट्स",
        
        # Admin Dashboard
        "admin_panel": "प्रशासन पैनल",
        "filter_by_status": "स्थिति के अनुसार फ़िल्टर करें",
        "filter_by_category": "श्रेणी के अनुसार फ़िल्टर करें",
        "filter_by_priority": "प्राथमिकता के अनुसार फ़िल्टर करें",
        "update_status": "स्थिति अपडेट करें",
        "save_changes": "💾 परिवर्तन सहेजें",
        "view_analysis": "विश्लेषण देखें",
        "view_history": "स्थिति इतिहास देखें",
        
        # Analytics Dashboard
        "analytics": "विश्लेषण डैशबोर्ड",
        "real_time_insights": "नागरिक शिकायतों और सिस्टम प्रदर्शन में वास्तविक समय की जानकारी",
        "key_indicators": "मुख्य प्रदर्शन संकेतक",
        "total_grievances": "कुल शिकायतें",
        "avg_confidence": "औसत विश्वास",
        "avg_resolution_time": "औसत समाधान समय",
        "grievance_distribution": "शिकायत वितरण",
        "trends_analysis": "रुझान और विश्लेषण",
        "by_category": "श्रेणी के अनुसार शिकायतें",
        "by_priority": "प्राथमिकता स्तर के अनुसार शिकायतें",
        "by_status": "स्थिति के अनुसार शिकायतें",
        "recent_grievances": "हाल की शिकायतें",
        "refresh_dashboard": "🔄 डैशबोर्ड रीफ्रेश करें",
        
        # Metrics
        "this_week": "इस सप्ताह",
        "days": "दिन",
        "excellent": "उत्कृष्ट",
        "good": "अच्छा",
        "fair": "ठीक",
        
        # Help & Info
        "need_help": "मदद चाहिए?",
        "what_happens_next": "आगे क्या होगा?",
        "tips_for_submission": "सबमिशन के लिए सुझाव",
        "be_specific": "विशिष्ट रहें",
        
        # Timeline
        "grievance_submitted_action": "शिकायत दर्ज की गई",
        "status_changed_to": "स्थिति बदलकर",
        "by_citizen": "नागरिक द्वारा",
        "by_admin": "प्रशासक द्वारा",
        "by_system": "सिस्टम द्वारा",
    }
}

def get_translation(key, lang="en"):
    """
    Get translation for a given key in the specified language
    
    Args:
        key: Translation key
        lang: Language code ('en' or 'hi')
    
    Returns:
        Translated string or key if not found
    """
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["en"].get(key, key))

def get_all_translations(lang="en"):
    """Get all translations for a language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"])
