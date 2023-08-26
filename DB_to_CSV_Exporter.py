import os
import sqlite3
import csv

db_files = [file for file in os.listdir() if file.endswith(".db")]
total_files = len(db_files)

print(f"Процесс конвертации: 0/{total_files} файлов (00.00% завершено)")

for index, db_file in enumerate(db_files, start=1):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_index, table in enumerate(tables, start=1):
        table_name = table[0]
        
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({table_name});")
        column_info = cursor.fetchall()
        column_names = [column[1] for column in column_info]

        csv_file_name = os.path.splitext(db_file)[0] + f"_{table_name}.csv"

        with open(csv_file_name, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(column_names)

            csv_writer.writerows(data)

    connection.close()

    progress = (index / total_files) * 100
    print(f"Процесс конвертации: {index}/{total_files} файлов ({progress:.2f}% завершено)")

print("Конвертация завершена.")
