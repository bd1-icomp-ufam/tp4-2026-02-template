"""Utilitarios comuns: conexao, execucao de arquivos SQL, COPY em lote, leitura de consultas."""
import os
import subprocess
from pathlib import Path

import psycopg

RESULTADOS = Path("resultados")


def conectar(autocommit=True, dbname=None):
    return psycopg.connect(
        host=os.environ.get("PGHOST", "db"), user=os.environ.get("PGUSER", "tp4"),
        password=os.environ.get("PGPASSWORD", "tp4"),
        dbname=dbname or os.environ.get("PGDATABASE", "tp4"), autocommit=autocommit)


def executar_arquivo(caminho, dbname=None):
    """Executa um arquivo SQL com psql (ON_ERROR_STOP). Retorna (ok, saida)."""
    env = dict(os.environ)
    if dbname:
        env["PGDATABASE"] = dbname
    r = subprocess.run(["psql", "-v", "ON_ERROR_STOP=1", "-q", "-f", str(caminho)],
                       capture_output=True, text=True, env=env)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def recriar_esquema(cur):
    """Apaga tudo que existe no schema public e o recria vazio."""
    cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
    cur.execute("CREATE SCHEMA public")


def copiar(cur, tabela, colunas, linhas):
    """Carrega `linhas` (iteravel de tuplas) em `tabela` com COPY, que e muito mais rapido que INSERT."""
    with cur.copy(f"COPY {tabela} ({', '.join(colunas)}) FROM STDIN") as cp:
        for linha in linhas:
            cp.write_row(linha)


def separar_instrucoes(sql):
    """Divide um texto SQL em instrucoes, ignorando comentarios e ';' dentro de literais."""
    instrucoes, atual = [], []
    i, n = 0, len(sql)
    em_aspas = None
    while i < n:
        c = sql[i]
        if em_aspas:
            atual.append(c)
            if c == em_aspas:
                if i + 1 < n and sql[i + 1] == em_aspas:
                    atual.append(sql[i + 1])
                    i += 1
                else:
                    em_aspas = None
        elif c in ("'", '"'):
            em_aspas = c
            atual.append(c)
        elif sql.startswith("--", i):
            j = sql.find("\n", i)
            i = n if j < 0 else j
            continue
        elif sql.startswith("/*", i):
            j = sql.find("*/", i + 2)
            i = n if j < 0 else j + 1
        elif c == ";":
            instrucoes.append("".join(atual).strip())
            atual = []
        else:
            atual.append(c)
        i += 1
    resto = "".join(atual).strip()
    if resto:
        instrucoes.append(resto)
    return [s for s in instrucoes if s]


def ler_consulta(caminho):
    """Le um arquivo de consulta e exige uma unica instrucao SELECT (ou WITH ... SELECT)."""
    instrucoes = separar_instrucoes(Path(caminho).read_text(encoding="utf-8"))
    if len(instrucoes) != 1:
        raise ValueError(f"{caminho}: esperada 1 instrucao, encontradas {len(instrucoes)}")
    s = instrucoes[0]
    if s.split(None, 1)[0].lower() not in ("select", "with"):
        raise ValueError(f"{caminho}: a instrucao deve ser um SELECT")
    return s


def tabular(colunas, linhas, limite=20):
    """Texto alinhado com cabecalho e ate `limite` linhas."""
    linhas = [tuple("" if v is None else str(v) for v in l) for l in linhas[:limite]]
    larg = [max([len(c)] + [len(l[k]) for l in linhas]) for k, c in enumerate(colunas)]
    fmt = " | ".join("{:<%d}" % w for w in larg)
    saida = [fmt.format(*colunas), "-+-".join("-" * w for w in larg)]
    saida += [fmt.format(*l) for l in linhas]
    return "\n".join(saida) + "\n"
