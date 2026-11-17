"""make consultas: executa sql/consultas/*.sql e grava as 20 primeiras linhas em resultados/<nome>.txt."""
import sys
import time
from pathlib import Path

from common import RESULTADOS, conectar, ler_consulta, tabular


def main():
    arquivos = sorted(Path("sql/consultas").glob("*.sql"))
    if not arquivos:
        sys.exit("nenhuma consulta em sql/consultas/")
    RESULTADOS.mkdir(exist_ok=True)
    falhas = 0
    with conectar() as con:
        cur = con.cursor()
        for f in arquivos:
            try:
                sql = ler_consulta(f)
                t0 = time.time()
                cur.execute(sql)
                linhas = cur.fetchall()
                dt = time.time() - t0
                colunas = [d.name for d in cur.description]
                (RESULTADOS / f"{f.stem}.txt").write_text(tabular(colunas, linhas), encoding="utf-8")
                print(f"{f.stem}: {len(linhas)} linhas em {dt:.2f}s")
            except Exception as e:  # noqa: BLE001
                falhas += 1
                print(f"{f.stem}: ERRO {str(e).splitlines()[0]}")
                con.rollback()
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
