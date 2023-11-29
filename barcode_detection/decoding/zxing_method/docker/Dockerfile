FROM python:3.9

WORKDIR /workspace

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt update && apt install -y default-jre

COPY main.py main.py

ENTRYPOINT ["python3", "main.py"]