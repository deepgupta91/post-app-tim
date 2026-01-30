# Simple Social - Setup & Run Instructions

## Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- ImageKit account (for image/video hosting)

## Setup Instructions

### 1. Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
IMAGEKIT_URL_ENDPOINT=your_imagekit_url_endpoint
```

Replace with your actual values:
- `DATABASE_URL`: PostgreSQL connection string
- ImageKit credentials from your ImageKit dashboard

### 4. Run the Backend Server
```bash
python main.py
```

The backend API will start on `http://localhost:8000`

### 5. Run the Frontend (in a new terminal)
Make sure your virtual environment is activated, then:

```bash
streamlit run frontend.py
```

The frontend will start on `http://localhost:8501`

## API Endpoints

- **Auth**
  - `POST /auth/jwt/login` - Login with email/password
  - `POST /auth/register` - Register new user
  - `POST /auth/reset-password` - Reset password
  - `POST /auth/verify` - Verify email

- **Users**
  - `GET /users/me` - Get current user info
  - `GET /users/{id}` - Get user by ID

- **Posts**
  - `POST /upload` - Upload image/video with caption
  - `GET /feed` - Get feed of all posts
  - `DELETE /posts/{id}` - Delete a post

## Project Structure

```
yt-proj-2/
├── main.py              # Backend server entry point
├── frontend.py          # Streamlit frontend
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── app/
    ├── app.py          # FastAPI application
    ├── db.py           # Database models & session
    ├── users.py        # User authentication
    ├── schema.py       # Pydantic schemas
    └── images.py       # ImageKit configuration
```

## Troubleshooting

- **Database connection error**: Verify `DATABASE_URL` in `.env`
- **ImageKit errors**: Check ImageKit credentials in `.env`
- **Port already in use**: Change port in `main.py` or kill process using port 8000/8501
