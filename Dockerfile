FROM python:3-onbuild
RUN apt-get update && apt-get install -y python3-pip python3-dev && apt-get install -y libsm6 libxext6 libxrender-dev

RUN apt-get install -y tesseract-ocr

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["./api.py"]
