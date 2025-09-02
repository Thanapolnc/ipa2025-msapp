FROM python

WORKDIR /home/myapp

COPY . /home/myapp

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt


EXPOSE 15672

CMD ["python", "-u" , "scheduler.py"]