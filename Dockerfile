FROM python:3.9-slim

# Diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências do sistema, SQLite CLI e cURL
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    && apt-get clean

# Instalar dependências do Python
RUN pip install --no-cache-dir pandas flask

# Copiar o código do projeto
COPY src/ src/
COPY data/ data/

# Configurar o PYTHONPATH
ENV PYTHONPATH=/app

# Manter o contêiner ativo e executar os serviços
CMD ["sh", "-c", "python src/initialize_database.py && python src/api.py && tail -f /dev/null"]
