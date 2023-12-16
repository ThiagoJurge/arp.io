# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos de dependências e instale-os
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos do seu projeto
COPY . /app

# Defina a variável de ambiente para informar ao Flask como executar
ENV FLASK_APP=backend/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Exponha a porta em que o Flask será executado
EXPOSE 81

# Comando para rodar a aplicação
CMD ["flask", "run"]
