import socket
import threading
import hashlib
from os import getppid
import json

# Функция для обработки клиента
def handle_client(client_socket, client_address, target_hash):
    global num_digits
    try:
        print(f"Новое подключение от клиента {client_address[0]}:{client_address[1]}")
        print(getppid())
        # Отправляем хэш клиенту
        #client_socket.send(f"{target_hash},{num_digits}".encode('utf-8'))
        client_socket.send(json.dumps({'number': number, 'hash': my_hash}).encode('utf-8'))
        while True:
            # Получаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

            if not data:
                # Если клиент закрыл соединение, выходим из цикла
                break

            if data == "None":
                # Если клиент прислал None, отправляем следующее число разрядов
                num_digits += 1
                client_socket.send(str(num_digits).encode('utf-8'))
            else:
                # Вычисляем хэш полученного числа и сравниваем с целевым хэшем
                # hashed_data = hashlib.md5(data.encode('utf-8')).hexdigest()
                # if hashed_data == target_hash:
                    # Если хэши совпадают, отправляем результат всем клиентам и завершаем соединение
                print(f"Клиент {client_address[0]}:{client_address[1]} нашел нужное число: {data}")
                response = f"Найдено нужное число: {data}"
                print(response)
                    # for client in clients:
                    #     client.send(response.encode('utf-8'))
                break
                # else:
                #     # Если хэши не совпадают, отправляем следующее число разрядов
                #     num_digits += 1
                #     client_socket.send(str(num_digits).encode('utf-8'))

    except Exception as e:
        print(f"Ошибка при обработке клиента {client_address[0]}:{client_address[1]}: {e}")

    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        print(f"Соединение с клиентом {client_address[0]}:{client_address[1]} закрыто")


if __name__ == '__main__':
    # Задаем адрес и порт сервера
    server_address = ('localhost', 9090)
    # target_hash = "c4ca4238a0b923820dcc509a6f75849b"  # Пример целевого хэша (MD5 хэш для строки "1")
    target_hash = hashlib.md5(bytes(112345)).hexdigest()
    num_digits: int = 0

    try:
        print("Сервер запущен и ожидает подключений...")

        # Создаем список для хранения соединений с клиентами
        clients = []

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
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, target_hash))
            client_thread.start()

            # Добавляем сокет клиента в список
            clients.append(client_socket)
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
