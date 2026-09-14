# Setup development environment
install:
    cd backend && uv sync

# Run backend development server
dev-backend:
    cd backend && uv run uvicorn src.main:app --reload

# Run tests
test:
    cd backend && uv run pytest
