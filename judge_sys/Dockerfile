FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    openjdk-11-jdk \
    g++ \
    && apt-get clean

# Set working directory
WORKDIR /judge

# Copy the judging script and test cases
COPY judge.py /judge/judge.py
COPY test_cases /judge/test_cases

# Ensure the judge script is executable
RUN chmod +x /judge/judge.py

# Set the entry point to the judge script
ENTRYPOINT ["python3", "judge.py"]

