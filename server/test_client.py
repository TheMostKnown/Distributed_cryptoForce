import socket
import hashlib


def calculate_hash(data, number):
    print(data, number)
    for i in range(pow(10, number - 1), pow(10, number)):
        sha = hashlib.md5(bytes(i))
        # sha.update(data.encode('utf-8'))
        # print(i, data, sha.hexdigest())
        if data == sha.hexdigest():
            return sha.hexdigest(), i
    else:
        return "None", "None"


# Функция для подключения к серверу и обработки вычислений
def connect_to_server(server_address):
    # Создаем сокет TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        client_socket.connect(server_address)

        # Получаем хэш и начальное число от сервера
        response = client_socket.recv(1024).decode('utf-8')
        target_hash, start_num = response.split(',')
        start_num = int(start_num)
        print(f"Полученное хэш: {target_hash}")
        print(f"Начальное число: {start_num}")

        while True:
            # for i in range(pow(10, start_num-1), pow(10, start_num)):
                # Вычисляем хэш от текущего числа
            current_hash, i = calculate_hash(target_hash, start_num)
            print(current_hash, i)

                # Если хэш совпадает с целевым хэшем, отправляем число серверу
            if current_hash == target_hash:
                client_socket.send(str(i).encode('utf-8'))
                break

            if current_hash == "None":
                client_socket.send("None".encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                print(response)
                start_num = int(response)
                # Иначе, увеличиваем число и продолжаем вычисления
                # start_num += 1
            print(start_num)

        print("Результат отправлен серверу")

    except Exception as e:
        print(f"Ошибка при подключении к серверу: {e}")

    finally:
        # Закрываем соединение
        client_socket.close()


if __name__ == '__main__':
    # Задаем адрес и порт сервера
    server_address = ('localhost', 9090)

    # Подключаемся к серверу и обрабатываем вычисления
    connect_to_server(server_address)
