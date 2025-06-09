FROM python:3.9-slim
WORKDIR /bot

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Updating pip before installing dependencies
RUN pip install --upgrade pip

# Copying and installing Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying the source code
COPY . .

# Launching the bot
CMD ["python", "main.py"]