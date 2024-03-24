# Using the official Python slim image
FROM python:3.11-slim AS builder-image

# Set the working directory
WORKDIR /home/myuser

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential libssl-dev libffi-dev libgrpc-dev \
    gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav \
    libgstreamer1.0-dev libsdl2-dev libsdl2-mixer-dev \
    libsdl2-ttf-dev libsdl2-image-dev libpango1.0-dev libpangocairo-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir wheel setuptools pillow Cython==0.29.36
RUN pip3 install --no-cache-dir mpf==0.57.0 mpf-mc==0.57.0 mpf-monitor==0.57.0
RUN pip3 install --no-cache-dir --force-reinstall -Iv grpcio==1.62.1

# Runner image
FROM python:3.11-slim AS runner-image

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libsdl2-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \
    libsdl2-image-2.0-0 libpango1.0-0 libpangocairo-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a user and copy the virtual environment from the builder image
RUN useradd --create-home myuser
COPY --from=builder-image /home/myuser/venv /home/myuser/venv

# Set user and working directory
USER myuser
WORKDIR /home/myuser/code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# Set the default command
CMD ["mpf", "--version"]
