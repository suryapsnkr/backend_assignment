FROM python:3.12

WORKDIR /backend_assignment

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend_assignment.asgi:application"]
