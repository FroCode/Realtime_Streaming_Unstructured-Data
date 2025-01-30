FROM bitnami/spark:latest

# Install additional dependencies (e.g., Python libraries)
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy any additional scripts or files into the container
COPY ./jobs/* /opt/bitnami/spark/jobs
COPY ./input/* /opt/bitnami/spark/input

# Set the working directory
WORKDIR /opt/bitnami/spark

# Optionally run the script automatically when the container starts
CMD ["spark-submit", "--master", "spark://spark-master:7077", "/opt/bitnami/spark/jobs/main.py"]

