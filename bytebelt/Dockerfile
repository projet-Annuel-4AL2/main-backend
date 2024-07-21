FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

WORKDIR /bytebelt

# Install dependencies
COPY requirements.txt /bytebelt/
#installer psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN apt-get install libpq-dev -y
RUN pip install psycopg
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bytebelt/


# Command to run your Django application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
#mise en production
#CMD ["daphne", "-b", "0.0.0.0", "-p", "$PORT", "bytebelt.asgi:application"]
RUN python manage.py collectstatic --noinput
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p ${PORT} bytebelt.asgi:application"]



# heroku logs --tail -a bytebelt-app  
#docker build --platform linux/amd64 -t bytebelt-app .
#docker tag bytebelt-app registry.heroku.com/bytebelt-app/web
#docker push registry.heroku.com/bytebelt-app/web
#heroku container:release web -a bytebelt-app
#see  heroku ps -a bytebelt-app 
#heroku ps:autoscale web --min=2 --max=10 -a your-app-name

#RUN chmod +x ./start.sh
#CMD ["./start.sh"]