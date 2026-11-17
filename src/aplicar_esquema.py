"""make esquema: recria o schema public e executa sql/01_esquema.sql (e sql/01b_restricoes.sql, se existir)."""
import sys
from pathlib import Path

from common import conectar, executar_arquivo, recriar_esquema


def main():
    with conectar() as con:
        recriar_esquema(con.cursor())
    for nome in ("sql/01_esquema.sql", "sql/01b_restricoes.sql"):
        f = Path(nome)
        if not f.exists():
            if nome.endswith("01_esquema.sql"):
                sys.exit(f"{nome} nao encontrado")
            continue
        ok, saida = executar_arquivo(f)
        print(f"{nome}: {'ok' if ok else 'ERRO'}")
        if saida:
            print(saida)
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
