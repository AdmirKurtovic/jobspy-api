# JobSpy API Valid Parameters

## ✅ **Valid Location Values**
- `"Remote"` - Remote jobs worldwide
- `"United States"` - Jobs in the US
- `"Canada"` - Jobs in Canada
- `"United Kingdom"` - Jobs in the UK
- `"Germany"` - Jobs in Germany
- `"France"` - Jobs in France
- `"Australia"` - Jobs in Australia
- `"Worldwide"` - Jobs worldwide (may not work with all sites)

## ✅ **Valid Country Codes (country_indeed)**
- `"usa"` or `"us"` - United States
- `"canada"` - Canada
- `"uk"` or `"united kingdom"` - United Kingdom
- `"germany"` - Germany
- `"france"` - France
- `"australia"` - Australia
- `"worldwide"` - Worldwide search

## ❌ **Invalid Values (Will Cause 500 Errors)**
- `"jordan"` - Not a valid country
- `"Worldwide"` - May not work with all job sites
- `"worldwide"` - Inconsistent casing

## 🎯 **Recommended Combinations**

### For Remote Jobs:
```json
{
  "location": "Remote",
  "country_indeed": "usa",
  "is_remote": true
}
```

### For US Jobs:
```json
{
  "location": "United States",
  "country_indeed": "usa",
  "is_remote": false
}
```

### For Canadian Jobs:
```json
{
  "location": "Canada",
  "country_indeed": "canada",
  "is_remote": false
}
```

## 🔧 **Testing Your Parameters**

Use this curl command to test:
```bash
curl -X POST https://579a981d74db.ngrok-free.app/scrape-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Product Designer",
    "location": "Remote",
    "is_remote": true,
    "results_wanted": 3,
    "site_name": ["indeed"],
    "country_indeed": "usa"
  }'
```

## 📝 **Updated Workflow**

The `n8n_apply_pipeline_fixed.json` now uses:
- `location: "Remote"` ✅
- `country_indeed: "usa"` ✅

This should eliminate the 500 errors you were seeing!




