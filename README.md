# Personal Budgeting API

A RESTful backend API for personal budgeting applications built with Django and Django REST Framework. This API allows users to manage budgets, track expenses, and generate financial reports.

## Features

- **User Authentication**: JWT-based login/registration system
- **Budget Management**: Create, update, and delete budgets with categories
- **Expense Tracking**: Log expenses tied to budgets with detailed categorization
- **Financial Reports**: Generate monthly and weekly spending summaries
- **Budget Analytics**: Track remaining budget amounts and spending percentages
- **RESTful API**: Clean, consistent API design following REST principles

## Tech Stack

- **Backend**: Django 4.2.7
- **API Framework**: Django REST Framework 3.14.0
- **Authentication**: JWT tokens (djangorestframework-simplejwt)
- **Database**: SQLite (development), PostgreSQL ready (production)
- **Filtering**: django-filter for advanced querying
- **Python Version**: 3.8+

## Project Structure

```
Personal-Budgeting-API/
├── personal_budgeting_api/     # Main project settings
├── users/                      # User authentication app
├── budgets/                    # Budget management app
├── expenses/                   # Expense tracking app
├── reports/                    # Financial reporting app
├── manage.py                   # Django management script
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Personal-Budgeting-API
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/` - Update user profile

### JWT Token Endpoints
- `POST /api/token/` - Obtain JWT access token
- `POST /api/token/refresh/` - Refresh JWT token

### Budget Endpoints
- `GET /api/budgets/` - List user budgets
- `POST /api/budgets/` - Create new budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget

### Expense Endpoints
- `GET /api/expenses/` - List user expenses
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense

### Report Endpoints
- `GET /api/reports/monthly/` - Monthly financial report
- `GET /api/reports/weekly/` - Weekly financial report

## API Usage Examples

### User Registration
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### User Login
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### Create Budget (with JWT token)
```bash
curl -X POST http://127.0.0.1:8000/api/budgets/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly Groceries",
    "total_amount": "500.00",
    "category": "Food"
  }'
```

### Create Expense
```bash
curl -X POST http://127.0.0.1:8000/api/expenses/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "budget_id": 1,
    "description": "Grocery shopping",
    "amount": "75.50",
    "date": "2025-01-15",
    "category": "Food"
  }'
```

### Get Monthly Report
```bash
curl -X GET "http://127.0.0.1:8000/api/reports/monthly/?month=1&year=2025" \
  -H "Authorization: Bearer <your_jwt_token>"
```

## Data Models

### User Model
- Extends Django's AbstractUser
- Username, email, first_name, last_name
- JWT authentication support

### Budget Model
- User association
- Name, total amount, category
- Automatic calculation of remaining amount and spent percentage
- Timestamps for creation and updates

### Expense Model
- Budget association
- Description, amount, date, category
- User association (inherited from budget)
- Validation for positive amounts and non-future dates

## Features in Detail

### Budget Management
- Create budgets with categories
- Track spending against budgets
- Calculate remaining amounts automatically
- Monitor spending percentages

### Expense Tracking
- Log expenses with detailed descriptions
- Categorize expenses for better organization
- Filter and search expenses
- Date-based expense tracking

### Financial Reporting
- Monthly spending summaries
- Weekly expense breakdowns
- Category-based expense analysis
- Budget vs. actual spending comparison

### Security Features
- JWT-based authentication
- User-specific data isolation
- Input validation and sanitization
- Secure password handling

## Development Timeline

- **Week 1**: Project setup, Django project creation, users app
- **Week 2**: JWT authentication, budget model & API endpoints
- **Week 3**: Expense model & endpoints, testing
- **Week 4**: Reports generation, optional currency API
- **Week 5**: Testing, documentation, deployment preparation

## Future Enhancements

- Currency conversion using external APIs
- Budget templates and recurring budgets
- Advanced analytics and charts
- Mobile app support
- Export functionality (CSV, PDF)
- Multi-currency support
- Budget sharing and collaboration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or support, please open an issue in the repository or contact the development team.

---

**Author**: Brahim Chatri  
**Date**: August 3, 2025  
**Version**: 1.0.0