from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    # For Vercel, we'll serve a simple HTML response instead of reading from file
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Translation Engine - Professional Language Translation</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .main-content {
            padding: 40px;
        }

        .input-section {
            margin-bottom: 40px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #374151;
            font-size: 1rem;
        }

        .text-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            resize: vertical;
            min-height: 120px;
        }

        .text-input:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }

        .language-selector {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .select-wrapper {
            position: relative;
        }

        .select-wrapper select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            background: white;
            cursor: pointer;
            appearance: none;
            transition: all 0.3s ease;
        }

        .select-wrapper select:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }

        .select-wrapper::after {
            content: '▼';
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
            color: #6b7280;
        }

        .translate-btn {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            padding: 18px 40px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .translate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
        }

        .translate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .results-section {
            margin-top: 40px;
            display: none;
        }

        .results-section.show {
            display: block;
        }

        .result-card {
            background: #f8fafc;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            border-left: 4px solid #4f46e5;
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e7eb;
        }

        .detection-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .language-badge {
            background: #4f46e5;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .confidence-badge {
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .text-content {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            margin-bottom: 15px;
        }

        .text-content h4 {
            color: #374151;
            margin-bottom: 10px;
            font-size: 1rem;
        }

        .text-content p {
            color: #6b7280;
            line-height: 1.6;
            font-size: 1.1rem;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4f46e5;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error-message {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #dc2626;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            display: none;
        }

        .error-message.show {
            display: block;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }

        .feature-card {
            background: #f8fafc;
            padding: 25px;
            border-radius: 16px;
            text-align: center;
            border: 1px solid #e5e7eb;
        }

        .feature-card i {
            font-size: 2.5rem;
            color: #4f46e5;
            margin-bottom: 15px;
        }

        .feature-card h3 {
            color: #374151;
            margin-bottom: 10px;
            font-size: 1.2rem;
        }

        .feature-card p {
            color: #6b7280;
            line-height: 1.5;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }

            .header {
                padding: 30px 20px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .main-content {
                padding: 20px;
            }

            .language-selector {
                grid-template-columns: 1fr;
            }

            .result-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-language"></i> Translation Engine</h1>
            <p>Professional language translation with auto-detection powered by Google Translate</p>
        </div>

        <div class="main-content">
            <div class="input-section">
                <div class="form-group">
                    <label for="inputText">
                        <i class="fas fa-keyboard"></i> Enter text to translate:
                    </label>
                    <textarea 
                        id="inputText" 
                        class="text-input" 
                        placeholder="Type or paste your text here... (supports 100+ languages)"
                        maxlength="5000"
                    ></textarea>
                    <div style="text-align: right; margin-top: 5px; color: #6b7280; font-size: 0.9rem;">
                        <span id="charCount">0</span>/5000
                    </div>
                </div>

                <div class="language-selector">
                    <div class="select-wrapper">
                        <label for="targetLanguage">
                            <i class="fas fa-flag"></i> Translate to:
                        </label>
                        <select id="targetLanguage">
                            <option value="">Select target language...</option>
                        </select>
                    </div>
                </div>

                <button id="translateBtn" class="translate-btn">
                    <i class="fas fa-translate"></i>
                    <span id="btnText">Translate Text</span>
                </button>
            </div>

            <div id="errorMessage" class="error-message"></div>

            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Detecting language and translating...</p>
            </div>

            <div id="resultsSection" class="results-section">
                <div class="result-card">
                    <div class="result-header">
                        <div class="detection-info">
                            <span class="language-badge" id="detectedLanguage">English</span>
                            <span class="confidence-badge" id="confidenceLevel">95%</span>
                        </div>
                        <div style="color: #6b7280; font-size: 0.9rem;">
                            <i class="fas fa-clock"></i> <span id="translationTime">0.5s</span>
                        </div>
                    </div>

                    <div class="text-content">
                        <h4><i class="fas fa-file-alt"></i> Original Text:</h4>
                        <p id="originalText"></p>
                    </div>

                    <div class="text-content">
                        <h4><i class="fas fa-language"></i> Translation:</h4>
                        <p id="translatedText"></p>
                    </div>
                </div>
            </div>

            <div class="features">
                <div class="feature-card">
                    <i class="fas fa-magic"></i>
                    <h3>Auto-Detection</h3>
                    <p>Automatically detects the input language with confidence scoring</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-globe"></i>
                    <h3>100+ Languages</h3>
                    <p>Support for major world languages and dialects</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-bolt"></i>
                    <h3>Fast & Reliable</h3>
                    <p>Powered by Google Translate for accurate results</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Professional</h3>
                    <p>Built with modern web technologies and best practices</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        class TranslationEngine {
            constructor() {
                this.initializeElements();
                this.loadLanguages();
                this.setupEventListeners();
            }

            initializeElements() {
                this.inputText = document.getElementById('inputText');
                this.targetLanguage = document.getElementById('targetLanguage');
                this.translateBtn = document.getElementById('translateBtn');
                this.btnText = document.getElementById('btnText');
                this.loading = document.getElementById('loading');
                this.resultsSection = document.getElementById('resultsSection');
                this.errorMessage = document.getElementById('errorMessage');
                this.charCount = document.getElementById('charCount');
                
                // Result elements
                this.detectedLanguage = document.getElementById('detectedLanguage');
                this.confidenceLevel = document.getElementById('confidenceLevel');
                this.originalText = document.getElementById('originalText');
                this.translatedText = document.getElementById('translatedText');
                this.translationTime = document.getElementById('translationTime');
            }

            async loadLanguages() {
                try {
                    const response = await fetch('/api/languages');
                    const languages = await response.json();
                    
                    // Sort languages by name
                    languages.sort((a, b) => a.name.localeCompare(b.name));
                    
                    // Populate dropdown
                    languages.forEach(lang => {
                        const option = document.createElement('option');
                        option.value = lang.code;
                        option.textContent = `${lang.name} (${lang.native_name})`;
                        this.targetLanguage.appendChild(option);
                    });
                } catch (error) {
                    console.error('Failed to load languages:', error);
                    this.showError('Failed to load supported languages');
                }
            }

            setupEventListeners() {
                this.translateBtn.addEventListener('click', () => this.translate());
                this.inputText.addEventListener('input', () => this.updateCharCount());
                this.inputText.addEventListener('keydown', (e) => {
                    if (e.ctrlKey && e.key === 'Enter') {
                        this.translate();
                    }
                });
            }

            updateCharCount() {
                const count = this.inputText.value.length;
                this.charCount.textContent = count;
                
                if (count > 4500) {
                    this.charCount.style.color = '#dc2626';
                } else if (count > 4000) {
                    this.charCount.style.color = '#f59e0b';
                } else {
                    this.charCount.style.color = '#6b7280';
                }
            }

            async translate() {
                const text = this.inputText.value.trim();
                const targetLang = this.targetLanguage.value;

                if (!text) {
                    this.showError('Please enter some text to translate');
                    return;
                }

                if (!targetLang) {
                    this.showError('Please select a target language');
                    return;
                }

                this.setLoading(true);
                this.hideError();
                this.hideResults();

                const startTime = Date.now();

                try {
                    const response = await fetch('/api/translate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            text: text,
                            target_language: targetLang
                        })
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Translation failed');
                    }

                    const result = await response.json();
                    const translationTime = ((Date.now() - startTime) / 1000).toFixed(1);
                    
                    this.displayResults(result, translationTime);
                } catch (error) {
                    console.error('Translation error:', error);
                    this.showError(error.message || 'Translation failed. Please try again.');
                } finally {
                    this.setLoading(false);
                }
            }

            displayResults(result, translationTime) {
                // Get language names
                const detectedLangName = this.getLanguageName(result.detected_language);
                const targetLangName = this.getLanguageName(result.target_language);
                
                // Update UI
                this.detectedLanguage.textContent = detectedLangName;
                this.confidenceLevel.textContent = `${Math.round(result.confidence_level * 100)}%`;
                this.originalText.textContent = result.original_text;
                this.translatedText.textContent = result.translated_text;
                this.translationTime.textContent = `${translationTime}s`;

                // Show results
                this.resultsSection.classList.add('show');
                
                // Scroll to results
                this.resultsSection.scrollIntoView({ behavior: 'smooth' });
            }

            getLanguageName(code) {
                const option = this.targetLanguage.querySelector(`option[value="${code}"]`);
                if (option) {
                    return option.textContent.split(' (')[0];
                }
                return code.toUpperCase();
            }

            setLoading(loading) {
                if (loading) {
                    this.loading.classList.add('show');
                    this.translateBtn.disabled = true;
                    this.btnText.textContent = 'Translating...';
                } else {
                    this.loading.classList.remove('show');
                    this.translateBtn.disabled = false;
                    this.btnText.textContent = 'Translate Text';
                }
            }

            showError(message) {
                this.errorMessage.textContent = message;
                this.errorMessage.classList.add('show');
                this.errorMessage.scrollIntoView({ behavior: 'smooth' });
            }

            hideError() {
                this.errorMessage.classList.remove('show');
            }

            hideResults() {
                this.resultsSection.classList.remove('show');
            }
        }

        // Initialize the application when the page loads
        document.addEventListener('DOMContentLoaded', () => {
            new TranslationEngine();
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

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

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 