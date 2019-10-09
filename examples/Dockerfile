# docker build -t browser-engine-image .
# docker run -d --name browser-engine browser-engine-image
FROM python:3.7-stretch
RUN pip install browser-engine
CMD python3 -m browser_engine.server.app