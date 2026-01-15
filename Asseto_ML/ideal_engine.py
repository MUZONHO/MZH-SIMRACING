import os
import csv
import glob
import pandas as pd
import re
from datetime import datetime
from ac_structs import decode_wchar


class IdealLapEngine:
    def __init__(self, base_folder="session_data"):
        # Define a pasta raiz absoluta para evitar bugs de caminho no Windows
        self.base_folder = os.path.abspath(base_folder)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_lap = -1
        self.file = None
        self.writer = None
        self.current_path = ""

    def setup_session(self, track_name, car_name):
        """Cria a hierarquia session_data > Pista > Carro de forma limpa."""

        def clean_name(name: str) -> str:
            name = re.sub(r'[\\/*?:"<>|]', "", name)
            return name.replace(" ", "_").strip()

        track = clean_name(track_name)
        car = clean_name(car_name)

        self.current_path = os.path.join(self.base_folder, track, car)

        try:
            os.makedirs(self.current_path, exist_ok=True)
            print(f"[*] Diretório de telemetria: {self.current_path}")
        except Exception as e:
            print(f"[ERRO FATAL] Não foi possível criar pastas: {e}")

    def start_lap_file(self, lap_num: int):
        """Fecha o arquivo anterior e abre um novo CSV para a nova volta."""
        if self.file:
            self.file.close()

        self.current_lap = lap_num
        filename = f"SESS_{self.session_id}_LAP_{lap_num}.csv"
        full_path = os.path.join(self.current_path, filename)

        try:
            self.file = open(full_path, "w", newline="", encoding="utf-8")
            self.writer = csv.writer(self.file)

            # >>> NOVO CABEÇALHO (BIG DATA / ML)
            header = [
                "micro_sector", "speedKmh", "gas", "brake", "steer", "gear", "rpm", "fuel",
                "clutch", "abs_active", "tc_active", "brake_bias",
                "slip_ratio_FL", "slip_ratio_FR", "slip_ratio_RL", "slip_ratio_RR",
                "slip_angle_FL", "slip_angle_FR", "slip_angle_RL", "slip_angle_RR",
                "tyreWear_FL", "tyreWear_FR", "tyreWear_RL", "tyreWear_RR",
                "tyreTemp_FL", "tyreTemp_FR", "tyreTemp_RL", "tyreTemp_RR",
                "brakeTemp_FL", "brakeTemp_FR", "brakeTemp_RL", "brakeTemp_RR",
                "airTemp", "roadTemp", "accG_lat", "accG_lon", "tyresOut",
                # >>> vento (Graphics)
                "wind_speed", "wind_dir",
            ]

            self.writer.writerow(header)
            print(f"[*] Gravando Volta {lap_num}")
        except Exception as e:
            print(f"[ERRO] Falha ao criar arquivo de volta: {e}")

    def log(self, p, g, s):
        """Recebe os dados brutos e decide onde e como gravar."""

        # 1) início da sessão -> cria pastas
        if not self.current_path:
            t_name = decode_wchar(s.track)
            c_name = decode_wchar(s.carModel)
            if not t_name or not c_name:
                return
            self.setup_session(t_name, c_name)

        # 2) mudou a volta -> novo CSV
        if g.completedLaps != self.current_lap:
            self.start_lap_file(g.completedLaps)

        # 3) grava linha
        if self.writer:
            m_sector = int(g.normalizedCarPosition * 2000)

            row = [
                m_sector, p.speedKmh, p.gas, p.brake, p.steerAngle, p.gear, p.rpms, p.fuel,
                p.clutch, p.abs, p.tc, p.brakeBias,
                p.slipRatio[0], p.slipRatio[1], p.slipRatio[2], p.slipRatio[3],
                p.slipAngle[0], p.slipAngle[1], p.slipAngle[2], p.slipAngle[3],
                p.tyreWear[0], p.tyreWear[1], p.tyreWear[2], p.tyreWear[3],
                p.tyreCoreTemperature[0], p.tyreCoreTemperature[1], p.tyreCoreTemperature[2], p.tyreCoreTemperature[3],
                p.brakeTemp[0], p.brakeTemp[1], p.brakeTemp[2], p.brakeTemp[3],
                p.airTemp, p.roadTemp, p.accG[0], p.accG[1], p.numberOfTyresOut,
                # vento (Graphics)
                getattr(g, "windSpeed", 0.0), getattr(g, "windDirection", 0.0),
            ]
            self.writer.writerow(row)

    def process_ideal_lap(self):
        """Extrai a 'volta ideal' da sessão: melhor speed por micro_sector,
        filtrando dados ruins (tyresOut>0)."""
        if not self.current_path or not os.path.exists(self.current_path):
            return

        print(f"\n--- PROCESSANDO VOLTA IDEAL DA SESSÃO ---")
        files = glob.glob(os.path.join(self.current_path, f"SESS_{self.session_id}_LAP_*.csv"))

        if len(files) < 1:
            print("[!] Nenhuma volta completa para analisar.")
            return

        try:
            df_list = [pd.read_csv(f) for f in files]
            df = pd.concat(df_list, ignore_index=True)

            # filtro básico: só as amostras dentro da pista
            if "tyresOut" in df.columns:
                df = df[df["tyresOut"] == 0]

            # pega a melhor velocidade por micro_sector
            ideal = df.sort_values("speedKmh", ascending=False).drop_duplicates("micro_sector")

            ideal_path = os.path.join(self.current_path, f"IDEAL_{self.session_id}.csv")
            ideal.to_csv(ideal_path, index=False)

            print(f"[OK] Volta ideal salva em: {ideal_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao processar volta ideal: {e}")
