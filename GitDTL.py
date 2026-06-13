from __future__ import annotations

import datetime as _dt
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk


APP_NAME = "GitDTL"
APP_VERSION = "v1.0-3"
APP_SUBTITLE = "Git simplifié pour les projets DTL"
HELP_FILE = "aide.md"
EXPERT_FILE = "expert_git.md"
WELCOME_COOKIE = ".gitdtl_welcome_seen"
DEFAULT_HELP_TEXTS = {
    "welcome": (
        "Bienvenue dans GitDTL.\n\n"
        "GitDTL vous accompagne dans les opérations Git courantes sans passer par la ligne de commande.\n\n"
        "Commencez par choisir un dossier de projet, puis utilisez le menu numéroté."
    ),
    "first_project_choice": (
        "GitDTL doit savoir quel dossier vous voulez gérer.\n\n"
        "Choisissez 'Créer un nouveau projet' pour sélectionner ou créer un dossier, puis initialiser Git.\n"
        "Choisissez 'Gérer un projet existant' pour sélectionner un dossier déjà présent sur votre ordinateur."
    ),
    "create_git_repository": (
        "Un projet Git permet de suivre l'historique des fichiers.\n\n"
        "Choisissez 'Créer le projet Git' pour lancer git init dans le dossier courant.\n"
        "Choisissez 'Annuler' pour revenir au menu sans créer de dépôt."
    ),
    "remove_file_action": (
        "Le premier choix supprime l'élément du disque et de Git.\n\n"
        "Le deuxième choix conserve l'élément dans le dossier, le retire seulement du suivi Git "
        "et l'ajoute dans .gitignore pour qu'il ne soit plus proposé ensuite.\n\n"
        "Annuler ne modifie rien."
    ),
    "commit_message": (
        "Cette description est le message de commit.\n\n"
        "Elle doit expliquer brièvement ce qui vient de changer, par exemple :\n"
        "- Ajout du logo NetDTL\n"
        "- Correction de la suppression des fichiers\n"
        "- Mise à jour de l'interface principale"
    ),
    "release_version": (
        "Indiquez le numéro de version à publier.\n\n"
        "Exemples : 1.0.0, 1.1.0, 2.0.0.\n"
        "GitDTL ajoutera automatiquement le préfixe v pour créer le tag Git."
    ),
    "release_confirmation": (
        "Une version crée un point de repère officiel dans l'historique Git.\n\n"
        "GitDTL va créer un commit, poser un tag de version, puis publier le tout sur GitHub.\n"
        "Utilisez cette action uniquement quand la version est prête à être conservée."
    ),
    "clear_log": (
        "Le journal contient les actions et erreurs enregistrées par GitDTL.\n\n"
        "Effacer le journal vide le fichier de log courant, mais ne modifie pas le projet Git."
    ),
    "publish_with_uncommitted_changes": (
        "Publier envoie le projet vers le dépôt GitHub configuré.\n\n"
        "Si des fichiers ne sont pas validés dans un commit, ils ne feront pas partie de la version publiée. "
        "Il est souvent préférable d'ajouter les fichiers puis de valider les changements avant de publier."
    ),
    "github_remote_url": (
        "Git a besoin de connaître l'adresse du dépôt GitHub où publier le projet.\n\n"
        "Créez d'abord un dépôt vide sur GitHub, puis copiez son URL.\n"
        "Exemples :\n"
        "- https://github.com/compte/projet.git\n"
        "- git@github.com:compte/projet.git"
    ),
    "clone_repository_url": (
        "Cette action crée une copie locale d'un dépôt Git déjà existant.\n\n"
        "Copiez l'adresse du dépôt GitHub, par exemple :\n"
        "- https://github.com/compte/projet.git\n"
        "- git@github.com:compte/projet.git\n\n"
        "GitDTL vous demandera ensuite dans quel dossier parent créer le projet."
    ),
    "common_python_ignores": (
        "Ces dossiers sont produits automatiquement par Python ou par GitDTL.\n\n"
        "Les ajouter à .gitignore évite qu'ils apparaissent dans les fichiers non suivis."
    ),
    "stage_modified_files": (
            "Cette action lance git add sur les fichiers modifiés déjà connus de Git "
            "et sur les nouveaux fichiers non suivis.\n\n"
            "Elle prépare ces changements pour la prochaine validation."
    ),
}
DEFAULT_EXPERT_RULES = [
    {
        "name": "Aucun dépôt distant configuré",
        "patterns": ["no configured push destination", "git remote add"],
        "advice": (
            "Git ne connaît pas encore l'adresse GitHub du projet.\n\n"
            "Dans GitDTL, utilisez l'option 7 : l'outil demandera l'adresse du dépôt GitHub "
            "et configurera automatiquement le remote origin."
        ),
    },
    {
        "name": "Branche sans upstream",
        "patterns": ["has no upstream branch", "--set-upstream"],
        "advice": (
            "La branche locale n'est pas encore reliée à sa branche GitHub.\n\n"
            "GitDTL sait corriger ce cas automatiquement avec :\n"
            "git push --set-upstream origin <branche>"
        ),
    },
    {
        "name": "Rien à valider",
        "patterns": ["nothing to commit", "working tree clean"],
        "advice": (
            "Il n'y a plus de changement local à valider.\n\n"
            "L'étape suivante logique est de publier avec l'option 7, ou simplement de revenir au menu."
        ),
    },
    {
        "name": "Push refusé par avance distante",
        "patterns": ["failed to push some refs", "fetch first"],
        "advice": (
            "Le dépôt GitHub contient probablement des changements absents du dossier local.\n\n"
            "Commencez par l'option 10 pour synchroniser depuis GitHub, puis relancez la publication."
        ),
    },
    {
        "name": "Authentification GitHub refusée",
        "patterns": ["authentication failed", "permission denied", "could not read from remote repository"],
        "advice": (
            "GitHub refuse l'accès au dépôt distant.\n\n"
            "Vérifiez l'URL du remote, le compte GitHub utilisé, et l'authentification HTTPS ou SSH."
        ),
    },
    {
        "name": "Fichier introuvable pour Git",
        "patterns": ["pathspec", "did not match any file"],
        "advice": (
            "Git ne trouve pas le fichier demandé.\n\n"
            "Vérifiez que le fichier existe encore dans le dossier du projet, puis relancez l'action."
        ),
    },
]

COLOR_BG = "#090d0f"
COLOR_PANEL = "#12171b"
COLOR_TERMINAL = "#070b0d"
COLOR_TEXT = "#00ff2f"
COLOR_WELCOME_TEXT = "#00ff00"
COLOR_MUTED = "#9aa0a6"
COLOR_BLUE = "#2f8cff"
COLOR_DEC_BLUE = "#00a0e3"
COLOR_WARNING = "#ffbf00"
COLOR_ERROR = "#ff1a1a"
COLOR_BORDER = "#30363d"
COLOR_BORDER_LIGHT = "#d8dee9"
COLOR_INPUT_BG = "#f5f5f5"
COLOR_INPUT_TEXT = "#0b0d0f"
FONT_MONO = ("Courier New", 10, "bold")
FONT_MONO_SMALL = ("Courier New", 9, "bold")
FONT_TITLE = ("Courier New", 22, "bold")
FONT_MENU = ("Courier New", 11)

NETDTL_LOGO_BASE64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAQ4AAABfCAYAAAAZFClDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJ'
    'cEhZcwAADsMAAA7DAcdvqGQAAAAPdEVYdFNvZnR3YXJlAEdvb2dsZQJuDl8AAALSaVRYdFhNTDpjb20uYWRvYmUu'
    'eG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCc/Pg0KPHg6'
    'eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyI+PHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3Lncz'
    'Lm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj48cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0idXVpZDpm'
    'YWY1YmRkNS1iYTNkLTExZGEtYWQzMS1kMzNkNzUxODJmMWIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNv'
    'bS94YXAvMS4wLyI+PHhtcDpDcmVhdG9yVG9vbD5Hb29nbGU8L3htcDpDcmVhdG9yVG9vbD48eG1wOmNyZWF0b3J0'
    'b29sPkdvb2dsZTwveG1wOmNyZWF0b3J0b29sPjwvcmRmOkRlc2NyaXB0aW9uPjxyZGY6RGVzY3JpcHRpb24gcmRm'
    'OmFib3V0PSJ1dWlkOmZhZjViZGQ1LWJhM2QtMTFkYS1hZDMxLWQzM2Q3NTE4MmYxYiIgeG1sbnM6ZXhpZj0iaHR0'
    'cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iPjxleGlmOkV4aWZWZXJzaW9uPjAyMjA8L2V4aWY6RXhpZlZlcnNp'
    'b24+PC9yZGY6RGVzY3JpcHRpb24+PHJkZjpEZXNjcmlwdGlvbiB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUu'
    'Y29tL3RpZmYvMS4wLyI+PHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj48L3JkZjpEZXNjcmlw'
    'dGlvbj48L3JkZjpSREY+PC94OnhtcG1ldGE+DQo8P3hwYWNrZXQgZW5kPSd3Jz8+MAA8hgAAI+hJREFUeF7tnW2M'
    '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'
    'HDNmzC7n/wPMpc6GOqcVowAAAABJRU5ErkJggg=='
)

class GitDTLApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.app_dir = self.detect_app_dir()
        self.project_dir = self.detect_initial_project_dir()
        self.log_dir = self.project_dir / "logs"
        self.log_file = self.log_dir / "gitdtl.log"
        self.help_texts = self.load_help_texts()
        self.expert_rules = self.load_expert_rules()
        self.project_selected = True
        self.menu_buttons = {}
        self.highlighted_options = set()

        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry("920x760")
        self.root.state("zoomed")
        self.root.minsize(760, 620)
        self.root.configure(bg=COLOR_BG)

        self._configure_style()
        self._build_ui()
        self._ensure_log()
        self.log_info(f"Projet ouvert : {self.project_dir}")
        self.update_project_label()
        self.root.after(300, self.show_welcome_if_first_use)

    def detect_app_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parent

    def detect_initial_project_dir(self) -> Path:
        current_dir = Path.cwd().resolve()
        if current_dir.name.lower() == "dist" and self.looks_like_project_dir(current_dir.parent):
            return current_dir.parent
        if self.app_dir.name.lower() == "dist" and self.looks_like_project_dir(self.app_dir.parent):
            return self.app_dir.parent
        return current_dir

    def looks_like_project_dir(self, directory: Path) -> bool:
        return any(
            (directory / marker).exists()
            for marker in [".git", "GitDTL.py", "README.md", "aide.md"]
        )

    def welcome_cookie_path(self) -> Path:
        if self.app_dir.name.lower() == "dist":
            return self.app_dir.parent / WELCOME_COOKIE
        return self.app_dir / WELCOME_COOKIE

    def show_welcome_if_first_use(self) -> None:
        cookie_path = self.welcome_cookie_path()
        if cookie_path.exists():
            self.highlight_initial_status_option()
            return

        self.clear_current_project()
        welcome_window = self.show_markdown_window(
            "Bienvenue dans GitDTL",
            self.help_text("welcome"),
            body_color=COLOR_WELCOME_TEXT,
            show_title_label=False,
            top_image_path=self.find_app_file("Gitou_small.png"),
        )
        welcome_window.transient(self.root)
        self.center_window(welcome_window)
        welcome_window.grab_set()
        self.root.wait_window(welcome_window)
        try:
            cookie_path.write_text(
                f"{APP_NAME} {APP_VERSION}\n{_dt.datetime.now().isoformat(timespec='seconds')}\n",
                encoding="utf-8",
            )
        except OSError as exc:
            self.log_error(f"Impossible d'écrire le cookie de bienvenue : {exc}")
        self.prompt_project_to_manage()

    def highlight_initial_status_option(self) -> None:
        self.highlight_next_options(["1"])

    def load_help_texts(self) -> dict[str, str]:
        help_texts = DEFAULT_HELP_TEXTS.copy()
        help_path = self.app_dir / HELP_FILE
        if not help_path.exists() and self.app_dir.name.lower() == "dist":
            help_path = self.app_dir.parent / HELP_FILE
        if not help_path.exists():
            return help_texts

        try:
            content = help_path.read_text(encoding="utf-8")
        except OSError:
            return help_texts

        current_key = None
        sections: dict[str, list[str]] = {}
        for line in content.splitlines():
            if line.startswith("## "):
                key = line[3:].strip()
                current_key = key if key in help_texts else None
                if current_key is not None:
                    sections[current_key] = []
                continue
            if current_key is not None:
                sections[current_key].append(line)

        for key, lines in sections.items():
            text = "\n".join(lines).strip()
            if text:
                help_texts[key] = text
        return help_texts

    def find_app_file(self, filename: str) -> Path:
        path = self.app_dir / filename
        if not path.exists() and self.app_dir.name.lower() == "dist":
            path = self.app_dir.parent / filename
        return path

    def help_text(self, key: str) -> str:
        return self.help_texts.get(key, DEFAULT_HELP_TEXTS.get(key, "Aucune aide disponible."))

    def load_expert_rules(self) -> list[dict[str, object]]:
        expert_path = self.app_dir / EXPERT_FILE
        if not expert_path.exists() and self.app_dir.name.lower() == "dist":
            expert_path = self.app_dir.parent / EXPERT_FILE
        if not expert_path.exists():
            return DEFAULT_EXPERT_RULES

        try:
            content = expert_path.read_text(encoding="utf-8")
        except OSError:
            return DEFAULT_EXPERT_RULES

        rules = []
        current_rule = None
        current_field = None
        for raw_line in content.splitlines():
            line = raw_line.rstrip()
            stripped = line.strip()

            if stripped.startswith("## "):
                if current_rule is not None:
                    rules.append(current_rule)
                current_rule = {"name": stripped[3:].strip(), "patterns": [], "advice_lines": []}
                current_field = None
                continue

            if current_rule is None:
                continue

            if stripped.lower() == "patterns:":
                current_field = "patterns"
                continue
            if stripped.lower() == "advice:":
                current_field = "advice"
                continue

            if current_field == "patterns" and stripped.startswith("- "):
                current_rule["patterns"].append(stripped[2:].lower())
            elif current_field == "advice":
                current_rule["advice_lines"].append(line)

        if current_rule is not None:
            rules.append(current_rule)

        parsed_rules = []
        for rule in rules:
            patterns = [pattern for pattern in rule["patterns"] if pattern]
            advice = "\n".join(rule["advice_lines"]).strip()
            if patterns and advice:
                parsed_rules.append({"name": rule["name"], "patterns": patterns, "advice": advice})

        return parsed_rules or DEFAULT_EXPERT_RULES

    def expert_advice(self, output: str) -> str | None:
        normalized_output = output.lower()
        for rule in self.expert_rules:
            patterns = rule.get("patterns", [])
            if any(pattern in normalized_output for pattern in patterns):
                return f"{rule.get('name', 'Conseil GitDTL')}\n\n{rule.get('advice', '')}"
        return None

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "GitDTL.TButton",
            background=COLOR_TERMINAL,
            foreground=COLOR_TEXT,
            bordercolor=COLOR_BORDER_LIGHT,
            focusthickness=1,
            focuscolor=COLOR_BLUE,
            padding=(12, 10),
            font=FONT_MONO_SMALL,
        )
        style.map(
            "GitDTL.TButton",
            background=[("active", "#10171a"), ("pressed", "#182126")],
            foreground=[("disabled", COLOR_MUTED)],
        )

    def _build_ui(self) -> None:
        shell = tk.Frame(self.root, bg=COLOR_BG, padx=20, pady=26)
        shell.pack(fill="both", expand=True)

        header = tk.Frame(shell, bg=COLOR_BG)
        header.pack(fill="x")

        self.logo_image = tk.PhotoImage(data=NETDTL_LOGO_BASE64).subsample(2, 2)
        tk.Label(
            header,
            image=self.logo_image,
            bg=COLOR_BG,
            borderwidth=0,
        ).pack(side="right", anchor="ne", padx=(16, 0))

        title_block = tk.Frame(header, bg=COLOR_BG)
        title_block.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_block,
            text=f"{APP_NAME} {APP_VERSION}",
            bg=COLOR_BG,
            fg=COLOR_BLUE,
            font=FONT_TITLE,
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="Menu simplifié pour la\ngestion de projets avec Git",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            justify="left",
            font=FONT_MONO_SMALL,
        ).pack(anchor="w", pady=(10, 0))

        project_panel = tk.Frame(shell, bg=COLOR_PANEL, highlightthickness=1, highlightbackground=COLOR_BORDER)
        project_panel.pack(fill="x", pady=(18, 18))

        self.project_label = tk.Label(
            project_panel,
            text="",
            justify="left",
            anchor="w",
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            font=FONT_MONO,
            padx=8,
            pady=18,
        )
        self.project_label.pack(side="left", fill="x", expand=True)

        tk.Button(
            project_panel,
            text="Changer de projet",
            command=self.choose_project,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            activebackground=COLOR_TERMINAL,
            activeforeground=COLOR_TEXT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_LIGHT,
            highlightcolor=COLOR_BORDER_LIGHT,
            relief="solid",
            font=FONT_MONO_SMALL,
            padx=4,
            pady=8,
        ).pack(side="right", padx=14, pady=10)

        menu_panel = tk.Frame(shell, bg=COLOR_PANEL, padx=16, pady=16, highlightthickness=1, highlightbackground=COLOR_BORDER)
        menu_panel.pack(fill="both", expand=True)

        terminal = tk.Frame(menu_panel, bg=COLOR_TERMINAL)
        terminal.pack(fill="both", expand=True)

        menu_items = tk.Frame(terminal, bg=COLOR_TERMINAL)
        menu_items.place(relx=0.5, rely=0.08, anchor="n")
        menu_items.grid_columnconfigure(0, minsize=28)

        actions = [
            ("1", "État du projet : que faire maintenant ? (git status)", self.show_status, False),
            ("2", "Voir les modifications (git diff)", self.show_diff, True),
            ("3", "Ajouter un fichier au projet (git add)", self.add_file, True),
            ("4", "Enregistrer un fichier modifié dans le projet (git add)", self.update_file, True),
            ("5", "Supprimer un fichier ou un dossier (git rm)", self.remove_file, True),
            ("6", "Valider les changements (git commit)", self.commit_changes, True),
            ("7", "Publier le projet sur GitHub (git push)", self.push_to_github, True),
            ("8", "Créer une version (git tag)", self.create_release, True),
            ("9", "Historique des versions (git log)", self.show_history, True),
            ("10", "Synchroniser le projet depuis GitHub (git pull)", self.pull_from_github, True),
            ("11", "Diagnostic technique du dépôt (git status)", self.show_diagnostic, True),
            ("12", "Lire le journal (log)", self.show_log_window, True),
            ("13", "Voir le projet dans GitHub", self.open_project_on_github, True),
            ("14", "Documentation", self.show_documentation, False),
            ("15", "Commande magique : GitScan", self.show_git_scan, False),
            ("16", "Cloner un dépôt GitHub (git clone)", self.clone_repository, False),
            ("0", "Quitter le menu", self.root.destroy, False),
        ]

        for index, (number, label, command, needs_git) in enumerate(actions):
            if command is None:
                tk.Label(menu_items, text="", bg=COLOR_TERMINAL, font=FONT_MENU).grid(row=index, column=0, columnspan=2, sticky="w", pady=(6, 2))
                continue
            button_command = self.menu_command(number, command, needs_git)
            number_button = tk.Button(
                menu_items,
                text=number,
                command=button_command,
                anchor="e",
                bg=COLOR_TERMINAL,
                fg=COLOR_TEXT,
                activebackground=COLOR_TERMINAL,
                activeforeground=COLOR_BLUE,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                cursor="hand2",
                font=FONT_MENU,
                padx=0,
                pady=0,
                width=2,
            )
            number_button.grid(row=index, column=0, sticky="e", padx=(0, 8))
            label_button = tk.Button(
                menu_items,
                text=label,
                command=button_command,
                anchor="w",
                bg=COLOR_TERMINAL,
                fg=COLOR_TEXT,
                activebackground=COLOR_TERMINAL,
                activeforeground=COLOR_BLUE,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                cursor="hand2",
                font=FONT_MENU,
                padx=0,
                pady=0,
            )
            label_button.grid(row=index, column=1, sticky="w")
            self.menu_buttons[number] = (number_button, label_button)

        self.command_status_bar = tk.Frame(
            shell,
            bg=COLOR_PANEL,
            padx=12,
            pady=7,
        )

        tk.Label(
            self.command_status_bar,
            text="Commande envoyée : ",
            bg=COLOR_PANEL,
            fg=COLOR_MUTED,
            font=("Arial", 10),
        ).pack(side="left")

        self.command_status_label = tk.Label(
            self.command_status_bar,
            text="",
            anchor="w",
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            font=FONT_MONO_SMALL,
        )
        self.command_status_label.pack(side="left", fill="x", expand=True)

        self.footer = tk.Label(
            shell,
            text="In Memoriam Jean-Claude BELLAMY (1937-2015)",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=("Courier New", 10),
        )
        self.footer.pack(anchor="w", pady=(18, 0))

    def highlight_next_options(self, option_numbers: list[str]) -> None:
        self.highlighted_options = set(option_numbers)
        for number, buttons in self.menu_buttons.items():
            color = COLOR_WARNING if number in self.highlighted_options else COLOR_TEXT
            for button in buttons:
                button.configure(fg=color)

    def clear_highlighted_option(self, option_number: str) -> None:
        if option_number not in self.highlighted_options:
            return
        self.highlighted_options.discard(option_number)
        for button in self.menu_buttons.get(option_number, ()):
            button.configure(fg=COLOR_TEXT)

    def show_command_status(self, command_for_log: str) -> None:
        self.command_status_label.config(text=command_for_log)
        if not self.command_status_bar.winfo_ismapped():
            self.command_status_bar.pack(fill="x", pady=(12, 0), before=self.footer)

    def clear_command_status(self) -> None:
        self.command_status_label.config(text="")
        if self.command_status_bar.winfo_ismapped():
            self.command_status_bar.pack_forget()

    def menu_command(self, option_number: str, command, needs_git: bool):
        action = self.with_git_repository(command) if needs_git else command

        def wrapped_menu_command() -> None:
            self.clear_highlighted_option(option_number)
            self.clear_command_status()
            action()

        return wrapped_menu_command

    def with_git_repository(self, command):
        def wrapped_command() -> None:
            try:
                if not self.ensure_git_repository():
                    return
                command()
            except Exception as exc:
                self.show_error(exc)

        return wrapped_command

    def center_window(self, window: tk.Toplevel) -> None:
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_help(self, title: str, content: str) -> None:
        self.show_info(f"Aide - {title}", content)

    def message_color(self, kind: str) -> str:
        if kind == "warning":
            return COLOR_WARNING
        if kind == "error":
            return COLOR_ERROR
        return COLOR_DEC_BLUE

    def show_message(self, title: str, content: str, kind: str = "info") -> None:
        color = self.message_color(kind)

        window = tk.Toplevel(self.root)
        window.title(title)
        window.configure(bg=COLOR_BG)
        window.resizable(False, False)
        window.transient(self.root)

        tk.Label(
            window,
            text=title,
            bg=COLOR_BG,
            fg=color,
            font=FONT_MONO,
            padx=18,
            pady=12,
        ).pack(anchor="w")

        tk.Label(
            window,
            text=content,
            bg=COLOR_BG,
            fg=color,
            justify="left",
            wraplength=620,
            font=("Courier New", 10),
            padx=18,
            pady=8,
        ).pack(anchor="w")

        button_bar = tk.Frame(window, bg=COLOR_BG, padx=18)
        button_bar.pack(fill="x", pady=(8, 16))
        tk.Button(
            button_bar,
            text="OK",
            command=window.destroy,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            activebackground=COLOR_TERMINAL,
            activeforeground=COLOR_TEXT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_LIGHT,
            highlightcolor=COLOR_BORDER_LIGHT,
            relief="solid",
            font=FONT_MONO_SMALL,
            padx=18,
            pady=7,
        ).pack(side="right")

        window.protocol("WM_DELETE_WINDOW", window.destroy)
        self.center_window(window)
        window.grab_set()
        window.wait_window()

    def show_info(self, title: str, content: str) -> None:
        self.show_message(title, content, "info")

    def show_warning(self, title: str, content: str) -> None:
        self.show_message(title, content, "warning")

    def show_error_message(self, title: str, content: str) -> None:
        self.show_message(title, content, "error")

    def ask_text(self, title: str, prompt: str, help_text: str) -> str | None:
        answer = {"value": None}

        window = tk.Toplevel(self.root)
        window.title(title)
        window.configure(bg=COLOR_BG)
        window.resizable(False, False)
        window.transient(self.root)

        top_bar = tk.Frame(window, bg=COLOR_BG, padx=18)
        top_bar.pack(fill="x", pady=(12, 0))
        tk.Button(
            top_bar,
            text="? pour Aide",
            command=lambda: self.show_help(title, help_text),
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            activebackground=COLOR_BG,
            activeforeground=COLOR_TEXT,
            borderwidth=0,
            highlightthickness=0,
            font=FONT_MONO_SMALL,
            cursor="hand2",
        ).pack(side="right")

        tk.Label(
            window,
            text=prompt,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            justify="left",
            font=FONT_MONO,
            padx=18,
            pady=8,
        ).pack(anchor="w")

        entry = tk.Entry(
            window,
            bg=COLOR_INPUT_BG,
            fg=COLOR_INPUT_TEXT,
            insertbackground=COLOR_INPUT_TEXT,
            relief="flat",
            borderwidth=0,
            font=("Courier New", 10),
            width=56,
        )
        entry.pack(fill="x", padx=18, pady=(0, 12), ipady=7)

        button_bar = tk.Frame(window, bg=COLOR_BG, padx=18)
        button_bar.pack(fill="x", pady=(0, 16))

        def submit() -> None:
            value = entry.get().strip()
            answer["value"] = value or None
            window.destroy()

        def cancel() -> None:
            answer["value"] = None
            window.destroy()

        tk.Button(
            button_bar,
            text="Valider",
            command=submit,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            activebackground=COLOR_TERMINAL,
            activeforeground=COLOR_TEXT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_LIGHT,
            highlightcolor=COLOR_BORDER_LIGHT,
            relief="solid",
            font=FONT_MONO_SMALL,
            padx=12,
            pady=7,
        ).pack(side="right", padx=(8, 0))
        tk.Button(
            button_bar,
            text="Annuler",
            command=cancel,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            activebackground=COLOR_TERMINAL,
            activeforeground=COLOR_TEXT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER_LIGHT,
            highlightcolor=COLOR_BORDER_LIGHT,
            relief="solid",
            font=FONT_MONO_SMALL,
            padx=12,
            pady=7,
        ).pack(side="right")

        window.protocol("WM_DELETE_WINDOW", cancel)
        entry.bind("<Return>", lambda _event: submit())
        entry.focus_set()
        self.center_window(window)
        window.grab_set()
        window.wait_window()
        return answer["value"]

    def ask_choice(
        self,
        title: str,
        question: str,
        choices: list[tuple[str, object]],
        help_text: str,
        kind: str = "info",
    ) -> object:
        answer = {"value": None}
        message_color = self.message_color(kind)

        window = tk.Toplevel(self.root)
        window.title(title)
        window.configure(bg=COLOR_BG)
        window.resizable(False, False)
        window.transient(self.root)

        top_bar = tk.Frame(window, bg=COLOR_BG, padx=18)
        top_bar.pack(fill="x", pady=(12, 0))
        tk.Button(
            top_bar,
            text="? pour Aide",
            command=lambda: self.show_help(title, help_text),
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            activebackground=COLOR_BG,
            activeforeground=COLOR_TEXT,
            borderwidth=0,
            highlightthickness=0,
            font=FONT_MONO_SMALL,
            cursor="hand2",
        ).pack(side="right")

        tk.Label(
            window,
            text=question,
            bg=COLOR_BG,
            fg=message_color,
            justify="left",
            font=FONT_MONO,
            padx=18,
            pady=8,
        ).pack(anchor="w", pady=(0, 4))

        button_bar = tk.Frame(window, bg=COLOR_BG, padx=18)
        button_bar.pack(fill="x", pady=(0, 16))

        def select(value: object) -> None:
            answer["value"] = value
            window.destroy()

        for label, value in choices:
            tk.Button(
                button_bar,
                text=label,
                command=lambda selected=value: select(selected),
                bg=COLOR_PANEL,
                fg=COLOR_TEXT,
                activebackground=COLOR_TERMINAL,
                activeforeground=COLOR_TEXT,
                borderwidth=1,
                highlightthickness=1,
                highlightbackground=COLOR_BORDER_LIGHT,
                highlightcolor=COLOR_BORDER_LIGHT,
                relief="solid",
                font=FONT_MONO_SMALL,
                padx=10,
                pady=8,
            ).pack(fill="x", pady=4)

        window.protocol("WM_DELETE_WINDOW", lambda: select(None))
        self.center_window(window)
        window.grab_set()
        window.wait_window()
        return answer["value"]

    def update_project_label(self) -> None:
        if not self.project_selected:
            self.project_label.config(text="Projet courant :\nAucun projet sélectionné")
            return
        self.project_label.config(text=f"Projet courant :\n{self.project_dir}")

    def clear_current_project(self) -> None:
        self.project_selected = False
        self.update_project_label()

    def set_project_dir(self, selected: str | Path, write_log: bool = True) -> None:
        self.project_dir = Path(selected).resolve()
        self.log_dir = self.project_dir / "logs"
        self.log_file = self.log_dir / "gitdtl.log"
        self.project_selected = True
        self._ensure_log()
        if write_log:
            self.log_info(f"Projet ouvert : {self.project_dir}")
        self.update_project_label()

    def choose_project(self) -> None:
        selected = filedialog.askdirectory(title="Choisir le projet Git")
        if not selected:
            return
        self.set_project_dir(selected)

    def clone_repository(self) -> None:
        remote_url = self.ask_text(
            "Cloner un dépôt GitHub",
            "Adresse du dépôt GitHub à cloner :",
            self.help_text("clone_repository_url"),
        )
        if not remote_url:
            return

        parent_dir = filedialog.askdirectory(
            title="Choisir le dossier où créer la copie locale",
            initialdir=self.project_dir if self.project_selected else self.app_dir,
        )
        if not parent_dir:
            return

        parent_path = Path(parent_dir).resolve()
        before_dirs = self.git_directories_in(parent_path)
        result = self.run_git_in(parent_path, ["clone", remote_url])
        if result.returncode != 0:
            self.show_command_error(result)
            return

        cloned_path = self.detect_cloned_repository(parent_path, before_dirs, remote_url)
        if cloned_path is not None:
            self.set_project_dir(cloned_path)
            self.highlight_next_options(["1"])
            self.show_info(
                APP_NAME,
                "Dépôt cloné avec succès.\n\n"
                f"Projet courant :\n{self.project_dir}",
            )
            return

        self.show_info(
            APP_NAME,
            "Dépôt cloné avec succès.\n\n"
            "GitDTL n'a pas identifié automatiquement le dossier créé. "
            "Utilisez le bouton Changer de projet pour le sélectionner.",
        )

    def git_directories_in(self, parent_path: Path) -> set[Path]:
        if not parent_path.exists():
            return set()
        return {
            child.resolve()
            for child in parent_path.iterdir()
            if child.is_dir()
        }

    def detect_cloned_repository(self, parent_path: Path, before_dirs: set[Path], remote_url: str) -> Path | None:
        after_dirs = self.git_directories_in(parent_path)
        new_git_dirs = [
            directory
            for directory in after_dirs - before_dirs
            if (directory / ".git").exists()
        ]
        if len(new_git_dirs) == 1:
            return new_git_dirs[0]

        expected_name = self.repository_name_from_url(remote_url)
        if expected_name:
            expected_path = parent_path / expected_name
            if (expected_path / ".git").exists():
                return expected_path.resolve()
        return None

    def repository_name_from_url(self, remote_url: str) -> str | None:
        cleaned_url = remote_url.strip().rstrip("/")
        if not cleaned_url:
            return None
        if cleaned_url.endswith(".git"):
            cleaned_url = cleaned_url[:-4]
        if "://" not in cleaned_url and ":" in cleaned_url:
            path_part = cleaned_url.rsplit(":", 1)[1]
        else:
            path_part = cleaned_url
        name = path_part.rsplit("/", 1)[-1]
        name = name.strip()
        return name or None

    def prompt_project_to_manage(self) -> bool:
        choice = self.ask_choice(
            APP_NAME,
            "Quel projet voulez-vous gérer ?",
            [
                ("Créer un nouveau projet", "new"),
                ("Gérer un projet existant", "existing"),
                ("Annuler", None),
            ],
            self.help_text("first_project_choice"),
        )
        if choice is None:
            return False

        title = "Choisir ou créer le dossier du nouveau projet" if choice == "new" else "Choisir le projet existant"
        selected = filedialog.askdirectory(title=title, initialdir=self.app_dir.parent if self.app_dir.name.lower() == "dist" else self.app_dir)
        if not selected:
            return False

        self.set_project_dir(selected)
        if choice == "new":
            return self.ensure_git_repository(offer_project_choice=False)
        return True

    def _ensure_log(self) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.touch(exist_ok=True)

    def log_info(self, message: str) -> None:
        self._write_log("INFO", message)

    def log_error(self, message: str) -> None:
        self._write_log("ERREUR", message)

    def _write_log(self, level: str, message: str) -> None:
        self._ensure_log()
        stamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.log_file.open("a", encoding="utf-8") as handle:
            handle.write(f"{stamp} [{level}] {message}\n")

    def run_git(self, args: list[str], check_git: bool = True) -> subprocess.CompletedProcess[str]:
        if check_git and shutil.which("git") is None:
            raise RuntimeError("Git n'est pas installé ou n'est pas disponible dans le PATH Windows.")

        command_for_log = "git " + " ".join(self._quote_for_log(arg) for arg in args)
        self.show_command_status(command_for_log)
        self.log_info(command_for_log)
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        return subprocess.run(
            ["git", *args],
            cwd=self.project_dir,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            creationflags=creationflags,
        )

    def run_git_in(self, directory: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
        if shutil.which("git") is None:
            raise RuntimeError("Git n'est pas installé ou n'est pas disponible dans le PATH Windows.")

        command_for_log = "git " + " ".join(self._quote_for_log(arg) for arg in args)
        self.show_command_status(f"{command_for_log}   [{directory}]")
        self.log_info(f"{command_for_log} [{directory}]")
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        return subprocess.run(
            ["git", *args],
            cwd=directory,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            creationflags=creationflags,
        )

    def _quote_for_log(self, value: str) -> str:
        if any(char.isspace() for char in value):
            return f'"{value}"'
        return value

    def get_porcelain_status(self) -> list[str]:
        result = self.run_git(["status", "--porcelain"])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Impossible de lire l'état Git.")
        return [line for line in result.stdout.splitlines() if line.strip()]

    def is_git_repository(self) -> bool:
        result = self.run_git(["rev-parse", "--is-inside-work-tree"])
        return result.returncode == 0 and result.stdout.strip().lower() == "true"

    def ensure_git_repository(self, offer_project_choice: bool = True) -> bool:
        if not self.project_selected:
            if offer_project_choice and self.prompt_project_to_manage():
                return self.ensure_git_repository(offer_project_choice=False)
            return False

        if self.is_git_repository():
            return True

        confirmed = self.ask_choice(
            APP_NAME,
            "Aucun projet Git n'a été créé dans ce dossier.\n\n"
            f"{self.project_dir}\n\n"
            "Voulez-vous le créer maintenant ?",
            [("Créer le projet Git", True), ("Annuler", False)],
            self.help_text("create_git_repository"),
            kind="warning",
        )
        if not confirmed:
            return False

        result = self.run_git(["init"])
        if result.returncode != 0:
            self.show_command_error(result)
            return False

        self.log_info("Dépôt Git initialisé.")
        self.show_info(APP_NAME, "Projet Git créé avec succès.")
        return True

    def summarize_status(self) -> tuple[int, int, bool]:
        lines = self.get_porcelain_status()
        untracked = sum(1 for line in lines if line.startswith("??"))
        modified = len(lines) - untracked
        ready = len(lines) == 0
        return modified, untracked, ready

    def blocking_status_filenames(self) -> list[str]:
        return self.extract_status_filenames(self.get_porcelain_status())

    def next_status_option(self) -> str | None:
        lines = self.get_porcelain_status()
        if any(line.startswith("??") or (len(line) > 1 and line[1] != " ") for line in lines):
            return "4"
        if any(line and line[0] != " " for line in lines):
            return "6"
        return None

    def format_status_details(self) -> str:
        lines = self.get_porcelain_status()
        if not lines:
            return "Aucune modification détectée."

        categories = {
            "Fichiers ajoutés": [],
            "Fichiers modifiés": [],
            "Fichiers supprimés": [],
            "Fichiers renommés": [],
            "Fichiers copiés": [],
            "Fichiers non suivis": [],
            "Autres changements": [],
        }
        staged_labels = {
            "A": "Fichiers ajoutés",
            "M": "Fichiers modifiés",
            "D": "Fichiers supprimés",
            "R": "Fichiers renommés",
            "C": "Fichiers copiés",
        }
        unstaged_labels = {
            "A": "Fichiers ajoutés",
            "M": "Fichiers modifiés",
            "D": "Fichiers supprimés",
            "R": "Fichiers renommés",
            "C": "Fichiers copiés",
        }

        for line in lines:
            if line.startswith("??"):
                categories["Fichiers non suivis"].append(line[3:])
                continue

            staged = line[0]
            unstaged = line[1]
            filename = line[3:]
            added = False

            if staged in staged_labels:
                categories[staged_labels[staged]].append(filename)
                added = True
            if unstaged in unstaged_labels:
                categories[unstaged_labels[unstaged]].append(filename)
                added = True
            if not added:
                categories["Autres changements"].append(filename)

        sections = []
        for title, filenames in categories.items():
            if not filenames:
                continue
            sections.append(title + " :")
            sections.extend(f"- {filename}" for filename in filenames)
            sections.append("")

        return "\n".join(sections).strip()

    def show_status(self) -> None:
        try:
            if not self.ensure_git_repository():
                return
            modified, untracked, ready = self.summarize_status()
            blocking_files = self.blocking_status_filenames()
            content = (
                f"Fichiers modifiés : {modified}\n\n"
                f"Fichiers non suivis : {untracked}\n\n"
                f"Prêt à publier : {'Oui' if ready else 'Non'}"
            )
            if blocking_files:
                content += (
                    "\n\n"
                    "Pourquoi non ?\n\n"
                    "Ces éléments ne sont pas encore validés dans Git :\n\n"
                    + "\n".join(f"- {filename}" for filename in blocking_files)
                )
                next_option = self.next_status_option()
                if next_option:
                    self.highlight_next_options([next_option])
            self.show_text_window("État du projet", content)
            self.offer_common_python_ignores()
        except Exception as exc:
            self.show_error(exc)

    def offer_common_python_ignores(self) -> None:
        common_dirs = self.common_untracked_python_dirs()
        if not common_dirs:
            return

        dir_list = "\n".join(f"□ {dirname}" for dirname in common_dirs)
        selected = self.ask_choice(
            "Dossiers à ignorer",
            "Les dossiers suivants sont généralement\n"
            "ignorés dans les projets Python :\n\n"
            f"{dir_list}\n\n"
            "Les ajouter à .gitignore ?",
            [("Les ajouter à .gitignore", "add"), ("Annuler", None)],
            self.help_text("common_python_ignores"),
            kind="warning",
        )
        if selected != "add":
            return

        self.add_to_gitignore(common_dirs)
        self.highlight_next_options(["4"])
        self.show_info(APP_NAME, "Dossier(s) ajouté(s) à .gitignore.")

    def common_untracked_python_dirs(self) -> list[str]:
        common_dirs = ["__pycache__/", "logs/"]
        untracked = {
            line[3:]
            for line in self.get_porcelain_status()
            if line.startswith("??")
        }
        missing_patterns = set(self.missing_gitignore_patterns(common_dirs))
        return [
            dirname
            for dirname in common_dirs
            if dirname in untracked and f"/{dirname}" in missing_patterns
        ]

    def missing_gitignore_patterns(self, filenames: list[str]) -> list[str]:
        gitignore = self.project_dir / ".gitignore"
        if gitignore.exists():
            lines = gitignore.read_text(encoding="utf-8", errors="replace").splitlines()
        else:
            lines = []

        existing = set(lines)
        patterns = [f"/{filename}" for filename in filenames]
        return [pattern for pattern in patterns if pattern not in existing]

    def show_diff(self) -> None:
        try:
            status_content = self.format_status_details()
            unstaged_diff = self.run_git(["diff"])
            staged_diff = self.run_git(["diff", "--cached"])

            if unstaged_diff.returncode != 0:
                self.show_command_error(unstaged_diff)
                return
            if staged_diff.returncode != 0:
                self.show_command_error(staged_diff)
                return

            sections = ["Résumé :", status_content]
            if unstaged_diff.stdout.strip():
                sections.extend(["", "Détail des modifications non ajoutées :", unstaged_diff.stdout.strip()])
            if staged_diff.stdout.strip():
                sections.extend(["", "Détail des modifications ajoutées au prochain commit :", staged_diff.stdout.strip()])

            content = "\n".join(sections)
            self.show_text_window("Voir les modifications", content, scroll_to_end=True)
        except Exception as exc:
            self.show_error(exc)

    def add_file(self) -> None:
        filenames = self.ask_project_files("Choisir les fichiers à ajouter")
        if not filenames:
            return
        new_files, ignored_files = self.filter_new_files(filenames)
        if ignored_files:
            self.show_info(
                APP_NAME,
                "Ces fichiers sont déjà connus de Git ou déjà ajoutés :\n\n"
                + "\n".join(ignored_files),
            )
        if not new_files:
            return
        self.git_add_files(new_files, "Fichier(s) ajouté(s) avec succès.")

    def update_file(self) -> None:
        filenames = self.pending_files_for_add()
        if not filenames:
            self.show_info(APP_NAME, "Aucun fichier à enregistrer.")
            return
        confirmed = self.ask_choice(
            "Enregistrer les modifications",
            "GitDTL a détecté les fichiers suivants :\n\n"
            + "\n".join(f"- {filename}" for filename in filenames)
            + "\n\nLes enregistrer dans le projet ?",
            [("Enregistrer", True), ("Annuler", False)],
            self.help_text("stage_modified_files"),
        )
        if not confirmed:
            return
        self.git_add_files(filenames, "Modification(s) enregistrée(s).")

    def git_add_files(self, filenames: list[str], success_message: str) -> None:
        try:
            result = self.run_git(["add", "--", *filenames])
            if result.returncode == 0:
                self.highlight_next_options(["6"])
                self.show_info(APP_NAME, success_message)
            else:
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

    def filter_new_files(self, filenames: list[str]) -> tuple[list[str], list[str]]:
        status_by_file = self.get_status_by_file()
        new_files = []
        ignored_files = []

        for filename in filenames:
            if status_by_file.get(filename) == "??":
                new_files.append(filename)
            else:
                ignored_files.append(filename)

        return new_files, ignored_files

    def pending_files_for_add(self) -> list[str]:
        result = self.run_git(["status", "--porcelain"])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Impossible de lire l'état Git.")

        filenames = []
        seen = set()
        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            status = line[:2]
            if status == "??":
                filename = line[3:]
            elif status[1] != " ":
                filename = line[3:]
            else:
                continue

            if " -> " in filename:
                filename = filename.split(" -> ", 1)[1]
            if filename not in seen:
                filenames.append(filename)
                seen.add(filename)
        return filenames

    def get_status_by_file(self) -> dict[str, str]:
        result = self.run_git(["status", "--porcelain", "--untracked-files=all"])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Impossible de lire l'état Git.")

        statuses = {}
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            status = line[:2]
            filename = line[3:]
            statuses[filename] = status
        return statuses

    def remove_file(self) -> None:
        targets = self.ask_project_removal_targets()
        if not targets:
            return
        removal_action = self.ask_removal_action()
        if removal_action is None:
            return
        try:
            tracked_targets = [target for target in targets if self.has_tracked_content(target)]
            untracked_targets = [target for target in targets if target not in tracked_targets]

            if removal_action == "delete":
                if tracked_targets:
                    result = self.run_git(["rm", "-r", "-f", "--", *tracked_targets])
                    if result.returncode != 0:
                        self.show_command_error(result)
                        return
                self.delete_untracked_targets(untracked_targets)
                self.highlight_next_options(["6"])
                self.show_info(APP_NAME, "Élément(s) supprimé(s) du dépôt et du dossier.")
            else:
                if tracked_targets:
                    result = self.run_git(["rm", "-r", "-f", "--cached", "--", *tracked_targets])
                    if result.returncode != 0:
                        self.show_command_error(result)
                        return
                self.add_to_gitignore(targets)
                self.highlight_next_options(["4"])
                self.show_info(APP_NAME, "Élément(s) retiré(s) du dépôt et ajouté(s) dans .gitignore.")
        except Exception as exc:
            self.show_error(exc)

    def ask_project_removal_targets(self) -> list[str]:
        target_type = self.ask_choice(
            "Sélection",
            "Que voulez-vous sélectionner ?",
            [
                ("Un ou plusieurs fichiers", "files"),
                ("Un dossier entier", "folder"),
                ("Annuler", None),
            ],
            self.help_text("remove_file_action"),
        )
        if target_type == "files":
            return self.ask_project_files("Choisir les fichiers à supprimer du projet")
        if target_type == "folder":
            folder = filedialog.askdirectory(
                title="Choisir le dossier à supprimer du projet",
                initialdir=self.project_dir,
                mustexist=True,
            )
            if not folder:
                return []
            return self.project_relative_path(folder, require_inside=True, as_directory=True)
        return []

    def project_relative_path(self, selected: str, require_inside: bool = True, as_directory: bool = False) -> list[str]:
        project_dir = self.project_dir.resolve()
        selected_path = Path(selected).resolve()
        try:
            relative_path = selected_path.relative_to(project_dir)
        except ValueError:
            if require_inside:
                self.show_error_message(
                    APP_NAME,
                    "L'élément choisi doit se trouver dans le dossier du projet courant.",
                )
                return []
            raise

        if relative_path == Path("."):
            self.show_error_message(APP_NAME, "Le dossier du projet lui-même ne peut pas être sélectionné.")
            return []

        value = relative_path.as_posix()
        if as_directory and not value.endswith("/"):
            value += "/"
        return [value]

    def has_tracked_content(self, target: str) -> bool:
        result = self.run_git(["ls-files", "--", target])
        return result.returncode == 0 and bool(result.stdout.strip())

    def delete_untracked_targets(self, targets: list[str]) -> None:
        project_dir = self.project_dir.resolve()
        for target in targets:
            target_path = (project_dir / target.rstrip("/")).resolve()
            try:
                target_path.relative_to(project_dir)
            except ValueError:
                raise RuntimeError(f"Chemin hors projet refuse : {target}")

            if target_path.is_dir():
                shutil.rmtree(target_path)
            elif target_path.exists():
                target_path.unlink()

    def ask_removal_action(self) -> str | None:
        return self.ask_choice(
            "ATTENTION",
            "Que voulez-vous faire  ?",
            [
                ("Retirer l'élément du projet et le supprimer du dossier", "delete"),
                ("Retirer l'élément du projet mais le conserver dans le dossier", "keep"),
                ("Annuler", None),
            ],
            self.help_text("remove_file_action"),
            kind="warning",
        )

    def add_to_gitignore(self, filenames: list[str]) -> None:
        gitignore = self.project_dir / ".gitignore"

        if gitignore.exists():
            lines = gitignore.read_text(encoding="utf-8", errors="replace").splitlines()
        else:
            lines = []

        existing = set(lines)
        patterns = [f"/{filename}" for filename in filenames]
        missing_patterns = [pattern for pattern in patterns if pattern not in existing]
        if not missing_patterns:
            return

        with gitignore.open("a", encoding="utf-8") as handle:
            if lines:
                handle.write("\n")
            for pattern in missing_patterns:
                handle.write(f"{pattern}\n")
        self.log_info(f"Ajout dans .gitignore : {', '.join(missing_patterns)}")

    def commit_changes(self) -> None:
        message = self.ask_text(
            "Valider les changements",
            "Description du changement :",
            self.help_text("commit_message"),
        )
        if not message:
            return
        try:
            result = self.run_git(["commit", "-m", message])
            if result.returncode == 0:
                self.highlight_next_options(["7"])
                self.show_info(APP_NAME, "Changements validés avec succès.")
            elif self.is_nothing_to_commit(result):
                self.show_info(APP_NAME, "Aucun changement à valider.\n\nLe projet est déjà à jour.")
            else:
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

    def is_nothing_to_commit(self, result: subprocess.CompletedProcess[str]) -> bool:
        output = f"{result.stdout}\n{result.stderr}".lower()
        return "nothing to commit" in output and "working tree clean" in output

    def push_to_github(self) -> None:
        try:
            if not self.confirm_before_push():
                return
            if not self.ensure_remote_repository():
                return
            result = self.run_git(["push"])
            if result.returncode == 0:
                self.highlight_next_options(["13"])
                self.show_info(APP_NAME, "Publication réussie.")
            elif self.is_missing_upstream_error(result):
                branch = self.current_branch()
                if not branch:
                    self.show_command_error(result)
                    return
                upstream = self.run_git(["push", "--set-upstream", "origin", branch])
                if upstream.returncode == 0:
                    self.highlight_next_options(["13"])
                    self.show_info(APP_NAME, "Publication réussie.")
                else:
                    self.show_command_error(upstream)
            else:
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

    def is_missing_upstream_error(self, result: subprocess.CompletedProcess[str]) -> bool:
        output = f"{result.stdout}\n{result.stderr}".lower()
        return "has no upstream branch" in output or "--set-upstream" in output

    def current_branch(self) -> str | None:
        result = self.run_git(["branch", "--show-current"])
        if result.returncode != 0:
            return None
        branch = result.stdout.strip()
        return branch or None

    def ensure_remote_repository(self) -> bool:
        remote = self.run_git(["remote", "get-url", "origin"])
        if remote.returncode == 0 and remote.stdout.strip():
            return True

        remote_url = self.ask_text(
            "Configurer GitHub",
            "Aucun dépôt GitHub n'est configuré.\n\n"
            "Adresse du dépôt GitHub :",
            self.help_text("github_remote_url"),
        )
        if not remote_url:
            return False

        existing_remotes = self.run_git(["remote"])
        if existing_remotes.returncode != 0:
            self.show_command_error(existing_remotes)
            return False

        if "origin" in existing_remotes.stdout.split():
            result = self.run_git(["remote", "set-url", "origin", remote_url])
        else:
            result = self.run_git(["remote", "add", "origin", remote_url])

        if result.returncode != 0:
            self.show_command_error(result)
            return False

        self.show_info(APP_NAME, "Dépôt GitHub configuré.")
        return True

    def create_release(self) -> None:
        version = self.ask_text(
            "Créer une version",
            "Numéro de version :\n\nExemple : 1.0.0",
            self.help_text("release_version"),
        )
        if not version:
            return
        version = version.strip().lstrip("v")
        if not version:
            return

        tag = f"v{version}"
        message = f"Version {version}"
        confirmed = self.ask_choice(
            "Confirmation obligatoire",
            "GitDTL va créer une version.\n\n"
            f"Version : {version}\n\n"
            "Opérations prévues :\n"
            f"- git commit -m \"{message}\"\n"
            f"- git tag -a {tag} -m \"{message}\"\n"
            "- git push\n"
            f"- git push origin {tag}\n\n"
            "Continuer ?",
            [("Continuer", True), ("Annuler", False)],
            self.help_text("release_confirmation"),
            kind="warning",
        )
        if not confirmed:
            return

        try:
            self.log_info(f"Création release {tag}")
            commit = self.run_git(["commit", "-m", message])
            if commit.returncode != 0:
                self.show_command_error(commit)
                return
            tag_result = self.run_git(["tag", "-a", tag, "-m", message])
            if tag_result.returncode != 0:
                self.show_command_error(tag_result)
                return
            if not self.confirm_before_push():
                return
            push = self.run_git(["push"])
            if push.returncode != 0:
                self.show_command_error(push)
                return
            push_tag = self.run_git(["push", "origin", tag])
            if push_tag.returncode != 0:
                self.show_command_error(push_tag)
                return
            self.highlight_next_options(["13"])
            self.show_info(APP_NAME, f"Version {tag} créée et publiée.")
        except Exception as exc:
            self.show_error(exc)

    def show_history(self) -> None:
        try:
            result = self.run_git(["log", "--oneline", "-30"])
            content = result.stdout.strip() or "Aucun historique disponible."
            self.show_text_window("Historique", content)
        except Exception as exc:
            self.show_error(exc)

    def pull_from_github(self) -> None:
        try:
            result = self.run_git(["pull"])
            if result.returncode == 0:
                self.show_text_window("Synchroniser depuis GitHub", result.stdout.strip() or "Synchronisation terminée.")
            else:
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

    def open_project_on_github(self) -> None:
        try:
            result = self.run_git(["remote", "get-url", "origin"])
            if result.returncode != 0 or not result.stdout.strip():
                self.show_warning(APP_NAME, "Aucune adresse GitHub n'est configurée pour ce projet.")
                return

            github_url = self.github_web_url(result.stdout.strip())
            if github_url is None:
                self.show_warning(
                    APP_NAME,
                    "L'adresse configurée ne semble pas être une adresse GitHub valide :\n\n"
                    f"{result.stdout.strip()}",
                )
                return

            webbrowser.open(github_url)
        except Exception as exc:
            self.show_error(exc)

    def github_web_url(self, remote_url: str) -> str | None:
        remote_url = remote_url.strip()
        if remote_url.startswith("git@github.com:"):
            path = remote_url.removeprefix("git@github.com:")
            return "https://github.com/" + path.removesuffix(".git")
        if remote_url.startswith("ssh://git@github.com/"):
            path = remote_url.removeprefix("ssh://git@github.com/")
            return "https://github.com/" + path.removesuffix(".git")
        if remote_url.startswith("https://github.com/") or remote_url.startswith("http://github.com/"):
            return remote_url.removesuffix(".git")
        return None

    def show_documentation(self) -> None:
        readme_path = self.project_dir / "README.md"
        if not readme_path.exists():
            self.show_warning(APP_NAME, f"README.md introuvable dans :\n\n{self.project_dir}")
            return

        content = readme_path.read_text(encoding="utf-8", errors="replace")
        self.show_markdown_window(
            "Documentation - README.md",
            content or "README.md est vide.",
            body_color=COLOR_WELCOME_TEXT,
        )

    def show_markdown_window(
        self,
        title: str,
        content: str,
        body_color: str = COLOR_DEC_BLUE,
        show_title_label: bool = True,
        top_image_path: Path | None = None,
    ) -> tk.Toplevel:
        window = self.make_text_window(
            title,
            width=980,
            height=680,
            text_color=COLOR_DEC_BLUE,
            show_title_label=show_title_label,
        )
        text = window.text_widget
        text.configure(wrap="word")
        text.tag_configure("h1", foreground=COLOR_BLUE, font=("Courier New", 18, "bold"), spacing1=8, spacing3=10)
        text.tag_configure("h2", foreground=COLOR_TEXT, font=("Courier New", 14, "bold"), spacing1=8, spacing3=8)
        text.tag_configure("h3", foreground=COLOR_DEC_BLUE, font=("Courier New", 12, "bold"), spacing1=6, spacing3=6)
        text.tag_configure("paragraph", foreground=body_color, spacing3=5)
        text.tag_configure("strong", foreground=COLOR_TEXT, font=("Courier New", 10, "bold"), spacing3=5)
        text.tag_configure("list", foreground=body_color, lmargin1=28, lmargin2=44, spacing2=2)
        text.tag_configure("code", foreground=COLOR_WARNING, background=COLOR_PANEL, font=("Courier New", 10), lmargin1=18, lmargin2=18)
        text.tag_configure("table", foreground=COLOR_WARNING, font=("Courier New", 10), spacing2=1)
        text.tag_configure("rule", foreground=COLOR_BORDER_LIGHT, spacing1=4, spacing3=8)

        table_rows = []

        if top_image_path is not None and top_image_path.exists():
            try:
                image = tk.PhotoImage(file=str(top_image_path))
                window.markdown_images = getattr(window, "markdown_images", [])
                window.markdown_images.append(image)
                text.image_create(tk.END, image=image)
                text.insert(tk.END, "\n\n")
            except tk.TclError as exc:
                self.log_error(f"Impossible d'afficher l'image {top_image_path} : {exc}")

        def flush_table() -> None:
            if not table_rows:
                return

            widths = [
                max(len(row[index]) for row in table_rows)
                for index in range(max(len(row) for row in table_rows))
            ]
            for row_index, row in enumerate(table_rows):
                padded_cells = [
                    row[index].ljust(widths[index])
                    for index in range(len(row))
                ]
                text.insert(tk.END, "  ".join(padded_cells) + "\n", "table")
                if row_index == 0 and len(table_rows) > 1:
                    text.insert(tk.END, "  ".join("-" * width for width in widths) + "\n", "table")
            text.insert(tk.END, "\n")
            table_rows.clear()

        in_code = False
        for raw_line in content.splitlines():
            line = raw_line.rstrip()
            stripped = line.strip()

            if stripped.startswith("```"):
                flush_table()
                in_code = not in_code
                continue

            if in_code:
                text.insert(tk.END, line + "\n", "code")
                continue

            if not stripped:
                flush_table()
                text.insert(tk.END, "\n")
                continue

            if stripped in {"---", "***", "___"}:
                flush_table()
                text.insert(tk.END, "─" * 72 + "\n", "rule")
                continue

            if stripped.startswith("# "):
                flush_table()
                text.insert(tk.END, stripped[2:] + "\n", "h1")
                continue
            if stripped.startswith("## "):
                flush_table()
                text.insert(tk.END, stripped[3:] + "\n", "h2")
                continue
            if stripped.startswith("### "):
                flush_table()
                text.insert(tk.END, stripped[4:] + "\n", "h3")
                continue

            if stripped.startswith("- "):
                flush_table()
                text.insert(tk.END, "• " + self.clean_inline_markdown(stripped[2:]) + "\n", "list")
                continue

            if stripped.startswith("|"):
                if set(stripped.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
                    continue
                table_rows.append([
                    self.clean_inline_markdown(cell.strip())
                    for cell in stripped.strip("|").split("|")
                ])
                continue

            if stripped.startswith("**") and stripped.endswith("**") and len(stripped) > 4:
                flush_table()
                text.insert(tk.END, self.clean_inline_markdown(stripped) + "\n", "strong")
                continue

            flush_table()
            text.insert(tk.END, self.clean_inline_markdown(stripped) + "\n", "paragraph")

        flush_table()
        text.config(state="disabled")
        return window

    def clean_inline_markdown(self, value: str) -> str:
        return value.replace("**", "").replace("`", "")

    def show_diagnostic(self) -> None:
        try:
            status = self.run_git(["status", "--porcelain"])
            branch = self.run_git(["branch", "--show-current"])
            remotes = self.run_git(["remote", "-v"])
            log = self.run_git(["log", "--oneline", "-5"])

            lines = [line for line in status.stdout.splitlines() if line.strip()]
            untracked = sum(1 for line in lines if line.startswith("??"))
            modified = len(lines) - untracked
            current_branch = branch.stdout.strip() or "inconnue"
            remote_ok = "configuré" if remotes.stdout.strip() else "non configuré"
            last_commit = log.stdout.splitlines()[0] if log.stdout.splitlines() else "Aucun commit"

            report = (
                f"État du dépôt : {'OK' if status.returncode == 0 else 'Erreur'}\n\n"
                f"Branche : {current_branch}\n\n"
                f"Remote GitHub : {remote_ok}\n\n"
                f"Fichiers modifiés : {modified}\n\n"
                f"Fichiers non suivis : {untracked}\n\n"
                "Dernier commit :\n\n"
                f"{last_commit}\n\n"
                "Commandes de diagnostic :\n\n"
                "git status\n"
                "git branch\n"
                "git remote -v\n"
                "git log --oneline -5"
            )
            self.show_text_window("Diagnostic GitDTL", report)
        except Exception as exc:
            self.show_error(exc)

    def show_git_scan(self) -> None:
        try:
            selected_root = filedialog.askdirectory(
                title="Choisir le dossier racine à scanner avec GitScan",
                initialdir=self.project_dir if self.project_selected else self.app_dir,
            )
            if not selected_root:
                return

            root_dir = Path(selected_root).resolve()
            repositories = self.discover_git_repositories(root_dir)
            if not repositories:
                self.show_text_window(
                    "Commande magique : GitScan",
                    f"Aucun dépôt Git détecté dans :\n\n{root_dir}",
                )
                return

            scan_results = []
            action_sections = []

            for repository in repositories:
                summary, actions, diagnostics, metrics = self.git_scan_repository_summary(repository, root_dir)
                scan_results.append((repository.name, summary, actions, diagnostics, metrics))
                if actions:
                    action_sections.append((repository.name, actions))

            self.show_git_scan_report(root_dir, scan_results, action_sections)
        except Exception as exc:
            self.show_error(exc)

    def show_git_scan_report(
        self,
        root_dir: Path,
        scan_results: list[tuple[str, str, list[str], list[str], dict[str, int]]],
        action_sections: list[tuple[str, list[str]]],
    ) -> None:
        window = self.make_text_window("Commande magique : GitScan", width=980, height=680)
        text = window.text_widget
        text.tag_configure("header", foreground=COLOR_BLUE, font=("Courier New", 13, "bold"), spacing3=8)
        text.tag_configure("global_ok", foreground=COLOR_TEXT, font=("Courier New", 12, "bold"), spacing3=5)
        text.tag_configure("global_warn", foreground=COLOR_WARNING, font=("Courier New", 12, "bold"), spacing3=5)
        text.tag_configure("repo_title", foreground=COLOR_WARNING, font=("Courier New", 12, "bold"), spacing1=8, spacing3=4)
        text.tag_configure("body", foreground=COLOR_TEXT, spacing2=1)
        text.tag_configure("action_required", foreground="#ff0000", font=("Courier New", 10, "bold"), spacing2=1)
        text.tag_configure("action_required_title", foreground="#ff0000", font=("Courier New", 12, "bold"), spacing1=8, spacing3=4)
        text.tag_configure("rule", foreground=COLOR_BORDER_LIGHT, spacing1=4, spacing3=6)

        repositories_count = len(scan_results)
        intervention_count = len(action_sections)
        commits_to_publish = sum(metrics.get("ahead", 0) for *_rest, metrics in scan_results)
        global_ok = intervention_count == 0

        text.insert(tk.END, "GitScan - bilan des projets Git\n", "header")
        text.insert(tk.END, f"\nDossier analysé : {root_dir}\n", "body")
        if global_ok:
            text.insert(tk.END, "\nÉtat général : OK\n", "global_ok")
            text.insert(tk.END, f"{repositories_count} dépôts analysés\n", "body")
            text.insert(tk.END, "Aucune action requise\n\n", "body")
        else:
            text.insert(tk.END, "\nÉtat général : ATTENTION\n", "global_warn")
            text.insert(tk.END, f"{repositories_count} dépôts analysés\n", "body")
            intervention_text = "nécessite une intervention" if intervention_count == 1 else "nécessitent une intervention"
            commit_text = "commit en attente de publication" if commits_to_publish == 1 else "commits en attente de publication"
            text.insert(tk.END, f"{intervention_count} {intervention_text}\n", "body")
            text.insert(tk.END, f"{commits_to_publish} {commit_text}\n\n", "body")
        text.insert(tk.END, "=" * 72 + "\n", "rule")

        for _name, summary, actions, _diagnostics, _metrics in scan_results:
            lines = summary.splitlines()
            if lines:
                text.insert(tk.END, "\n" + lines[0] + "\n", "repo_title")
                remaining = "\n".join(lines[1:])
                if remaining:
                    text.insert(tk.END, remaining + "\n", "body")
                if actions:
                    text.insert(tk.END, "\nActions à réaliser :\n", "action_required_title")
                    for index, action in enumerate(actions, start=1):
                        text.insert(tk.END, f"{index}. {action}\n", "action_required")
            text.insert(tk.END, "-" * 72 + "\n", "rule")

        text.insert(tk.END, "\nACTIONS À RÉALISER\n\n", "header")
        if not action_sections:
            text.insert(tk.END, "Aucune action urgente détectée.\n", "body")
        else:
            for name, actions in action_sections:
                text.insert(tk.END, name + " :\n", "action_required_title")
                for index, action in enumerate(actions, start=1):
                    text.insert(tk.END, f"{index}. {action}\n", "action_required")
                text.insert(tk.END, "\n", "body")

        text.config(state="disabled")

    def discover_git_repositories(self, root_dir: Path) -> list[Path]:
        repositories = []
        ignored_dirs = {".git", "build", "dist", "__pycache__", "logs", "node_modules"}
        try:
            entries = sorted(root_dir.iterdir(), key=lambda path: path.name.lower())
        except OSError as exc:
            raise RuntimeError(f"Impossible de lire le dossier racine choisi : {exc}") from exc

        for entry in entries:
            if entry.name.startswith("."):
                continue
            if not entry.is_dir() or entry.name in ignored_dirs:
                continue
            if (entry / ".git").exists():
                repositories.append(entry)
                continue
            repositories.extend(self.discover_nested_git_repositories(entry, ignored_dirs))
        return repositories

    def discover_nested_git_repositories(self, directory: Path, ignored_dirs: set[str]) -> list[Path]:
        repositories = []
        try:
            for current, dirs, _files in os.walk(directory):
                dirs[:] = [
                    dirname
                    for dirname in dirs
                    if dirname not in ignored_dirs and not dirname.startswith(".")
                ]
                current_path = Path(current)
                if (current_path / ".git").exists():
                    repositories.append(current_path)
                    dirs[:] = []
        except OSError:
            return repositories
        return repositories

    def git_scan_repository_summary(self, repository: Path, tools_dir: Path) -> tuple[str, list[str], list[str], dict[str, int]]:
        status = self.run_git_in(repository, ["status", "--porcelain", "--branch"])
        branch = self.run_git_in(repository, ["branch", "--show-current"])
        remotes = self.run_git_in(repository, ["remote", "-v"])
        log = self.run_git_in(repository, ["log", "--oneline", "-1"])

        relative_name = repository.relative_to(tools_dir).as_posix()
        if status.returncode != 0:
            output = (status.stderr or status.stdout or "Erreur Git inconnue.").strip()
            return (
                f"{relative_name}\nÉtat : ERREUR\n{output}",
                ["Ouvrir le diagnostic du dépôt ou vérifier manuellement Git."],
                ["Erreur Git pendant l'analyse."],
                {"ahead": 0},
            )

        lines = [line for line in status.stdout.splitlines() if line.strip()]
        branch_line = next((line for line in lines if line.startswith("## ")), "## branche inconnue")
        change_lines = [line for line in lines if not line.startswith("## ")]
        untracked = sum(1 for line in change_lines if line.startswith("??"))
        staged = sum(1 for line in change_lines if not line.startswith("??") and line[0] != " ")
        unstaged = sum(1 for line in change_lines if not line.startswith("??") and len(line) > 1 and line[1] != " ")
        remote_ok = "oui" if remotes.stdout.strip() else "non"
        current_branch = branch.stdout.strip() or "inconnue"
        last_commit = log.stdout.strip() or "Aucun commit"
        ahead, behind = self.parse_branch_ahead_behind(branch_line)

        diagnostics = []
        actions = []
        if untracked or unstaged:
            diagnostics.append("Modifications locales non enregistrées.")
            actions.append("Option 4 : enregistrer les modifications.")
        if staged:
            diagnostics.append("Changements prêts à être validés.")
            actions.append("Option 6 : valider les changements déjà enregistrés.")
        if behind:
            diagnostics.append("Des commits distants sont absents du dossier local.")
            actions.append("Option 10 : synchroniser depuis GitHub avant de publier.")
        if ahead:
            diagnostics.append("Un commit est en attente de publication." if ahead == 1 else f"{ahead} commits sont en attente de publication.")
            actions.append("Option 7 : publier le commit sur GitHub." if ahead == 1 else "Option 7 : publier les commits sur GitHub.")
        if remote_ok == "non":
            diagnostics.append("Aucun dépôt GitHub distant n'est configuré.")
            actions.append("Configurer le dépôt GitHub distant avant publication.")
        if not change_lines and not ahead and not behind:
            diagnostics.append("Aucune anomalie détectée.")

        remote_symbol = "✓" if remote_ok == "oui" else "⚠"
        untracked_symbol = "✓" if untracked == 0 else "⚠"
        staged_symbol = "✓" if staged == 0 else "⚠"
        unstaged_symbol = "✓" if unstaged == 0 else "⚠"
        ahead_symbol = "✓" if ahead == 0 else "⚠"
        behind_symbol = "✓" if behind == 0 else "⚠"

        summary = (
            f"{relative_name}\n"
            f"Branche : {current_branch}\n"
            f"{remote_symbol} Remote GitHub : {remote_ok}\n"
            f"Dernier commit : {last_commit}\n"
            f"{untracked_symbol} Fichiers non suivis : {untracked}\n"
            f"{staged_symbol} Changements enregistrés pour commit : {staged}\n"
            f"{unstaged_symbol} Changements non enregistrés : {unstaged}\n"
            f"{ahead_symbol} Commits locaux à publier : {ahead}\n"
            f"{behind_symbol} Commits distants à récupérer : {behind}\n"
            "\n"
            "Diagnostic :\n"
            + "\n".join(f"- {diagnostic}" for diagnostic in diagnostics)
        )
        metrics = {
            "ahead": ahead,
            "behind": behind,
            "untracked": untracked,
            "staged": staged,
            "unstaged": unstaged,
            "has_changes": 1 if change_lines else 0,
        }
        return summary, actions, diagnostics, metrics

    def parse_branch_ahead_behind(self, branch_line: str) -> tuple[int, int]:
        ahead = 0
        behind = 0
        if "ahead " in branch_line:
            try:
                ahead_part = branch_line.split("ahead ", 1)[1].split(",", 1)[0].split("]", 1)[0]
                ahead = int(ahead_part.strip())
            except (ValueError, IndexError):
                ahead = 0
        if "behind " in branch_line:
            try:
                behind_part = branch_line.split("behind ", 1)[1].split(",", 1)[0].split("]", 1)[0]
                behind = int(behind_part.strip())
            except (ValueError, IndexError):
                behind = 0
        return ahead, behind

    def show_log_window(self) -> None:
        self._ensure_log()
        window = self.make_text_window("Lire le journal", width=980, height=680)
        text = window.text_widget

        button_bar = tk.Frame(window, bg=COLOR_PANEL)
        button_bar.pack(fill="x", padx=16, pady=(0, 16))

        def load_log() -> None:
            lines = self.log_file.read_text(encoding="utf-8", errors="replace").splitlines()
            content = "\n".join(lines[-1000:]) or "Le journal GitDTL est vide."
            text.config(state="normal")
            text.delete("1.0", tk.END)
            text.insert("1.0", content)
            text.see("end")
            text.config(state="disabled")

        def clear_log() -> None:
            confirmed = self.ask_choice(
                "ATTENTION",
                "ATTENTION\n\nLe journal GitDTL sera définitivement supprimé.\n\nContinuer ?",
                [("Effacer le journal", True), ("Annuler", False)],
                self.help_text("clear_log"),
                kind="warning",
            )
            if not confirmed:
                return
            self.log_file.write_text("", encoding="utf-8")
            self.log_info("Journal effacé")
            load_log()

        def export_log() -> None:
            stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = self.log_dir / f"gitdtl_{stamp}.txt"
            export_path.write_text(self.log_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            self.log_info(f"Journal exporté : {export_path}")
            self.show_info(APP_NAME, f"Journal exporté :\n{export_path}")
            load_log()

        ttk.Button(button_bar, text="Actualiser", style="GitDTL.TButton", command=load_log).pack(side="left", padx=(0, 8))
        ttk.Button(button_bar, text="Effacer le journal", style="GitDTL.TButton", command=clear_log).pack(side="left", padx=8)
        ttk.Button(button_bar, text="Exporter", style="GitDTL.TButton", command=export_log).pack(side="left", padx=8)

        load_log()

    def confirm_before_push(self) -> bool:
        result = self.run_git(["status", "--porcelain"])
        if result.returncode != 0:
            self.show_command_error(result)
            return False

        lines = [line for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            return True

        unpublished_files = self.extract_status_filenames(lines)
        file_list = "\n".join(f"- {filename}" for filename in unpublished_files)
        return self.ask_choice(
            "Vérification avant publication",
            "Les fichiers suivants existent dans le dossier\n"
            "mais ne feront pas partie de la publication :\n\n"
            f"{file_list}\n\n"
            "Si vous publiez maintenant :\n\n"
            "✓ les changements validés seront publiés\n\n"
            "✗ ces fichiers ne seront pas envoyés sur GitHub\n\n"
            "Voulez-vous continuer ?",
            [("Publier quand même", True), ("Annuler", False)],
            self.help_text("publish_with_uncommitted_changes"),
            kind="warning",
        )

    def extract_status_filenames(self, status_lines: list[str]) -> list[str]:
        filenames = []
        seen = set()

        for line in status_lines:
            filename = line[3:]
            if " -> " in filename:
                filename = filename.split(" -> ", 1)[1]
            if filename not in seen:
                filenames.append(filename)
                seen.add(filename)

        return filenames

    def ask_project_files(self, title: str) -> list[str]:
        selected_files = filedialog.askopenfilenames(
            title=title,
            initialdir=self.project_dir,
        )
        if not selected_files:
            return []

        project_dir = self.project_dir.resolve()
        filenames = []
        try:
            for selected in selected_files:
                filenames.append(Path(selected).resolve().relative_to(project_dir).as_posix())
        except ValueError:
            self.show_error_message(
                APP_NAME,
                "Tous les fichiers choisis doivent se trouver dans le dossier du projet courant.",
            )
            return []
        return filenames

    def make_text_window(
        self,
        title: str,
        width: int = 860,
        height: int = 560,
        text_color: str = COLOR_TEXT,
        show_title_label: bool = True,
    ):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(f"{width}x{height}")
        window.configure(bg=COLOR_BG)

        if show_title_label:
            title_label = tk.Label(
                window,
                text=title,
                bg=COLOR_BG,
                fg=text_color,
                font=FONT_MONO,
                padx=16,
                pady=14,
            )
            title_label.pack(anchor="w")
            frame_pady = (0, 16)
        else:
            frame_pady = (16, 16)

        frame = tk.Frame(window, bg=COLOR_PANEL, padx=16, pady=16, highlightthickness=1, highlightbackground=COLOR_BORDER)
        frame.pack(fill="both", expand=True, padx=16, pady=frame_pady)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(
            frame,
            bg=COLOR_TERMINAL,
            fg=text_color,
            insertbackground=COLOR_TEXT,
            selectbackground=COLOR_BLUE,
            wrap="word",
            font=("Courier New", 10),
            borderwidth=0,
            padx=12,
            pady=12,
            yscrollcommand=scrollbar.set,
        )
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)
        window.text_widget = text
        return window

    def show_text_window(
        self,
        title: str,
        content: str,
        scroll_to_end: bool = False,
        text_color: str = COLOR_TEXT,
        selectable: bool = False,
    ) -> None:
        window = self.make_text_window(title, text_color=text_color)
        text = window.text_widget
        text.insert("1.0", content)
        if scroll_to_end:
            text.see("end")
        if selectable:
            self.make_text_selectable_readonly(text)
        else:
            text.config(state="disabled")

    def make_text_selectable_readonly(self, text: tk.Text) -> None:
        def block_edit(event) -> str | None:
            is_control = bool(event.state & 0x4)
            key = event.keysym.lower()
            if is_control and key == "c":
                return None
            if is_control and key == "a":
                text.tag_add("sel", "1.0", "end-1c")
                return "break"
            return "break"

        text.bind("<Key>", block_edit)
        text.bind("<<Cut>>", lambda _event: "break")
        text.bind("<<Paste>>", lambda _event: "break")
        text.focus_set()

    def show_command_error(self, result: subprocess.CompletedProcess[str]) -> None:
        output = "\n".join(part.strip() for part in [result.stdout, result.stderr] if part.strip())
        self.log_error(output or f"Commande terminée avec le code {result.returncode}")
        content = output or "Erreur détectée."
        advice = self.expert_advice(content)
        if advice:
            content += "\n\n" + "=" * 72 + "\n\nConseil du système expert :\n\n" + advice
        self.show_text_window("Erreur détectée", content, text_color=COLOR_ERROR, selectable=True)

    def show_error(self, exc: Exception) -> None:
        self.log_error(str(exc))
        self.show_error_message(APP_NAME, str(exc))


def main() -> None:
    root = tk.Tk()
    GitDTLApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


