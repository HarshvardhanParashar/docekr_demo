FROM python:slim

WORKDIR /pandas_demo

COPY req.txt .
RUN pip install -r req.txt
COPY pandas-demo.py .

CMD ["python", "pandas-demo.py"]