# Basic Python image
FROM python:3.12.6-bookworm

# Environment configuration for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv package manager for dependency management
RUN pip install --no-cache-dir uv

# Copy dependency metadata and install locked dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy application source code
COPY . .

# Run application entrypoint
CMD ["uv", "run", "python", "start_bot.py"]