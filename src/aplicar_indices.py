"""make indices: executa sql/02_indices.sql sobre o banco ja povoado."""
import sys

from common import executar_arquivo

ok, saida = executar_arquivo("sql/02_indices.sql")
print(f"sql/02_indices.sql: {'ok' if ok else 'ERRO'}")
if saida:
    print(saida)
sys.exit(0 if ok else 1)
