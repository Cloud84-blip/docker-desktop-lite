import tkinter as tk
from tkinter import ttk
import subprocess
import re
from DockerLogsWindow import DockerLogsWindow
from DockerExecWindow import DockerExecWindow

def docker_ps():
    try:
        # Utilisez subprocess.run pour exécuter la commande et capturer la sortie
        result = subprocess.run(['docker', 'ps', '--format', "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Affiche la sortie standard
        print("Voici la liste des conteneurs Docker en cours d'exécution:")
        return result.stdout
        
        # Si vous voulez également traiter des erreurs, décommentez la ligne suivante:
        # print(result.stderr)  # Pour afficher les erreurs potentielles

    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite lors de l'exécution de 'docker ps': {e}")
    except FileNotFoundError:
        print("Il semble que Docker ne soit pas installé ou ne soit pas dans le PATH de l'utilisateur courant.")

def docker_images():
    try:
        # Utilisez subprocess.run pour exécuter la commande et capturer la sortie
        result = subprocess.run(['docker', 'images', '--format', "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Affiche la sortie standard
        print("Voici la liste des images Docker:")
        return result.stdout
        
        # Si vous voulez également traiter des erreurs, décommentez la ligne suivante:
        # print(result.stderr)  # Pour afficher les erreurs potentielles

    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite lors de l'exécution de 'docker images': {e}")
    except FileNotFoundError:
        print("Il semble que Docker ne soit pas installé ou ne soit pas dans le PATH de l'utilisateur courant.")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Docker Desktop Lite")
        self.geometry("900x500")
        self.resizable()
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        #self.checked_items = set()  # Ensemble pour stocker les IDs des conteneurs cochés
        self.checked_items = dict()
        self.checked_images = dict()
        self.create_widgets()
        self.create_widgets_for_images()
        self.create_widegets_for_utils()


    def create_widegets_for_utils(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Utils")
        
        self.prune_button = ttk.Button(tab, text="prune all", command=self.docker_system_prune)
        self.prune_button.grid(row=0, column=0, sticky='nsew')

    def create_widgets_for_images(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Images")
        
        self.label_image = tk.Text(tab, wrap='word', height=10, width=90)
        self.label_image.configure(state='disabled', inactiveselectbackground=self.label_image.cget("selectbackground"))
        self.label_image.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        # Ajouter un cadre pour contenir les cases à cocher
        self.check_frame_image = tk.Frame(tab)
        self.check_frame_image.grid(row=1, column=0, sticky='nsew')
        
        self.button_image = ttk.Button(tab, text="docker images", command=self.on_button_click_images)
        self.button_image.grid(row=0, column=2, sticky='e')
        
        self.button_image_kill = ttk.Button(tab, text="docker kill", command=self.docker_kill_and_remove_images)
        self.button_image_kill.grid(row=1, column=2, sticky='e')
        
        self.check_all_button_image = ttk.Button(tab, text="Select all", command=self.check_all_images)
        self.check_all_button_image.grid(row=1, column=4, sticky='w')
    
    def create_widgets(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Containers")
        
        self.label = tk.Text(tab, wrap='word', height=10, width=90)
        self.label.configure(state='disabled', inactiveselectbackground=self.label.cget("selectbackground"))
        self.label.grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        self.button = ttk.Button(tab, text="docker ps", command=self.on_button_click)
        self.button.grid(row=0, column=2, sticky='e')

        # Ajouter un cadre pour contenir les cases à cocher
        self.check_frame = tk.Frame(tab)
        self.check_frame.grid(row=1, column=0, sticky='nsew')
        
        self.button_logs = ttk.Button(tab, text="docker logs", command=self.docker_logs)
        self.button_logs.grid(row=1, column=2, sticky='e')
        
        self.button_exec = ttk.Button(tab, text="docker exec", command=self.docker_exec)
        self.button_exec.grid(row=1, column=3, sticky='e')
        
        self.button_kill = ttk.Button(tab, text="docker kill", command=self.docker_kill_and_remove)
        self.button_kill.grid(row=1, column=4, sticky='e')
        
        self.check_all_button = ttk.Button(tab, text="Select all", command=self.check_all)
        self.check_all_button.grid(row=2, column=3, sticky='w')
        
    def check_all(self):
        for widget in self.check_frame.winfo_children():
            widget.configure(state='normal')
            widget.select()
            widget.configure(state='disabled')
        
        # Mettre à jour les conteneurs sélectionnés
        self.checked_items.clear()
        for line in self.label.get('1.0', tk.END).strip().split('\n')[1:]:
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 3:
                container_id, name, status = parts[0], parts[1], ' '.join(parts[2:])
                self.checked_items[container_id] = name
        print(self.checked_items)

    def check_all_images(self):
        for widget in self.check_frame_image.winfo_children():
            widget.configure(state='normal')
            widget.select()
            widget.configure(state='disabled')
        
        # Mettre à jour les conteneurs sélectionnés
        self.checked_images.clear()
        for line in self.label_image.get('1.0', tk.END).strip().split('\n')[1:]:
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 3:
                repository, tag, image_id, size = parts[0], parts[1], parts[2], parts[3]
                self.checked_images[image_id] = tag, size
        print(self.checked_images)

    def docker_kill_and_remove(self):
        for container_id in self.checked_items.keys():
            try:
                subprocess.run(['docker', 'rm', '-f', container_id], check=True)
                print(f"Container {container_id} has been killed and removed.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove container {container_id}: {e}")
        
        # Mettre à jour les checkboxes et la liste des conteneurs sélectionnés
        self.update_checkboxes()
    
    def docker_kill_and_remove_images(self):
        for image_id in self.checked_images.keys():
            try:
                subprocess.run(['docker', 'rmi', '-f', image_id], check=True)
                print(f"Image {image_id} has been killed and removed.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove image {image_id}: {e}")
    
    # Mettre à jour les checkboxes après la suppression des conteneurs
    def update_checkboxes(self):
        # Effacer tous les widgets dans le frame des checkboxes
        for widget in self.check_frame.winfo_children():
            widget.destroy()
        
        # Effacer la liste des conteneurs sélectionnés
        self.checked_items.clear()
        
        # Appeler la fonction qui recrée les checkboxes
        self.on_button_click()
        
        for widget in self.check_frame_image.winfo_children():
            widget.destroy()
            
        self.checked_images.clear()
        
        self.on_button_click_images()
    
    def update_checked_images(self, image_id, tag, size, is_checked):
        if is_checked:
            self.checked_images[image_id] = tag, size
        else:
            del self.checked_images[image_id]
        print(self.checked_images)
    
    def docker_logs(self):
        self.logs_window = DockerLogsWindow(self, self.checked_items)
        
    def docker_exec(self):
        self.exec_window = DockerExecWindow(self, self.checked_items)

    def update_checked_items(self, container_id, name, is_checked):
        if is_checked:
            self.checked_items[container_id] = name
        else:
            del self.checked_items[container_id]
        print(self.checked_items)  # Affiche la liste mise à jour

    def on_button_click(self):
        text = docker_ps()
        if text:
            lines = text.strip().split('\n')[1:]  # Omettre l'en-tête de la table
            
            # Activer le widget pour la mise à jour
            self.label.configure(state='normal')
            # Effacer le contenu actuel
            self.label.delete('1.0', tk.END)
            # Insérer le nouveau texte
            self.label.insert('1.0', text)
            # Désactiver le widget pour empêcher la modification par l'utilisateur
            self.label.configure(state='disabled')
            
            # Nettoyer les anciennes cases à cocher
            for widget in self.check_frame.winfo_children():
                widget.destroy()

            # Créer une case à cocher pour chaque conteneur
            for line in lines:
                parts = re.split(r'\s{2,}', line)
                
                if len(parts) >= 3:  # S'assurer qu'il y a suffisamment de parties pour ID, nom et statut
                    container_id, image, status, ports = parts[0], parts[1], ' '.join(parts[2:]), parts[3]
                    var = tk.BooleanVar()
                    cb = tk.Checkbutton(self.check_frame, text=f"{image.upper()}", variable=var,
                                        command=lambda id=container_id, name=image, var=var: self.update_checked_items(id, name, var.get()))
                    cb.pack(anchor='w')

    def on_button_click_images(self):
        text = docker_images()
        if text:
            lines = text.strip().split('\n')[1:]
            
            # Activer le widget pour la mise à jour
            self.label_image.configure(state='normal')
            # Effacer le contenu actuel
            self.label_image.delete('1.0', tk.END)
            # Insérer le nouveau texte
            self.label_image.insert('1.0', text)
            # Désactiver le widget pour empêcher la modification par l'utilisateur
            self.label_image.configure(state='disabled')
            
            # Nettoyer les anciennes cases à cocher
            for widget in self.check_frame_image.winfo_children():
                widget.destroy()

            # Créer une case à cocher pour chaque conteneur
            for line in lines:
                parts = re.split(r'\s{2,}', line)
                
                if len(parts) >= 3:  # S'assurer qu'il y a suffisamment de parties pour ID, nom et statut
                    repository, tag, image_id, size = parts[0], parts[1], parts[2], parts[3]
                    var = tk.BooleanVar()
                    cb = tk.Checkbutton(self.check_frame_image, text=f"{repository}", variable=var,
                                        command=lambda id=image_id, tag=tag, size=size, var=var: self.update_checked_images(id, tag, size, var.get()))
                    cb.pack(anchor='w')

    def docker_system_prune(self):
        try:
            subprocess.run(['docker', 'system', 'prune', '-a', '-f'], check=True)
            print(f"System has been pruned.")
            subprocess.run(['docker', 'volume', 'prune', '-a', '-f'], check=True)
            print(f"Volumes has been pruned.")
            subprocess.run(['docker', 'buildx', 'prune', '-a', '-f'], check=True)
            print(f"Buildx has been pruned.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to prune system: {e}")
        
        # Mettre à jour les checkboxes et la liste des conteneurs sélectionnés
        self.update_checkboxes()
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    

