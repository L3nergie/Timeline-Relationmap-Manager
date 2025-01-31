import os
import json
import uuid
import logging
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLabel, QLineEdit, QFormLayout,
    QListWidget, QListWidgetItem, QStackedWidget, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def CreateEssentiel():
    """Crée les répertoires et fichiers essentiels pour l'application."""
    # Obtenir le répertoire du script en cours d'exécution
    project_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Création du répertoire data : {project_dir}")

    # Définir les chemins des répertoires et fichiers
    data_dir = os.path.join(project_dir, 'data')
    json_dir = os.path.join(data_dir, 'json')
    json_file_path = os.path.join(json_dir, 'project_directories.json')

    # Créer les répertoires si ils n'existent pas
    if not os.path.exists(data_dir):
        logging.info(f"Création du répertoire data : {data_dir}")
        os.makedirs(data_dir)
    if not os.path.exists(json_dir):
        logging.info(f"Création du répertoire json : {json_dir}")
        os.makedirs(json_dir)

    # Créer le fichier JSON si il n'existe pas
    if not os.path.exists(json_file_path):
        logging.info(f"Création du fichier JSON : {json_file_path}")
        with open(json_file_path, 'w') as file:
            json.dump({}, file, indent=4)

    return json_file_path  # Retourner le chemin du fichier JSON

# Chemin du fichier JSON pour enregistrer les répertoires
json_file_path = CreateEssentiel()

def load_project_directories():
    """Charge les projets depuis le fichier JSON."""
    if os.path.exists(json_file_path):
        logging.info(f"Chargement des projets depuis : {json_file_path}")
        with open(json_file_path, 'r') as file:
            return json.load(file)
    logging.warning(f"Le fichier JSON n'existe pas : {json_file_path}")
    return {}

def save_project_directories(directories):
    """Sauvegarde les projets dans le fichier JSON."""
    logging.info(f"Sauvegarde des projets dans : {json_file_path}")
    with open(json_file_path, 'w') as file:
        json.dump(directories, file, indent=4)

class ProjectForm(QWidget):
    project_added = Signal()  # Signal pour indiquer qu'un projet a été ajouté

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un nouveau projet")
        self.setGeometry(100, 100, 400, 200)

        # Définir un fond noir et une bordure blanche de 2px
        self.setStyleSheet("""
            background-color: black;
            border: 2px solid white;
            border-radius: 5px;
        """)

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Entrez le nom du projet")
        self.project_name_input.setStyleSheet("color: white;")  # Texte blanc pour le QLineEdit
        self.layout.addRow("Nom du projet:", self.project_name_input)

        self.project_directory_button = QPushButton("Sélectionner l'emplacement")
        self.project_directory_button.clicked.connect(self.select_directory)
        self.project_directory_button.setStyleSheet("color: white;")  # Texte blanc pour le bouton
        self.layout.addRow(self.project_directory_button)

        self.add_project_button = QPushButton("Ajouter le projet")
        self.add_project_button.clicked.connect(self.add_project)
        self.add_project_button.setStyleSheet("color: white;")  # Texte blanc pour le bouton
        self.layout.addRow(self.add_project_button)

        self.project_directory = ""

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner un répertoire")
        if directory:
            logging.info(f"Répertoire sélectionné : {directory}")
            self.project_directory = directory
            self.project_directory_button.setText(f"Emplacement sélectionné: {directory}")

    def add_project(self):
        project_name = self.project_name_input.text()
        if not project_name or not self.project_directory:
            logging.warning("Veuillez remplir tous les champs.")
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        project_directories = load_project_directories()
        project_id = str(uuid.uuid4())
        project_directories[project_id] = {
            "name": project_name,
            "directory": self.project_directory,
            "added_date": datetime.now().isoformat()
        }
        save_project_directories(project_directories)
        logging.info(f"Projet ajouté : {project_name}")
        QMessageBox.information(self, "Succès", f"Projet '{project_name}' ajouté avec succès.")
        self.project_added.emit()  # Émettre le signal pour indiquer qu'un projet a été ajouté
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestionnaire de Timeline en Relationmap")
        self.setGeometry(100, 100, 600, 400)

        # Utiliser un QStackedWidget pour basculer entre les vues
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Créer le widget principal
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.project_list_label = QLabel("Liste des projets:")
        self.project_list_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.main_layout.addWidget(self.project_list_label)

        self.project_list = QListWidget()
        self.project_list.itemDoubleClicked.connect(self.show_project_details)
        self.main_layout.addWidget(self.project_list)

        self.add_project_button = QPushButton("Ajouter un nouveau projet")
        self.add_project_button.clicked.connect(self.show_project_form)
        self.main_layout.addWidget(self.add_project_button)

        # Ajouter le widget principal au QStackedWidget
        self.stacked_widget.addWidget(self.main_widget)

        # Créer le formulaire d'ajout de projet
        self.project_form = ProjectForm()
        self.project_form.project_added.connect(self.update_project_list)
        self.project_form.destroyed.connect(self.show_main_widget)  # Revenir au widget principal après la fermeture du formulaire
        self.stacked_widget.addWidget(self.project_form)

        self.update_project_list()

    def update_project_list(self):
        """Met à jour la liste des projets."""
        self.project_list.clear()
        project_directories = load_project_directories()
        if project_directories:
            logging.info(f"Nombre de projets chargés : {len(project_directories)}")
            for project_id, project in project_directories.items():
                item = QListWidgetItem()
                item.setData(Qt.UserRole, project_id)

                # Créer un widget personnalisé pour chaque élément de la liste
                widget = QWidget()
                layout = QHBoxLayout()
                widget.setLayout(layout)

                # Ajouter le nom du projet
                label = QLabel(project['name'])
                layout.addWidget(label)

                # Ajouter des boutons d'action (voir, modifier, supprimer) avec des icônes personnalisées
                btn_view = QPushButton()
                btn_view.setIcon(QIcon(QPixmap("view_icon.png")))  # Icône "voir"
                btn_view.clicked.connect(lambda _, pid=project_id: self.view_project(pid))
                layout.addWidget(btn_view)

                btn_edit = QPushButton()
                btn_edit.setIcon(QIcon(QPixmap("edit_icon.png")))  # Icône "modifier"
                btn_edit.clicked.connect(lambda _, pid=project_id: self.edit_project(pid))
                layout.addWidget(btn_edit)

                btn_delete = QPushButton()
                btn_delete.setIcon(QIcon(QPixmap("delete_icon.png")))  # Icône "supprimer"
                btn_delete.clicked.connect(lambda _, pid=project_id: self.delete_project(pid))
                layout.addWidget(btn_delete)

                # Définir le widget personnalisé comme item de la liste
                item.setSizeHint(widget.sizeHint())
                self.project_list.addItem(item)
                self.project_list.setItemWidget(item, widget)
        else:
            logging.info("Aucun projet trouvé.")
            self.project_list.addItem("Aucun projet pour le moment.")

    def show_project_form(self):
        self.stacked_widget.setCurrentWidget(self.project_form)  # Afficher le formulaire

    def show_main_widget(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)  # Revenir au widget principal
        self.update_project_list()  # Mettre à jour la liste des projets

    def show_project_details(self, item):
        project_id = item.data(Qt.UserRole)
        project_directories = load_project_directories()
        project = project_directories.get(project_id)
        if project:
            logging.info(f"Affichage des détails du projet : {project['name']}")
            QMessageBox.information(self, "Détails du projet", f"Nom: {project['name']}\nEmplacement: {project['directory']}\nDate d'ajout: {project['added_date']}")

    def view_project(self, project_id):
        project_directories = load_project_directories()
        project = project_directories.get(project_id)
        if project:
            logging.info(f"Voir le projet : {project['name']}")
            QMessageBox.information(self, "Voir le projet", f"Nom: {project['name']}\nEmplacement: {project['directory']}\nDate d'ajout: {project['added_date']}")

    def edit_project(self, project_id):
        logging.info(f"Modification du projet avec l'ID : {project_id}")
        QMessageBox.information(self, "Modifier le projet", f"Modifier le projet avec l'ID: {project_id}")

    def delete_project(self, project_id):
        reply = QMessageBox.question(self, "Supprimer le projet", "Êtes-vous sûr de vouloir supprimer ce projet ?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            project_directories = load_project_directories()
            if project_id in project_directories:
                logging.info(f"Suppression du projet : {project_directories[project_id]['name']}")
                del project_directories[project_id]
                save_project_directories(project_directories)
                self.update_project_list()  # Mettre à jour la liste après suppression

def main():
    # Créer les répertoires et fichiers essentiels
    CreateEssentiel()

    # Lancer l'application
    app = QApplication([])

    # Appliquer un style CSS global
    app.setStyleSheet("""
        QWidget {
            font-size: 14px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
            color: black;  /* Texte noir par défaut */
        }
        QListWidget {
            border: 1px solid #ccc;
            border-radius: 3px;
        }
    """)

    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
