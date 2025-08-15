# 🔧 Virtual Environment Setup Guide

This guide explains how to set up and manage the virtual environment for the Translation Engine project.

## 🌟 What is a Virtual Environment?

A virtual environment is an isolated Python environment that:
- ✅ **Isolates project dependencies** from your system Python
- ✅ **Prevents conflicts** between different projects
- ✅ **Makes projects portable** and reproducible
- ✅ **Keeps your system clean** from unnecessary packages

## 🚀 Automatic Setup (Recommended)

### **Option 1: Use the Management Script**
```bash
python manage_venv.py
```
This script will:
- Check Python version compatibility
- Create the virtual environment
- Install all dependencies
- Test the installation
- Provide usage instructions

### **Option 2: Use the Startup Scripts**
- **Windows:** Double-click `start.bat` (automatically activates venv)
- **Python:** Run `python start.py` (interactive setup)

## 🔧 Manual Setup

### **Step 1: Create Virtual Environment**
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### **Step 2: Activate Virtual Environment**
```bash
# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

**You'll know it's activated when you see `(venv)` in your prompt**

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Verify Installation**
```bash
python -c "import fastapi, uvicorn, deep_translator, langdetect; print('✅ All packages imported successfully!')"
```

## 📁 Virtual Environment Structure

```
venv/
├── Scripts/              # Windows executables
│   ├── python.exe       # Python interpreter
│   ├── pip.exe          # Package installer
│   ├── activate.bat     # Activation script
│   └── ...              # Other tools
├── bin/                  # Unix/Linux executables
├── Lib/                  # Installed packages
├── Include/              # Header files
└── pyvenv.cfg           # Configuration file
```

## 🎯 Common Commands

### **Activation**
```bash
# Windows
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### **Deactivation**
```bash
deactivate
```

### **Check if Activated**
```bash
# Look for (venv) in your prompt
# Or check Python path
python -c "import sys; print(sys.executable)"
```

### **Install Packages**
```bash
# Make sure venv is activated first
pip install package_name
```

### **List Installed Packages**
```bash
pip list
```

### **Update pip**
```bash
python -m pip install --upgrade pip
```

## 🧪 Testing Your Setup

### **Test Package Imports**
```bash
python -c "import fastapi, uvicorn, deep_translator, langdetect; print('✅ Success!')"
```

### **Test the Application**
```bash
# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, test the API
python test_app.py
```

### **Run the Demo**
```bash
python demo.py
```

## 🚨 Troubleshooting

### **Virtual Environment Not Found**
```bash
# Recreate the environment
rmdir /s venv          # Windows
rm -rf venv            # macOS/Linux
python -m venv venv    # Recreate
```

### **Dependencies Installation Failed**
```bash
# Update pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt

# If still failing, try individual packages
pip install fastapi uvicorn deep-translator langdetect
```

### **Permission Errors (macOS/Linux)**
```bash
# Use sudo if needed
sudo python3 -m venv venv
```

### **Python Version Issues**
```bash
# Check Python version
python --version

# Make sure you have Python 3.8+
# Install from python.org if needed
```

## 🔄 Updating Dependencies

### **Update All Packages**
```bash
# Activate venv first
pip install --upgrade -r requirements.txt
```

### **Update Individual Packages**
```bash
pip install --upgrade fastapi uvicorn
```

### **Check for Updates**
```bash
pip list --outdated
```

## 📱 IDE Integration

### **VS Code**
1. Open the project folder
2. Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (macOS)
3. Type "Python: Select Interpreter"
4. Choose the interpreter from `venv/Scripts/python.exe` (Windows) or `venv/bin/python` (macOS/Linux)

### **PyCharm**
1. Go to File → Settings → Project → Python Interpreter
2. Click the gear icon → Add
3. Choose "Existing Environment"
4. Select the Python executable from your venv

### **Jupyter Notebook**
```bash
# Install jupyter in your venv
pip install jupyter

# Launch jupyter
jupyter notebook
```

## 🎉 Success Indicators

Your virtual environment is properly set up when:
- ✅ You see `(venv)` in your command prompt
- ✅ `python -c "import fastapi"` runs without errors
- ✅ The server starts with `python -m uvicorn app.main:app --reload`
- ✅ You can access http://localhost:8000 in your browser

## 🔗 Quick Reference

| Action | Windows | macOS/Linux |
|--------|---------|-------------|
| **Create** | `python -m venv venv` | `python3 -m venv venv` |
| **Activate** | `venv\Scripts\activate.bat` | `source venv/bin/activate` |
| **Deactivate** | `deactivate` | `deactivate` |
| **Install** | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| **Test** | `python test_app.py` | `python test_app.py` |

---

**🎯 Pro Tip:** Always activate your virtual environment before running any Python commands or scripts!

**Need help?** Run `python manage_venv.py` for automatic setup and troubleshooting. 