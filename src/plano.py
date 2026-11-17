"""make plano Q=q03 TAG=antes: grava EXPLAIN (ANALYZE, BUFFERS) de sql/consultas/<Q>.sql em resultados/plano_<Q>_<TAG>.txt."""
import sys

from common import RESULTADOS, conectar, ler_consulta


def main():
    if len(sys.argv) < 3:
        sys.exit("uso: make plano Q=q03 TAG=antes")
    q, tag = sys.argv[1], sys.argv[2]
    sql = ler_consulta(f"sql/consultas/{q}.sql")
    with conectar() as con:
        cur = con.cursor()
        cur.execute("EXPLAIN (ANALYZE, BUFFERS) " + sql)
        texto = "\n".join(r[0] for r in cur.fetchall()) + "\n"
    RESULTADOS.mkdir(exist_ok=True)
    destino = RESULTADOS / f"plano_{q}_{tag}.txt"
    destino.write_text(texto, encoding="utf-8")
    print(texto)
    print(f"gravado {destino}")


if __name__ == "__main__":
    main()
