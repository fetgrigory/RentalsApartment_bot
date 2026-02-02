# Basic Python image
FROM python:3.12

# Environment variables to control Python behavior
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Working directory in the container
WORKDIR /app

# Updating pip and installing wheel
RUN pip install --upgrade pip wheel

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying the source code
COPY . .

# Launching the bot
CMD ["python","-u", "main.py"]