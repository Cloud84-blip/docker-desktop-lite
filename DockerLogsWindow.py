import tkinter as tk
from tkinter import ttk
import subprocess
import threading

class DockerLogsWindow(tk.Toplevel):
    def __init__(self, master, container_dic):
        super().__init__(master)
        self.container_ids = container_dic
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        self.log_threads = {}
        self.create_tabs()

    def create_tabs(self):
        for cid in self.container_ids.keys():
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=self.container_ids[cid])
            
            text_widget = tk.Text(tab, wrap='word')
            text_widget.pack(expand=True, fill='both')
            text_widget.tag_configure('info', foreground='blue')
            text_widget.tag_configure('warning', foreground='orange')
            text_widget.tag_configure('error', foreground='red', font=('TkDefaultFont', 10, 'bold'))
            text_widget.tag_configure('debug', foreground='grey')
            text_widget.tag_configure('good', foreground='green')
            
            start_button = ttk.Button(tab, text="Start watching", command=lambda c=cid, text_widget=text_widget: self.start_log_stream(c, text_widget))
            start_button.pack()
            stop_button = ttk.Button(tab, text="Stop watching", command=lambda c=cid: self.stop_logs(c))
            stop_button.pack()
            self.start_log_stream(cid, text_widget)

    def start_log_stream(self, container_id, text_widget):
        def log_stream():
            process = subprocess.Popen(['docker', 'logs', '-f', container_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.log_threads[container_id] = process
            while True:
                line = process.stdout.readline()
                if line:
                    self.format_line(text_widget, line)
                    text_widget.insert('end', line)
                    text_widget.see('end')
                else:
                    break

        t = threading.Thread(target=log_stream, daemon=True)
        t.start()
    
    def format_line(self, text_widget, line):
        # Simple exemple de formatage basé sur le contenu de la ligne
        if 'error' in line.lower():
            tag = 'error'
        elif '32m' or '39m' in line.lower():
            tag = 'good'
        elif 'warning' in line.lower():
            tag = 'warning'
        elif 'info' in line.lower():
            tag = 'info'
        elif 'debug' in line.lower():
            tag = 'debug'
        else:
            tag = None
            
        # Insertion de la ligne avec le tag approprié
        text_widget.insert('end', line, tag)

    def stop_logs(self, container_id):
        process = self.log_threads.get(container_id)
        if process:
            process.terminate()
            # Optionally, remove the tab if you want to close it after stopping logs.
            # index = self.notebook.index(container_id)
            # self.notebook.forget(index)
