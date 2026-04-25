from http.server import HTTPServer
from config import PORT
from handlers import SecurityAPIHandler


def main():
    server = HTTPServer(("0.0.0.0", PORT), SecurityAPIHandler)
    print(f"Industria Alfa API rodando em http://0.0.0.0:{PORT}")
    print("Pressione Ctrl+C para encerrar.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")


if __name__ == "__main__":
    main()