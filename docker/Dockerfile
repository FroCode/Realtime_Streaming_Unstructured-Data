# Use the Bitnami Spark image as the base
FROM bitnami/spark:latest

# Switch to root to install dependencies
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /opt/bitnami/spark

# Copy dependencies
COPY requirements.txt .

# Install required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy Spark job scripts
COPY jobs /opt/bitnami/spark/jobs/

# Copy input files
COPY input /opt/bitnami/spark/input/

# Ensure correct permissions
RUN chmod -R 777 /opt/bitnami/spark

# Default command to submit the Spark job
CMD ["spark-submit", "--master", "spark://spark-master:7077", "/opt/bitnami/spark/jobs/main.py"]
