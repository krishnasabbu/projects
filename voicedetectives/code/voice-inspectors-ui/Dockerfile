# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install build dependencies for PyAudio
RUN apt-get update && apt-get install -y \
    gcc \
    libportaudio2 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Install PulseAudio and dependencies
RUN apt-get update && apt-get install -y \
    pulseaudio \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Install ffmpeg and other necessary dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install production dependencies.
RUN pip install --upgrade -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --chdir app app:app
ENTRYPOINT ["streamlit", "run", "app/streamdeepfake.py", "--server.port=8080", "--server.address=0.0.0.0"]