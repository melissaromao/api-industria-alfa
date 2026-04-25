import os
import json
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.environ.get("PORT", 8080))

_raw_users = os.environ.get("API_USERS", "")
try:
    USERS: dict = json.loads(_raw_users) if _raw_users else {}
except json.JSONDecodeError:
    raise RuntimeError(
        "API_USERS must be valid JSON. Example:\n"
        '\'{"gestor": {"password": "sua-senha", "role": "admin"}}\''
    )

ROLE_PERMISSIONS: dict = {
    "admin": ["read_sensor", "send_command", "update_firmware"],
    "operator": ["read_sensor"],
}