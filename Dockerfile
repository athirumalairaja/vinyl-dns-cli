FROM python:bullseye
WORKDIR /app
COPY . ./
# COPY requirements.txt . 
# RUN pip3 install -r requirements.txt
RUN pip3 install .
# ENTRYPOINT ["python3", "vinylcli.py"]