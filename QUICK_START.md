# 🚀 Quick Start Guide

Get your Translation Engine up and running in minutes!

## ⚡ Quick Start (Windows)

1. **Double-click `start.bat`** - This will activate the virtual environment and start the server automatically

2. **Open your browser** and go to: http://localhost:8000

3. **Start translating!** 🎉

## 🐍 Quick Start (Python)

1. **Open a terminal/command prompt** in this directory

2. **Run the startup script:**
   ```bash
   python start.py
   ```

3. **Open your browser** and go to: http://localhost:8000

## 🔧 Virtual Environment Management

**First time setup:**
```bash
python manage_venv.py
```

**Activate virtual environment manually:**
- **Windows:** `venv\Scripts\activate.bat`
- **macOS/Linux:** `source venv/bin/activate`

**Deactivate:** `deactivate`

## 🌐 What You'll See

- **Beautiful web interface** with modern design
- **100+ supported languages** in organized dropdowns
- **Auto-language detection** with confidence scoring
- **Real-time translation** powered by Google Translate
- **Professional API** with automatic documentation

## 🔧 Manual Setup (if needed)

1. **Install Python 3.8+** if you don't have it
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📱 Features at a Glance

- ✅ **Auto-language detection** - No need to specify source language
- ✅ **Confidence scoring** - See how sure the system is about detection
- ✅ **100+ languages** - From English to Zulu, Arabic to Japanese
- ✅ **Modern UI** - Responsive design that works on all devices
- ✅ **Fast API** - Built with FastAPI for high performance
- ✅ **Error handling** - Comprehensive validation and user feedback

## 🧪 Test the System

Run the demo to see all features in action:
```bash
python demo.py
```

## 📚 API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## 🆘 Need Help?

- Check the full README.md for detailed information
- Run `python test_app.py` to verify everything works
- The web interface includes helpful error messages

---

**Ready to translate the world? Start with `start.bat` or `python start.py`!** 🌍✨ 