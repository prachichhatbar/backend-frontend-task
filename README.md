# Movie Database Project

Full-stack project with Django REST API backend and Vue.js frontend.

## Backend - Django REST API

Django REST Framework API for posts with infinite scrolling functionality.

### Features
- Posts ordered by timestamp (latest first)
- Up to 3 latest comments per post
- Pagination support for infinite scrolling
- Optimized queries to avoid N+1 problems

### Setup
```bash
cd backend_repo
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### API Endpoint
```
GET /api/posts/
GET /api/posts/?page=2
GET /api/posts/?page_size=20
```

### Response Format
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "uuid",
            "text": "Post content",
            "timestamp": "2025-07-31T10:07:12.341908Z",
            "username": "testuser",
            "comment_count": 4,
            "latest_comments": [
                {
                    "text": "Comment text",
                    "timestamp": "2025-07-31T10:07:12.401714Z",
                    "username": "testuser"
                }
            ]
        }
    ]
}
```

## Frontend - Vue.js Movie Page

Recreation of TMDB movie page layout using Vue.js and OMDB API.

### Features
- Responsive design (mobile, tablet, desktop)
- Real movie data from OMDB API
- Interactive rating system
- Quick action buttons

### Setup
```bash
cd frontend/movie-app
open index.html  # Or double-click the file
```

### Improvements Made
1. **Enhanced Rating Modal** - Interactive 10-star rating system with hover effects
2. **Quick Action Buttons** - Floating share and scroll-to-top buttons

### Tech Stack
- Vue.js 3 (via CDN)
- Vanilla CSS with modern design patterns
- OMDB API integration

## Project Structure
```
├── backend_repo/           # Django REST API
│   ├── apps/demo/         
│   │   ├── models.py      # Post and Comment models
│   │   ├── serializers.py # API serializers
│   │   ├── views.py       # API views
│   │   └── tests.py       # API tests
│   └── manage.py
├── frontend/
│   └── movie-app/
│       └── index.html     # Vue.js movie page
└── README.md
```

## Demo
- Backend API: http://127.0.0.1:8000/api/posts/
- Frontend: Open frontend/movie-app/index.html in browser
