import tkinter as tk
from tkinter import ttk
import subprocess
import os

class DockerExecWindow:
    def __init__(self, root, selected_containers):
        self.root = root
        self.selected_containers = selected_containers
        self.create_window()

    def create_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Docker Exec Terminals")

        # Créer un onglet pour chaque conteneur sélectionné
        self.tab_control = ttk.Notebook(self.window)
        for container_id in self.selected_containers:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=container_id)
            exec_button = ttk.Button(tab, text="Open Terminal",
                                     command=lambda cid=container_id: self.open_terminal(cid))
            exec_button.pack(padx=10, pady=10)
        self.tab_control.pack(expand=1, fill="both")

    def open_terminal(self, container_id):
        # Sur macOS, ouvrez un nouveau terminal avec le shell dans le conteneur
        if os.sys.platform == "darwin":
            subprocess.run(["osascript", "-e",
                            f'tell app "Terminal" to do script "docker exec -it {container_id} /bin/bash"'],
                            capture_output=True)
        # Sur Windows, ouvrez un nouveau terminal avec le shell dans le conteneur
        elif os.sys.platform == "win32":
            subprocess.run(["start", "cmd", "/k", f"docker exec -it {container_id} sh"],
                            capture_output=True)
        # Sur Linux, ouvrez un nouveau terminal avec le shell dans le conteneur
        elif os.sys.platform == "linux":
            subprocess.run(["gnome-terminal", "--", "bash", "-c", f"docker exec -it {container_id} /bin/bash"],
                            capture_output=True)
        else:
            raise Exception("Platform not supported")
        
        # Fermer la fenêtre
        self.window.destroy()
        