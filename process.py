import psutil
import os

def get_top_cpu_processes(limit=5):
    # First, initialize CPU usage stats by calling cpu_percent once with interval=0
    for process in psutil.process_iter():
        process.cpu_percent(interval=None)
    
    # Now, fetch the CPU usage with a proper sampling interval
    process_list = [[p.name(), p.cpu_percent(interval=1.0)] for p in psutil.process_iter()]
    
    # Sort the processes by CPU usage in descending order and limit to the top 5
    sorted_list = sorted(process_list, key=lambda item: item[1], reverse=True)[:limit]
    
    print("Top CPU-consuming processes:")
    for process in sorted_list:
        print(f"Name: {process[0]}, CPU%: {process[1]}")
def get_top_mem_processes(limit=5):
    process_list = [[p.name(), p.memory_percent()] for p in psutil.process_iter()]
    sorted_list = sorted(process_list, key=lambda item: item[1], reverse=True)[:limit]
    print("Top Memory-consuming processes:")
    for process in sorted_list:
        print(f"Name: {process[0]}, Memory%: {process[1]}")
    return

def get_process_info(pid):
    try:
        proc = psutil.Process(pid)
        info = {
            'pid': pid,
            'name': proc.name(),
            'ppid': proc.ppid(),
            'uid': proc.uids().real,
            'cpu_usage': proc.cpu_percent(interval=1.0),
            'mem_usage': proc.memory_percent()
        }
        return info
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} not found.")
        return None

def search_process(query):
    for process in psutil.process_iter():
        if query in [str(process.pid), process.name()]:
            return get_process_info(process.pid)
    return None

def kill_process(pid=None, name=None):
    try:
        if pid:
            psutil.Process(pid).terminate()
            print(f"Process with PID {pid} terminated.")
        elif name:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == name:
                    proc.terminate()
                    print(f"Process {name} with PID {proc.info['pid']} terminated.")
                    return
            print(f"Process {name} not found.")
    except psutil.NoSuchProcess:
        print("No such process.")
    except psutil.AccessDenied:
        print("Permission denied.")

def monitor_process(pid=None, name=None):
    try:
        proc = psutil.Process(pid) if pid else next(p for p in psutil.process_iter() if p.name() == name)
        print(f"Monitoring process: {proc.name()} (PID: {proc.pid})")
        while True:
            print(f"CPU%: {proc.cpu_percent(interval=1.0)}, Memory%: {proc.memory_percent()}")
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} not found.")
    except psutil.AccessDenied:
        print("Permission denied.")

def main():
    while True:
        print("\nMenu:")
        print("1. Top 5 CPU usage processes")
        print("2. Top 5 Memory usage processes")
        print("3. Search for a process by name or PID")
        print("4. Get process info by PID")
        print("5. Kill a process by name or PID")
        print("6. Monitor a process by name or PID")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            get_top_cpu_processes()
        elif choice == '2':
            get_top_mem_processes()
        elif choice == '3':
            query = input("Enter the process name or PID to search: ")
            process_info = search_process(query)
            print(process_info)
        elif choice == '4':
            pid = int(input("Enter the PID to get process info: "))
            process_info = get_process_info(pid)
            print(process_info)
        elif choice == '5':
            query = input("Enter the process name or PID to kill: ")
            if query.isdigit():
                kill_process(pid=int(query))
            else:
                kill_process(name=query)
        elif choice == '6':
            query = input("Enter the process name or PID to monitor: ")
            if query.isdigit():
                monitor_process(pid=int(query))
            else:
                monitor_process(name=query)
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
