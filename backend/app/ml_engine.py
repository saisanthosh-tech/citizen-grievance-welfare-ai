"""
AI engine for analyzing citizen grievances.

This module should:
- Take grievance text as input
- Classify the grievance into a category
- Detect urgency using keywords or sentiment
- Assign a priority level: HIGH, MEDIUM, or LOW
- Return results in a structured dictionary

NOTE:
This ML engine is intentionally simple and explainable.
It uses lightweight NLP techniques suitable for government systems.
Logic clarity and fairness are prioritized over black-box complexity.
"""
import re

class GrievanceAnalyzer:
    def __init__(self):
        # Define keywords for categorization
        self.categories = {
            "Healthcare": ["hospital", "doctor", "nurse", "medicine", "health", "clinic", "treatment", "ambulance"],
            "Education": ["school", "teacher", "class", "student", "books", "education", "college", "exam"],
            "Water Supply": ["water", "leak", "pipe", "shortage", "dirty", "supply", "tank"],
            "Roads & Transport": ["road", "pothole", "bus", "traffic", "transport", "street", "bridge"],
            "Electricity": ["power", "electricity", "outage", "voltage", "wire", "pole", "light"],
            "Sanitation": ["garbage", "trash", "waste", "clean", "drain", "sewage", "dustbin"]
        }

        # Define keywords for priority
        self.priority_keywords = {
            "High": ["urgent", "immediate", "emergency", "severe", "critical", "danger", "hazard", "death", "accident"],
            "Low": ["minor", "suggestion", "feedback", "delay", "slow"]
        }

        # Define schemes mapping
        self.schemes_mapping = {
            "Healthcare": ["Ayushman Bharat", "Pradhan Mantri Jan Arogya Yojana (PMJAY)", "National Health Mission"],
            "Education": ["Sarva Shiksha Abhiyan", "Mid-Day Meal Scheme", "National Scholarship Portal"],
            "Water Supply": ["Jal Jeevan Mission", "Atal Bhujal Yojana"],
            "Roads & Transport": ["Pradhan Mantri Gram Sadak Yojana"],
            "Electricity": ["Saubhagya Scheme", "Deen Dayal Upadhyaya Gram Jyoti Yojana"],
            "Sanitation": ["Swachh Bharat Mission"]
        }

    def analyze(self, text: str):
        """
        Analyze grievance with explainable logic.
        Returns: category, priority, schemes, confidence, and reasoning.
        Government-grade transparency and fairness.
        """
        if not text or len(text.strip()) < 5:
            raise ValueError("Grievance text must be at least 5 characters")
            
        text_lower = text.lower()
        
        # 1. Detect Category with confidence
        detected_category = "General"
        max_matches = 0
        category_matches = {}
        
        for category, keywords in self.categories.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            category_matches[category] = matches
            if matches > max_matches:
                max_matches = matches
                detected_category = category
        
        # Calculate confidence: more keyword matches = higher confidence
        confidence = min(1.0, (max_matches / 3.0)) if max_matches > 0 else 0.0
        
        # 2. Detect Priority with explanation
        priority = "Medium"
        priority_reason = "No urgent keywords detected"
        
        # Check High priority
        high_keywords_found = [kw for kw in self.priority_keywords["High"] if kw in text_lower]
        if high_keywords_found:
            priority = "High"
            priority_reason = f"High urgency keywords detected: {', '.join(high_keywords_found)}"
        # Check Low priority (only if not High)
        elif any(keyword in text_lower for keyword in self.priority_keywords["Low"]):
            priority = "Low"
            priority_reason = "Low urgency - marked as feedback or minor issue"
        
        # 3. Recommend Schemes
        suggested_schemes = self.schemes_mapping.get(detected_category, ["General Welfare Schemes"])
        
        # 4. Generate explanation for transparency
        explanation = {
            "category_detection": f"Matched {max_matches} keyword(s) in '{detected_category}' category",
            "confidence": f"{int(confidence * 100)}%",
            "priority_reason": priority_reason,
            "relevant_keywords": category_matches
        }
        
        return {
            "category": detected_category,
            "priority": priority,
            "suggested_schemes": suggested_schemes,
            "confidence_score": round(confidence, 2),
            "analysis_explanation": explanation
        }

analyzer = GrievanceAnalyzer()
