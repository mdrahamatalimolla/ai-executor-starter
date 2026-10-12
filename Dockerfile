# Dockerfile - non-root executor image
FROM python:3.11-slim

# create user
RUN useradd --create-home --shell /bin/bash executor
WORKDIR /home/executor

# copy app
COPY . /opt/executor
RUN chown -R executor:executor /opt/executor
RUN chmod +x /opt/executor/scripts/*.sh

USER executor
WORKDIR /opt/executor

# venv optional: use system python here for simplicity
RUN python3 -m venv venv
ENV PATH="/opt/executor/venv/bin:${PATH}"
RUN /opt/executor/venv/bin/pip install --upgrade pip
RUN /opt/executor/venv/bin/pip install -r requirements.txt

ENV PORT=5000

EXPOSE 5000
CMD ["python3", "app.py"]
