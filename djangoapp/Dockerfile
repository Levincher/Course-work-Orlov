FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app ./
COPY mysite ./
COPY manage.py ./
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ENTRYPOINT ["entrypoint.sh"]