# Usa a imagem base do Python 3.11 slim
FROM python:3.11-slim

# Define a variável de ambiente para que a saída do Python não seja armazenada em buffer
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos do diretório atual para o diretório de trabalho no container
COPY . /app

# Instala as dependências necessárias usando pip, sem armazenar cache
RUN pip install --no-cache-dir flask pandas

# Expõe a porta 5000 para acesso externo
EXPOSE 5000

# Define o comando padrão a ser executado quando o container iniciar
CMD ["python3"]
