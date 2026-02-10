FROM python:3.12-slim

WORKDIR /app

# Copia tudo que precisas
COPY pkm-sim-commons/ /pkm-sim-commons/
COPY pkm-sim-api/requirements.txt .

# Instala com pip
RUN pip install --no-cache-dir /pkm-sim-commons
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY pkm-sim-api/src/ src/
COPY pkm-sim-api/.env .env

EXPOSE 8000

CMD ["uvicorn", "src.pkm_sim_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]