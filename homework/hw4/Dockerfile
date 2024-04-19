# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Install the pre-reqs
ADD requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Add the code as the last Docker layer because it changes the most
ADD main.py  /app/main.py

# Run main.py when the container launches
CMD ["python", "main.py", "--epochs", "1"]


