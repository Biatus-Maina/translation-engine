from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import logging
from typing import Dict, List, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Initialize FastAPI app
app = FastAPI(
    title="Translation Engine",
    description="A professional translation service with auto-language detection",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    detected_language: str
    confidence_level: float
    translated_text: str
    target_language: str

class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str

# Supported languages mapping
SUPPORTED_LANGUAGES = {
    "af": {"name": "Afrikaans", "native_name": "Afrikaans"},
    "sq": {"name": "Albanian", "native_name": "Shqip"},
    "am": {"name": "Amharic", "native_name": "አማርኛ"},
    "ar": {"name": "Arabic", "native_name": "العربية"},
    "hy": {"name": "Armenian", "native_name": "Հայերեն"},
    "az": {"name": "Azerbaijani", "native_name": "Azərbaycan"},
    "eu": {"name": "Basque", "native_name": "Euskara"},
    "be": {"name": "Belarusian", "native_name": "Беларуская"},
    "bn": {"name": "Bengali", "native_name": "বাংলা"},
    "bs": {"name": "Bosnian", "native_name": "Bosanski"},
    "bg": {"name": "Bulgarian", "native_name": "Български"},
    "ca": {"name": "Catalan", "native_name": "Català"},
    "ceb": {"name": "Cebuano", "native_name": "Cebuano"},
    "zh": {"name": "Chinese (Simplified)", "native_name": "中文 (简体)"},
    "zh-TW": {"name": "Chinese (Traditional)", "native_name": "中文 (繁體)"},
    "co": {"name": "Corsican", "native_name": "Corsu"},
    "hr": {"name": "Croatian", "native_name": "Hrvatski"},
    "cs": {"name": "Czech", "native_name": "Čeština"},
    "da": {"name": "Danish", "native_name": "Dansk"},
    "nl": {"name": "Dutch", "native_name": "Nederlands"},
    "en": {"name": "English", "native_name": "English"},
    "eo": {"name": "Esperanto", "native_name": "Esperanto"},
    "et": {"name": "Estonian", "native_name": "Eesti"},
    "fi": {"name": "Finnish", "native_name": "Suomi"},
    "fr": {"name": "French", "native_name": "Français"},
    "fy": {"name": "Frisian", "native_name": "Frysk"},
    "gl": {"name": "Galician", "native_name": "Galego"},
    "ka": {"name": "Georgian", "native_name": "ქართული"},
    "de": {"name": "German", "native_name": "Deutsch"},
    "el": {"name": "Greek", "native_name": "Ελληνικά"},
    "gu": {"name": "Gujarati", "native_name": "ગુજરાતી"},
    "ht": {"name": "Haitian Creole", "native_name": "Kreyòl Ayisyen"},
    "ha": {"name": "Hausa", "native_name": "Hausa"},
    "haw": {"name": "Hawaiian", "native_name": "ʻŌlelo Hawaiʻi"},
    "he": {"name": "Hebrew", "native_name": "עברית"},
    "hi": {"name": "Hindi", "native_name": "हिन्दी"},
    "hmn": {"name": "Hmong", "native_name": "Hmong"},
    "hu": {"name": "Hungarian", "native_name": "Magyar"},
    "is": {"name": "Icelandic", "native_name": "Íslenska"},
    "ig": {"name": "Igbo", "native_name": "Igbo"},
    "id": {"name": "Indonesian", "native_name": "Indonesia"},
    "ga": {"name": "Irish", "native_name": "Gaeilge"},
    "it": {"name": "Italian", "native_name": "Italiano"},
    "ja": {"name": "Japanese", "native_name": "日本語"},
    "jv": {"name": "Javanese", "native_name": "Basa Jawa"},
    "kn": {"name": "Kannada", "native_name": "ಕನ್ನಡ"},
    "kk": {"name": "Kazakh", "native_name": "Қазақ"},
    "km": {"name": "Khmer", "native_name": "ខ្មែរ"},
    "ko": {"name": "Korean", "native_name": "한국어"},
    "ku": {"name": "Kurdish", "native_name": "Kurdî"},
    "ky": {"name": "Kyrgyz", "native_name": "Кыргызча"},
    "lo": {"name": "Lao", "native_name": "ລາວ"},
    "la": {"name": "Latin", "native_name": "Latina"},
    "lv": {"name": "Latvian", "native_name": "Latviešu"},
    "lt": {"name": "Lithuanian", "native_name": "Lietuvių"},
    "lb": {"name": "Luxembourgish", "native_name": "Lëtzebuergesch"},
    "mk": {"name": "Macedonian", "native_name": "Македонски"},
    "mg": {"name": "Malagasy", "native_name": "Malagasy"},
    "ms": {"name": "Malay", "native_name": "Bahasa Melayu"},
    "ml": {"name": "Malayalam", "native_name": "മലയാളം"},
    "mt": {"name": "Maltese", "native_name": "Malti"},
    "mi": {"name": "Maori", "native_name": "Māori"},
    "mr": {"name": "Marathi", "native_name": "मराठी"},
    "mn": {"name": "Mongolian", "native_name": "Монгол"},
    "my": {"name": "Myanmar (Burmese)", "native_name": "မြန်မာ (ဗမာ)"},
    "ne": {"name": "Nepali", "native_name": "नेपाली"},
    "no": {"name": "Norwegian", "native_name": "Norsk"},
    "ny": {"name": "Nyanja (Chichewa)", "native_name": "Nyanja (Chichewa)"},
    "or": {"name": "Odia (Oriya)", "native_name": "ଓଡ଼ିଆ (ଓଡ଼ିଆ)"},
    "ps": {"name": "Pashto", "native_name": "پښتو"},
    "fa": {"name": "Persian", "native_name": "فارسی"},
    "pl": {"name": "Polish", "native_name": "Polski"},
    "pt": {"name": "Portuguese", "native_name": "Português"},
    "pa": {"name": "Punjabi", "native_name": "ਪੰਜਾਬੀ"},
    "ro": {"name": "Romanian", "native_name": "Română"},
    "ru": {"name": "Russian", "native_name": "Русский"},
    "sm": {"name": "Samoan", "native_name": "Gagana Samoa"},
    "gd": {"name": "Scots Gaelic", "native_name": "Gàidhlig"},
    "sr": {"name": "Serbian", "native_name": "Српски"},
    "st": {"name": "Sesotho", "native_name": "Sesotho"},
    "sn": {"name": "Shona", "native_name": "Shona"},
    "sd": {"name": "Sindhi", "native_name": "سنڌي"},
    "si": {"name": "Sinhala (Sinhalese)", "native_name": "සිංහල"},
    "sk": {"name": "Slovak", "native_name": "Slovenčina"},
    "sl": {"name": "Slovenian", "native_name": "Slovenščina"},
    "so": {"name": "Somali", "native_name": "Soomaali"},
    "es": {"name": "Spanish", "native_name": "Español"},
    "su": {"name": "Sundanese", "native_name": "Basa Sunda"},
    "sw": {"name": "Swahili", "native_name": "Kiswahili"},
    "sv": {"name": "Swedish", "native_name": "Svenska"},
    "tg": {"name": "Tajik", "native_name": "Тоҷикӣ"},
    "ta": {"name": "Tamil", "native_name": "தமிழ்"},
    "tt": {"name": "Tatar", "native_name": "Татар"},
    "te": {"name": "Telugu", "native_name": "తెలుగు"},
    "th": {"name": "Thai", "native_name": "ไทย"},
    "tr": {"name": "Turkish", "native_name": "Türkçe"},
    "tk": {"name": "Turkmen", "native_name": "Türkmen"},
    "ak": {"name": "Twi", "native_name": "Twi"},
    "uk": {"name": "Ukrainian", "native_name": "Українська"},
    "ur": {"name": "Urdu", "native_name": "اردو"},
    "ug": {"name": "Uyghur", "native_name": "ئۇيغۇرچە"},
    "uz": {"name": "Uzbek", "native_name": "O'zbek"},
    "ve": {"name": "Venda", "native_name": "Tshivenda"},
    "vi": {"name": "Vietnamese", "native_name": "Tiếng Việt"},
    "cy": {"name": "Welsh", "native_name": "Cymraeg"},
    "xh": {"name": "Xhosa", "native_name": "isiXhosa"},
    "yi": {"name": "Yiddish", "native_name": "יידיש"},
    "yo": {"name": "Yoruba", "native_name": "Yorùbá"},
    "zu": {"name": "Zulu", "native_name": "isiZulu"}
}

def detect_language_with_confidence(text: str) -> tuple[str, float]:
    """
    Detect language with confidence level using multiple detection attempts
    """
    try:
        # Use langdetect for primary detection
        detected_lang = detect(text)
        
        # Simple confidence calculation based on text characteristics
        # This is a simplified approach - in production you might use more sophisticated methods
        confidence = min(0.95, 0.7 + (len(text) * 0.01))
        
        return detected_lang, confidence
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "en", 0.5  # Default fallback

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/languages", response_model=List[LanguageInfo])
async def get_supported_languages():
    """Get list of all supported languages"""
    languages = []
    for code, info in SUPPORTED_LANGUAGES.items():
        languages.append(LanguageInfo(
            code=code,
            name=info["name"],
            native_name=info["native_name"]
        ))
    return languages

@app.post("/api/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate text from detected language to target language"""
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if request.target_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Target language not supported")
        
        # Detect source language
        detected_lang, confidence = detect_language_with_confidence(request.text)
        
        # Don't translate if source and target are the same
        if detected_lang == request.target_language:
            return TranslationResponse(
                original_text=request.text,
                detected_language=detected_lang,
                confidence_level=confidence,
                translated_text=request.text,
                target_language=request.target_language
            )
        
        # Perform translation
        try:
            translator = GoogleTranslator(source=detected_lang, target=request.target_language)
            translated_text = translator.translate(request.text)
            
            if not translated_text:
                raise HTTPException(status_code=500, detail="Translation failed")
            
            return TranslationResponse(
                original_text=request.text,
                detected_language=detected_lang,
                confidence_level=confidence,
                translated_text=translated_text,
                target_language=request.target_language
            )
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            raise HTTPException(status_code=500, detail="Translation service error")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "translation-engine"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 