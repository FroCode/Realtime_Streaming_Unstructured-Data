FROM bitnami/spark:latest

# Install Python and pip (if not already included in the base image)
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Install additional dependencies (e.g., Python libraries)
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy any additional scripts or files into the container
COPY ./jobs/* /opt/bitnami/spark/jobs
COPY ./input/* /opt/bitnami/spark/input

# Set the working directory
WORKDIR /opt/bitnami/spark

# Optionally run the script automatically when the container starts
CMD ["spark-submit", "--master", "spark://spark-master:7077", "/opt/bitnami/spark/jobs/main.py"]
