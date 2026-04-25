import json
from http.server import BaseHTTPRequestHandler
from security import get_auth_context, has_permission, is_input_safe


class SecurityAPIHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    def respond(self, status: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def get_json_body(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length))
        except Exception:
            return None

    def do_GET(self):
        if self.path == "/health":
            return self.respond(200, {"status": "ok"})
        self.respond(404, {"error": "Rota não encontrada"})

    def do_POST(self):
        user = get_auth_context(self.headers)
        if not user:
            return self.respond(401, {"error": "Credenciais inválidas ou ausentes"})

        body = self.get_json_body()
        if body is None:
            return self.respond(400, {"error": "JSON inválido ou ausente"})

        if self.path == "/execute-command":
            self._handle_execute_command(user, body)
        else:
            self.respond(404, {"error": "Rota não encontrada"})

    def _handle_execute_command(self, user: dict, body: dict):
        if not has_permission(user, "send_command"):
            return self.respond(403, {"error": "Seu perfil não tem permissão para enviar comandos"})

        command = body.get("command", "").strip()
        if not command:
            return self.respond(400, {"error": "Campo 'command' é obrigatório"})

        safe, message = is_input_safe(command)
        if not safe:
            return self.respond(400, {"error": "Comando bloqueado", "reason": message})

        self.respond(200, {"status": "Executado", "command": command})