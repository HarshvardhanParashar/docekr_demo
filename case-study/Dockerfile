#base image
FROM python:3.12-slim

#Install java 21
RUN apt-get update && apt-get install -y\
   openjdk-21-jdk \
   wget \
   curl \
   && rm -rf /var/lib/apt/lists/*

#SET JAVA HOME
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

#SPARK VERSION
ENV SPARK_VERSION=3.5.6

#DOWNLOAD SPARK
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

#SPARK ENVIRONMENT
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Working Directory
WORKDIR /workspace

# Install Python Packages
COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

# Jupyter Port
EXPOSE 8080

# Start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8080", "--no-browser", "--allow-root"]