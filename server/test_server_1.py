import socket
import threading
import hashlib
from os import getppid
import json


# Функция для обработки клиента
def handle_client(client_socket, client_address, client_id, target_hash):
    global num_digits
    try:
        print(f"Новое подключение от клиента {client_address[0]}:{client_address[1]}")
        print(getppid())

        # Отправляем хэш клиенту
        client_socket.send(json.dumps({'number': num_digits, 'hash': target_hash}).encode('utf-8'))
        print(f"I'm before while loop, sending: {json.dumps({'number': num_digits, 'hash': target_hash}).encode('utf-8')}")

        while True:
            # Получаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Got from client:{data}")

            if not data:
                # Если клиент закрыл соединение, выходим из цикла
                break

            if data == "None":
                # Если клиент прислал None, отправляем следующее число разрядов
                num_digits += 1
                client_socket.send(json.dumps({'number': num_digits, 'hash': target_hash}).encode('utf-8'))
                print(f"Im in data == None, sending: {json.dumps({'number': num_digits, 'hash': target_hash}).encode('utf-8')}")
            else:
                # Если хэши совпадают, отправляем результат всем клиентам и завершаем соединение
                print(f"Клиент {client_address[0]}:{client_address[1]} нашел нужное число: {data}")
                response = f"Найдено нужное число: {data}"
                print(response)
                interrupt_other_clients(client_id)
                break

    except Exception as e:
        print(f"Ошибка при обработке клиента {client_address[0]}:{client_address[1]}: {e}")

    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        print(f"Соединение с клиентом {client_address[0]}:{client_address[1]} закрыто")


# Функция для отправки прерывания другим клиентам
def interrupt_other_clients(current_client_id):
    for client_id, client_socket in clients.items():
        if client_id != current_client_id:
            try:
                # Отправляем прерывание клиенту
                client_socket.send("Interrupt".encode('utf-8'))
            except Exception as e:
                print(f"Ошибка при отправке прерывания клиенту {client_id}: {e}")


if __name__ == '__main__':
    # Задаем адрес и порт сервера
    server_address = ('10.1.1.209', 9090)
    target_hash = "698d51a19d8a121ce581499d7b701668"  # Пример целевого хэша (MD5 хэш для строки "111")
    #target_hash = hashlib.md5(bytes(11)).hexdigest()
    num_digits: int = 0

    try:
        print("Сервер запущен и ожидает подключений...")

        # Создаем список для хранения соединений с клиентами
        clients = {}
        client_id = 1

        # Создаем сокет TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Задаем опцию переиспользования адреса
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Привязываем сокет к заданному адресу и порту
        server_socket.bind(server_address)

        # Начинаем прослушивать входящие подключения
        server_socket.listen(5)

        while True:
            # Принимаем входящее подключение от клиента
            client_socket, client_address = server_socket.accept()

            # Создаем новый поток для обработки клиента
            num_digits += 1
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id, target_hash))
            client_thread.start()

            # Добавляем сокет клиента в список
            clients[client_id] = client_socket
            client_id += 1
            # num_digits += 1

    except Exception as e:
        print(f"Ошибка при работе сервера: {e}")

    finally:
        # Закрываем все соединения с клиентами
        for client in clients:
            client.close()

        # Закрываем сокет сервера
        server_socket.close()
        print("Сервер остановлен")
