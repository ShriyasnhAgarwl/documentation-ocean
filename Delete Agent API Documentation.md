# Delete Agent API Documentation

## Overview
This API endpoint allows authorized users to securely delete agents from the `oceanAgents` collection with comprehensive validation and edge case handling.

## Endpoint Details
- **URL**: `/user/deleteAgent`
- **Method**: `DELETE`
- **Authentication**: Required (JWT Token via `tokenVerifyMiddileware`)
- **Content-Type**: `application/json`

## Request Headers
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Request Body
```json
{
  "agentId": 123456,
  "comment": "Agent is no longer needed for this project and has completed all assigned tasks."
}
```

### Request Parameters

| Parameter | Type    | Required | Validation | Description |
|-----------|---------|----------|------------|-------------|
| agentId   | Integer | Yes      | Positive integer | The unique ID of the agent to delete |
| comment   | String  | Yes      | 10-500 characters | Reason for deletion (audit trail) |

## Response

### Success Response (200 OK)
```json
{
  "code": 100,
  "message": "Agent deleted successfully",
  "details": {
    "agentId": 123456,
    "agentEmail": "agent@example.com",
    "deletedAt": "2025-12-08T06:36:28.000Z",
    "archived": true
  }
}
```

### Error Responses

#### 1. Empty Request Body (400 Bad Request)
```json
{
  "code": 104,
  "message": "Request body cannot be empty"
}
```

#### 2. Validation Error (400 Bad Request)
```json
{
  "code": 104,
  "message": "Comment must be at least 10 characters long"
}
```

#### 3. Unauthorized Access (401 Unauthorized)
```json
{
  "code": 104,
  "message": "Unauthorized Access!"
}
```

#### 4. Agent Not Found (404 Not Found)
```json
{
  "code": 103,
  "message": "Agent with ID 123456 does not exist"
}
```

#### 5. Ownership Violation (401 Unauthorized)
```json
{
  "code": 104,
  "message": "Unauthorized! You can only delete agents created by you."
}
```

#### 6. Active Calls Exist (403 Forbidden)
```json
{
  "code": 104,
  "message": "Cannot delete agent with active calls. Please wait for all calls to complete."
}
```

#### 7. Ongoing Verifications (403 Forbidden)
```json
{
  "code": 104,
  "message": "Cannot delete agent with ongoing verification sessions. Please complete or reject all sessions first."
}
```

## Security Features

### 1. **Authentication & Authorization**
- Validates JWT token
- Verifies user exists and is active
- Ensures agent belongs to requesting user (ownership check)

### 2. **Data Integrity Checks**
- Prevents deletion of agents with active calls
- Prevents deletion of agents with ongoing verification sessions
- Validates agentId is a positive integer
- Prevents empty object bugs with strict validation

### 3. **Audit Trail**
- Archives agent data before deletion in `oceanAgentsArchive` collection
- Stores deletion metadata (deletedBy, deletedAt, deletionComment)
- Maintains original agentId for reference

### 4. **Session Management**
- Invalidates all agent refresh tokens
- Prevents deleted agents from logging in again

### 5. **Verification Steps**
- Double-checks deletion was successful
- Verifies agent no longer exists in database
- Prevents partial deletions

## Edge Cases Handled

### 1. **Empty Object Bug Prevention**
- Strict validation of request body
- Checks for empty objects before processing
- Validates all required fields exist

### 2. **Invalid Agent ID**
- Validates agentId is a number
- Ensures agentId is positive
- Checks for NaN values after parsing

### 3. **Inactive User Account**
- Prevents operations by inactive users
- Returns appropriate error message

### 4. **Agent with Active Sessions**
- Checks for active calls (`isCalling = true`)
- Checks for ongoing verifications (`status = "ongoing"`)
- Prevents data inconsistency

### 5. **Archive Failure Handling**
- Continues with deletion even if archive fails
- Logs error for manual review
- Ensures operation completes

### 6. **Token Deletion Failure**
- Continues with agent deletion
- Logs warning for manual cleanup
- Prevents operation from failing

### 7. **Deletion Verification**
- Confirms deletion was successful
- Checks deleteCount from database
- Verifies agent no longer exists

## Related Collections

### Collections Modified
1. **oceanAgents** - Agent record deleted
2. **agentsRrefreshToken** - All refresh tokens deleted
3. **oceanAgentsArchive** - Archive record created

### Collections Checked (Not Modified)
1. **customerVerifications** - Checked for active calls and ongoing sessions
2. **trulogusers** - Verified user exists and is active

## Example cURL Request

```bash
curl -X DELETE https://your-domain.com/user/deleteAgent \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agentId": 123456,
    "comment": "Agent is no longer needed for this project and has completed all assigned tasks."
  }'
```

## Testing Scenarios

### Test Case 1: Successful Deletion
```json
{
  "agentId": 123456,
  "comment": "This is a valid deletion comment with sufficient length."
}
```
**Expected**: 200 OK with success message

### Test Case 2: Short Comment
```json
{
  "agentId": 123456,
  "comment": "Too short"
}
```
**Expected**: 400 Bad Request - Comment must be at least 10 characters

### Test Case 3: Missing Comment
```json
{
  "agentId": 123456
}
```
**Expected**: 400 Bad Request - Comment is required

### Test Case 4: Invalid Agent ID
```json
{
  "agentId": -1,
  "comment": "This is a valid deletion comment."
}
```
**Expected**: 400 Bad Request - Agent ID must be positive

### Test Case 5: Non-existent Agent
```json
{
  "agentId": 999999999,
  "comment": "This is a valid deletion comment."
}
```
**Expected**: 404 Not Found - Agent does not exist

### Test Case 6: Agent with Active Calls
```json
{
  "agentId": 123456,
  "comment": "This is a valid deletion comment."
}
```
**Expected**: 403 Forbidden - Cannot delete agent with active calls

## Production Readiness Checklist

- ✅ Comprehensive input validation
- ✅ Authentication and authorization
- ✅ Ownership verification
- ✅ Active session checks
- ✅ Data archiving for audit trail
- ✅ Session invalidation
- ✅ Deletion verification
- ✅ Empty object bug prevention
- ✅ Detailed error messages
- ✅ Logging for debugging
- ✅ Transaction-like behavior (archive before delete)
- ✅ Graceful error handling
- ✅ No side effects on failure
- ✅ CORS support
- ✅ RESTful design

## Notes

1. **Archive Collection**: The `oceanAgentsArchive` collection must exist in your database. If it doesn't exist, MongoDB will create it automatically on first insert.

2. **Deletion is Permanent**: While the agent data is archived, the deletion from `oceanAgents` is permanent. Ensure the comment field is meaningful for future reference.

3. **Session Invalidation**: All refresh tokens for the agent are deleted, ensuring the agent cannot log in again even if they had active sessions.

4. **No Cascade Delete**: The API does not delete historical records in `customerVerifications` or `callVerifications`. This preserves audit trail and historical data.

5. **Idempotency**: Attempting to delete an already deleted agent will return a 404 error, making the operation safe to retry.

## Maintenance

- Monitor `oceanAgentsArchive` collection size
- Implement archive cleanup policy if needed
- Review deletion logs regularly
- Update validation rules as business requirements change
