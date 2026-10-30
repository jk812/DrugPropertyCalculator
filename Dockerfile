FROM python:3.12-slim

ENV MPLBACKEND=Agg \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
RUN pip install --no-cache-dir ".[dev]"

COPY tests/ ./tests/
COPY scripts/ ./scripts/
COPY data/raw/ ./data/raw/

CMD ["python", "-c", "import property_prediction; print('property_prediction ready')"]