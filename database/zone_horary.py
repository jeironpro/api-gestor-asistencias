# Importaciones
from datetime import datetime
from zoneinfo import ZoneInfo


def madrid_utc():
    """
    Obtiene la fecha y hora actual en Madrid en formato UTC.

    Argumentos: None

    Retorna: datetime
    """
    madrid = datetime.now(ZoneInfo("Europe/Madrid"))
    return madrid.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
