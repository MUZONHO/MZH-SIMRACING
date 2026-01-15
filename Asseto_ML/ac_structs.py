import ctypes

def decode_wchar(arr) -> str:
    try:
        return "".join(arr).split("\x00", 1)[0]
    except Exception:
        return ""

class SPageFilePhysics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId", ctypes.c_int), ("gas", ctypes.c_float), ("brake", ctypes.c_float),
        ("fuel", ctypes.c_float), ("gear", ctypes.c_int), ("rpms", ctypes.c_int),
        ("steerAngle", ctypes.c_float), ("speedKmh", ctypes.c_float),
        ("velocity", ctypes.c_float * 3), ("accG", ctypes.c_float * 3),
        ("wheelSlip", ctypes.c_float * 4), ("wheelLoad", ctypes.c_float * 4),
        ("wheelsPressure", ctypes.c_float * 4), ("wheelAngularSpeed", ctypes.c_float * 4),
        ("tyreWear", ctypes.c_float * 4), ("tyreDirtyLevel", ctypes.c_float * 4),
        ("tyreCoreTemperature", ctypes.c_float * 4), ("camberRAD", ctypes.c_float * 4),
        ("suspensionTravel", ctypes.c_float * 4), ("drs", ctypes.c_float),
        ("tc", ctypes.c_float), ("heading", ctypes.c_float), ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float), ("cgHeight", ctypes.c_float), ("carDamage", ctypes.c_float * 5),
        ("numberOfTyresOut", ctypes.c_int), ("pitLimiterOn", ctypes.c_int),
        ("abs", ctypes.c_float), ("kersCharge", ctypes.c_float), ("kersInput", ctypes.c_float),
        ("autoShifterOn", ctypes.c_int), ("rideHeight", ctypes.c_float * 2),
        ("turboBoost", ctypes.c_float), ("ballast", ctypes.c_float), ("airDensity", ctypes.c_float),
        ("airTemp", ctypes.c_float), ("roadTemp", ctypes.c_float), ("localAngularVel", ctypes.c_float * 3),
        ("finalFF", ctypes.c_float), ("performanceMeter", ctypes.c_float), ("engineBrake", ctypes.c_int),
        ("ersRecoveryLevel", ctypes.c_int), ("ersPowerLevel", ctypes.c_int), ("ersHeatCharging", ctypes.c_int),
        ("ersIsCharging", ctypes.c_int), ("kersCurrentKJ", ctypes.c_float), ("drsAvailable", ctypes.c_int),
        ("drsEnabled", ctypes.c_int), ("brakeTemp", ctypes.c_float * 4), ("clutch", ctypes.c_float),
        ("tyreTempI", ctypes.c_float * 4), ("tyreTempM", ctypes.c_float * 4), ("tyreTempO", ctypes.c_float * 4),
        ("isAIControlled", ctypes.c_int), ("tyreContactPoint", ctypes.c_float * 12),
        ("tyreContactNormal", ctypes.c_float * 12), ("tyreContactHeading", ctypes.c_float * 12),
        ("brakeBias", ctypes.c_float), ("localVelocity", ctypes.c_float * 3),
        ("P2PActivations", ctypes.c_int), ("P2PStatus", ctypes.c_int), ("currentMaxRpm", ctypes.c_float),
        ("mz", ctypes.c_float * 4), ("fx", ctypes.c_float * 4), ("fy", ctypes.c_float * 4),
        ("slipRatio", ctypes.c_float * 4), ("slipAngle", ctypes.c_float * 4), ("tireTemp", ctypes.c_float * 4),
        ("waterTemp", ctypes.c_float), ("brakePressure", ctypes.c_float), ("frontBrakeCompound", ctypes.c_int),
        ("rearBrakeCompound", ctypes.c_int), ("padLife", ctypes.c_float * 4), ("discLife", ctypes.c_float * 4),
        ("ignitionOn", ctypes.c_int), ("starterEngineOn", ctypes.c_int), ("isEngineRunning", ctypes.c_int),
        ("kerbVibration", ctypes.c_float), ("slipVibration", ctypes.c_float), ("gVibration", ctypes.c_float),
        ("absVibration", ctypes.c_float),
    ]

class SPageFileGraphics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId", ctypes.c_int), ("status", ctypes.c_int), ("session", ctypes.c_int),
        ("currentTime", ctypes.c_wchar * 15), ("lastTime", ctypes.c_wchar * 15),
        ("bestTime", ctypes.c_wchar * 15), ("split", ctypes.c_wchar * 15),
        ("completedLaps", ctypes.c_int), ("position", ctypes.c_int),
        ("iCurrentTime", ctypes.c_int), ("iLastTime", ctypes.c_int), ("iBestTime", ctypes.c_int),
        ("sessionTimeLeft", ctypes.c_float), ("distanceTraveled", ctypes.c_float),
        ("isInPit", ctypes.c_int), ("currentSectorIndex", ctypes.c_int),
        ("lastSectorTime", ctypes.c_int), ("numberOfLaps", ctypes.c_int),
        ("tyreCompound", ctypes.c_wchar * 33), ("replayTimeMultiplier", ctypes.c_float),
        ("normalizedCarPosition", ctypes.c_float), ("carCoordinates", ctypes.c_float * 3),
        ("penaltyTime", ctypes.c_float), ("flag", ctypes.c_int), ("idealLineOn", ctypes.c_int),
        ("isInPitLane", ctypes.c_int), ("surfaceGrip", ctypes.c_float), ("mandatoryPitDone", ctypes.c_int),
        ("windSpeed", ctypes.c_float), ("windDirection", ctypes.c_float), ("isSetupMenuVisible", ctypes.c_int),
        ("mainDisplayIndex", ctypes.c_int), ("secondaryDisplayIndex", ctypes.c_int),
        ("TC", ctypes.c_int), ("TCCut", ctypes.c_int), ("EngineMap", ctypes.c_int),
        ("ABS", ctypes.c_int), ("fuelXLap", ctypes.c_float), ("rainLights", ctypes.c_int),
        ("flashingLights", ctypes.c_int), ("lightsStage", ctypes.c_int),
        ("exhaustTemperature", ctypes.c_float), ("wiperLV", ctypes.c_int),
        ("driverStintTotalTimeLeft", ctypes.c_int), ("driverStintTimeLeft", ctypes.c_int),
        ("rainTyres", ctypes.c_int), ("sessionIndex", ctypes.c_int), ("usedFuel", ctypes.c_float),
    ]

class SPageFileStatic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("smVersion", ctypes.c_wchar * 15), ("acVersion", ctypes.c_wchar * 15),
        ("numberOfSessions", ctypes.c_int), ("numCars", ctypes.c_int),
        ("carModel", ctypes.c_wchar * 33), ("track", ctypes.c_wchar * 33),
    ]