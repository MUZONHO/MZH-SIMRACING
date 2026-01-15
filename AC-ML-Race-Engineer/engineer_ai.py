import joblib
import os
import pandas as pd
import numpy as np
import warnings

# Mantém o console limpo (sklearn às vezes reclama de nomes de colunas)
warnings.filterwarnings("ignore", category=UserWarning)


class EngineerAI:
    """
    ML de engenharia de volta ideal.

    - Carrega um modelo por pista/carro: models/<track>/<car>/ia_engineer.pkl
    - Faz previsão de velocidade alvo (target_v)
    - Calcula delta suavizado (smooth_delta) para feedback estável em tempo real
    - Inclui vento (windSpeed/windDirection) vindo do Graphics (g)
    """

    # >>> IMPORTANTE:
    # Esta lista DEVE bater com as features do treino (train_model.py)
    FEATURE_COLS = [
        "micro_sector",
        "fuel", "gear", "rpm",
        "clutch", "abs_active", "tc_active", "brake_bias",
        "slip_ratio_FL", "slip_ratio_FR", "slip_ratio_RL", "slip_ratio_RR",
        "slip_angle_FL", "slip_angle_FR", "slip_angle_RL", "slip_angle_RR",
        "tyreWear_FL", "tyreWear_FR", "tyreWear_RL", "tyreWear_RR",
        "tyreTemp_FL", "tyreTemp_FR", "tyreTemp_RL", "tyreTemp_RR",
        "brakeTemp_FL", "brakeTemp_FR", "brakeTemp_RL", "brakeTemp_RR",
        "airTemp", "roadTemp",
        "accG_lat", "accG_lon",
        "wind_speed", "wind_dir",
    ]

    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.model = None
        self.current_model_key = ""
        self.delta_history = []  # suavização

    def load_model(self, track, car):
        model_path = os.path.join(self.model_dir, track, car, "ia_engineer.pkl")
        model_key = f"{track}_{car}"

        if model_key == self.current_model_key and self.model is not None:
            return True

        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                self.current_model_key = model_key
                self.delta_history.clear()
                print(f"\n[ML] Modelo carregado: {car} em {track}")
                return True
            except Exception as e:
                print(f"[ML] Erro ao carregar modelo: {e}")
        return False

    def _safe_float(self, v, default=0.0):
        try:
            return float(v)
        except Exception:
            return float(default)

    def get_target_data(self, p, g):
        """
        Retorna:
          { "target_v": <km/h>, "smooth_delta": <km/h> }

        - target_v: velocidade alvo prevista
        - smooth_delta: (speedKmh - target_v) suavizado (média móvel)
        """
        if self.model is None:
            return None

        try:
            m_sector = int(g.normalizedCarPosition * 2000)

            # Vento vem do Graphics
            wind_speed = self._safe_float(getattr(g, "windSpeed", 0.0), 0.0)
            wind_dir = self._safe_float(getattr(g, "windDirection", 0.0), 0.0)

            # Monta linha com a MESMA ordem/nomes do treino
            row = {
                "micro_sector": m_sector,
                "fuel": self._safe_float(p.fuel),
                "gear": self._safe_float(p.gear),
                "rpm": self._safe_float(p.rpms),

                "clutch": self._safe_float(p.clutch),
                "abs_active": self._safe_float(p.abs),
                "tc_active": self._safe_float(p.tc),
                "brake_bias": self._safe_float(p.brakeBias),

                "slip_ratio_FL": self._safe_float(p.slipRatio[0]),
                "slip_ratio_FR": self._safe_float(p.slipRatio[1]),
                "slip_ratio_RL": self._safe_float(p.slipRatio[2]),
                "slip_ratio_RR": self._safe_float(p.slipRatio[3]),

                "slip_angle_FL": self._safe_float(p.slipAngle[0]),
                "slip_angle_FR": self._safe_float(p.slipAngle[1]),
                "slip_angle_RL": self._safe_float(p.slipAngle[2]),
                "slip_angle_RR": self._safe_float(p.slipAngle[3]),

                "tyreWear_FL": self._safe_float(p.tyreWear[0]),
                "tyreWear_FR": self._safe_float(p.tyreWear[1]),
                "tyreWear_RL": self._safe_float(p.tyreWear[2]),
                "tyreWear_RR": self._safe_float(p.tyreWear[3]),

                "tyreTemp_FL": self._safe_float(p.tyreCoreTemperature[0]),
                "tyreTemp_FR": self._safe_float(p.tyreCoreTemperature[1]),
                "tyreTemp_RL": self._safe_float(p.tyreCoreTemperature[2]),
                "tyreTemp_RR": self._safe_float(p.tyreCoreTemperature[3]),

                "brakeTemp_FL": self._safe_float(p.brakeTemp[0]),
                "brakeTemp_FR": self._safe_float(p.brakeTemp[1]),
                "brakeTemp_RL": self._safe_float(p.brakeTemp[2]),
                "brakeTemp_RR": self._safe_float(p.brakeTemp[3]),

                "airTemp": self._safe_float(p.airTemp),
                "roadTemp": self._safe_float(p.roadTemp),

                "accG_lat": self._safe_float(p.accG[0]),
                "accG_lon": self._safe_float(p.accG[1]),

                "wind_speed": wind_speed,
                "wind_dir": wind_dir,
            }

            input_df = pd.DataFrame([[row[c] for c in self.FEATURE_COLS]], columns=self.FEATURE_COLS)

            # Previsão
            target_v = float(self.model.predict(input_df)[0])

            # Delta + suavização
            current_delta = float(p.speedKmh) - target_v
            self.delta_history.append(current_delta)
            if len(self.delta_history) > 15:
                self.delta_history.pop(0)

            smooth_delta = float(np.mean(self.delta_history))

            return {"target_v": target_v, "smooth_delta": smooth_delta}
        except Exception:
            return None

    def get_target_speed(self, p, g):
        data = self.get_target_data(p, g)
        if data is None:
            return None
        return data["target_v"]
