# syntax=docker/dockerfile:1

# Start with a Container binary that already has Python and pyodbc installed
FROM laudio/pyodbc

# Create a Working directory for the application
WORKDIR /flask2sql

# Copy all of the code from the current directory into the WORKDIR
COPY . .

# Install the  libraries that are required
RUN pip install -r ./requirements.txt

# Once the container starts, run the application, and open all TCP/IP ports 
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]