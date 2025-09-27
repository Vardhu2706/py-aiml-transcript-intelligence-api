FROM python:3.11-slim-bookworm
WORKDIR /code
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code
RUN chmod +x worker/run_worker.sh
CMD ["sh", "-c", "./worker/run_worker.sh"]