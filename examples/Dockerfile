# docker build -t browser-engine-image .
# docker run -d -p 5000:5000 --name browser-engine-88 browser-engine-image
FROM python:3.7-stretch
RUN pip install browser-engine
CMD python3 -m browser_engine.server.app