# src/keyword_injector.py

# ৫০+ সাধারণ বাংলা শব্দ -> ইংরেজি ক্লিনিক্যাল টার্ম ডিকশনারি
MEDICAL_DICT = {
    # সাধারণ লক্ষণ (Symptoms)
    "জ্বর": "fever, pyrexia",
    "মাথা ব্যথা": "headache, cephalalgia",
    "মাথাব্যথা": "headache, cephalalgia",
    "বমি বমি ভাব": "nausea",
    "বমি": "vomiting, emesis",
    "কাশি": "cough, tussis",
    "কফ": "sputum, phlegm",
    "শ্বাসকষ্ট": "shortness of breath, dyspnea",
    "বুকে ব্যথা": "chest pain, angina",
    "পেট ব্যথা": "abdominal pain",
    "পাতলা পায়খানা": "diarrhea",
    "ডায়রিয়া": "diarrhea",
    "আমাশয়": "dysentery",
    "কোষ্ঠকাঠিন্য": "constipation",
    "গ্যাস্ট্রিক": "acidity, gastritis",
    "বুক জ্বালাপোড়া": "heartburn, dyspepsia",
    "মাথা ঘোরা": "dizziness, vertigo",
    "দুর্বলতা": "weakness, fatigue, asthenia",
    "ওজন কমা": "weight loss",
    "ওজন বাড়া": "weight gain, obesity",
    "চুলকানি": "itching, pruritus",
    "র্যাশ": "rash, erythema",
    "এলার্জি": "allergy, hypersensitivity",
    "ফুলে যাওয়া": "swelling, edema",
    "রক্তপাত": "bleeding, hemorrhage",
    "ঘা": "ulcer, lesion",
    "ব্যথা": "pain, myalgia",
    "গিরায় ব্যথা": "joint pain, arthralgia",
    "মাংসপেশিতে ব্যথা": "muscle pain, myalgia",
    "খিঁচুনি": "seizure, convulsion",
    "অজ্ঞান": "unconscious, syncope",
    "ঘুম না হওয়া": "insomnia",
    "অস্থিরতা": "restlessness, anxiety",
    
    # রোগ ও অবস্থা (Diseases & Conditions)
    "উচ্চ রক্তচাপ": "high blood pressure, hypertension",
    "প্রেসার": "blood pressure, hypertension",
    "সুগার": "blood sugar, diabetes mellitus",
    "ডায়াবেটিস": "diabetes mellitus",
    "জন্ডিস": "jaundice, icterus",
    "ম্যালেরিয়া": "malaria",
    "ডেঙ্গু": "dengue",
    "টাইফয়েড": "typhoid fever",
    "যক্ষ্মা": "tuberculosis, TB",
    "হাঁপানি": "asthma",
    "স্ট্রোক": "stroke, cerebrovascular accident",
    "হার্ট অ্যাটাক": "heart attack, myocardial infarction",
    "ক্যান্সার": "cancer, malignancy",
    "টিউমার": "tumor, neoplasm",
    "পাইলস": "piles, hemorrhoids",
    "থাইরয়েড": "thyroid disorder",
    "আলসার": "ulcer",
    "করোনা": "COVID-19, SARS-CoV-2",
    "নিউমোনিয়া": "pneumonia",
    "গর্ভবতী": "pregnant, pregnancy",
    "গর্ভাবস্থায়": "during pregnancy, maternal"
}

def inject_clinical_terms(bengali_query, translated_english_query):
    """
    বাংলা প্রশ্ন থেকে কিওয়ার্ড খুঁজে বের করে ইংরেজি অনুবাদের সাথে ক্লিনিক্যাল টার্ম যোগ করবে।
    """
    injected_terms = set()
    
    for bn_term, en_clinical in MEDICAL_DICT.items():
        if bn_term in bengali_query:
            injected_terms.add(en_clinical)
            
    if injected_terms:
        # ইংরেজি প্রশ্নের শেষে ক্লিনিক্যাল টার্মগুলো ব্র্যাকেটে যোগ করে দেওয়া হলো
        enhanced_query = f"{translated_english_query} (Clinical Context: {', '.join(injected_terms)})"
        return enhanced_query
        
    return translated_english_query