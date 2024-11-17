# Use the official Python image from the Docker Hub
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Install build dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \    
    && rm -rf /var/lib/apt/lists/*

# Set GIT_PYTHON_GIT_EXECUTABLE to ensure GitPython finds Git
ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git
ENV GIT_PYTHON_REFRESH=quiet

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip show GitPython

# Remove build dependencies to keep the image slim
RUN apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--loop", "asyncio"]