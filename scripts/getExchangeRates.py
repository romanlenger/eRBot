import os
import subprocess
import logging
import datetime
import shutil
import win32com.client as win32
from app.variables import UPDATE_SCRIPT, INTERPRET


def run_update_kurs() -> None:
    script_path = UPDATE_SCRIPT
    python_interpreter = INTERPRET
    subprocess.run([python_interpreter, script_path])


def find_latest_excel_file(folder_path: str) -> str:
    latest_date = datetime.datetime.min
    latest_file = None

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.xlsx'):
                try:
                    date_str = file_name.split(' ')[3].split('.')[:2]  # Дата в названии файла после разделения по пробелу и точке
                    file_date = datetime.datetime.strptime('.'.join(date_str), "%d.%m")
                    if file_date > latest_date:
                        latest_date = file_date
                        latest_file = os.path.join(root, file_name)
                except (IndexError, ValueError) as error:
                    logging.error(error)
                    continue

    return latest_file


def create_new_file(file_path: str) -> str:
    if file_path is not None:
        today = datetime.datetime.now()
        if today.hour < 17:
            next_date = today
        else:
            next_date = today + datetime.timedelta(days=1)
        new_file_name = f"курс валют на {next_date.strftime('%d.%m.%Y')}.xlsx"

        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        if not os.path.exists(new_file_path):
            shutil.copy(file_path, new_file_path)
            logging.info(f"Создан новый файл: {new_file_path}")
        else:
            logging.warning('Такой файл уже существует')
    else:
        logging.error('Невозможно создать новый файл, возможно передано None')
        return None

    return new_file_path


def update_excel_file(file_path: str) -> str:
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        wb = excel.Workbooks.Open(file_path)
        
        # Обновляем каждый запрос Power Query
        for connection in wb.Connections:
            if connection.Type == win32.constants.xlConnectionTypeOLEDB:
                connection.OLEDBConnection.BackgroundQuery = False
                connection.Refresh()
        
        wb.Save()
        wb.Close()

        excel.Quit()
        logging.info("Запросы Power Query успешно обновлены.")
        return file_path
   
    except Exception as e:
        logging.error(f"Ошибка при обновлении запросов Power Query: {e}")
        return None

