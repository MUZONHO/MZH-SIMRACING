import pandas as pd
import glob
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

DATA_DIR = "session_data"
MODEL_DIR = "models"

# >>> FEATURES DO TREINO (DEVEM BATER COM engineer_ai.py)
FEATURES = [
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

TARGET = "speedKmh"


def get_available_sessions():
    """Varre a pasta session_data/ e encontra pistas e carros disponíveis."""
    sessions = []
    if not os.path.exists(DATA_DIR):
        return sessions

    for track in os.listdir(DATA_DIR):
        track_path = os.path.join(DATA_DIR, track)
        if not os.path.isdir(track_path):
            continue
        for car in os.listdir(track_path):
            car_path = os.path.join(track_path, car)
            if os.path.isdir(car_path):
                sessions.append((track, car))
    return sessions


def train_for(track: str, car: str):
    data_path = os.path.join(DATA_DIR, track, car)
    files = glob.glob(os.path.join(data_path, "SESS_*_LAP_*.csv"))
    if not files:
        print(f"[!] Nenhum CSV encontrado em: {data_path}")
        return

    print(f"[>>>] Treinando ML para: {car} em {track}")
    print(f"[] Processando {len(files)} arquivos de telemetria...")

    # Carrega tudo (para big data real: dá pra evoluir pra chunks)
    df_list = []
    for f in files:
        try:
            df_list.append(pd.read_csv(f))
        except Exception:
            pass

    if not df_list:
        print("[!] Não consegui ler nenhum arquivo CSV válido.")
        return

    df = pd.concat(df_list, ignore_index=True)

    # Limpeza básica (recomendado pro ML)
    if "tyresOut" in df.columns:
        df = df[df["tyresOut"] == 0]  # só dentro da pista

    # Garante que todas as colunas existem
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        print("[ERRO] Faltam colunas no CSV (provável header/log diferente):")
        for c in missing:
            print(" -", c)
        return

    # Drop NaNs/inf
    df = df.replace([float("inf"), float("-inf")], pd.NA).dropna(subset=FEATURES + [TARGET])

    X = df[FEATURES]
    y = df[TARGET]

    # Split por amostra (ideal: split por VOLTA/SESSÃO pra evitar leakage; isso é o próximo passo)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("[] Criando rede de decisão (RandomForest)...")
    model = RandomForestRegressor(
        n_estimators=250,
        max_depth=18,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"[OK] Treino concluído! Precisão: {score*100:.2f}%")

    # Salva modelo em models/<track>/<car>/
    out_dir = os.path.join(MODEL_DIR, track, car)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ia_engineer.pkl")
    joblib.dump(model, out_path)

    print(f"[SAV] Modelo salvo em: {out_path}")


def main():
    sessions = get_available_sessions()
    if not sessions:
        print("[!] Nenhuma sessão encontrada. Grave voltas em session_data/ primeiro.")
        return

    # Treina tudo (big data)
    for track, car in sessions:
        train_for(track, car)


if __name__ == "__main__":
    main()
