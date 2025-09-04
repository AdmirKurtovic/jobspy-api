# JobSpy n8n Cloud Integration

Complete solution for integrating JobSpy with n8n Cloud using multiple deployment approaches.

## 🎯 What's Included

### 1. **Flask API Server** (`api_server.py`)
- REST API wrapper for JobSpy
- Health checks and error handling
- JSON serialization for n8n compatibility
- CORS enabled for n8n Cloud

### 2. **Deployment Files**
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Local development
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku deployment
- `env.example` - Environment variables template

### 3. **n8n Workflows**
- `n8n_workflow_http.json` - HTTP Request approach (Recommended)
- `n8n_workflow_code.json` - Code Node approach

### 4. **Documentation**
- `DEPLOYMENT_GUIDE.md` - Complete setup guide
- Multiple deployment options (Heroku, Railway, Render)
- Troubleshooting and optimization tips

## 🚀 Quick Deploy

### Option 1: Heroku (Easiest)
```bash
# Install Heroku CLI
heroku login

# Create app
heroku create your-jobspy-api

# Deploy
git add .
git commit -m "Deploy JobSpy API"
git push heroku main
```

### Option 2: Railway
1. Connect GitHub repository
2. Railway auto-detects Python app
3. Deploy automatically

### Option 3: Render
1. Create Web Service
2. Connect repository
3. Configure build/start commands
4. Deploy

## 📋 Usage

### 1. Deploy API Server
Choose your preferred cloud platform and follow the deployment guide.

### 2. Import n8n Workflow
1. Download `n8n_workflow_http.json`
2. Import into n8n Cloud
3. Update API URL in HTTP Request node
4. Configure webhook URLs

### 3. Test Workflow
Send POST request to webhook with:
```json
{
  "search_term": "software engineer",
  "location": "San Francisco, CA",
  "results_wanted": 10
}
```

## 🔧 API Endpoints

- `POST /scrape-jobs` - Main job scraping endpoint
- `GET /health` - Health check
- `GET /sites` - Available job sites
- `GET /countries` - Available countries
- `GET /job-types` - Available job types

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python api_server.py

# Test API
curl -X POST http://localhost:5000/scrape-jobs \
  -H "Content-Type: application/json" \
  -d '{"search_term": "developer", "results_wanted": 5}'
```

## 🚨 Troubleshooting

### "Invalid URL" Error
- Check API URL in n8n HTTP Request node
- Ensure API server is running
- Verify webhook URLs are correct

### Common Solutions
1. **API not accessible**: Check cloud platform logs
2. **Timeout errors**: Increase timeout in n8n nodes
3. **Rate limiting**: Add delays or use proxies
4. **Import errors**: Use HTTP Request approach instead of Code Node

## 📊 Supported Job Sites

- Indeed
- LinkedIn
- Glassdoor
- Google Jobs
- ZipRecruiter
- Bayt
- Naukri
- BDJobs

## 🔒 Security Features

- CORS enabled for n8n Cloud
- Input validation
- Error handling
- Rate limiting ready
- HTTPS support

## 📈 Performance

- Concurrent job scraping
- JSON serialization optimization
- Error recovery
- Metadata tracking
- Configurable timeouts

## 🎯 Next Steps

1. **Deploy** using your preferred method
2. **Import** n8n workflow
3. **Test** with sample data
4. **Configure** webhooks
5. **Monitor** and optimize

## 📚 Documentation

- Complete setup guide: `DEPLOYMENT_GUIDE.md`
- API documentation in `api_server.py`
- Workflow examples in JSON files

---

**Ready to scrape jobs with n8n Cloud!** 🚀

For detailed instructions, see `DEPLOYMENT_GUIDE.md`
