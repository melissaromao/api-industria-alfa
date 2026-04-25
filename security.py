import re
import base64
from config import USERS, ROLE_PERMISSIONS

ALLOWED_COMMANDS = ["REBOOT", "CALIBRATE", "STATUS_CHECK"]
MALICIOUS_PATTERNS = [r"['\";\-]", r"\.\./", r"sudo", r"rm\s-rf"]


def is_input_safe(command: str) -> tuple[bool, str]:
    if command not in ALLOWED_COMMANDS:
        return False, f"Comando inválido. Permitidos: {', '.join(ALLOWED_COMMANDS)}"
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, "Padrão malicioso detectado!"
    return True, "Sucesso"


def get_auth_context(headers) -> dict | None:
    auth_header = headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, password = decoded.split(":", 1)
        user_data = USERS.get(username)
        if user_data and user_data["password"] == password:
            return user_data
    except Exception:
        return None
    return None


def has_permission(user: dict, permission: str) -> bool:
    role = user.get("role", "")
    return permission in ROLE_PERMISSIONS.get(role, [])