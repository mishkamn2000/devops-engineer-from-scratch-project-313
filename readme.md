# URL Shortener Service

FastAPI-based URL shortener service with PostgreSQL database and React frontend, deployed with Nginx.

## Architecture
- **Frontend**: React app served by Nginx
- **Backend**: FastAPI with PostgreSQL
- **Proxy**: Nginx serves static files and proxies API requests
- **Database**: PostgreSQL
- **Monitoring**: Sentry for error tracking

## Features
- Create, read, update, delete short URLs
- Pagination with Content-Range headers
- Sentry error monitoring
- PostgreSQL database
- React frontend
- Docker deployment with Nginx

## Nginx Configuration
Nginx is configured to:
1. Serve React frontend static files from `/app/static`
2. Proxy API requests to FastAPI backend on port 8080
3. Handle redirects for short URLs
4. Provide health checks

## API Endpoints
- `GET /ping` - Health check (returns "pong")
- `GET /api/links` - List links (with pagination via `range` query parameter)
- `POST /api/links` - Create new link
- `GET /api/links/{id}` - Get specific link
- `PUT /api/links/{id}` - Update link
- `DELETE /api/links/{id}` - Delete link
- `GET /r/{short_name}` - Redirect to original URL

## Deployment on Render

### 1. Create Services on Render
- **Web Service** for the application
- **PostgreSQL Database** (free tier)

### 2. Web Service Configuration
- **Build Command**: `docker build -t url-shortener .`
- **Start Command**: `/start.sh`
- **Port**: `80`

### 3. Environment Variables
Set these in your Render Web Service:
- `DATABASE_URL`: From your Render PostgreSQL database
- `PORT`: `80`
- `SENTRY_DSN`: Your Sentry DSN (optional)
- `BASE_URL`: Your Render URL (e.g., `https://your-app.onrender.com`)

### 4. Deployment
Push to GitHub and Render will automatically deploy.

## Local Development

```bash
# Install dependencies
make install

# Run tests
make test

# Run linter
make lint

# Format code
make format

# Run locally (FastAPI only)
make run

# Build Docker image
make docker-build

# Run with Docker (Nginx + FastAPI)
make docker-run