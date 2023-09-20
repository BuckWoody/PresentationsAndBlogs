# syntax=docker/dockerfile:1

# Start with a Container binary that already has Python and pyodbc installed
FROM laudio/pyodbc

# Create a Working directory for the application
WORKDIR /flask2sql

# Install the other two libraries that are required - this could also be done in a "requirements file"
RUN pip install Flask
RUN pip install configparser

# Copy all of the code from the current directory into the WORKDIR
COPY . .

# Once the container starts, run the application, and open all TCP/IP ports 
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]