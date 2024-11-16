FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir osmnx
COPY graphml_generator.py .
CMD ["python", "graphml_generator.py"]
