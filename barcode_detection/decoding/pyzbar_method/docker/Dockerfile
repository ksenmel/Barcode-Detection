FROM python:3.10

WORKDIR /workspace

RUN apt update && apt-get install -y libzbar0 libgl1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py

ENTRYPOINT ["python3", "main.py"]