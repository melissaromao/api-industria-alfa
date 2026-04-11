import json
import re
import os
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

USERS = {
    "gestor": {"password": "123", "role": "admin"},
    "operador": {"password": "456", "role": "operator"}
}

ROLE_PERMISSIONS = {
    "admin": ["read_sensor", "send_command", "update_firmware"],
    "operator": ["read_sensor"]
}

ALLOWED_COMMANDS = ["REBOOT", "CALIBRATE", "STATUS_CHECK"]

def is_input_safe(command):
    if command not in ALLOWED_COMMANDS:
        return False, "Comando inválido."
    
    malicious_patterns = [r"['\";\-]", r"\.\./", r"sudo", r"rm\s-rf"]
    for pattern in malicious_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return False, "Padrão malicioso detectado!"
            
    return True, "Sucesso"

class SecurityAPIHandler(BaseHTTPRequestHandler):
    
    def get_auth_context(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return None
        try:
            decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
            user, pwd = decoded.split(':')
            user_data = USERS.get(user)
            if user_data and user_data['password'] == pwd:
                return user_data
        except Exception:
            return None
        return None

    def respond(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        user = self.get_auth_context()
        if not user:
            return self.respond(401, {"error": "Não autorizado"})

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = json.loads(self.rfile.read(content_length))
        except Exception:
            return self.respond(400, {"error": "JSON inválido"})
        
        if self.path == '/execute-command':
            if "send_command" not in ROLE_PERMISSIONS[user['role']]:
                return self.respond(403, {"error": "Acesso negado para seu perfil"})

            cmd = post_data.get('command', '')
            safe, message = is_input_safe(cmd)
            if not safe:
                return self.respond(400, {"error": "Security Block", "reason": message})
            
            self.respond(200, {"status": "Executado", "command": cmd})
        else:
            self.respond(404, {"error": "Rota não encontrada"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SecurityAPIHandler)
    print(f"API Industria Alfa rodando na porta {port}")
    server.serve_forever()
