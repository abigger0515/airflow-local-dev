FROM apache/airflow:2.5.3

COPY new_requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r new_requirements.txt