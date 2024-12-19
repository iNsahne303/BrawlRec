FROM python:3
COPY src/requirements /root/
RUN pip install -r /root/requirements && useradd -m user
ENV HOME=/home/user
USER user
COPY src/* /home/user/
WORKDIR /home/user/
EXPOSE 8080
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
