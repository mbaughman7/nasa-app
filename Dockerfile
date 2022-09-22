FROM python:3.10
COPY . /app
RUN pip install requests tk matplotlib PrettyTable

WORKDIR /app
CMD ["python", "./terminal_app.py"]