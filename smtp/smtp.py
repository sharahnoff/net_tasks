import base64
import socket
import ssl
import json
import message


def request(socket, request):
    socket.send((request + '\n').encode())
    recv_data = socket.recv(65535).decode()
    return recv_data

def load_config(filename):
    with open(filename, encoding="utf8") as f:
        conf = json.load(f)
        return conf

def main():
    config = load_config("./configs/config.json")
    user = config['user_name']
    user_adr = config['user_address']
    msg = message.create_message("./configs/message.txt", user, user_adr, config['targets'], config['subject'], config['attachments'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((config['host_addr'], config['port']))
        client = ssl.wrap_socket(client)
        print(request(client, f'EHLO {user}'))
        base64login = base64.b64encode(user_adr.encode()).decode()
        base64password = base64.b64encode(config['password'].encode()).decode()
        print(request(client, 'AUTH LOGIN'))
        print(request(client, base64login))
        print(request(client, base64password))
        err = request(client, f'MAIL FROM:{user_adr}')
        if err.startswith("503"):
            print("Неверный пароль или логин")
            return
        print(err)
        for target in config['targets']:
            print(request(client, f"RCPT TO:{target}"))
        print(request(client, 'DATA'))
        print(msg)
        print(request(client, msg))
        input("Для завершения работы нажмите ENTER")


if __name__ == "__main__":
    main()


