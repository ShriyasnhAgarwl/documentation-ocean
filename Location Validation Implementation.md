# 🎯 Location Validation Implementation - Quick Start Guide

## ✅ What We've Implemented (Frontend)

### 1. **API Endpoints Added** ✓
File: `src/Base/AgentConfig.js`
```javascript
export const validateLocation = "/agent/validate-location";
export const getLocationAudits = "/agent/location-audits/";
```

### 2. **Location Validator Utility** ✓
File: `src/VideoKycAgent/Utils/LocationValidator.js`
- `validateLocationWithBackend()` - Validates GPS + IP location
- `getLocationAuditLogs()` - Retrieves audit logs
- Fail-open strategy for better UX

### 3. **Enhanced Geolocation** ✓
Updated in: `AadhaarCheck.js` (Example implementation)
- Stores GPS accuracy
- Validates location before OCR upload
- Shows error if deviation > 200m
- Shows warning if validation service unavailable

### 4. **Integration Example** ✓
File: `src/VideoKycAgent/Calls/MeetingVerification/AadhaarCheck.js`
- Added `accuracy` state
- Calls `validateLocationWithBackend()` before upload
- Handles validation failures gracefully

---

## 🔧 What You Need to Do (Backend)

### Step 1: Install Dependencies
```bash
# If not already installed
npm install axios mongoose
```

### Step 2: Get Google API Key
1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable **"Geolocation API"**
4. Create credentials (API Key)
5. Restrict API key to Geolocation API only
6. Add to your `.env` file:
```env
GOOGLE_GEOLOCATION_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3: Create Database Model
Create: `models/LocationAudit.js`

```javascript
const mongoose = require('mongoose');

const locationAuditSchema = new mongoose.Schema({
    requestId: { type: String, required: true, index: true },
    checkList: { 
        type: String, 
        required: true,
        enum: ['aadhaarOcr', 'panOcr', 'drivingLicenseOcr', 'faceMatch', 'signatureOcr', 'otpOcr']
    },
    gpsLocation: {
        latitude: { type: Number, required: true },
        longitude: { type: Number, required: true },
        accuracy: { type: Number }
    },
    googleLocation: {
        latitude: { type: Number },
        longitude: { type: Number },
        accuracy: { type: Number }
    },
    ipAddress: { type: String, required: true },
    deviation: { type: Number, required: true },
    deviceInfo: {
        userAgent: String,
        platform: String,
        timezone: String,
        language: String,
        screenResolution: String
    },
    validationStatus: {
        type: String,
        enum: ['PASSED', 'FAILED', 'WARNING'],
        required: true
    },
    failureReason: String,
    timestamp: { type: Date, default: Date.now, index: true }
}, { timestamps: true });

locationAuditSchema.index({ requestId: 1, timestamp: -1 });
locationAuditSchema.index({ validationStatus: 1, timestamp: -1 });

module.exports = mongoose.model('LocationAudit', locationAuditSchema);
```

### Step 4: Create Utility Functions
Create: `utils/locationUtils.js`

```javascript
const axios = require('axios');

// Calculate distance using Haversine formula
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371e3; // Earth's radius in meters
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return R * c; // Distance in meters
}

// Get location from Google Geolocation API
async function getGoogleGeolocation(ipAddress) {
    const GOOGLE_API_KEY = process.env.GOOGLE_GEOLOCATION_API_KEY;

    if (!GOOGLE_API_KEY) {
        throw new Error('GOOGLE_GEOLOCATION_API_KEY not configured');
    }

    try {
        const response = await axios.post(
            `https://www.googleapis.com/geolocation/v1/geolocate?key=${GOOGLE_API_KEY}`,
            { considerIp: true }
        );

        return {
            latitude: response.data.location.lat,
            longitude: response.data.location.lng,
            accuracy: response.data.accuracy
        };
    } catch (error) {
        console.error('Google Geolocation API error:', error.response?.data || error.message);
        throw new Error('Failed to get Google geolocation');
    }
}

// Validate deviation
function validateDeviation(deviation, threshold = 200) {
    if (deviation <= threshold) {
        return { status: 'PASSED', message: 'Location validated successfully' };
    } else if (deviation <= threshold * 2) {
        return { 
            status: 'WARNING', 
            message: `Location deviation is ${deviation.toFixed(0)}m (above threshold but within tolerance)` 
        };
    } else {
        return { 
            status: 'FAILED', 
            message: `Location mismatch: ${deviation.toFixed(0)}m deviation exceeds ${threshold}m threshold` 
        };
    }
}

module.exports = { calculateDistance, getGoogleGeolocation, validateDeviation };
```

### Step 5: Create Controller
Create: `controllers/locationValidation.js`

```javascript
const LocationAudit = require('../models/LocationAudit');
const { calculateDistance, getGoogleGeolocation, validateDeviation } = require('../utils/locationUtils');

async function validateLocation(req, res) {
    try {
        const { requestId, checkList, gps, deviceInfo } = req.body;

        // Validation
        if (!requestId || !checkList || !gps || !gps.latitude || !gps.longitude) {
            return res.status(400).json({
                code: 400,
                message: 'Missing required fields: requestId, checkList, gps (latitude, longitude)'
            });
        }

        // Get client IP
        const ipAddress = req.headers['x-forwarded-for']?.split(',')[0] || 
                         req.connection.remoteAddress || 
                         req.socket.remoteAddress;

        console.log(`[Location Validation] RequestId: ${requestId}, CheckList: ${checkList}, IP: ${ipAddress}`);

        let googleLocation = null;
        let deviation = 0;
        let validationResult = null;

        try {
            // Get Google's IP-based geolocation
            googleLocation = await getGoogleGeolocation(ipAddress);

            // Calculate deviation
            deviation = calculateDistance(
                gps.latitude, gps.longitude,
                googleLocation.latitude, googleLocation.longitude
            );

            // Validate deviation (200m threshold)
            validationResult = validateDeviation(deviation, 200);

            console.log(`[Location Validation] Deviation: ${deviation.toFixed(0)}m, Status: ${validationResult.status}`);

        } catch (googleError) {
            console.error('[Location Validation] Google API failed:', googleError.message);
            
            // Fallback: Accept GPS without validation
            validationResult = {
                status: 'WARNING',
                message: 'Location validated using GPS only (Google API unavailable)'
            };
        }

        // Store audit log
        const auditLog = new LocationAudit({
            requestId,
            checkList,
            gpsLocation: {
                latitude: gps.latitude,
                longitude: gps.longitude,
                accuracy: gps.accuracy
            },
            googleLocation: googleLocation ? {
                latitude: googleLocation.latitude,
                longitude: googleLocation.longitude,
                accuracy: googleLocation.accuracy
            } : null,
            ipAddress,
            deviation,
            deviceInfo: {
                userAgent: deviceInfo?.userAgent || req.headers['user-agent'],
                platform: deviceInfo?.platform,
                timezone: deviceInfo?.timezone,
                language: deviceInfo?.language,
                screenResolution: deviceInfo?.screenResolution
            },
            validationStatus: validationResult.status,
            failureReason: validationResult.status === 'FAILED' ? validationResult.message : null
        });

        await auditLog.save();

        // Return response
        if (validationResult.status === 'FAILED') {
            return res.status(403).json({
                code: 403,
                message: validationResult.message,
                deviation: deviation.toFixed(0),
                auditId: auditLog._id
            });
        }

        return res.json({
            code: 100,
            message: validationResult.message,
            deviation: deviation.toFixed(0),
            validationStatus: validationResult.status,
            gpsAccuracy: gps.accuracy,
            googleAccuracy: googleLocation?.accuracy,
            auditId: auditLog._id
        });

    } catch (error) {
        console.error('[Location Validation] Error:', error);
        return res.status(500).json({
            code: 500,
            message: 'Location validation failed',
            error: error.message
        });
    }
}

async function getLocationAudits(req, res) {
    try {
        const { requestId } = req.params;

        const audits = await LocationAudit.find({ requestId })
            .sort({ timestamp: -1 })
            .lean();

        return res.json({
            code: 100,
            data: audits,
            count: audits.length
        });

    } catch (error) {
        console.error('[Get Location Audits] Error:', error);
        return res.status(500).json({
            code: 500,
            message: 'Failed to fetch location audits',
            error: error.message
        });
    }
}

module.exports = { validateLocation, getLocationAudits };
```

### Step 6: Create Routes
Create: `routes/locationRoutes.js`

```javascript
const express = require('express');
const router = express.Router();
const { validateLocation, getLocationAudits } = require('../controllers/locationValidation');
const { tokenVerifyMiddleware } = require('../middleware/tokenVerify'); // Your auth middleware

router.post('/validate-location', tokenVerifyMiddleware, validateLocation);
router.get('/location-audits/:requestId', tokenVerifyMiddleware, getLocationAudits);

module.exports = router;
```

### Step 7: Register Routes
In your main `app.js` or `server.js`:

```javascript
const locationRoutes = require('./routes/locationRoutes');

// Add this line with your other routes
app.use('/agent', locationRoutes);
```

---

## 🧪 Testing

### 1. Test Backend API
```bash
curl -X POST http://localhost:2021/agent/validate-location \
  -H "Content-Type: application/json" \
  -H "token: YOUR_AGENT_TOKEN" \
  -d '{
    "requestId": "test123",
    "checkList": "aadhaarOcr",
    "gps": {
      "latitude": 28.6139,
      "longitude": 77.2090,
      "accuracy": 20
    },
    "deviceInfo": {
      "userAgent": "Mozilla/5.0...",
      "platform": "Linux",
      "timezone": "Asia/Kolkata",
      "language": "en-US"
    }
  }'
```

### 2. Test Frontend Integration
1. Open browser console (F12)
2. Navigate to Aadhaar verification
3. Upload documents
4. Watch for console logs:
   - `[Location Validation] Validating location for aadhaarOcr...`
   - `[Location Validation] Success: {...}`

### 3. Check Database
```javascript
// MongoDB query
db.locationaudits.find().sort({ timestamp: -1 }).limit(10)

// Check failed validations
db.locationaudits.find({ validationStatus: "FAILED" })
```

---

## 📊 Monitoring & Analytics

### Query Examples

```javascript
// Average deviation
db.locationaudits.aggregate([
    { $group: { _id: null, avgDeviation: { $avg: "$deviation" } } }
])

// Validation status breakdown
db.locationaudits.aggregate([
    { $group: { _id: "$validationStatus", count: { $sum: 1 } } }
])

// Failed validations by checkList
db.locationaudits.aggregate([
    { $match: { validationStatus: "FAILED" } },
    { $group: { _id: "$checkList", count: { $sum: 1 } } }
])
```

---

## ⚙️ Configuration

### Adjust Deviation Threshold
In `controllers/locationValidation.js`, line 36:
```javascript
validationResult = validateDeviation(deviation, 200); // Change 200 to your threshold
```

**Recommended thresholds:**
- **100m** - Very strict (high-security)
- **200m** - Balanced (recommended)
- **500m** - Lenient (rural areas)
- **1000m** - Very lenient (testing)

### Fail-Open vs Fail-Closed
**Current: Fail-Open** (allows upload if Google API fails)

To make **Fail-Closed** (reject if Google API fails):
```javascript
// In validateLocation controller, replace the catch block:
catch (googleError) {
    return res.status(503).json({
        code: 503,
        message: 'Location validation service unavailable'
    });
}
```

---

## 💰 Cost Estimation

**Google Geolocation API Pricing:**
- Free tier: $200/month credit = 40,000 requests
- After free tier: $5 per 1,000 requests

**Example:**
- 10,000 KYC sessions/month
- 6 verification steps per session
- Total: 60,000 requests/month
- Cost: ~$100/month (after free tier)

**Optimization:** Cache IP-based location for same IP within 1 hour.

---

## 🚀 Deployment Checklist

- [ ] Backend: Install dependencies (`npm install axios mongoose`)
- [ ] Backend: Get Google Geolocation API key
- [ ] Backend: Add API key to `.env`
- [ ] Backend: Create `models/LocationAudit.js`
- [ ] Backend: Create `utils/locationUtils.js`
- [ ] Backend: Create `controllers/locationValidation.js`
- [ ] Backend: Create `routes/locationRoutes.js`
- [ ] Backend: Register routes in `app.js`
- [ ] Frontend: Already done! ✅
- [ ] Test: API endpoint with curl
- [ ] Test: Frontend integration
- [ ] Monitor: Check database logs
- [ ] Tune: Adjust threshold based on real data

---

## 🔍 Troubleshooting

### Google API Returns 400
- Verify API key is correct
- Check Geolocation API is enabled
- Ensure billing is enabled in Google Cloud

### All Validations Failing
- Check if `GOOGLE_GEOLOCATION_API_KEY` is set
- Verify backend can reach Google API
- Check IP address is being captured correctly

### High Deviation in Urban Areas
- Increase threshold to 500m
- Check GPS accuracy (should be < 100m)
- Verify Google API is returning correct location

---

## 📝 Next Steps

1. **Apply to Other Verification Files**
   - Copy the pattern from `AadhaarCheck.js`
   - Update: `PanCheck.js`, `DrivingLicenceCheck.js`, `FaceMatchCheck.js`, `SignatureCheck.js`, `OtpCheck.js`

2. **Monitor for 1 Week**
   - Track deviation patterns
   - Identify false positives
   - Adjust threshold if needed

3. **Add Alerts**
   - Email/Slack notification for suspicious patterns
   - Dashboard for location validation metrics

4. **Future Enhancements**
   - Mobile app for WiFi scanning
   - Device integrity checks (SafetyNet/DeviceCheck)
   - ML-based anomaly detection

---

## 🎯 Summary

**What's Working:**
- ✅ Frontend: Location validation integrated in `AadhaarCheck.js`
- ✅ Frontend: Utility functions created
- ✅ Frontend: API endpoints configured
- ✅ Frontend: Enhanced geolocation with accuracy

**What You Need to Do:**
- 🔧 Backend: Implement 4 files (model, utils, controller, routes)
- 🔑 Backend: Get Google API key
- 🧪 Backend: Test and deploy

**Time Estimate:** 1-2 hours for backend implementation

**Ready to go!** 🚀
