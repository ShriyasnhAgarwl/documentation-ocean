# Edit Template API Documentation

## Overview
This API allows users to edit/update existing templates by modifying the template name and/or checklist. The API includes comprehensive validation and edge case handling.

## Endpoint Details

**Method:** `PATCH`  
**Route:** `/user/editTemplate`  
**Authentication:** Required (tokenVerifyMiddileware)  
**Content-Type:** `application/json`

---

## Request Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `token` | string | Yes | User authentication token |
| `Content-Type` | string | Yes | Must be `application/json` |

---

## Request Body

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `templateId` | string | Yes | Non-empty string | The ID of the template to edit |
| `templateName` | string | No | 3-100 characters | New name for the template |
| `checkList` | array | No | Min 1 item, valid values only | Array of check items |

**Note:** At least one of `templateName` or `checkList` must be provided.

### Valid CheckList Values
- `panOcr`
- `aadhaarOcr`
- `otpOcr`
- `faceMatch`
- `visaOcr`
- `passportOcr`
- `drivingLicenseOcr`
- `ssnIdOcr`
- `signatureOcr`
- `internationalPassportOcr`
- `ukDrivingLicenseOcr`
- `emiratesIdOcr`
- `otherDocument`

---

## cURL Examples

### Example 1: Edit Template Name Only
```bash
curl -X PATCH \
  'http://localhost:3000/user/editTemplate' \
  -H 'token: YOUR_USER_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
    "templateName": "Updated Template Name"
  }'
```

### Example 2: Edit CheckList Only
```bash
curl -X PATCH \
  'http://localhost:3000/user/editTemplate' \
  -H 'token: YOUR_USER_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
    "checkList": [
      "panOcr",
      "aadhaarOcr",
      "faceMatch",
      "otpOcr"
    ]
  }'
```

### Example 3: Edit Both Template Name and CheckList
```bash
curl -X PATCH \
  'http://localhost:3000/user/editTemplate' \
  -H 'token: YOUR_USER_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
    "templateName": "New Template Name",
    "checkList": [
      "panOcr",
      "aadhaarOcr",
      "faceMatch",
      "passportOcr",
      "visaOcr"
    ]
  }'
```

---

## Response Examples

### Success Response (200 OK)
```json
{
  "code": 100,
  "message": "Template updated successfully.",
  "template": {
    "templateName": "Updated Template Name",
    "checkList": [
      "panOcr",
      "aadhaarOcr",
      "faceMatch",
      "otpOcr"
    ],
    "subdomain": "priya",
    "userId": 209800212,
    "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
    "createdAt": "2024-11-07T09:06:41.039Z",
    "updatedAt": "2025-12-08T09:50:00.000Z"
  }
}
```

### No Changes Detected (200 OK)
```json
{
  "code": 100,
  "message": "No changes detected. Template remains unchanged.",
  "template": {
    "templateName": "Test data",
    "checkList": ["panOcr", "aadhaarOcr"],
    "subdomain": "priya",
    "userId": 209800212,
    "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
    "createdAt": "2024-11-07T09:06:41.039Z"
  }
}
```

### Error Response - Template Not Found (404)
```json
{
  "code": 404,
  "message": "Template not found or you don't have permission to edit it"
}
```

### Error Response - Duplicate Template Name (400)
```json
{
  "code": 400,
  "message": "A template with the name \"Existing Template\" already exists"
}
```

### Error Response - Validation Error (400)
```json
{
  "code": 400,
  "message": "At least one field (templateName or checkList) must be provided for update"
}
```

### Error Response - Empty CheckList (400)
```json
{
  "code": 400,
  "message": "CheckList cannot be empty"
}
```

### Error Response - Invalid CheckList Item (400)
```json
{
  "code": 400,
  "message": "CheckList contains invalid items"
}
```

### Error Response - Unauthorized (401)
```json
{
  "code": 401,
  "error": "Unauthorized",
  "message": "Token not provided in header"
}
```

---

## Edge Cases Handled

1. **Template Ownership Validation**
   - Only the template owner (userId) can edit their templates
   - Returns 404 if template doesn't exist or belongs to another user

2. **Duplicate Name Prevention**
   - Checks if another template with the same name already exists for the user
   - Case-sensitive comparison
   - Ignores the current template when checking for duplicates

3. **Empty Updates**
   - If no actual changes are detected, returns success with existing template
   - Prevents unnecessary database updates

4. **CheckList Deduplication**
   - Automatically removes duplicate items from checkList
   - Example: `["panOcr", "panOcr", "aadhaarOcr"]` → `["panOcr", "aadhaarOcr"]`

5. **Partial Updates**
   - Supports updating only templateName, only checkList, or both
   - Fields not provided remain unchanged

6. **Template Name Trimming**
   - Automatically trims whitespace from template names
   - Prevents accidental spaces causing issues

7. **Empty CheckList Prevention**
   - Validates that checkList has at least one item if provided
   - Returns error if empty array is submitted

8. **Invalid CheckList Items**
   - Validates each item against allowed values
   - Returns clear error message for invalid items

9. **Same Name Update**
   - If new name is same as current name, no duplicate check is performed
   - Allows other fields to be updated without name conflicts

10. **Database Update Failure**
    - Handles cases where database update fails
    - Returns appropriate error message

---

## Security Features

1. **User Authentication**
   - Requires valid user token via `tokenVerifyMiddileware`
   - Extracts userId from authenticated token

2. **Authorization**
   - Validates template ownership before allowing edits
   - Prevents users from editing templates they don't own

3. **Input Validation**
   - Comprehensive Joi schema validation
   - Prevents injection attacks and malformed data

4. **Error Handling**
   - Catches and handles all exceptions gracefully
   - Doesn't expose sensitive system information

---

## Testing Scenarios

### Test Case 1: Valid Update - Name Only
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
  "templateName": "My New Template"
}
```
**Expected:** Success with updated template

### Test Case 2: Valid Update - CheckList Only
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
  "checkList": ["panOcr", "aadhaarOcr"]
}
```
**Expected:** Success with updated template

### Test Case 3: Invalid - Missing Both Fields
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf"
}
```
**Expected:** Error - At least one field required

### Test Case 4: Invalid - Empty CheckList
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
  "checkList": []
}
```
**Expected:** Error - CheckList cannot be empty

### Test Case 5: Invalid - Duplicate Name
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
  "templateName": "Existing Template Name"
}
```
**Expected:** Error - Template name already exists

### Test Case 6: Invalid - Wrong User
**Input:** Valid payload but templateId belongs to another user
**Expected:** Error - Template not found

### Test Case 7: Invalid - Invalid CheckList Item
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
  "checkList": ["panOcr", "invalidItem"]
}
```
**Expected:** Error - CheckList contains invalid items

### Test Case 8: Valid - Duplicate Items in CheckList
**Input:**
```json
{
  "templateId": "1YiQYRT2SjKLFeF6GEBPYPAHf",
  "checkList": ["panOcr", "panOcr", "aadhaarOcr"]
}
```
**Expected:** Success with deduplicated checkList

---

## Implementation Details

### Files Modified

1. **`/middleware/models/payloads.js`**
   - Added `editTemplate` Joi validation schema
   - Exported validation schema

2. **`/services/onboardingSolution.js`**
   - Added `editTemplate` function with comprehensive logic
   - Exported function

3. **`/routes/routes.js`**
   - Added PATCH route `/user/editTemplate`
   - Applied `tokenVerifyMiddileware` authentication

### Database Operations

- **Read:** `db.get()` - Check template existence and ownership
- **Read:** `db.get()` - Check for duplicate template names
- **Update:** `db.update()` - Update template with new values
- **Read:** `db.get()` - Fetch updated template for response

---

## Notes

- The API uses PATCH method following REST conventions for partial updates
- The `subdomain` field cannot be edited (security measure)
- The `userId` field cannot be edited (security measure)
- The `templateId` field cannot be edited (immutable identifier)
- The `createdAt` field is preserved
- The `updatedAt` field is automatically set to current timestamp
- All string fields are trimmed to prevent whitespace issues
- CheckList duplicates are automatically removed

---

## Related APIs

- **Create Template:** `POST /user/createTemplates`
- **Get Templates:** `GET /user/getTemplates`
- **Get Template by ID:** `GET /user/getTemplatesById/:templateId`
- **Delete Template:** `DELETE /user/deleteTemplate/:templateId`
