# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements_app.txt .
RUN pip install --no-cache-dir -r requirements_app.txt

# Copy your app code into the container
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run the Streamlit app, ensuring it listens on all interfaces
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
