# n8n Integration Guide for JobSpy API

## 🚀 Quick Start

Your JobSpy API is deployed at: **https://jobspy-api-jlyc.onrender.com**

## 📋 Available Endpoints

### 1. **Job Scraping** (`/scrape-jobs`)
- **Method**: POST
- **Purpose**: Find job listings
- **Input**: `search_term`, `location`, `results_wanted`, `site_name`

### 2. **Company Research** (`/company-research`)
- **Method**: POST
- **Purpose**: Find company website and HR emails
- **Input**: `company_name`

### 3. **Email Finding** (`/find-emails`)
- **Method**: POST
- **Purpose**: Find company emails (same as company research)
- **Input**: `company_name`

## 🔧 n8n Setup Instructions

### Step 1: Import Workflows
1. **Download the workflow files**:
   - `n8n_company_research_workflow.json`
   - `n8n_job_scraping_workflow.json`

2. **Import into n8n**:
   - Go to your n8n instance
   - Click "Import from file"
   - Select the JSON files
   - Click "Import"

### Step 2: Activate Workflows
1. **Open each workflow**
2. **Click "Activate"** in the top right
3. **Copy the webhook URLs** for testing

## 🧪 Testing Your Workflows

### Test Company Research:
```bash
curl -X POST https://your-n8n-instance.com/webhook/company-research \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google"
  }'
```

### Test Job Scraping:
```bash
curl -X POST https://your-n8n-instance.com/webhook/job-scraping \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "software engineer",
    "location": "San Francisco, CA",
    "results_wanted": 5
  }'
```

## 📊 Workflow Details

### Company Research Workflow
**Input**: Company name
**Output**: 
- Company website
- HR emails
- General emails
- Social media links
- Company info (industry, size, location)

**n8n Nodes**:
1. **Webhook Trigger** - Receives company name
2. **HTTP Request** - Calls JobSpy API
3. **IF Node** - Checks for success
4. **Set Node** - Formats results
5. **Respond to Webhook** - Returns formatted data

### Job Scraping Workflow
**Input**: Search parameters
**Output**:
- Job listings
- Search summary
- Job count

**n8n Nodes**:
1. **Webhook Trigger** - Receives search parameters
2. **HTTP Request** - Calls JobSpy API
3. **IF Node** - Checks for success
4. **Set Node** - Formats results
5. **Respond to Webhook** - Returns formatted data

## 🔗 Direct API Usage

You can also use the API directly without n8n:

### Company Research:
```bash
curl -X POST https://jobspy-api-jlyc.onrender.com/company-research \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Microsoft"}'
```

### Job Scraping:
```bash
curl -X POST https://jobspy-api-jlyc.onrender.com/scrape-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "data scientist",
    "location": "New York, NY",
    "results_wanted": 10
  }'
```

## 🎯 Use Cases

### 1. **Lead Generation**
- Use company research to find HR contacts
- Automate outreach to potential employers

### 2. **Job Market Analysis**
- Scrape jobs to analyze market trends
- Track salary ranges and requirements

### 3. **Recruitment Automation**
- Find relevant job postings
- Research companies before applying

### 4. **Sales Prospecting**
- Find decision maker emails
- Research target companies

## 🛠️ Customization

### Modify API URL
If you deploy to a different URL, update the HTTP Request nodes:
1. **Open the workflow**
2. **Click on the HTTP Request node**
3. **Update the URL** to your new API endpoint
4. **Save and activate**

### Add More Parameters
You can add more input parameters by:
1. **Modifying the webhook trigger**
2. **Adding parameters to the HTTP Request body**
3. **Updating the response formatting**

## 📈 Monitoring

### Check API Status:
```bash
curl https://jobspy-api-jlyc.onrender.com/health
```

### View Available Endpoints:
```bash
curl https://jobspy-api-jlyc.onrender.com/
```

## 🚨 Troubleshooting

### Common Issues:
1. **API not responding** - Check if Render deployment is active
2. **Webhook not working** - Verify n8n workflow is activated
3. **Invalid JSON** - Check request format and parameters

### Debug Steps:
1. **Test API directly** with curl
2. **Check n8n execution logs**
3. **Verify webhook URLs** are correct
4. **Check API response** format

## 🎉 Success!

Your JobSpy API is now fully integrated with n8n! You can:
- ✅ **Scrape jobs** automatically
- ✅ **Research companies** for leads
- ✅ **Find HR emails** for outreach
- ✅ **Automate workflows** with n8n

Happy automating! 🚀
