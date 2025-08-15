# Translation Engine

A professional FastAPI application that provides language translation services with automatic language detection. Built with modern web technologies and powered by Google Translate through the Deep-Translator library.

## Features

- 🌍 **Auto-Language Detection**: Automatically detects the input language with confidence scoring
- 🔄 **Multi-Language Support**: Translate to 100+ supported languages
- ⚡ **Fast Performance**: Built with FastAPI for high-performance API endpoints
- 🎨 **Modern UI**: Responsive, professional web interface
- 📱 **Mobile Friendly**: Optimized for all device sizes
- 🛡️ **Error Handling**: Comprehensive error handling and validation
- 📊 **Confidence Metrics**: Shows detection confidence levels
- 🚀 **RESTful API**: Clean, documented API endpoints

## Technology Stack

- **Backend**: FastAPI (Python)
- **Translation**: Deep-Translator with Google Translate
- **Language Detection**: langdetect library
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Translation-Engine
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## 🚀 Deployment

### Vercel Deployment (Recommended)

The application is optimized for Vercel deployment:

1. **Prepare for deployment:**
   ```bash
   python deploy-vercel.py
   ```

2. **Deploy to Vercel:**
   - Push to GitHub
   - Connect to Vercel
   - Automatic deployment

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed instructions.

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter the text you want to translate in the input field
3. Select your desired target language from the dropdown
4. Click "Translate Text" or press Ctrl+Enter
5. View the results including:
   - Detected source language
   - Confidence level
   - Original text
   - Translated text
   - Translation time

### API Endpoints

#### Translate Text
```http
POST /api/translate
Content-Type: application/json

{
    "text": "Hello, world!",
    "target_language": "es"
}
```

Response:
```json
{
    "original_text": "Hello, world!",
    "detected_language": "en",
    "confidence_level": 0.95,
    "translated_text": "¡Hola, mundo!",
    "target_language": "es"
}
```

#### Get Supported Languages
```http
GET /api/languages
```

Response:
```json
[
    {
        "code": "en",
        "name": "English",
        "native_name": "English"
    },
    {
        "code": "es",
        "name": "Spanish",
        "native_name": "Español"
    }
]
```

#### Health Check
```http
GET /api/health
```

Response:
```json
{
    "status": "healthy",
    "service": "translation-engine"
}
```

## Supported Languages

The application supports 100+ languages including:

- **European Languages**: English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Czech, Hungarian, Romanian, Bulgarian, Greek, Turkish, Ukrainian, and many more.

- **Asian Languages**: Chinese (Simplified & Traditional), Japanese, Korean, Thai, Vietnamese, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Persian, Arabic, Hebrew, and more.

- **African Languages**: Swahili, Hausa, Yoruba, Zulu, Xhosa, Afrikaans, Amharic, and others.

- **Other Languages**: Latin, Esperanto, Hawaiian, Maori, and many indigenous languages.

## Project Structure

```
Translation-Engine/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application and endpoints
├── static/
│   └── index.html       # Frontend web interface
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore file
```

## Configuration

### Environment Variables

The application can be configured using environment variables:

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

### Customization

You can customize the application by:

1. **Adding new languages**: Modify the `SUPPORTED_LANGUAGES` dictionary in `app/main.py`
2. **Changing the UI theme**: Modify the CSS in `static/index.html`
3. **Adding new features**: Extend the FastAPI endpoints in `app/main.py`

## Development

### Running in Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload when code changes are detected.

### Code Quality

The application follows Python best practices:

- Type hints for all functions
- Comprehensive error handling
- Logging for debugging
- Pydantic models for data validation
- Clean code structure and documentation

## Performance

- **Language Detection**: Uses langdetect library for fast and accurate detection
- **Translation**: Leverages Google Translate through Deep-Translator
- **API Response**: Optimized for minimal latency
- **Frontend**: Lightweight vanilla JavaScript with no heavy frameworks

## Error Handling

The application includes comprehensive error handling:

- Input validation
- Network error handling
- Translation service fallbacks
- User-friendly error messages
- Detailed logging for debugging

## Security

- CORS middleware for cross-origin requests
- Input sanitization and validation
- Rate limiting considerations (can be added)
- Secure headers (can be enhanced)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support and questions:

1. Check the API documentation at `/docs`
2. Review the error logs
3. Open an issue on the repository

## Roadmap

Future enhancements planned:

- [ ] User authentication and history
- [ ] Batch translation support
- [ ] Translation memory and suggestions
- [ ] Advanced language detection algorithms
- [ ] API rate limiting and quotas
- [ ] Docker containerization
- [ ] Kubernetes deployment support
- [ ] Performance monitoring and metrics
- [ ] Multi-language UI support
- [ ] Offline translation capabilities

---

**Built with ❤️ using FastAPI and modern web technologies** 