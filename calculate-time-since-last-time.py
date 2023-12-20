import datetime
import os
import zipfile

def add_to_history(line):
    with open("history.txt", "a") as file:
        file.write(line)

def backup_file():
    if os.path.exists("tasks.txt"):
        # Crear la carpeta backups si no existe
        if not os.path.exists("backups"):
            os.mkdir("backups")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = os.path.join("backups", f"{timestamp}.zip")
        
        with zipfile.ZipFile(backup_path, "w") as backup:
            backup.write("tasks.txt")
        print("Brackup created")
    else:
        print("File not found")

def main_menu():
    recalculate_time()
    print("0.- List tasks")
    print("1.- Add New Task")
    print("2.- Modify Time of Existing Task")
    print("3.- Recalculate Time")
    print("4.- Exit")
    return int(input("Choose an option: "))

def list_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            for idx, task in enumerate(tasks):
                print(f"{idx}. {task.strip()}")
    else:
        print("Aún no has añadido tareas.")

def add_task():
    task_name = input("Escribe el nombre de la tarea: ")
    date_choice = input("¿Quieres usar la fecha actual? (s/n): ").lower()
    if date_choice == "s":
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        date = input("Introduce la fecha (formato: YYYY-MM-DD HH:MM:SS): ")

    line = f"{task_name}, {date}\n"
    with open("tasks.txt", "a") as file:
        file.write(line)

    # Añadir al histórico
    add_to_history(line)

def modify_task():
    list_tasks()
    task_id = int(input("Introduce el ID de la tarea que quieres modificar: "))

    date_choice = input("¿Quieres usar la fecha actual? (s/n): ").lower()
    if date_choice == "s":
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        date = input("Introduce la nueva fecha (formato: YYYY-MM-DD HH:MM:SS): ")

    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    line = f"{tasks[task_id].split(',')[0]}, {date}\n"
    tasks[task_id] = line

    with open("tasks.txt", "w") as file:
        file.writelines(tasks)

    # Añadir al histórico
    add_to_history(line)

def recalculate_time():
    print("")
    print("")
    print("")
    print("")
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            
            now = datetime.datetime.now()
            deltas = []

            # Calcular la diferencia de tiempo para cada tarea
            for task in tasks:
                name, date = task.strip().split(", ")
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                delta = now - date
                deltas.append((name, date, delta))

            # Ordenar las tareas por la diferencia de tiempo de mayor a menor
            deltas_sorted = sorted(deltas, key=lambda x: x[2], reverse=True)
            
            for name, date, delta in deltas_sorted:
                print(f"{name} - Última vez realizado hace {delta.days} días y {delta.seconds // 3600} horas.")
    else:
        print("No se encontraron tareas.")
    print("")
    print("")
    print("")
    print("")


if __name__ == "__main__":
    backup_file()
    while True:
        choice = main_menu()
        if choice == 0:
            list_tasks()
        elif choice == 1:
            add_task()
        elif choice == 2:
            modify_task()
        elif choice == 3:
            recalculate_time()
        elif choice == 4:
            break

