# Step 1: Use an official Python base image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install dependencies
# Only copy the requirements file first to take advantage of Docker's layer caching
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Expose the FastAPI default port
EXPOSE 8000

# Step 5: Set the command to run FastAPI
CMD ["uvicorn", "shareFile:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

