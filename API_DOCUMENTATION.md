# Personal Budgeting API Documentation

## Overview

The Personal Budgeting API is a RESTful service that allows users to manage budgets, track expenses, and generate financial reports. The API uses JWT authentication for security and provides comprehensive endpoints for all budgeting operations.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://yourdomain.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid JWT token in the Authorization header.

### Authentication Flow

1. **Register** a new user account
2. **Login** to receive access and refresh tokens
3. **Use** the access token for authenticated requests
4. **Refresh** the access token when it expires

### Headers

```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Endpoints

### Authentication Endpoints

#### User Registration
```http
POST /api/register/
```

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-01-15T10:30:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### User Login
```http
POST /api/login/
```

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "securepass123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-01-15T10:30:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### JWT Token Refresh
```http
POST /api/token/refresh/
```

**Request Body:**
```json
{
    "refresh": "your_refresh_token_here"
}
```

**Response:**
```json
{
    "access": "new_access_token_here"
}
```

#### User Profile
```http
GET /api/profile/
PUT /api/profile/
```

**GET Response:**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-01-15T10:30:00Z"
}
```

**PUT Request Body:**
```json
{
    "first_name": "Johnny",
    "last_name": "Smith"
}
```

### Budget Endpoints

#### List Budgets
```http
GET /api/budgets/
```

**Query Parameters:**
- `page`: Page number for pagination
- `page_size`: Number of items per page (default: 20)

**Response:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": "john_doe",
            "name": "Monthly Groceries",
            "total_amount": "500.00",
            "category": "Food",
            "created_at": "2025-01-15T10:30:00Z",
            "updated_at": "2025-01-15T10:30:00Z",
            "remaining_amount": "325.00",
            "spent_percentage": 35.0
        }
    ]
}
```

#### Create Budget
```http
POST /api/budgets/
```

**Request Body:**
```json
{
    "name": "Monthly Entertainment",
    "total_amount": "200.00",
    "category": "Entertainment"
}
```

**Response:**
```json
{
    "id": 2,
    "user": "john_doe",
    "name": "Monthly Entertainment",
    "total_amount": "200.00",
    "category": "Entertainment",
    "created_at": "2025-01-15T11:00:00Z",
    "updated_at": "2025-01-15T11:00:00Z",
    "remaining_amount": "200.00",
    "spent_percentage": 0.0
}
```

#### Get Budget Details
```http
GET /api/budgets/{id}/
```

**Response:**
```json
{
    "id": 1,
    "user": "john_doe",
    "name": "Monthly Groceries",
    "total_amount": "500.00",
    "category": "Food",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z",
    "remaining_amount": "325.00",
    "spent_percentage": 35.0
}
```

#### Update Budget
```http
PUT /api/budgets/{id}/
PATCH /api/budgets/{id}/
```

**Request Body:**
```json
{
    "name": "Updated Groceries Budget",
    "total_amount": "600.00",
    "category": "Food"
}
```

#### Delete Budget
```http
DELETE /api/budgets/{id}/
```

**Response:**
```json
{
    "message": "Budget deleted successfully"
}
```

### Expense Endpoints

#### List Expenses
```http
GET /api/expenses/
```

**Query Parameters:**
- `category`: Filter by expense category
- `date`: Filter by specific date (YYYY-MM-DD)
- `budget`: Filter by budget ID
- `search`: Search in description and category
- `ordering`: Sort by field (date, amount, created_at)
- `page`: Page number for pagination

**Response:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "budget": {
                "id": 1,
                "user": "john_doe",
                "name": "Monthly Groceries",
                "total_amount": "500.00",
                "category": "Food",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:30:00Z",
                "remaining_amount": "325.00",
                "spent_percentage": 35.0
            },
            "user": "john_doe",
            "description": "Grocery shopping",
            "amount": "75.50",
            "date": "2025-01-15",
            "category": "Food",
            "created_at": "2025-01-15T10:30:00Z",
            "updated_at": "2025-01-15T10:30:00Z"
        }
    ]
}
```

#### Create Expense
```http
POST /api/expenses/
```

**Request Body:**
```json
{
    "budget_id": 1,
    "description": "Restaurant dinner",
    "amount": "45.00",
    "date": "2025-01-15",
    "category": "Food"
}
```

#### Get Expense Details
```http
GET /api/expenses/{id}/
```

#### Update Expense
```http
PUT /api/expenses/{id}/
PATCH /api/expenses/{id}/
```

#### Delete Expense
```http
DELETE /api/expenses/{id}/
```

### Report Endpoints

#### Monthly Report
```http
GET /api/reports/monthly/
```

**Query Parameters:**
- `month`: Month number (1-12, default: current month)
- `year`: Year (default: current year)

**Response:**
```json
{
    "month": 1,
    "year": 2025,
    "period": "2025-01-01 to 2025-01-31",
    "summary": {
        "total_budget": 700.0,
        "total_expenses": 245.0,
        "remaining_budget": 455.0,
        "spent_percentage": 35.0
    },
    "expenses_by_category": [
        {
            "category": "Food",
            "total": 175.0
        },
        {
            "category": "Transport",
            "total": 70.0
        }
    ],
    "budget_vs_actual": [
        {
            "budget_name": "Monthly Groceries",
            "category": "Food",
            "budgeted_amount": 500.0,
            "actual_amount": 175.0,
            "remaining_amount": 325.0,
            "spent_percentage": 35.0
        }
    ]
}
```

#### Weekly Report
```http
GET /api/reports/weekly/
```

**Query Parameters:**
- `weeks_ago`: Number of weeks ago (default: 0 for current week)

**Response:**
```json
{
    "week_start": "2025-01-13",
    "week_end": "2025-01-19",
    "period": "2025-01-13 to 2025-01-19",
    "summary": {
        "total_budget": 700.0,
        "total_expenses": 120.0,
        "remaining_budget": 580.0,
        "spent_percentage": 17.14
    },
    "daily_expenses": [
        {
            "date": "2025-01-15",
            "total": 75.0
        },
        {
            "date": "2025-01-17",
            "total": 45.0
        }
    ],
    "expenses_by_category": [
        {
            "category": "Food",
            "total": 120.0
        }
    ]
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### Common Error Responses

#### 400 Bad Request
```json
{
    "field_name": [
        "This field is required."
    ]
}
```

#### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
    "detail": "Not found."
}
```

#### 500 Internal Server Error
```json
{
    "detail": "Internal server error."
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- **Authentication endpoints**: 5 requests per minute
- **Other endpoints**: 100 requests per hour per user

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

## Filtering and Search

### Expense Filtering
- **Category**: Filter by expense category
- **Date**: Filter by specific date
- **Budget**: Filter by budget ID
- **Search**: Full-text search in description and category

### Budget Filtering
- **Category**: Filter by budget category
- **Date**: Filter by creation date

## Data Validation

### Budget Validation
- **Name**: Required, max 100 characters
- **Total Amount**: Required, positive decimal
- **Category**: Required, max 100 characters

### Expense Validation
- **Budget ID**: Required, must exist and belong to user
- **Description**: Required, max 200 characters
- **Amount**: Required, positive decimal
- **Date**: Required, cannot be in the future
- **Category**: Required, max 100 characters

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **User Isolation**: Users can only access their own data
- **Input Validation**: Comprehensive validation of all inputs
- **HTTPS Required**: Production endpoints require HTTPS
- **CORS Protection**: Configurable cross-origin resource sharing

## Best Practices

### Authentication
1. Store JWT tokens securely
2. Refresh tokens before they expire
3. Never expose refresh tokens in client-side code

### Error Handling
1. Always check HTTP status codes
2. Handle validation errors gracefully
3. Implement retry logic for transient failures

### Performance
1. Use pagination for large datasets
2. Implement caching where appropriate
3. Minimize API calls by batching requests

## Support

For API support and questions:
- **Documentation**: This file
- **Issues**: GitHub repository issues
- **Email**: support@yourdomain.com

## Versioning

The API follows semantic versioning (SemVer):
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

Current version: **1.0.0**
