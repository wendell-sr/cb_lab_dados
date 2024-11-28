# Usar uma imagem Python como base
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para manter o contêiner ativo
CMD ["tail", "-f", "/dev/null"]
