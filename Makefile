# TP4 — Introducao a Bancos de Dados (IBD 2026/02)
#
#   make up                 sobe o PostgreSQL e constroi a imagem
#   make esquema            recria o banco e executa sql/01_esquema.sql (e sql/01b_restricoes.sql, se existir)
#   make dados              executa src/gerar_dados.py (povoamento sintetico)
#   make indices            executa sql/02_indices.sql
#   make consultas          executa sql/consultas/*.sql e grava as 20 primeiras linhas em resultados/
#   make plano Q=q03 TAG=antes   grava EXPLAIN (ANALYZE, BUFFERS) de sql/consultas/q03.sql em resultados/
#   make test               autoverificacao (o mesmo teste que corrige o trabalho)
#   make down               derruba os servicos (make clean-all apaga tambem os dados)

DC := docker compose
RUN := $(DC) run --rm app

.PHONY: up down clean-all esquema dados indices consultas plano test shell

up:
	$(DC) up -d --build db
	$(DC) build app

down:
	$(DC) down

clean-all:
	$(DC) down -v

esquema:
	$(RUN) python src/aplicar_esquema.py

dados:
	$(RUN) python src/gerar_dados.py

indices:
	$(RUN) python src/aplicar_indices.py

consultas:
	$(RUN) python src/rodar_consultas.py

plano:
	$(RUN) python src/plano.py $(Q) $(TAG)

test:
	$(RUN) python tests/check.py

shell:
	$(RUN) bash
