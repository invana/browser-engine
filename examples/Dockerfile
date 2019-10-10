# docker build -t browser-engine-image .
# docker run -d -p 5000:5000 --name browser-engine-8 browser-engine-image
FROM python:3.7-stretch
RUN pip install browser-engine==0.0.5
CMD python3 -m browser_engine.server.app