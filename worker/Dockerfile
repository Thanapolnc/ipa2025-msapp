FROM python

WORKDIR /home/myapp

COPY . /home/myapp

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt


CMD ["python", "-u" , "worker.py"]