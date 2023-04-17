FROM python:3.10-bullseye
ENV PATH="/usr/app/scripts:${PATH}"
RUN apt-get update && apt-get -y install cron && apt-get -y install pip

RUN touch /var/log/cron.log
# Setup cron job
RUN (crontab -l ; echo "* * * * * echo "Hello world" >> /var/log/cron.log") | crontab

COPY . /usr/app/
WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt
RUN chmod +x /usr/app/scripts/entrypoint.sh

CMD ["sh","/usr/app/scripts/entrypoint.sh"]
