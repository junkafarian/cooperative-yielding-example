FROM lystable/python:3.5v0.3
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --user -r requirements.txt

ENV PATH $PATH:/root/.local/bin

COPY . /src

CMD ["bash"]
