# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port the app runs on
EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"] 