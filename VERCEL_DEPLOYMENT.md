# 🚀 Vercel Deployment Guide

This guide will walk you through deploying your Translation Engine FastAPI application on Vercel.

## 🌟 Why Vercel?

- ✅ **Serverless Functions** - Automatic scaling
- ✅ **Global CDN** - Fast worldwide access
- ✅ **Easy Deployment** - Connect your GitHub repo
- ✅ **Free Tier** - Generous free hosting
- ✅ **Automatic HTTPS** - SSL certificates included

## 📋 Prerequisites

1. **GitHub Repository** - Your code must be on GitHub
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **Python 3.9+** - Vercel supports Python 3.9, 3.10, 3.11

## 🔧 Preparation Steps

### **Step 1: Update Requirements**
Make sure your `requirements.txt` has specific versions:
```txt
fastapi==0.104.1
uvicorn==0.24.0
deep-translator==1.11.4
python-multipart==0.0.6
pydantic==2.5.0
langdetect==1.0.9
python-dotenv==1.0.0
requests==2.31.0
```

### **Step 2: Verify Vercel Configuration**
Ensure you have `vercel.json` in your root directory:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ],
  "functions": {
    "app/main.py": {
      "runtime": "python3.9"
    }
  },
  "env": {
    "PYTHONPATH": "."
  }
}
```

### **Step 3: Check Application Structure**
Your project should look like this:
```
Translation-Engine/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main FastAPI app
│   └── main_vercel.py       # Vercel-optimized version
├── static/
│   └── index.html           # Frontend (optional for Vercel)
├── requirements.txt          # Dependencies
├── vercel.json              # Vercel configuration
└── README.md
```

## 🚀 Deployment Methods

### **Method 1: GitHub Integration (Recommended)**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect it's a Python project

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (Vercel auto-detects)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live!

### **Method 2: Vercel CLI**

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Follow the prompts**
   - Link to existing project or create new
   - Set project name
   - Confirm deployment

## ⚙️ Configuration Options

### **Environment Variables**
Add these in your Vercel project settings if needed:
```bash
PYTHONPATH=.
DEBUG=false
```

### **Custom Domain**
1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### **Function Configuration**
You can customize function settings in `vercel.json`:
```json
{
  "functions": {
    "app/main.py": {
      "runtime": "python3.9",
      "maxDuration": 30
    }
  }
}
```

## 🔍 Troubleshooting

### **Build Errors**

#### **Python Version Issues**
```json
{
  "functions": {
    "app/main.py": {
      "runtime": "python3.9"
    }
  }
}
```

#### **Import Errors**
Make sure your `PYTHONPATH` is set correctly:
```json
{
  "env": {
    "PYTHONPATH": "."
  }
}
```

#### **Dependency Issues**
- Check `requirements.txt` has correct versions
- Ensure all imports are available
- Test locally before deploying

### **Runtime Errors**

#### **Function Timeout**
Increase max duration in `vercel.json`:
```json
{
  "functions": {
    "app/main.py": {
      "maxDuration": 60
    }
  }
}
```

#### **Memory Issues**
Some packages might be too large. Consider:
- Using lighter alternatives
- Optimizing imports
- Breaking into smaller functions

## 📊 Monitoring & Analytics

### **Vercel Dashboard**
- **Functions**: Monitor serverless function performance
- **Analytics**: Track usage and performance
- **Logs**: View function execution logs

### **Performance Metrics**
- **Cold Start Time**: First request latency
- **Execution Time**: Function runtime
- **Memory Usage**: Function memory consumption

## 🔄 Continuous Deployment

### **Automatic Deploys**
- Every push to `main` branch triggers deployment
- Preview deployments for pull requests
- Automatic rollback on failed deployments

### **Branch Deployments**
- `main` → Production
- `develop` → Preview
- Feature branches → Preview URLs

## 🚀 Post-Deployment

### **Test Your App**
1. **Health Check**: `https://your-app.vercel.app/api/health`
2. **Languages**: `https://your-app.vercel.app/api/languages`
3. **Translation**: Test the web interface

### **Monitor Performance**
- Check Vercel dashboard for metrics
- Monitor function execution times
- Watch for any errors in logs

### **Optimize**
- Identify slow functions
- Optimize dependencies
- Consider caching strategies

## 💡 Best Practices

### **Code Optimization**
- Minimize cold start time
- Use async/await properly
- Optimize imports

### **Dependencies**
- Keep requirements.txt minimal
- Use specific versions
- Test locally before deploying

### **Error Handling**
- Implement proper error responses
- Log errors appropriately
- Provide user-friendly messages

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Serverless Functions](https://vercel.com/docs/serverless-functions)
- [Deployment Guide](https://vercel.com/guides/deploying-python-with-vercel)

## 🎉 Success!

Once deployed, your Translation Engine will be available at:
- **Production**: `https://your-app.vercel.app`
- **API**: `https://your-app.vercel.app/api/*`
- **Docs**: `https://your-app.vercel.app/docs`

Your app will automatically scale and handle traffic worldwide! 🌍✨

---

**Need help?** Check the Vercel documentation or community forums for support. 