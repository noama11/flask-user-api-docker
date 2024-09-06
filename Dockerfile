# Use an official Python 3.10 runtime as a parent image
FROM python:3.10.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . . 
# Expose port 5000 to the outside world
EXPOSE 4000


# Run app.py when the container launches
# CMD ["python", "app.py"]
# CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0 --port=4000"]
