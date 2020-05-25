FROM python:3.7-slim

# Install Net tools
RUN apt-get update && apt-get install -y netcat

# Set Working Directory
WORKDIR /opt/app

# Install Python Requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy Application files to Working Directory
ADD app .
EXPOSE 5000

CMD bash run.sh