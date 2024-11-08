# FastAPI Social Media Application

This project is a **Social Media Application** for an [**Automated Trading System**](https://github.com/Josue-Castellanos/Automated_Trading_System) implemented using **FastAPI**, which includes various social media features like user authentication, post creation, follow system, and a voting system for posts. Built with SQLModel and MySQL, the application is designed to manage various CRUD operations securely and efficiently, aiming to provide a robust user experience.

## Features

### 1. **User Registration & Authentication**
   - Users can register, log in, and manage their accounts.
   - Secure password hashing and token-based authentication are implemented for secure access.
   - Securely register and authenticate users, with JWT-based authentication.
   - Only authenticated users can access certain features.

### 2. **Post Creation and Management**
   - Users can create, update, and delete their posts.
   - Posts include fields like title, content, timestamps, and are linked to the user who created them.

### 3. **Voting System**
   - Users can vote on posts (upvote or downvote).
   - A user cannot vote more than once on the same post.
   - Constraints ensure that if a user has already upvoted a post, they cannot downvote and vice versa.
   - A vote choice is required from the user before a vote is saved.

### 4. **Database Models with SQLModel**
   - Database models use SQLModel, with relationships and constraints set up between models.
   - Composite keys and foreign key constraints ensure data integrity for related entities.
   - Alembic is used for database migrations.

### 5. **Pagination**: 
   - Supports pagination for efficient data retrieval using offset/limit and cursors.

### 6. **Environment Variables for Configuration**
   - Sensitive information (e.g., database URL, JWT secrets) is managed using environment variables for security.

## Technologies Used

- **FastAPI**: For building the backend APIs.
- **SQLModel**: ORM to define and interact with the database.
- **MySQL**: Primary database for the application.
- **Pydantic**: Data validation and parsing.
- **JWT & OAUTH2**: Token Creation and Authentication.
- **Alembic**: Database migrations.
- **Postman**: API Endpoint testing.

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL database setup
- Install dependencies listed in `requirements.txt`

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
host=localhost
user=root
database=fastapi
password=yourpassword
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=30
database_url=mysql+mysqlconnector://{user}:{password}@{host}/{database}
```
### Setup
1. **Clone the Repository**
    ```bash
    git clone https://github.com/Josue-Castellanos/FastAPI-Trading_System.git
    cd FastAPI-Trading_System
    ```
    
2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   
5. **Run database migrations with Alembic**:
   ```bash
   alembic upgrade head
   
6. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   
### API Endpoints

- **POST /register** - Register a new user. Requires `username`, `email`, and `password` fields.

- **POST /login** - Authenticate and obtain a JWT token. Requires `username` and `password`.

- **POST /posts** - Create a new post (authenticated). Requires `title` and `content` fields.

- **GET /posts** - Retrieve all posts. Accepts optional query parameters like `limit` and `offset` for pagination.

- **GET /posts/{post_id}** - Retrieve a single post by its ID.

- **DELETE /posts/{post_id}** - Delete a post by its ID (authenticated and only if the post belongs to the current user).

- **POST /posts/{post_id}/vote** - Vote on a post (authenticated). Requires `vote_type` (`upvote` or `downvote`). Prevents duplicate or conflicting votes.

For full API details and additional endpoints, see the OpenAPI documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
