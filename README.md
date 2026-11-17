# TP4 — Introdução a Bancos de Dados (ICC205, 2026/02)

Projeto completo de banco de dados: modelo conceitual (EER), esquema relacional, projeto físico, povoamento sintético e consultas em SQL sobre o PostgreSQL.
O enunciado completo está em [`ENUNCIADO.md`](ENUNCIADO.md).

## Roteiro mínimo

```
# preencher dominio.txt (domínio e integrantes)
make up
make esquema
make dados
make indices
make consultas
make test
```

Requisitos: Docker (com o plugin `docker compose`) e `make`. Nada precisa ser instalado fora dos contêineres.

## Onde está cada coisa

| Caminho | Conteúdo |
| --- | --- |
| `docs/eer/` | diagrama EER exportado (PNG ou SVG) e arquivo-fonte da ferramenta |
| `docs/relatorio.pdf` | relatório (Seção 9 do enunciado) |
| `sql/01_esquema.sql` | DDL do esquema relacional |
| `sql/01b_restricoes.sql` | gatilhos e funções para as restrições semânticas |
| `sql/02_indices.sql` | índices do projeto físico |
| `sql/03_testes_restricoes.sql` | comando aceito e comando rejeitado para cada restrição (não executado pelo verificador) |
| `sql/consultas/` | `q01.sql`, `q02.sql`, … (consultas típicas do domínio) e `p01.sql` a `p05.sql` (consultas próprias) |
| `src/gerar_dados.py` | povoamento sintético (a implementar) |
| `src/common.py` | utilitários de conexão, execução de arquivos SQL e `COPY` em lote |
| `src/aplicar_esquema.py`, `aplicar_indices.py`, `rodar_consultas.py`, `plano.py` | scripts chamados pelo `Makefile` (fornecidos; não editar) |
| `tests/check.py` | verificador automático (`make test`) |
| `resultados/` | saída das consultas e planos de execução (versionada) |
| `dominio.txt` | domínio escolhido e integrantes |

## Comandos úteis

- `make esquema` apaga tudo no banco `tp4` e recria o esquema a partir de `sql/01_esquema.sql` (e `sql/01b_restricoes.sql`, se existir).
- `make consultas` grava as 20 primeiras linhas de cada consulta em `resultados/<nome>.txt`.
- `make plano Q=q03 TAG=antes` grava `EXPLAIN (ANALYZE, BUFFERS)` de `sql/consultas/q03.sql` em `resultados/plano_q03_antes.txt`. Repita com `TAG=depois` após criar o índice (`make indices`).
- `make shell` abre um terminal no contêiner da aplicação; dentro dele, `psql` já está conectado ao banco.

O verificador (`make test`) cria um banco temporário, recria o esquema do zero e executa o povoamento do começo ao fim, de modo que a correção não depende do estado do banco local.

## Entrega

Repositório privado, individual ou da dupla, criado a partir deste template na organização `bd1-icomp-ufam`, com o docente como colaborador e a tag `v1.0` enviada ao remoto (`git push origin v1.0`). Detalhes na Seção 11 do enunciado.
