FROM public.ecr.aws/lambda/python:3.11-x86_64

COPY requirements.txt ./

RUN python3.11 -m pip install pip --upgrade
RUN python3.11 -m pip install -r requirements.txt -t .

COPY app.py ./
COPY machine_generator_app.py ./

CMD ["app.index"]
