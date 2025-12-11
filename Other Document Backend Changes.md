# Backend Changes Required for Other Documents Functionality

## Overview
This document outlines all the backend changes needed to support the "Other Documents" feature in the Video KYC system. This feature allows agents to capture up to 50 images of miscellaneous documents during verification.

---

## 1. API Endpoint Modifications

### Endpoint: `/ocr-doc-upload` (or create new endpoint)

**Current Behavior:**
- Accepts single front and back images
- Processes specific document types (PAN, Aadhaar, etc.)

**Required Changes:**

#### Request Handling
```javascript
// Accept multiple files when checkList === "otherDocument"
if (req.body.checkList === "otherDocument") {
  // Handle multiple images (up to 50)
  const images = req.files.images; // Array of files
  
  // Validate:
  // 1. Maximum 50 images
  // 2. Each image size < 10MB
  // 3. Valid image formats (jpg, jpeg, png, pdf)
  
  if (images.length > 50) {
    return res.status(400).json({
      code: 101,
      message: "Maximum 50 images allowed"
    });
  }
}
```

#### FormData Structure
```javascript
// Frontend sends:
{
  requestId: String,
  checkList: "otherDocument",
  latitude: String,
  longitude: String,
  images: [File, File, File, ...] // Array of files (up to 50)
}
```

---

## 2. Database Schema Updates

### Collection: `customerVerifications` (or relevant collection)

**Add/Update Field:**

```javascript
otherDocument: {
  type: Object,
  default: null,
  properties: {
    urls: {
      type: [String],
      default: [],
      description: "Array of S3 URLs for uploaded documents (max 50)"
    },
    latitude: {
      type: String,
      default: ""
    },
    longitude: {
      type: String,
      default: ""
    },
    docStatus: {
      type: String,
      enum: ['pending', 'verified', 'rejected'],
      default: 'pending'
    },
    comment: {
      type: String,
      default: ""
    },
    uploadedAt: {
      type: Date,
      default: Date.now
    },
    verifiedAt: {
      type: Date,
      default: null
    },
    verifiedBy: {
      type: String,
      default: "" // Agent ID
    }
  }
}
```

---

## 3. File Upload Logic

### S3 Upload Implementation

```javascript
const uploadOtherDocuments = async (files, requestId) => {
  const uploadedUrls = [];
  
  try {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const fileName = `other_documents/${requestId}/${Date.now()}_${i + 1}.${file.mimetype.split('/')[1]}`;
      
      // Upload to S3
      const s3Params = {
        Bucket: process.env.S3_BUCKET_NAME,
        Key: fileName,
        Body: file.buffer,
        ContentType: file.mimetype,
        ACL: 'public-read'
      };
      
      const uploadResult = await s3.upload(s3Params).promise();
      uploadedUrls.push(uploadResult.Location);
    }
    
    return {
      success: true,
      urls: uploadedUrls
    };
  } catch (error) {
    console.error('S3 Upload Error:', error);
    return {
      success: false,
      error: error.message
    };
  }
};
```

---

## 4. API Response Structure

### Success Response
```javascript
{
  code: 100,
  message: "Other documents uploaded successfully",
  data: {
    requestId: "REQ123456",
    otherDocument: {
      urls: [
        "https://s3.amazonaws.com/bucket/other_documents/REQ123456/1234567890_1.png",
        "https://s3.amazonaws.com/bucket/other_documents/REQ123456/1234567890_2.png",
        // ... up to 50 URLs
      ],
      latitude: "28.7041",
      longitude: "77.1025",
      docStatus: "pending",
      uploadedAt: "2025-12-11T06:30:00.000Z"
    }
  }
}
```

### Error Responses
```javascript
// Too many images
{
  code: 101,
  message: "Maximum 50 images allowed. You uploaded 52 images."
}

// No images provided
{
  code: 102,
  message: "At least one image is required"
}

// File size too large
{
  code: 103,
  message: "Image size exceeds maximum limit of 10MB"
}

// Invalid file format
{
  code: 104,
  message: "Invalid file format. Only JPG, PNG, and PDF are allowed"
}

// Upload failed
{
  code: 105,
  message: "Failed to upload documents. Please try again."
}
```

---

## 5. Update Document Status API

### Endpoint: `/update-doc-status` (or similar)

**Handle otherDocument status updates:**

```javascript
// When checkList === "otherDocument"
if (checkList === "otherDocument") {
  const updateData = {
    'checkList.otherDocument.docStatus': status, // 'verified' or 'rejected'
    'checkList.otherDocument.comment': comment,
    'checkList.otherDocument.verifiedAt': new Date(),
    'checkList.otherDocument.verifiedBy': agentId
  };
  
  await CustomerVerification.findOneAndUpdate(
    { requestId: requestId },
    { $set: updateData },
    { new: true }
  );
}
```

---

## 6. Report Generation Updates

### Include Other Documents in PDF Report

```javascript
// In report generation logic
if (verificationData.checkList.otherDocument) {
  const otherDocs = verificationData.checkList.otherDocument;
  
  // Add section to PDF
  pdf.addSection({
    title: "Other Documents",
    status: otherDocs.docStatus,
    images: otherDocs.urls, // Display all images in grid
    location: {
      latitude: otherDocs.latitude,
      longitude: otherDocs.longitude
    },
    comment: otherDocs.comment,
    verifiedAt: otherDocs.verifiedAt
  });
}
```

**Display Format:**
- Show images in a grid layout (3-4 columns)
- Display image count (e.g., "15 documents uploaded")
- Show verification status with color coding
- Include geolocation data
- Display agent comments if rejected

---

## 7. Validation Schema

### Create/Update Joi Schema

```javascript
const otherDocumentSchema = Joi.object({
  requestId: Joi.string().required(),
  checkList: Joi.string().valid('otherDocument').required(),
  latitude: Joi.string().allow('').optional(),
  longitude: Joi.string().allow('').optional(),
  images: Joi.array()
    .items(Joi.object())
    .min(1)
    .max(50)
    .required()
    .messages({
      'array.min': 'At least one image is required',
      'array.max': 'Maximum 50 images allowed'
    })
});
```

---

## 8. Multer Configuration

### Update file upload middleware

```javascript
const multer = require('multer');

const storage = multer.memoryStorage();

const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
  
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Invalid file type. Only JPG, PNG, and PDF are allowed'), false);
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB per file
    files: 50 // Maximum 50 files
  }
});

// Use in route
router.post('/ocr-doc-upload', 
  upload.array('images', 50), // Accept up to 50 files with field name 'images'
  ocrDocUploadController
);
```

---

## 9. Complete API Implementation Example

```javascript
const uploadOtherDocuments = async (req, res) => {
  try {
    const { requestId, checkList, latitude, longitude } = req.body;
    const files = req.files; // Array of files from multer
    
    // Validation
    if (checkList !== 'otherDocument') {
      return res.status(400).json({
        code: 101,
        message: 'Invalid checkList value'
      });
    }
    
    if (!files || files.length === 0) {
      return res.status(400).json({
        code: 102,
        message: 'At least one image is required'
      });
    }
    
    if (files.length > 50) {
      return res.status(400).json({
        code: 103,
        message: `Maximum 50 images allowed. You uploaded ${files.length} images.`
      });
    }
    
    // Upload to S3
    const uploadResult = await uploadOtherDocuments(files, requestId);
    
    if (!uploadResult.success) {
      return res.status(500).json({
        code: 105,
        message: 'Failed to upload documents. Please try again.'
      });
    }
    
    // Update database
    const updateData = {
      'checkList.otherDocument': {
        urls: uploadResult.urls,
        latitude: latitude || '',
        longitude: longitude || '',
        docStatus: 'pending',
        comment: '',
        uploadedAt: new Date(),
        verifiedAt: null,
        verifiedBy: ''
      }
    };
    
    const updatedVerification = await CustomerVerification.findOneAndUpdate(
      { requestId: requestId },
      { $set: updateData },
      { new: true }
    );
    
    if (!updatedVerification) {
      return res.status(404).json({
        code: 106,
        message: 'Verification record not found'
      });
    }
    
    return res.status(200).json({
      code: 100,
      message: 'Other documents uploaded successfully',
      data: {
        requestId: requestId,
        otherDocument: updatedVerification.checkList.otherDocument
      }
    });
    
  } catch (error) {
    console.error('Upload Error:', error);
    return res.status(500).json({
      code: 500,
      message: 'Internal server error',
      error: error.message
    });
  }
};
```

---

## 10. Testing Checklist

### Backend Tests Required:

- [ ] Upload 1 image successfully
- [ ] Upload 50 images successfully (max limit)
- [ ] Reject upload with 51+ images
- [ ] Reject upload with 0 images
- [ ] Reject upload with invalid file types
- [ ] Reject upload with files > 10MB
- [ ] Verify S3 URLs are accessible
- [ ] Verify database update with correct structure
- [ ] Test status update (pending → verified)
- [ ] Test status update (pending → rejected)
- [ ] Verify geolocation data is saved correctly
- [ ] Test report generation with other documents
- [ ] Test error handling for S3 failures
- [ ] Test concurrent uploads

---

## 11. Environment Variables Required

```bash
# Add to .env file
S3_BUCKET_NAME=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
MAX_OTHER_DOCUMENTS=50
MAX_FILE_SIZE_MB=10
```

---

## 12. Security Considerations

1. **File Validation:**
   - Validate file types on both frontend and backend
   - Check file signatures (magic numbers) not just extensions
   - Scan for malware if possible

2. **Rate Limiting:**
   - Limit uploads per user/session
   - Prevent abuse with too many requests

3. **Access Control:**
   - Ensure only authorized agents can upload
   - Verify requestId belongs to the agent's session

4. **Data Privacy:**
   - Store S3 URLs securely
   - Implement proper access controls on S3 bucket
   - Consider encryption at rest

---

## 13. Performance Optimization

1. **Parallel Uploads:**
   - Upload images to S3 in parallel (use Promise.all)
   - Reduces total upload time

2. **Image Compression:**
   - Consider compressing images before upload
   - Reduces storage costs and improves load times

3. **CDN Integration:**
   - Use CloudFront or similar CDN for faster image delivery
   - Improves report generation speed

4. **Lazy Loading:**
   - In reports, lazy load images as user scrolls
   - Improves initial page load time

---

## Summary

The backend changes involve:
1. ✅ Modifying the upload API to handle multiple files
2. ✅ Updating database schema to store array of URLs
3. ✅ Implementing S3 upload for multiple files
4. ✅ Adding validation for file count, size, and type
5. ✅ Updating status management API
6. ✅ Modifying report generation to include all images
7. ✅ Adding proper error handling and responses

**Estimated Development Time:** 4-6 hours
**Testing Time:** 2-3 hours
**Total:** 6-9 hours

---

## Questions to Clarify

1. Should we process OCR on these "other documents" or just store them?
2. Do we need to categorize these documents (e.g., utility bill, bank statement)?
3. Should there be a minimum number of images required?
4. What should be the retention policy for these images?
5. Should agents be able to delete individual images before final upload?
