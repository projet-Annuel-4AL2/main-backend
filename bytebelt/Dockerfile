FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

WORKDIR /bytebelt

# Install dependencies
COPY requirements.txt /bytebelt/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bytebelt/


# Command to run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
