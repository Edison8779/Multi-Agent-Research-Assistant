# Setup development environment
install:
    cd backend && uv sync
    cd frontend && npm install

# Run backend development server
dev-backend:
    cd backend && uv run uvicorn app.main:app --reload --port 8000

# Run frontend development server
dev-frontend:
    cd frontend && npm run dev

# Run tests
test:
    cd backend && uv run pytest

