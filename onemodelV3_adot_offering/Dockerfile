FROM python:3.10.13-slim-bookworm

WORKDIR /var/task

ARG PHASE="dev"
ENV PHASE=$PHASE

ARG GRADIO_SERVER_PORT=8080
ENV GRADIO_SERVER_PORT=$GRADIO_SERVER_PORT

COPY requirements.txt  ./requirements.txt
RUN python -m pip install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org -r requirements.txt

COPY run.py  ./
CMD ["python3", "run.py"]