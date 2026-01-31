FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    gosu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . .

RUN useradd -m appuser && \
    chown -R appuser:appuser /app /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["sh", "-c", "chown -R appuser:appuser /app/data 2>/dev/null || true; exec gosu appuser \"$@\"", "sh"]
CMD ["python", "api/api.py"]