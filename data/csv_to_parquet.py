"""csv_to_parquet.py  (v1.1)

Conversor de CSV → Parquet usando DuckDB **com valores‑default**.

* Se executado **sem argumentos**, assume `data/tick_data_2024.csv` como
  entrada e cria `data/tick_data_2024.parquet` (mesmo nome, extensão .parquet).
  Pede confirmação antes de sobrescrever.
* Continua aceitando `--csv` e `--out` para caminhos customizados.

Exemplos
--------
# Com argumentos explícitos
python csv_to_parquet.py --csv data/tick_data_2024.csv --out data/usdjpy_2024.parquet

# Sem argumentos (usa defaults, pergunta Y/N)
python csv_to_parquet.py
"""
from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
import duckdb


def convert(csv_path: Path, out_path: Path):
    t0 = time.time()
    print(f"[DuckDB] Convertendo {csv_path} → {out_path} …")

    # Ajuste nomes de colunas se necessário
    query = f"""
        COPY (
            SELECT
                DateTime   AS DateTime,
                Bid        AS Bid,
                Ask        AS Ask
            FROM read_csv_auto('{csv_path}', HEADER=TRUE)
        ) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD);
    """
    duckdb.query(query)
    size_gb = out_path.stat().st_size / 1e9
    print(f"✅ Parquet gerado em {time.time()-t0:.1f}s → {size_gb:.2f} GB")


def main():
    parser = argparse.ArgumentParser("CSV→Parquet converter (DuckDB)")
    parser.add_argument("--csv", help="Arquivo CSV de ticks")
    parser.add_argument("--out", help="Arquivo Parquet de saída")
    args = parser.parse_args()

    if args.csv and args.out:
        csv_path = Path(args.csv)
        out_path = Path(args.out)
    else:
                # Defaults: tenta primeiro na mesma pasta do script, depois em <repo>/data
        script_dir = Path(__file__).resolve().parent
        candidates = list(script_dir.glob("*.csv"))
        if not candidates:
            # tenta na pasta /data relativa à raiz do projeto
            repo_root = script_dir.parent
            candidates = list((repo_root / "data").glob("*.csv"))
        if not candidates:
            print("[Erro] Nenhum CSV encontrado próximo ao script ou em ./data e argumentos não fornecidos.")
            parser.print_help(); sys.exit(2)
        csv_path = candidates[0]
        out_path = csv_path.with_suffix(".parquet")
        resp = input(f"Converter {csv_path} → {out_path}? [y/N] ").lower()
        if resp != "y":
            print("Abortado."); sys.exit(0)

    convert(csv_path, out_path)


if __name__ == "__main__":
    main()
