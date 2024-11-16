FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir osmnx pandas scikit-learn
COPY data.csv ../generate_graphs/*.graphml .
CMD ["python", "map_matching.py"]
