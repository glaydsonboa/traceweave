#!/usr/bin/env python3
"""
@file Coleta diaria do trafego do traceweave (clones, views, conteudo popular) e acumula em CSV.
@contract WOR-TRAFFIC-LOGGER-001
@status active
@provenance Proposta original do ChatGPT (26/09/2026) corrigida: a URL usava github.com em vez de
  api.github.com/repos (404 em toda execucao); o endpoint traffic/referrers NAO existe na API REST
  (404 — so a pagina web) e foi removido; popular/paths e array no topo (nao objeto com .paths);
  stdlib-only (urllib/csv) dispensa o pip install de requests.

NAO E RESPONSAVEL POR: julgar o trafego; referrers (endpoint web-only); garantir token — o chamador
  fornece TRAFFIC_TOKEN com acesso de push ao repositorio.

Uso: TRAFFIC_TOKEN=<token> python tools/backup-traffic.py
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

REPO = os.getenv("GITHUB_REPOSITORY", "glaydsonboa/traceweave")
TOKEN = os.getenv("TRAFFIC_TOKEN")
if not TOKEN:
    print("Erro: TRAFFIC_TOKEN nao configurado.", file=sys.stderr)
    sys.exit(1)

API = f"https://api.github.com/repos/{REPO}/traffic"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
BASE_DIR = os.path.join("research", "traffic-data")


def get(endpoint):
    req = urllib.request.Request(f"{API}/{endpoint}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def read_rows(filepath):
    rows = {}
    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                if row:
                    rows[row[0]] = row
    return rows


def write_rows(filepath, header, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        for key in sorted(rows):
            writer.writerow(rows[key])


def update_time_series(endpoint, filepath, header):
    entries = get(endpoint)[endpoint]  # {"clones": [...]} / {"views": [...]}
    rows = read_rows(filepath)
    for entry in entries:
        day = entry["timestamp"][:10]
        rows[day] = [day, str(entry["count"]), str(entry["uniques"])]
    write_rows(filepath, header, rows)
    print(f"{endpoint}: {len(entries)} dias acumulados em {filepath}")


def update_popular(filepath, header):
    entries = get("popular/paths")  # array no topo
    rows = read_rows(filepath)
    for entry in entries:
        key = f"{TODAY}_{entry['path']}"
        rows[key] = [TODAY, entry["path"], str(entry["count"]), str(entry["uniques"])]
    write_rows(filepath, header, rows)
    print(f"popular/paths: {len(entries)} entradas logadas em {filepath}")


if __name__ == "__main__":
    update_time_series("clones", f"{BASE_DIR}/clones_history.csv",
                       ["Date", "Total_Clones", "Unique_Cloners"])
    update_time_series("views", f"{BASE_DIR}/views_history.csv",
                       ["Date", "Total_Views", "Unique_Visitors"])
    update_popular(f"{BASE_DIR}/popular_content_history.csv",
                   ["Log_Date", "Content_Path", "Total_Views", "Unique_Visitors"])
    print(f"Coleta de {REPO} concluida em {TODAY} (UTC).")
