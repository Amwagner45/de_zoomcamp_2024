FROM python

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app/
RUN pip install -r requirements.txt

COPY main.py main.py


ENTRYPOINT [ "python", "/opt/app/main.py"]