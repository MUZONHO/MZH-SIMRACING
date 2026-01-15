import asyncio
import time
import json
import websockets
from datetime import datetime

from ac_reader import ACReader
from ideal_engine import IdealLapEngine

from engineer_ai import EngineerAI
from ac_structs import decode_wchar

CLIENTS = set()


async def ws_handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        CLIENTS.remove(websocket)


async def core_loop():
    reader = ACReader()
    while not reader.connect():
        print("Aguardando Assetto Corsa...")
        await asyncio.sleep(2)

    engine = IdealLapEngine()

    ml = EngineerAI()
    ml_loaded = False

    is_active = False
    last_feedback_t = 0.0
    FEEDBACK_COOLDOWN = 0.6

    print("Conectado! Vá para a pista.")

    while True:
        t0 = time.time()
        p, g, s = reader.read_all()

        target_v = None
        smooth_delta = None

        if g.status == 2:  # Dirigindo
            if not is_active:
                is_active = True
                ml_loaded = False

            engine.log(p, g, s)

            if not ml_loaded:
                track = decode_wchar(s.track).strip("\x00").strip()
                car = decode_wchar(s.carModel).strip("\x00").strip()
                ok = ml.load_model(track, car)
                if not ok:
                    print(f"[ML] Sem modelo para {car} em {track} (rodando sem alvo).")
                ml_loaded = True

            data = ml.get_target_data(p, g)
            if data is not None:
                target_v = data["target_v"]
                smooth_delta = data["smooth_delta"]

                now = time.time()
                if now - last_feedback_t >= FEEDBACK_COOLDOWN:
                    if smooth_delta < -2.0:
                        print(f"[ML] Acelera! -{abs(smooth_delta):.1f} km/h do seu melhor (alvo {target_v:.1f})")
                        last_feedback_t = now
                    elif smooth_delta > 1.0:
                        print(f"[ML] RECORDE! +{smooth_delta:.1f} km/h (alvo {target_v:.1f})")
                        last_feedback_t = now

        elif is_active and g.status != 2:  # Saiu da pista
            if engine.file:
                engine.file.close()

            engine.process_ideal_lap()

            is_active = False
            engine.current_path = ""
            engine.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # WebSocket Update (manda telemetria + ML)
        if CLIENTS:
            msg = json.dumps({
                "status": g.status,
                "rpm": p.rpms,
                "speed": p.speedKmh,
                "gas": p.gas,
                "brake": p.brake,
                "steer": p.steerAngle,
                "gear": p.gear,
                "tyresOut": p.numberOfTyresOut,
                "windSpeed": getattr(g, "windSpeed", 0.0),
                "windDir": getattr(g, "windDirection", 0.0),
                "target_speed": target_v,
                "smooth_delta": smooth_delta,
            })
            await asyncio.gather(*[ws.send(msg) for ws in CLIENTS], return_exceptions=True)

        await asyncio.sleep(max(0, (1/30) - (time.time() - t0)))


async def main():
    print("Iniciando Servidor...")
    await asyncio.gather(
        websockets.serve(ws_handler, "127.0.0.1", 8765),
        core_loop()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSaindo...")
