FROM python:3.13-alpine

# Step 2: Set working directory
WORKDIR /app
#COPY . /app

# Install system dependencies for MySQL support and building Python packages
RUN apk update && apk add --no-cache \
    build-base \
    mariadb-dev \
    curl \
    libffi-dev \
    musl-dev \
    gcc \
    py3-pip \
    python3-dev \
    linux-headers

# Step 3: Copy app files
COPY requirements.txt .
COPY dependencies.py/ ./dependencies.py
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY models/ ./models/
COPY schemas/ ./schemas/
COPY routers/ ./routers/
COPY alembic/ ./alembic
COPY auth/ ./auth
COPY core/ ./core
COPY media/ ./media
COPY utils/ ./utils
COPY database.py ./database.py
COPY templates/ ./templates/
COPY static/ ./static/


# Expose the port that Uvicorn will run on
EXPOSE 8000

# Step 5: Run FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

