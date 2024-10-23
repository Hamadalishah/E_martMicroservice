FROM python:3.12

LABEL maintainer="Syed Hamad Ali"
# Set the working directory in the container
WORKDIR /code
# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \ 
    && rm -rf /var/lib/apt/lists/*


RUN curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /code
COPY . /code/

# Configuration to avoid creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false

# Install dependencies including development ones
RUN poetry install

# Make port 8000 available to the world outside this container
EXPOSE 8000

CMD ["dapr", "run", "--app-id", "product_service", "--dapr-http-port", "3500", "--app-port", "8000", "--", "poetry", "run", "uvicorn", "product_service.main:app", "--host", "0.0.0.0", "--reload"]

