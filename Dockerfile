FROM python:3.9-slim-buster
COPY . .
RUN rm -rf .git/ Dockerfile README.md \
    && python -m pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "4433" ]