# Basic Python image
FROM python:3.12

# Environment configuration for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv package manager for dependency management
RUN pip install uv

# Copy dependency metadata and install locked dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy application source code
COPY . .

# Run application entrypoint
CMD ["python", "main.py"]