import threading
import time
import subprocess
from datetime import datetime, timedelta

class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()
    
    def add_task(self, name, command, delay):
        with self.lock:
            execution_time = datetime.now() + timedelta(seconds=delay)
            task = {'name': name, 'command': command, 'execution_time': execution_time}
            self.tasks.append(task)
            print(f"Task {name} scheduled to run at {execution_time}.")

    def remove_task(self, name):
        with self.lock:
            self.tasks = [task for task in self.tasks if task['name'] != name]
            print(f"Task {name} removed.")

    def list_tasks(self):
        with self.lock:
            for task in self.tasks:
                print(f"Task {task['name']}: scheduled for {task['execution_time']}")

    def run_pending(self):
        while True:
            now = datetime.now()
            with self.lock:
                for task in list(self.tasks):
                    if task['execution_time'] <= now:
                        threading.Thread(target=self.execute_task, args=(task['command'],)).start()
                        print(f"Task {task['name']} executed at {now}")
                        self.tasks.remove(task)
            time.sleep(1)
    
    def execute_task(self, command):
        subprocess.run(command, shell=True)

scheduler = TaskScheduler()

def run_scheduler():
    scheduler.run_pending()

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

while True:
    command = input("Enter command (add, remove, list, exit): ").strip().lower()
    if command == 'add':
        name = input("Task name: ").strip()
        cmd = input("Command to execute: ").strip()
        delay = int(input("Delay (seconds): ").strip())
        scheduler.add_task(name, cmd, delay)
    elif command == 'remove':
        name = input("Task name: ").strip()
        scheduler.remove_task(name)
    elif command == 'list':
        scheduler.list_tasks()
    elif command == 'exit':
        break
    else:
        print("Invalid command.")
