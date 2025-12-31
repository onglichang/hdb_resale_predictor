# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/

# Copy MLflow artifacts (the trained model)
# In production, this would ideally be pulled from a remote artifact store (S3/GCS)
# but for this standalone container, we embed it.
COPY mlruns/ mlruns/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
