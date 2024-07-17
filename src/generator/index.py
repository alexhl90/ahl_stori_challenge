import random
import datetime
import json
# Función para generar una fecha aleatoria en el rango dado
def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

# Generar datos
def generate_data(num_rows, num_negatives):
    start_date = datetime.date(2024, 8, 1)
    end_date = datetime.date(2024, 8, 30)
    data = []

    # Generar transacciones negativas
    for _ in range(num_negatives):
        date = random_date(start_date, end_date).strftime("%Y/%m/%d")  # Formatear fecha
        transaction = random.uniform(-1000, -1)  # Asegurar valor negativo
        transaction_str = f"{transaction:+.1f}"  # Asegurar el signo explícito
        data.append((date, transaction_str))

    # Generar transacciones positivas
    for _ in range(num_rows - num_negatives):
        date = random_date(start_date, end_date).strftime("%Y/%m/%d")  # Formatear fecha
        transaction = random.uniform(-1000, 10000)  # Asegurar valor positivo
        transaction_str = f"{transaction:+.1f}"  # Asegurar el signo explícito
        data.append((date, transaction_str))

    data.sort(key=lambda x: x[0])
    # Mezclar datos

    # Agregar IDs
    data = [(i, date, transaction) for i, (date, transaction) in enumerate(data)]

    return data

# Guardar datos en un archivo con formato pipe
def save_to_file(data, filename, user_email):
    try:
        with open(filename, 'w') as f:
            f.write(f"user_email:{user_email}\n")
            f.write("id,date,transaction\n")
            for row in data:
                f.write(f"{row[0]},{row[1]},{row[2]}\n")
    except Exception as e:
        print(f"Error saving data to file: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps("Error saving data to file.")
        }
    return {
        "statusCode": 200,
        "body": "Data saved successfully."
    }

def handler(event, context):
    num_rows = 100
    num_negatives = 20
    data = generate_data(num_rows, num_negatives)
    return save_to_file(data, '/shared_data/transactions.csv', 'ale.herreraluz@gmail.com')