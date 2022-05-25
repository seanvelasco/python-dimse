FROM python:3.10-slim-buster

WORKDIR /dicom

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py main.py
COPY scu.py scu.py

CMD [ "python3" , "main.py" ]