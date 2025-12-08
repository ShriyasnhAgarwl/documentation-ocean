# Edit Template Implementation Summary

## Overview
Successfully implemented the edit template functionality for Video KYC templates using the PATCH API endpoint `/user/editTemplate`. The implementation reuses the existing "Add Template" popup for editing templates.

## Changes Made

### 1. API Configuration (`/src/Base/TokenConfig.js`)
- **Added**: `videoKycEditTemplate` endpoint constant pointing to `/user/editTemplate`
- This endpoint is used for PATCH requests to update existing templates

### 2. SavedFlows Component (`/src/VideoKYC/Components/SavedFlows.jsx`)

#### State Management
- **Added** `isEditMode`: Boolean to track if the popup is in edit or create mode
- **Added** `currentTemplateId`: Stores the template ID being edited

#### Functions

**handleAddTemplate()** - Updated
- Resets edit mode state when opening popup for creating new template
- Clears `isEditMode` and `currentTemplateId`

**handleEditTemplate(template)** - New
- Sets edit mode to true
- Pre-fills the form with template data:
  - Template name
  - Selected checkboxes (checkList)
  - Subdomain (if available)
- Opens the popup in edit mode

**validateFields()** - Updated
- Skips subdomain validation when in edit mode (since PATCH doesn't require subdomain)

**addTemplateFunctionHandler()** - Updated
- Handles both create and edit operations
- Uses conditional API call:
  - **Edit mode**: `tokenapi.patch(videoKycEditTemplate, { templateId, templateName, checkList })`
  - **Create mode**: `tokenapi.post(videoKycCreateTemplates, { templateName, checkList, subdomain })`
- Updates button text based on mode ("Updating Template..." vs "Adding Template...")

**clearFunction()** - Updated
- Resets edit mode state along with other form fields

#### UI Changes

**Popup Title**
- Dynamic title: "Edit Template" when editing, "Add Template" when creating

**Domain Selection**
- Hidden in edit mode (wrapped with `{!isEditMode && ...}`)
- Only shown when creating new templates

**Checkboxes**
- Added `checked` attribute to properly reflect selected values in edit mode
- Ensures pre-selected items are checked when editing

**Submit Button**
- Dynamic text: "Update" when editing, "Add" when creating
- Calls appropriate handler based on mode

**Edit Icon**
- Made clickable with `onClick={() => handleEditTemplate(template)}`
- Added cursor pointer style for better UX
- Triggers edit mode when clicked

## API Request Format

### Edit Template (PATCH)
```bash
curl --location --request PATCH 'http://localhost:2021/user/editTemplate' \
--header 'token: <YOUR_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
    "templateId": "tdbpdwAuweiYTltNrZRYwVxEW",
    "templateName": "Updated Template Name",
    "checkList": [
      "panOcr",
      "aadhaarOcr",
      "faceMatch",
      "otpOcr"
    ]
}'
```

## Key Features

1. **Code Reusability**: Reuses the existing "Add Template" popup for editing
2. **Smart Validation**: Skips subdomain validation in edit mode
3. **Pre-filled Form**: Automatically populates form fields with existing template data
4. **Visual Feedback**: Edit icon has cursor pointer and proper alt text
5. **Dynamic UI**: Popup title and button text change based on mode
6. **Proper State Management**: Clears edit state when switching between modes

## User Flow

1. User clicks the edit icon on a template card
2. Popup opens with "Edit Template" title
3. Form is pre-filled with existing template data
4. Domain selection is hidden (cannot change subdomain)
5. User modifies template name and/or checklist items
6. Clicks "Update" button
7. PATCH request sent to `/user/editTemplate`
8. Success message shown and template list refreshed
9. Popup closes and state is cleared

## Testing Recommendations

1. Test editing a template with all fields
2. Verify subdomain is not sent in PATCH request
3. Test validation (empty template name, no checkboxes selected)
4. Verify checkboxes are properly checked when editing
5. Test switching between create and edit modes
6. Verify template list refreshes after successful edit
