# Use the official Debian base image
FROM debian:bullseye-slim

# Update the package repository and install necessary packages
RUN apt-get update && \
    apt-get install -y nginx python3 python3-pip

# Install required Python packages
RUN pip3 install IP2Location folium qbittorrent-api schedule

# Create a directory to store the generated index.html file
WORKDIR /app

# Copy the script into the container
COPY main.py /app/main.py

# Make the script executable
RUN chmod +x /app/main.py

# Expose port 6969
EXPOSE 9435

# Copy Nginx configuration file into the container
COPY nginx.conf /etc/nginx/sites-available/my_app.conf

# Create a symbolic link to enable the configuration
RUN ln -s /etc/nginx/sites-available/my_app.conf /etc/nginx/sites-enabled/

# Remove the default Nginx default configuration
RUN rm /etc/nginx/sites-enabled/default
# CMD to start Nginx and run the script in the foreground
CMD service nginx start & /app/main.py