# Trucker Wait List System

A Django web application for managing truck driver check-ins and drug testing queues.

## Features

- Driver check-in form with follow-up functionality
- Queue management system
- Company management
- Status tracking (Waiting, In Progress, Finished)
- Email notifications
- Report generation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd Level1
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up the database
```bash
python manage.py migrate
```

### 6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Environment Variables

The application uses environment variables for configuration. For local development, the following defaults are used:

- `DEBUG=True`
- `SECRET_KEY=django-insecure-local-development-key-change-in-production`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `DATABASE_URL=sqlite:///db.sqlite3`

For production, create a `.env` file with your specific values.

## Usage

### Driver Check-In
- Navigate to the main page to access the driver check-in form
- Fill out driver information and select company
- Check "Are you a Follow Up Driver?" if applicable (automatically assigns "FOLLOW-UP" company)

### Admin Panel
- Access at `http://127.0.0.1:8000/admin/`
- Manage companies, drivers, and system settings

### Queue Management
- Login required for queue management features
- View and update driver statuses
- Generate reports

## Project Structure

```
Level1/
├── TruckerWaitList/     # Django project settings
├── waitapp/            # Main application
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── forms.py        # Form definitions
│   └── templates/      # HTML templates
├── static/             # Static files (CSS, images)
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here] 