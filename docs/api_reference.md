# API Reference

## Introduction

The MedAI-Core API provides a set of endpoints for interacting with the system. This document outlines the available endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:5000/api/v1
```

## Endpoints

### 1. User Registration

- **Endpoint**: `/users/register`
- **Method**: `POST`
- **Request Body**:

```json
1   {
2     "username": "string",
3     "password": "string",
4     "email": "string"
5   }
```

- Response:

- 201 Created: User registered successfully.
- 400 Bad Request: Validation errors.

2. Health Data Submission

- **Endpoint**: /users/{userId}/health-data
- **Method**: POST
- **Request Body**:

```json
1 {
2   "heart_rate": 72,
3   "blood_pressure": "120/80",
4   "temperature": 98.6
5 }
```

- Response:

- 200 OK: Health data submitted successfully.
- 404 Not Found: User not found.

3. Get User Profile

- **Endpoint**: /users/{userId}
- **Method**: GET

- Response:

```json
1  {
2    "username": "string",
3    "email": "string",
4    "health_metrics": {
5    "heart_rate": 72,
6    "blood_pressure": "120/80"
7   }
8 }
```

- Response Codes:

- 200 OK: User profile retrieved successfully.
- 404 Not Found: User not found.

4. Virtual Assistant Interaction

- **Endpoint**: /assistant/chat
- **Method**: POST
- **Request Body**:

```json
1  {
2  "userId": "string",
3  "message": "string"
4  }
```
- Response:

```json
1 {
2   "response": "string"
3 }
```

- Response Codes:

- 200 OK: Response from the virtual assistant.
- 400 Bad Request: Invalid input.

# Conclusion

This API reference provides a comprehensive overview of the endpoints available in the MedAI-Core system. For further details, please refer to the source code and documentation.
