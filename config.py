import os

class Config:
    # Lê a URL do banco de dados da variável de ambiente DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:Oct081098#@localhost/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
