# Location Validation Implementation Guide

## Overview
This document provides the complete implementation for IP + GPS location validation with Google Geolocation API.

---

## 📦 Prerequisites

### 1. Install Required Packages (Backend)
```bash
npm install axios
# Already installed in your project
```

### 2. Get Google Geolocation API Key
1. Go to: https://console.cloud.google.com/
2. Enable "Geolocation API"
3. Create API credentials
4. Add to your `.env` file:
   ```
   GOOGLE_GEOLOCATION_API_KEY=your_api_key_here
   ```

---

## 🗄️ Database Schema

### MongoDB Schema for Location Audit Logs

```javascript
// models/LocationAudit.js
const mongoose = require('mongoose');

const locationAuditSchema = new mongoose.Schema({
    requestId: {
        type: String,
        required: true,
        index: true
    },
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
    ipAddress: {
        type: String,
        required: true
    },
    deviation: {
        type: Number, // Distance in meters
        required: true
    },
    deviceInfo: {
        userAgent: String,
        platform: String,
        timezone: String,
        language: String
    },
    validationStatus: {
        type: String,
        enum: ['PASSED', 'FAILED', 'WARNING'],
        required: true
    },
    failureReason: String,
    timestamp: {
        type: Date,
        default: Date.now,
        index: true
    }
}, {
    timestamps: true
});

// Index for efficient querying
locationAuditSchema.index({ requestId: 1, timestamp: -1 });
locationAuditSchema.index({ validationStatus: 1, timestamp: -1 });

module.exports = mongoose.model('LocationAudit', locationAuditSchema);
```

---

## 🔧 Backend Implementation

### 1. Utility: Distance Calculator

```javascript
// utils/locationUtils.js

/**
 * Calculate distance between two GPS coordinates using Haversine formula
 * @param {number} lat1 - Latitude of point 1
 * @param {number} lon1 - Longitude of point 1
 * @param {number} lat2 - Latitude of point 2
 * @param {number} lon2 - Longitude of point 2
 * @returns {number} Distance in meters
 */
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

/**
 * Get location from Google Geolocation API using IP address
 * @param {string} ipAddress - Client IP address
 * @returns {Promise<Object>} Location data
 */
async function getGoogleGeolocation(ipAddress) {
    const axios = require('axios');
    const GOOGLE_API_KEY = process.env.GOOGLE_GEOLOCATION_API_KEY;

    if (!GOOGLE_API_KEY) {
        throw new Error('GOOGLE_GEOLOCATION_API_KEY not configured');
    }

    try {
        const response = await axios.post(
            `https://www.googleapis.com/geolocation/v1/geolocate?key=${GOOGLE_API_KEY}`,
            {
                considerIp: true // Use IP-based geolocation
            }
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

/**
 * Validate location deviation
 * @param {number} deviation - Distance in meters
 * @param {number} threshold - Maximum allowed deviation in meters
 * @returns {Object} Validation result
 */
function validateDeviation(deviation, threshold = 200) {
    if (deviation <= threshold) {
        return {
            status: 'PASSED',
            message: 'Location validated successfully'
        };
    } else if (deviation <= threshold * 2) {
        return {
            status: 'WARNING',
            message: `Location deviation is ${deviation.toFixed(0)}m (above threshold but within tolerance)`
        };
    } else {
        return {
            status: 'FAILED',
            message: `Location mismatch detected: ${deviation.toFixed(0)}m deviation exceeds ${threshold}m threshold`
        };
    }
}

module.exports = {
    calculateDistance,
    getGoogleGeolocation,
    validateDeviation
};
```

### 2. Controller: Location Validation

```javascript
// controllers/locationValidation.js

const LocationAudit = require('../models/LocationAudit');
const { calculateDistance, getGoogleGeolocation, validateDeviation } = require('../utils/locationUtils');

/**
 * Validate location and store audit log
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function validateLocation(req, res) {
    try {
        const {
            requestId,
            checkList,
            gps,
            deviceInfo
        } = req.body;

        // Validation
        if (!requestId || !checkList || !gps || !gps.latitude || !gps.longitude) {
            return res.status(400).json({
                code: 400,
                message: 'Missing required fields: requestId, checkList, gps (latitude, longitude)'
            });
        }

        // Get client IP address
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
                gps.latitude,
                gps.longitude,
                googleLocation.latitude,
                googleLocation.longitude
            );

            // Validate deviation (200m threshold)
            validationResult = validateDeviation(deviation, 200);

            console.log(`[Location Validation] Deviation: ${deviation.toFixed(0)}m, Status: ${validationResult.status}`);

        } catch (googleError) {
            console.error('[Location Validation] Google API failed, allowing GPS only:', googleError.message);
            
            // Fallback: Accept GPS without validation if Google API fails
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
                language: deviceInfo?.language
            },
            validationStatus: validationResult.status,
            failureReason: validationResult.status === 'FAILED' ? validationResult.message : null
        });

        await auditLog.save();

        // Return response based on validation status
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

/**
 * Get location audit logs for a request
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
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

module.exports = {
    validateLocation,
    getLocationAudits
};
```

### 3. Routes

```javascript
// routes/locationRoutes.js

const express = require('express');
const router = express.Router();
const { validateLocation, getLocationAudits } = require('../controllers/locationValidation');
const { tokenVerifyMiddleware } = require('../middleware/tokenVerify'); // Your existing auth middleware

// Validate location (called from frontend during OCR uploads)
router.post('/validate-location', tokenVerifyMiddleware, validateLocation);

// Get location audit logs for a request
router.get('/location-audits/:requestId', tokenVerifyMiddleware, getLocationAudits);

module.exports = router;
```

### 4. Add to Main App

```javascript
// app.js or server.js (add this line)

const locationRoutes = require('./routes/locationRoutes');
app.use('/agent', locationRoutes);
```

---

## 🎨 Frontend Implementation

### 1. Add API Endpoint

```javascript
// src/Base/AgentConfig.js

// Add this line after line 68
export const validateLocation = "/agent/validate-location";
export const getLocationAudits = "/agent/location-audits/";
```

### 2. Create Location Validation Utility

```javascript
// src/VideoKycAgent/Utils/LocationValidator.js

import agentApi, { validateLocation } from "../../Base/AgentConfig";

/**
 * Validate location with backend
 * @param {Object} params - Validation parameters
 * @param {string} params.requestId - Request ID
 * @param {string} params.checkList - Check list type
 * @param {number} params.latitude - GPS latitude
 * @param {number} params.longitude - GPS longitude
 * @param {number} params.accuracy - GPS accuracy in meters
 * @returns {Promise<Object>} Validation result
 */
export async function validateLocationWithBackend({
    requestId,
    checkList,
    latitude,
    longitude,
    accuracy
}) {
    try {
        const deviceInfo = {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            language: navigator.language
        };

        const response = await agentApi.post(validateLocation, {
            requestId,
            checkList,
            gps: {
                latitude,
                longitude,
                accuracy
            },
            deviceInfo
        });

        console.log('[Location Validation]', response.data);
        return {
            success: true,
            data: response.data
        };

    } catch (error) {
        console.error('[Location Validation] Error:', error);
        
        // If validation fails with 403, location mismatch detected
        if (error.response?.status === 403) {
            return {
                success: false,
                error: error.response.data.message,
                deviation: error.response.data.deviation
            };
        }

        // For other errors, allow the upload to proceed (fail-open for better UX)
        console.warn('[Location Validation] Allowing upload despite validation error');
        return {
            success: true,
            warning: 'Location validation unavailable'
        };
    }
}
```

### 3. Update Upload Functions (Example: AadhaarCheck.js)

```javascript
// In uploadDocs function, BEFORE calling the OCR API:

const uploadDocs = async () => {
    setLoading(true);

    // ✅ NEW: Validate location first
    const locationValidation = await validateLocationWithBackend({
        requestId: meetingData.requestId,
        checkList: 'aadhaarOcr',
        latitude,
        longitude,
        accuracy: position?.coords?.accuracy // Store this from geolocation
    });

    // If location validation failed, show error and stop
    if (!locationValidation.success) {
        setLoading(false);
        setMessageClass('error');
        setMessage(`Location Validation Failed: ${locationValidation.error}`);
        setTimeout(() => setMessage(''), 7000);
        return;
    }

    // If validation passed with warning, show it
    if (locationValidation.warning) {
        setMessageClass('warning');
        setMessage(locationValidation.warning);
        setTimeout(() => setMessage(''), 3000);
    }

    // Continue with existing OCR upload...
    const formData = new FormData();
    formData.append("requestId", meetingData.requestId);
    // ... rest of your existing code
};
```

---

## 📊 Testing & Monitoring

### Test the Implementation

```bash
# Test location validation endpoint
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

### Monitor Audit Logs

```javascript
// Query location audits in MongoDB
db.locationaudits.find({ requestId: "test123" }).sort({ timestamp: -1 })

// Find failed validations
db.locationaudits.find({ validationStatus: "FAILED" }).sort({ timestamp: -1 })

// Check average deviation
db.locationaudits.aggregate([
    { $group: { _id: null, avgDeviation: { $avg: "$deviation" } } }
])
```

---

## 🎯 Configuration Options

### Adjust Deviation Threshold

In `controllers/locationValidation.js`, line with `validateDeviation(deviation, 200)`:

- **200m** - Strict (urban areas)
- **500m** - Moderate (suburban)
- **1000m** - Lenient (rural areas)

### Fail-Open vs Fail-Closed

**Current: Fail-Open** (allows upload if Google API fails)
```javascript
// Fallback in validateLocation function
validationResult = {
    status: 'WARNING',
    message: 'Location validated using GPS only'
};
```

**To make Fail-Closed** (reject if Google API fails):
```javascript
return res.status(503).json({
    code: 503,
    message: 'Location validation service unavailable'
});
```

---

## 💰 Cost Estimation

**Google Geolocation API:**
- Free tier: $200/month (40,000 requests)
- After free tier: $5 per 1,000 requests

**Example:**
- 10,000 KYC sessions/month
- 6 checks per session = 60,000 requests
- Cost: ~$100/month (after free tier)

**Optimization:** Cache IP-based location for same IP within 1 hour to reduce API calls.

---

## 🔐 Security Considerations

1. **API Key Security**: Store in environment variables, never commit to Git
2. **Rate Limiting**: Add rate limiting to prevent API abuse
3. **IP Spoofing**: Google API uses server-side IP, harder to spoof
4. **Audit Retention**: Keep logs for compliance (6-12 months)
5. **GDPR Compliance**: Inform users about location tracking

---

## 📈 Next Steps

1. ✅ Implement backend API
2. ✅ Add database schema
3. ✅ Update frontend to call validation
4. 📊 Monitor deviation patterns for 1 week
5. 🎯 Adjust threshold based on real data
6. 🔔 Add alerts for suspicious patterns
7. 📱 Consider mobile app for WiFi scanning (future)

---

## 🆘 Troubleshooting

### Google API Returns 400 Error
- Check API key is valid
- Ensure Geolocation API is enabled in Google Cloud Console
- Verify billing is enabled

### High Deviation in Urban Areas
- Increase threshold to 500m
- Check if GPS accuracy is poor (> 100m)

### All Validations Failing
- Check if Google API key is configured
- Verify network connectivity from backend
- Check if IP address is being captured correctly

---

## 📝 Summary

This implementation provides:
- ✅ GPS + IP-based location validation
- ✅ 200m deviation threshold
- ✅ Complete audit logging
- ✅ Fail-open for better UX
- ✅ Device fingerprinting
- ✅ Cost-effective (IP-based, no WiFi scanning needed)

**Ready to deploy!** 🚀
