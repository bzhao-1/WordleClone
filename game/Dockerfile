FROM python:3.7-alpine

WORKDIR /usr/src/app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

EXPOSE 5000

CMD ["python3", "api.py"]