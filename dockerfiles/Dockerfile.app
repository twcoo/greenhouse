# Stage 1: Build stage
FROM python:3.12-slim-bookworm AS builder

# Install necessary packages
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  curl ca-certificates && \
  rm -rf /var/lib/apt/lists/*

# Download the uv latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the uv installer
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy project files to install dependencies
WORKDIR /backend
COPY pyproject.toml uv.lock ./ 

# Create requirements file 
RUN uv export --no-dev \
  --no-editable \
  --no-hashes \
  --frozen \
  -o requirements.txt

# Stage 2: Final stage
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PYTHONDONTWRITEBYTECODE=1

# Add non-root user
RUN groupadd user && \ 
  useradd --create-home --home-dir /home/user -g user user

# Copy requirements.txt from builder stage
COPY --from=builder /backend/requirements.txt /backend/requirements.txt

# Set working directory
WORKDIR /backend

# Install dependencies
RUN pip install --no-cache-dir -r /backend/requirements.txt

# Copy backend code
COPY backend/ /backend
COPY .env /backend

# Ensure the backend runs as the non-root user
USER user

# Start Django server
CMD ["sh", "-c", "python manage.py initial_setup  && \
  python manage.py runserver 0.0.0.0:8000"]
