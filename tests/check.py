"""Autoverificacao do TP4 (o mesmo teste e usado na correcao).

Confere o que e mecanico (Secao 8 do enunciado), num banco temporario `tp4_check`,
criado vazio e apagado ao final:

  - sql/01_esquema.sql (e sql/01b_restricoes.sql) executam sem erro em banco vazio;
  - src/gerar_dados.py executa em ate 10 minutos e atende ao volume minimo (Secao 7.1);
  - sql/02_indices.sql executa sem erro sobre o banco povoado;
  - cada consulta de sql/consultas/ e uma unica instrucao SELECT e retorna ao menos uma linha;
  - os arquivos obrigatorios existem.

NAO avalia a especificacao de requisitos, o esquema EER, as justificativas nem a adequacao do esquema ao dominio.
Uso: make test
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "src")
from common import conectar, executar_arquivo, ler_consulta  # noqa: E402

BD = "tp4_check"
DOMINIOS = {"corrida", "comida", "hospedagem", "freelancers", "recarga", "frete"}
N_TIPICAS = 9
N_PROPRIAS = 5
TEMPO_MAX = 600  # segundos para gerar e carregar os dados
MAIOR_TABELA_MIN = 100_000
TABELAS_GRANDES_MIN = 5
LIMIAR_GRANDE = 1_000
TIMEOUT_CONSULTA = 120  # segundos por consulta

placar = []


def check(grupo, nome, ok, detalhe=""):
    placar.append((grupo, nome, bool(ok), detalhe))
    marca = "ok" if ok else "FALHOU"
    print(f"[{marca:6}] {grupo:9} {nome}" + (f"  -> {detalhe}" if detalhe and not ok else ""))
    return bool(ok)


def ler_dominio():
    f = Path("dominio.txt")
    if not f.exists():
        return None, []
    campos = {}
    for linha in f.read_text(encoding="utf-8").splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1)
            campos[k.strip().lower()] = v.strip()
    dom = campos.get("dominio", "").lower()
    nomes = [n.strip() for n in campos.get("integrantes", "").split(";") if n.strip()]
    return dom, nomes


def arquivos():
    dom, nomes = ler_dominio()
    check("arquivos", "dominio.txt: dominio valido", dom in DOMINIOS,
          f"'{dom}' nao esta em {sorted(DOMINIOS)}" if dom else "arquivo ausente ou sem 'dominio:'")
    check("arquivos", "dominio.txt: 1 ou 2 integrantes", 1 <= len(nomes) <= 2 and not any("<" in n for n in nomes),
          "informe 'integrantes: Nome; Nome' (no maximo 2, sem os sinais < >)")
    pdf = Path("docs/relatorio.pdf")
    check("arquivos", "docs/relatorio.pdf presente", pdf.exists() and pdf.stat().st_size > 5000)
    eer = [p for p in Path("docs/eer").glob("*") if p.is_file() and p.name != ".gitkeep"]
    imagens = [p for p in eer if p.suffix.lower() in (".png", ".svg")]
    check("arquivos", "docs/eer: diagrama exportado (PNG ou SVG)", bool(imagens))
    check("arquivos", "docs/eer: arquivo-fonte da ferramenta", len(eer) > len(imagens),
          "inclua o arquivo salvo pela ferramenta (por exemplo .eer)")
    for nome in ("sql/01_esquema.sql", "sql/02_indices.sql", "sql/03_testes_restricoes.sql", "src/gerar_dados.py"):
        check("arquivos", f"{nome} presente", Path(nome).exists())
    return dom


def banco_vazio():
    with conectar(dbname="postgres") as con:
        cur = con.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {BD} WITH (FORCE)")
        cur.execute(f"CREATE DATABASE {BD}")


def descartar_banco():
    try:
        with conectar(dbname="postgres") as con:
            con.cursor().execute(f"DROP DATABASE IF EXISTS {BD} WITH (FORCE)")
    except Exception:  # noqa: BLE001
        pass


def esquema():
    ok1, saida = executar_arquivo("sql/01_esquema.sql", dbname=BD) if Path("sql/01_esquema.sql").exists() else (False, "ausente")
    check("esquema", "sql/01_esquema.sql executa em banco vazio", ok1, saida.splitlines()[-1] if saida else "")
    if Path("sql/01b_restricoes.sql").exists():
        ok2, saida = executar_arquivo("sql/01b_restricoes.sql", dbname=BD)
        check("esquema", "sql/01b_restricoes.sql executa", ok2, saida.splitlines()[-1] if saida else "")
        ok1 = ok1 and ok2
    if ok1:
        with conectar(dbname=BD) as con:
            cur = con.cursor()
            cur.execute("SELECT count(*) FROM pg_tables WHERE schemaname = 'public'")
            n = cur.fetchone()[0]
        check("esquema", "o esquema criou ao menos uma tabela", n > 0, "nenhuma tabela em public")
    return ok1


def dados():
    env = dict(os.environ, PGDATABASE=BD)
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "src/gerar_dados.py"], env=env, capture_output=True, text=True, timeout=TEMPO_MAX)
    except subprocess.TimeoutExpired:
        check("dados", f"povoamento termina em ate {TEMPO_MAX // 60} min", False, f"excedeu {TEMPO_MAX}s")
        return False
    dt = time.time() - t0
    ok = r.returncode == 0
    check("dados", "src/gerar_dados.py executa sem erro", ok,
          (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["codigo %d" % r.returncode])[-1])
    if not ok:
        return False
    check("dados", f"tempo de geracao ate {TEMPO_MAX // 60} min", dt <= TEMPO_MAX, f"{dt:.0f}s")
    with conectar(dbname=BD) as con:
        cur = con.cursor()
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY 1")
        tabelas = [t[0] for t in cur.fetchall()]
        contagens = {}
        for t in tabelas:
            cur.execute(f'SELECT count(*) FROM "{t}"')
            contagens[t] = cur.fetchone()[0]
    maior = max(contagens.items(), key=lambda kv: kv[1], default=("-", 0))
    vazias = [t for t, n in contagens.items() if n == 0]
    grandes = [t for t, n in contagens.items() if n >= LIMIAR_GRANDE]
    check("dados", f"maior tabela com >= {MAIOR_TABELA_MIN} linhas", maior[1] >= MAIOR_TABELA_MIN, f"{maior[0]} tem {maior[1]}")
    check("dados", "nenhuma tabela vazia", not vazias, "vazias: " + ", ".join(vazias[:8]))
    check("dados", f">= {TABELAS_GRANDES_MIN} tabelas com >= {LIMIAR_GRANDE} linhas", len(grandes) >= TABELAS_GRANDES_MIN,
          f"apenas {len(grandes)}")
    print(f"           (tabelas: {len(tabelas)}; linhas: " + ", ".join(f"{t}={n}" for t, n in sorted(contagens.items(), key=lambda kv: -kv[1])[:6]) + ", ...)")
    return True


def indices():
    f = Path("sql/02_indices.sql")
    if not f.exists():
        return
    ok, saida = executar_arquivo(f, dbname=BD)
    check("indices", "sql/02_indices.sql executa sobre o banco povoado", ok, saida.splitlines()[-1] if saida else "")
    check("indices", "cria ao menos um indice", bool(re.search(r"create\s+(unique\s+)?index", f.read_text(encoding="utf-8"), re.I)),
          "nenhum CREATE INDEX encontrado")


def consultas():
    esperados = [f"q{i:02d}" for i in range(1, N_TIPICAS + 1)] + [f"p{i:02d}" for i in range(1, N_PROPRIAS + 1)]
    ausentes = [e for e in esperados if not Path(f"sql/consultas/{e}.sql").exists()]
    check("consultas", f"q01..q{N_TIPICAS:02d} e p01..p{N_PROPRIAS:02d} presentes", not ausentes, "faltam: " + ", ".join(ausentes))
    with conectar(dbname=BD) as con:
        cur = con.cursor()
        cur.execute(f"SET statement_timeout = {TIMEOUT_CONSULTA * 1000}")
        for nome in esperados:
            f = Path(f"sql/consultas/{nome}.sql")
            if not f.exists():
                continue
            try:
                sql = ler_consulta(f)
                cur.execute(sql)
                linhas = cur.fetchmany(1)
                check("consultas", f"{nome} retorna ao menos uma linha", bool(linhas), "resultado vazio")
            except Exception as e:  # noqa: BLE001
                con.rollback()
                check("consultas", f"{nome} executa", False, str(e).strip().splitlines()[0][:140])


def main():
    print("== TP4: autoverificacao ==")
    arquivos()
    banco_vazio()
    try:
        if esquema():
            if dados():
                indices()
                consultas()
            else:
                check("consultas", "consultas nao executadas (povoamento falhou)", False)
        else:
            check("dados", "povoamento nao executado (esquema falhou)", False)
    finally:
        descartar_banco()
    falhas = [p for p in placar if not p[2]]
    print(f"\n{len(placar) - len(falhas)}/{len(placar)} verificacoes ok")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
