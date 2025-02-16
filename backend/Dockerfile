FROM python:3.10-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables for better CPU performance
ENV OMP_NUM_THREADS=4 \
    MKL_NUM_THREADS=4 \
    NUMEXPR_NUM_THREADS=4 \
    OPENBLAS_NUM_THREADS=4

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "src/app.py"] 