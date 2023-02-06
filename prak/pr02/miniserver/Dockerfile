FROM python:slim-buster
RUN pip install Flask colorhash
COPY index.py .
COPY miniwhoami.py .
CMD flask --app index run -h :: -p 80