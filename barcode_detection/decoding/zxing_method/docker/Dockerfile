FROM python:3.9

WORKDIR /workspace
RUN python3 -m pip install zxing
RUN python3 -m pip install Pillow
RUN apt update
RUN apt-get install -y default-jre

COPY main.py main.py

ENTRYPOINT ["python3", "main.py"]