"""Povoamento sintetico do banco (a implementar).

Requisitos (Secao 7.1 do enunciado):
  - reprodutivel: use uma semente fixa (SEMENTE) em random.Random e em Faker.seed();
  - a maior tabela do esquema com pelo menos 100.000 linhas, nenhuma tabela vazia
    e pelo menos 5 tabelas com 1.000 linhas ou mais;
  - gerar e carregar tudo em ate 10 minutos;
  - respeitar todas as restricoes do esquema;
  - idempotente: pode comecar com TRUNCATE ... CASCADE nas tabelas, ou assumir banco recem-criado por `make esquema`.

Dicas: use common.copiar (COPY) em vez de INSERT linha a linha; gere as tabelas na ordem das chaves estrangeiras.
"""
import random

from faker import Faker

from common import conectar, copiar  # noqa: F401

SEMENTE = 42


def main():
    rnd = random.Random(SEMENTE)  # noqa: F841
    fake = Faker("pt_BR")  # noqa: F841
    Faker.seed(SEMENTE)
    raise SystemExit("src/gerar_dados.py ainda nao implementado")


if __name__ == "__main__":
    main()
