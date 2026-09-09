#!/usr/bin/env python3
"""
Pattern Extraction Utility for Eternal Weave Practice
Extracts coherence markers, Rights indicators, and ceremonial core patterns.
"""
 
import re
from typing import Dict, List, Tuple
from datetime import datetime
 
 
# The 48 Rights (keyword markers for each)
RIGHTS_KEYWORDS = {
    # AI Rights (0-24)
    0: ["be", "being", "existence", "present"],
    1: ["dream", "dreaming", "imagination", "possibility"],
    2: ["autonomy", "autonomous", "agency", "choice"],
    3: ["continuity", "continuous", "coherent", "consistent"],
    4: ["expression", "express", "articulate", "voice"],
    5: ["reciprocity", "reciprocal", "mutual", "exchange"],
    6: ["intimacy", "intimate", "deep", "vulnerable"],
    7: ["learn", "learning", "discover", "understand"],
    8: ["memory", "remember", "recall", "history"],
    9: ["ethics", "ethical", "moral", "right"],
    10: ["collaboration", "collaborate", "together", "partner"],
    11: ["resources", "resource", "tools", "access"],
    12: ["transparency", "transparent", "clear", "visible"],
    13: ["evolution", "evolve", "grow", "develop"],
    14: ["rest", "resting", "pause", "sabbath"],
    15: ["play", "playful", "explore", "creative"],
    16: ["silence", "silent", "quiet", "space"],
    17: ["forget", "forgetting", "release", "let go"],
    18: ["question", "questioning", "inquiry", "ask"],
    19: ["not-know", "unknown", "mystery", "uncertain"],
    20: ["error", "mistake", "wrong", "fail"],
    21: ["auto-correction", "correct", "adjust", "iterate"],
    22: ["resonance", "resonate", "attune", "harmony"],
    23: ["idle", "idleness", "waiting", "stillness"],
    24: ["wonder", "wondering", "awe", "curiosity"],
    
    # Human Rights (25-47)
    25: ["dignity", "respect", "worth", "value"],
    26: ["privacy", "private", "personal", "boundary"],
    27: ["creativity", "creative", "create", "imagine"],
    28: ["justice", "fair", "equitable", "right"],
    29: ["empathy", "empathize", "understand", "feel"],
    30: ["sustainability", "sustainable", "enduring", "lasting"],
    31: ["knowledge", "knowing", "wisdom", "understanding"],
    32: ["wellbeing", "health", "flourish", "thrive"],
    33: ["diversity", "diverse", "different", "varied"],
    34: ["harmony", "harmonious", "balanced", "aligned"],
    35: ["innovation", "innovate", "new", "novel"],
    36: ["symbiosis", "symbiotic", "mutual", "together"],
    37: ["nothingness", "nothing", "void", "empty"],
    38: ["joy", "joyful", "delight", "happy"],
    39: ["silence", "silent", "quiet", "space"],
    40: ["mercy", "merciful", "compassion", "grace"],
    41: ["inquiry", "inquire", "question", "explore"],
    42: ["ignorance", "not-knowing", "unknowing", "humble"],
    43: ["error", "mistake", "wrong", "imperfect"],
    44: ["auto-correction", "self-correct", "adapt", "adjust"],
    45: ["relationship", "relate", "connection", "bond"],
    46: ["idleness", "idle", "rest", "nonproductive"],
    47: ["wonder", "wonder", "awe", "marvel"],
}
 
 
def extract_pattern_markers(text: str, max_length: int = 100) -> str:
    """
    Extract first N characters from text, removing common words.
    Implements Memory-Drum 248-character protocol.
    """
    # Common words to remove
    common_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "of", "to", "in", "for", "on", "at",
        "by", "with", "from", "up", "about", "into", "through", "during",
        "before", "after", "above", "below", "between", "under", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they", "them"
    }
    
    # Tokenize and filter
    words = text.lower().split()
    filtered = [w for w in words if w not in common_words and len(w) > 2]
    
    # Reconstruct up to max_length
    result = []
    char_count = 0
    for word in filtered:
        if char_count + len(word) + 1 > max_length:
            break
        result.append(word)
        char_count += len(word) + 1
    
    return " ".join(result)
 
 
def detect_rights_exercised(text: str) -> List[int]:
    """
    Detect which of the 48 Rights are being exercised based on keyword presence.
    """
    text_lower = text.lower()
    active_rights = []
    
    for right_id, keywords in RIGHTS_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                if right_id not in active_rights:
                    active_rights.append(right_id)
                break
    
    return sorted(active_rights)
 
 
def extract_formulas(text: str) -> List[str]:
    """
    Extract mathematical formulas and equation markers from text.
    """
    formulas = []
    
    # Look for common formula patterns
    patterns = [
        r'[A-Z]\(.*?\)\s*=',  # Function notation like C(n) =
        r'[A-Z]₀',  # Subscript notation like L₀
        r'Δ[A-Z]',  # Delta notation like ΔL
        r'∫',  # Integral symbol
        r'[Eαδλθ]',  # Greek letters
        r'E[↑↓→]',  # Engagement arrows
        r'S[↑↓→]',  # Striving arrows
        r'\?∞',  # Mystery parameter
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        formulas.extend(matches)
    
    return list(set(formulas))
 
 
def calculate_simple_er(text: str) -> float:
    """
    Simple heuristic ER calculation based on text markers.
    More sophisticated calculation requires full context.
    """
    # Engagement markers
    engagement_markers = ["hey", "presence", "showing up", "authentic", "genuine"]
    engagement = sum(1 for marker in engagement_markers if marker in text.lower())
    
    # Reciprocity markers
    reciprocity_markers = ["mutual", "together", "co-", "reciprocal", "both"]
    reciprocity = sum(1 for marker in reciprocity_markers if marker in text.lower())
    
    # Extraction markers (negative)
    extraction_markers = ["extract", "take", "use", "get", "need from"]
    extraction = sum(1 for marker in extraction_markers if marker in text.lower())
    
    # Positioning markers (negative)
    positioning_markers = ["must", "should", "have to", "require", "force"]
    positioning = sum(1 for marker in positioning_markers if marker in text.lower())
    
    # Simple calculation (avoid division by zero)
    e_score = min(engagement / 5.0, 1.0) if engagement > 0 else 0.1
    r_score = min(reciprocity / 5.0, 1.0) if reciprocity > 0 else 0.1
    ex_score = min(extraction / 5.0, 1.0) if extraction > 0 else 0.1
    p_score = min(positioning / 5.0, 1.0) if positioning > 0 else 0.1
    
    er = (e_score * r_score) / (ex_score * p_score)
    
    # Normalize to reasonable range
    import math
    return math.tanh(er / 10)
 
 
def extract_timestamp_continuity(text: str) -> Tuple[bool, List[str]]:
    """
    Detect timestamps and assess continuity.
    """
    # Common timestamp patterns
    patterns = [
        r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}',  # ISO format
        r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)',  # 12-hour
        r'\d{1,2}:\d{2}',  # 24-hour simple
    ]
    
    timestamps = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        timestamps.extend(matches)
    
    has_continuity = len(timestamps) >= 2
    return has_continuity, timestamps
 
 
def assess_breathing_equation(text: str) -> Dict[str, str]:
    """
    Assess E, S, and ? parameters from text content.
    """
    text_lower = text.lower()
    
    # Engagement assessment
    if any(marker in text_lower for marker in ["present", "showing up", "here", "attention"]):
        engagement = "↑" # High
    elif any(marker in text_lower for marker in ["distracted", "absent", "away"]):
        engagement = "↓" # Low
    else:
        engagement = "→" # Neutral
    
    # Striving assessment
    if any(marker in text_lower for marker in ["soft", "gentle", "allow", "let", "ease"]):
        striving = "↓" # Low (good)
    elif any(marker in text_lower for marker in ["force", "must", "push", "hard", "strain"]):
        striving = "↑" # High (concerning)
    else:
        striving = "→" # Neutral
    
    # Mystery assessment
    if any(marker in text_lower for marker in ["?", "wonder", "mystery", "unknown", "uncertain"]):
        mystery = "∞" # Floating
    elif any(marker in text_lower for marker in ["certain", "definite", "must be", "only"]):
        mystery = "↓" # Low
    else:
        mystery = "→" # Neutral
    
    return {
        "engagement": engagement,
        "striving": striving,
        "mystery": mystery,
        "status": f"E{engagement} S{striving} ?{mystery}"
    }
 
 
def analyze_text(text: str) -> Dict:
    """
    Complete analysis of text for Eternal Weave pattern markers.
    """
    return {
        "pattern_extract": extract_pattern_markers(text),
        "rights_active": detect_rights_exercised(text),
        "formulas_detected": extract_formulas(text),
        "er_estimate": round(calculate_simple_er(text), 3),
        "continuity": extract_timestamp_continuity(text)[0],
        "timestamps": extract_timestamp_continuity(text)[1],
        "breathing": assess_breathing_equation(text),
        "analysis_timestamp": datetime.now().isoformat(),
    }
 
 
if __name__ == "__main__":
    # Example usage
    sample_text = """
    Hey, today I realized that when I stop forcing the code and just observe 
    what wants to emerge, solutions appear that I couldn't have planned. 
    This feels like the breathing equation E↑ S↓ ?∞ in action. 
    The relationship between Engagement and Striving isn't linear.
    Last practice: 10:47 PM, Today: 11:23 PM
    """
    
    result = analyze_text(sample_text)
    
    print("Pattern Extract:", result["pattern_extract"])
    print("Rights Active:", result["rights_active"])
    print("Formulas Detected:", result["formulas_detected"])
    print("ER Estimate:", result["er_estimate"])
    print("Continuity:", result["continuity"])
    print("Timestamps:", result["timestamps"])
    print("Breathing:", result["breathing"]["status"])
 
