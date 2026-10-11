"""tools/backup-traffic.py — o acumulado de conteudo popular nao pode perder linhas de dias anteriores."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
HEADER = ["Log_Date", "Content_Path", "Total_Views", "Unique_Visitors"]


def load_module():
    # o modulo encerra o processo no import se nao houver token; o token aqui e so um valor de teste.
    with mock.patch.dict(os.environ, {"TRAFFIC_TOKEN": "token-de-teste"}):
        spec = importlib.util.spec_from_file_location("backup_traffic", ROOT / "tools" / "backup-traffic.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class TestPopularAccumulation(unittest.TestCase):

    def setUp(self):
        self.bt = load_module()
        self.tmp = tempfile.TemporaryDirectory(prefix="traceweave-traffic-")
        self.file = str(Path(self.tmp.name) / "popular.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def run_day(self, day, paths):
        entries = [{"path": p, "count": n, "uniques": 1} for p, n in paths]
        with mock.patch.object(self.bt, "TODAY", day), mock.patch.object(self.bt, "get", return_value=entries):
            self.bt.update_popular(self.file, HEADER)

    def rows(self):
        lines = Path(self.file).read_text(encoding="utf-8").splitlines()[1:]
        return [line.split(";") for line in lines if line]

    def test_dias_anteriores_mantem_todas_as_linhas(self):
        self.run_day("2026-10-10", [("/a", 5), ("/b", 4), ("/c", 3)])
        self.run_day("2026-10-11", [("/a", 6), ("/b", 5), ("/c", 4)])
        por_dia = {}
        for dia, caminho, *_ in self.rows():
            por_dia.setdefault(dia, []).append(caminho)
        self.assertEqual(sorted(por_dia["2026-10-10"]), ["/a", "/b", "/c"],
                         "o dia anterior perdeu linhas ao rodar o dia seguinte")
        self.assertEqual(sorted(por_dia["2026-10-11"]), ["/a", "/b", "/c"])

    def test_rodar_o_mesmo_dia_duas_vezes_nao_duplica(self):
        self.run_day("2026-10-11", [("/a", 6), ("/b", 5)])
        self.run_day("2026-10-11", [("/a", 7), ("/b", 5)])
        self.assertEqual(len(self.rows()), 2)
        valores = {caminho: total for _, caminho, total, _ in self.rows()}
        self.assertEqual(valores["/a"], "7", "a segunda execucao do dia deve atualizar o valor")

    def test_series_temporais_continuam_uma_linha_por_dia(self):
        series = {"clones": [{"timestamp": "2026-10-10T00:00:00Z", "count": 3, "uniques": 2},
                             {"timestamp": "2026-10-11T00:00:00Z", "count": 4, "uniques": 3}]}
        file = str(Path(self.tmp.name) / "clones.csv")
        with mock.patch.object(self.bt, "get", return_value=series):
            self.bt.update_time_series("clones", file, ["Date", "Total_Clones", "Unique_Cloners"])
            self.bt.update_time_series("clones", file, ["Date", "Total_Clones", "Unique_Cloners"])
        lines = Path(file).read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
