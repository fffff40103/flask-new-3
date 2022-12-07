FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
# highlight-start
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# highlight-end
COPY . .
# highlight-start
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
# highlight-end