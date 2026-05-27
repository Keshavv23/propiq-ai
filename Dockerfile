FROM python:3.11-slim

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

# create chroma directory
RUN mkdir -p /app/chroma_store

# expose port
EXPOSE 8000

# start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]