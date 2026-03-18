"""Hindi translations for KG metadata and UI labels.

Used by the retriever (Hindi→English field mapping) and generator
(English→Hindi context labels) without modifying the KG schema.
"""

# ── Disability categories ─────────────────────────────────────────
DISABILITY_HI = {
    "visual": "दृष्टि बाधित",
    "hearing": "श्रवण बाधित",
    "locomotor": "चलने-फिरने की अक्षमता",
    "intellectual": "बौद्धिक अक्षमता",
    "mental_illness": "मानसिक बीमारी",
    "cerebral_palsy": "सेरेब्रल पाल्सी",
    "autism": "ऑटिज़्म",
    "multiple": "बहु-विकलांगता",
    "speech": "वाक् और भाषा अक्षमता",
    "specific_learning": "विशिष्ट अधिगम अक्षमता",
    "acid_attack": "तेज़ाब हमले से पीड़ित",
    "muscular_dystrophy": "मस्कुलर डिस्ट्रॉफी",
    "chronic_neurological": "पुरानी तंत्रिका संबंधी बीमारी",
    "thalassemia": "थैलेसीमिया / रक्त विकार",
}

# ── States ────────────────────────────────────────────────────────
STATE_HI = {
    "all_india": "पूरे भारत में",
    "karnataka": "कर्नाटक",
    "maharashtra": "महाराष्ट्र",
    "tamil_nadu": "तमिल नाडु",
    "delhi": "दिल्ली",
    "uttar_pradesh": "उत्तर प्रदेश",
    "west_bengal": "पश्चिम बंगाल",
    "rajasthan": "राजस्थान",
    "madhya_pradesh": "मध्य प्रदेश",
    "kerala": "केरल",
    "odisha": "ओडिशा",
    "andhra_pradesh": "आंध्र प्रदेश",
    "telangana": "तेलंगाना",
    "gujarat": "गुजरात",
    "himachal_pradesh": "हिमाचल प्रदेश",
    "bihar": "बिहार",
    "punjab": "पंजाब",
}

# ── Document types ────────────────────────────────────────────────
DOCUMENT_TYPE_HI = {
    "disability_cert": "विकलांगता प्रमाण पत्र",
    "income_cert": "आय प्रमाण पत्र",
    "age_proof": "आयु प्रमाण",
    "aadhaar": "आधार कार्ड",
    "bank_account": "बैंक खाता विवरण",
    "photo": "पासपोर्ट फ़ोटो",
    "residence_proof": "निवास प्रमाण पत्र",
    "bpl_card": "BPL कार्ड",
    "medical_cert": "चिकित्सा प्रमाण पत्र",
}

# ── Scheme names ──────────────────────────────────────────────────
SCHEME_NAME_HI = {
    "adip": "ADIP योजना — विकलांग व्यक्तियों को सहायक उपकरण",
    "ddrs": "DDRS — दीनदयाल विकलांग पुनर्वास योजना",
    "niramaya": "निरामय स्वास्थ्य बीमा योजना",
    "scholarship_pre_matric": "प्री-मैट्रिक छात्रवृत्ति (विकलांग छात्र)",
    "scholarship_post_matric": "पोस्ट-मैट्रिक छात्रवृत्ति (विकलांग छात्र)",
    "nhfdc_loan": "NHFDC ऋण योजना",
    "sipda": "SIPDA — विकलांगजन अधिनियम कार्यान्वयन योजना",
    "early_intervention": "ज़िला शीघ्र हस्तक्षेप केंद्र",
}

# ── Age groups (keyed by English label as stored in KG) ───────────
AGE_GROUP_HI = {
    "Early childhood (0-5)": "शिशु अवस्था (0-5 वर्ष)",
    "School age (6-14)": "स्कूल आयु (6-14 वर्ष)",
    "Children (6-18)": "बच्चे (6-18 वर्ष)",
    "Youth (15-25)": "युवा (15-25 वर्ष)",
    "Working age (18-60)": "कामकाजी आयु (18-60 वर्ष)",
    "All ages (0-100)": "सभी आयु (0-100 वर्ष)",
}

# ── Income levels ─────────────────────────────────────────────────
INCOME_LEVEL_HI = {
    "bpl": "गरीबी रेखा से नीचे",
    "low_income": "कम आय (< ₹1.5 लाख)",
    "ews": "आर्थिक रूप से कमजोर वर्ग (< ₹2.5 लाख)",
    "mid_income": "मध्यम आय (< ₹6 लाख)",
    "no_limit": "कोई आय सीमा नहीं",
}

# ── Context builder labels ────────────────────────────────────────
CONTEXT_LABELS_HI = {
    "Eligible Schemes (from Knowledge Graph)": "पात्र योजनाएं (Knowledge Graph से)",
    "Ministry": "मंत्रालय",
    "Benefit": "लाभ",
    "Covers": "विकलांगता प्रकार",
    "Age groups": "आयु वर्ग",
    "Required documents": "आवश्यक दस्तावेज़",
    "Source": "स्रोत",
    "KG-confirmed": "KG-सत्यापित",
}

# ── Disclaimer ────────────────────────────────────────────────────
DISCLAIMER_HI = (
    "⚠️ अस्वीकरण: यह जानकारी केवल मार्गदर्शन के लिए है। पात्रता और लाभ बदल सकते हैं। "
    "कृपया अपने निकटतम ज़िला विकलांगता पुनर्वास केंद्र (DDRC) से सत्यापित करें "
    "या नवीनतम आधिकारिक जानकारी के लिए https://disabilityaffairs.gov.in पर जाएं।"
)


def detect_hindi(text: str) -> bool:
    """Check if text contains Devanagari script characters (U+0900–U+097F)."""
    return any("\u0900" <= c <= "\u097F" for c in text)
