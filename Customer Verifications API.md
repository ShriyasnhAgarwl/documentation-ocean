# Customer Verifications API Implementation

## Overview
Two new APIs have been created to fetch `customerVerifications` data from the database:

1. **Agent API** - For agents to fetch their customer verifications based on agentId
2. **User API** - For users to fetch and filter their customer verifications

---

## API Endpoints

### 1. Agent API - Get Customer Verifications

**Endpoint:** `GET /agent/customerVerifications`

**Authentication:** Agent token (via `agentMiddleware`)

**Description:** Fetches all customer verifications associated with the authenticated agent's agentId.

**Query Parameters:**
- `pageNumber` (optional, default: 1) - Page number for pagination

**Headers:**
```
token: <agent_token>
```

**Response:**
```json
{
  "code": 100,
  "message": "Customer verifications found successfully",
  "totalRecords": 150,
  "pageNumber": 1,
  "pageSize": 50,
  "result": [
    {
      // customerVerification objects
    }
  ]
}
```

**Example cURL:**
```bash
curl --location 'http://localhost:3000/agent/customerVerifications?pageNumber=1' \
--header 'token: <your_agent_token>'
```

---

### 2. User API - Get Customer Verifications with Filtering

**Endpoint:** `GET /user/customerVerifications`

**Authentication:** User token (via `tokenVerifyMiddileware`)

**Description:** Fetches customer verifications for the authenticated user with optional filtering capabilities (similar to `/search/vkyc-reports-filter`).

**Query Parameters:**
- `pageNumber` (optional, default: 1) - Page number for pagination
- `agentId` (optional) - Filter by agent ID
- `firstName` (optional) - Filter by first name (case-insensitive regex search)
- `lastName` (optional) - Filter by last name (case-insensitive regex search)
- `email` (optional) - Filter by email (case-insensitive regex search)
- `mobile_no` (optional) - Filter by mobile number (exact match)
- `status` (optional) - Filter by status

**Headers:**
```
token: <user_token>
```

**Response:**
```json
{
  "code": 100,
  "message": "Customer verifications found successfully",
  "totalRecords": 75,
  "pageNumber": 1,
  "pageSize": 50,
  "result": [
    {
      // customerVerification objects
    }
  ]
}
```

**Example cURL:**
```bash
# Without filters
curl --location 'http://localhost:3000/user/customerVerifications?pageNumber=1' \
--header 'token: <your_user_token>'

# With filters
curl --location 'http://localhost:3000/user/customerVerifications?pageNumber=1&firstName=John&status=completed&agentId=123' \
--header 'token: <your_user_token>'
```

---

## Implementation Details

### Files Modified

1. **routes/routes.js** (Lines 3578-3588)
   - Added two new GET routes
   - Agent route uses `middleware.agentMiddleware`
   - User route uses `middleware.tokenVerifyMiddileware`

2. **services/onboardingSolution.js** (Lines 6525-6613)
   - Added `getCustomerVerificationsAgent` function
   - Added `getCustomerVerificationsUser` function
   - Both functions added to module exports

### Key Features

#### Agent API (`getCustomerVerificationsAgent`)
- Extracts `agentId` from the authenticated agent token
- Queries `customerverifications` collection filtered by `agentId`
- Supports pagination (50 records per page)
- Returns all customer verifications for that agent

#### User API (`getCustomerVerificationsUser`)
- Extracts `userId` from the authenticated user token
- Queries `customerverifications` collection filtered by `userId`
- Supports multiple filter parameters:
  - `agentId` - Exact match
  - `firstName` - Case-insensitive partial match
  - `lastName` - Case-insensitive partial match
  - `email` - Case-insensitive partial match
  - `mobile_no` - Exact match
  - `status` - Exact match
- Supports pagination (50 records per page)
- Similar filtering logic to `/search/vkyc-reports-filter`

### Middleware Used

1. **agentMiddleware** (Agent API)
   - Validates agent token from header
   - Extracts agent information and sets `req.agentId`
   - Returns 401 if unauthorized

2. **tokenVerifyMiddileware** (User API)
   - Validates user token from header
   - Extracts user information and sets `req.userAuth`
   - Returns 401 if unauthorized

### Database Query

Both APIs use the `db.getFilteredRecords()` method which:
- Accepts collection name, query object, page number, and page size
- Returns paginated results with total record count
- Efficiently handles filtering and pagination

---

## Response Codes

- **100** - Success, records found
- **103** - Success, but no records found
- **401** - Unauthorized (invalid or missing token)
- **500** - Server error (operation failed)

---

## Testing

### Test Agent API
```bash
# Replace <agent_token> with actual agent token
curl --location 'http://localhost:3000/agent/customerVerifications' \
--header 'token: <agent_token>'
```

### Test User API
```bash
# Replace <user_token> with actual user token
curl --location 'http://localhost:3000/user/customerVerifications?firstName=test&pageNumber=1' \
--header 'token: <user_token>'
```

---

## Notes

- Both APIs return a maximum of 50 records per page
- The user API filtering is case-insensitive for text fields (firstName, lastName, email)
- The agent API automatically filters by the agentId from the token
- The user API automatically filters by the userId from the token
- Both APIs follow the same response structure as existing VKYC filter APIs
