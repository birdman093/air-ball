FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install awslambdaric
RUN pip install -r requirements.txt
COPY . .
# Non-AWS Lambda container
# CMD [ "python", "./lambda_function.py" ] 
# AWS Lambda Container
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "lambda_function.handler" ]