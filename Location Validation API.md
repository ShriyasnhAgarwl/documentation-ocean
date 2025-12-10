# Location Validation API - Quick Reference

## 🚀 API Endpoints

### 1. Validate Location
**POST** `/agent/validate-location`

```bash
curl --location --request POST 'http://localhost:2021/agent/validate-location' \
--header 'Content-Type: application/json' \
--header 'token: YOUR_AGENT_TOKEN' \
--data-raw '{
    "requestId": "REQ123456",
    "checkList": "aadhaarOcr",
    "gps": {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "accuracy": 20
    },
    "deviceInfo": {
        "userAgent": "Mozilla/5.0...",
        "platform": "Win32",
        "timezone": "Asia/Kolkata",
        "language": "en-US"
    }
}'
```

### 2. Get Location Audits
**GET** `/agent/location-audits/:requestId`

```bash
curl --location --request GET 'http://localhost:2021/agent/location-audits/REQ123456' \
--header 'Content-Type: application/json' \
--header 'token: YOUR_AGENT_TOKEN'
```

---

## 📋 Valid checkList Values

- `aadhaarOcr`
- `panOcr`
- `drivingLicenseOcr`
- `faceMatch`
- `signatureOcr`
- `otpOcr`

---

## ✅ Success Response Examples

### PASSED (< 200m)
```json
{
    "code": 100,
    "message": "Location validated successfully",
    "deviation": "150",
    "validationStatus": "PASSED"
}
```

### WARNING (200m - 400m)
```json
{
    "code": 100,
    "message": "Location deviation is 350m (above threshold but within tolerance)",
    "deviation": "350",
    "validationStatus": "WARNING"
}
```

### FAILED (> 400m)
```json
{
    "code": 403,
    "message": "Location mismatch detected: 5000m deviation exceeds 200m threshold",
    "deviation": "5000"
}
```

---

## 🔑 Configuration

Add to `.env`:
```
GOOGLE_GEOLOCATION_API_KEY=your_api_key_here
```

Get API key: https://console.cloud.google.com/

---

## 📊 MongoDB Queries

```javascript
// Find all audits for a request
db.locationAudits.find({ requestId: "REQ123456" })

// Find failed validations
db.locationAudits.find({ validationStatus: "FAILED" })

// Average deviation
db.locationAudits.aggregate([
    { $group: { _id: null, avgDeviation: { $avg: "$deviation" } } }
])
```
