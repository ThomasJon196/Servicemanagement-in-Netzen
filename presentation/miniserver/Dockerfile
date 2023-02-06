FROM python:slim-buster
RUN pip install Flask colorhash
RUN mkdir resources
COPY index.py .
COPY miniwhoami.py .
CMD flask --app index run -h 0.0.0.0
