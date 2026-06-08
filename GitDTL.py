from __future__ import annotations

import datetime as _dt
import os
import shutil
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk


APP_NAME = "GitDTL"
APP_VERSION = "v1.0.0"
APP_SUBTITLE = "Git simplifié pour les projets DTL"
HELP_FILE = "aide.md"
DEFAULT_HELP_TEXTS = {
    "create_git_repository": (
        "Un projet Git permet de suivre l'historique des fichiers.\n\n"
        "Choisissez 'Créer le projet Git' pour lancer git init dans le dossier courant.\n"
        "Choisissez 'Annuler' pour revenir au menu sans créer de dépôt."
    ),
    "remove_file_action": (
        "Le premier choix supprime le fichier du disque et de Git.\n\n"
        "Le deuxième choix conserve le fichier dans le dossier, le retire seulement du suivi Git "
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
}

COLOR_BG = "#090d0f"
COLOR_PANEL = "#12171b"
COLOR_TERMINAL = "#070b0d"
COLOR_TEXT = "#00ff2f"
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
        self.project_dir = Path.cwd()
        self.log_dir = self.project_dir / "logs"
        self.log_file = self.log_dir / "gitdtl.log"
        self.help_texts = self.load_help_texts()

        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry("920x760")
        self.root.minsize(760, 620)
        self.root.configure(bg=COLOR_BG)

        self._configure_style()
        self._build_ui()
        self._ensure_log()
        self.log_info(f"Projet ouvert : {self.project_dir}")
        self.update_project_label()

    def load_help_texts(self) -> dict[str, str]:
        help_texts = DEFAULT_HELP_TEXTS.copy()
        help_path = Path(__file__).resolve().parent / HELP_FILE
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

    def help_text(self, key: str) -> str:
        return self.help_texts.get(key, DEFAULT_HELP_TEXTS.get(key, "Aucune aide disponible."))

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
            text=f"{APP_NAME} v1.0.0",
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

        actions = [
            ("1  État du projet (git status)", self.show_status, False),
            ("2  Voir les modifications (git diff)", self.show_diff, True),
            ("3  Ajouter un fichier au projet (git add)", self.add_file, True),
            ("4  Enregistrer un fichier modifié dans le projet (git add)", self.update_file, True),
            ("5  Supprimer un fichier du projet (git rm)", self.remove_file, True),
            ("6  Valider les changements (git commit)", self.commit_changes, True),
            ("7  Publier le projet sur GitHub (git push)", self.push_to_github, True),
            ("8  Créer une version (git tag)", self.create_release, True),
            ("9  Historique des versions (git log)", self.show_history, True),
            ("10 Synchroniser le projet depuis GitHub (git pull)", self.pull_from_github, True),
            ("11 Diagnostic GitDTL (git status)", self.show_diagnostic, True),
            ("12 Lire le journal (log)", self.show_log_window, True),
            ("", None, False),
            ("0  Quitter le menu", self.root.destroy, False),
        ]

        for index, (label, command, needs_git) in enumerate(actions):
            if command is None:
                tk.Label(menu_items, text="", bg=COLOR_TERMINAL, font=FONT_MENU).grid(row=index, column=0, sticky="w", pady=(6, 2))
                continue
            button_command = self.with_git_repository(command) if needs_git else command
            button = tk.Button(
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
            button.grid(row=index, column=0, sticky="w")

        footer = tk.Label(
            shell,
            text="In Memoriam Jean-Claude BELLAMY (1937-2015)",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=("Courier New", 10),
        )
        footer.pack(anchor="w", pady=(18, 0))

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
        self.project_label.config(text=f"Projet courant :\n{self.project_dir}")

    def choose_project(self) -> None:
        selected = filedialog.askdirectory(title="Choisir le projet Git")
        if not selected:
            return
        self.project_dir = Path(selected)
        self.log_dir = self.project_dir / "logs"
        self.log_file = self.log_dir / "gitdtl.log"
        self._ensure_log()
        self.log_info(f"Projet ouvert : {self.project_dir}")
        self.update_project_label()

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
        self.log_info(command_for_log)
        return subprocess.run(
            ["git", *args],
            cwd=self.project_dir,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
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

    def ensure_git_repository(self) -> bool:
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
            content = (
                f"Fichiers modifiés : {modified}\n\n"
                f"Fichiers non suivis : {untracked}\n\n"
                f"Prêt à publier : {'Oui' if ready else 'Non'}"
            )
            self.show_text_window("État du projet", content)
        except Exception as exc:
            self.show_error(exc)

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
        filenames = self.ask_project_files("Choisir les fichiers à mettre à jour")
        if not filenames:
            return
        self.git_add_files(filenames, "Modification(s) enregistrée(s).")

    def git_add_files(self, filenames: list[str], success_message: str) -> None:
        try:
            result = self.run_git(["add", "--", *filenames])
            if result.returncode == 0:
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
        filenames = self.ask_project_files("Choisir les fichiers à supprimer du projet")
        if not filenames:
            return
        removal_action = self.ask_removal_action()
        if removal_action is None:
            return
        try:
            if removal_action == "delete":
                result = self.run_git(["rm", "-f", "--", *filenames])
            else:
                result = self.run_git(["rm", "-f", "--cached", "--", *filenames])
            if result.returncode == 0:
                if removal_action == "delete":
                    self.show_info(APP_NAME, "Fichier(s) supprimé(s) du dépôt et du dossier.")
                else:
                    self.add_to_gitignore(filenames)
                    self.show_info(APP_NAME, "Fichier(s) retiré(s) du dépôt et ajouté(s) dans .gitignore.")
            else:
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

    def ask_removal_action(self) -> str | None:
        return self.ask_choice(
            "ATTENTION",
            "Que voulez-vous faire  ?",
            [
                ("Retirer le fichier du projet et le supprimer du dossier", "delete"),
                ("Retirer le fichier du projet mais le conserver dans le dossier", "keep"),
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
                self.show_info(APP_NAME, "Changements validés avec succès.")
            else:
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

    def push_to_github(self) -> None:
        try:
            if not self.confirm_before_push():
                return
            if not self.ensure_remote_repository():
                return
            result = self.run_git(["push"])
            if result.returncode == 0:
                self.show_info(APP_NAME, "Publication réussie.")
            else:
                self.show_error_message(APP_NAME, "Erreur détectée.")
                self.show_command_error(result)
        except Exception as exc:
            self.show_error(exc)

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

    def make_text_window(self, title: str, width: int = 860, height: int = 560, text_color: str = COLOR_TEXT):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(f"{width}x{height}")
        window.configure(bg=COLOR_BG)

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

        frame = tk.Frame(window, bg=COLOR_PANEL, padx=16, pady=16, highlightthickness=1, highlightbackground=COLOR_BORDER)
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

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
    ) -> None:
        window = self.make_text_window(title, text_color=text_color)
        window.text_widget.insert("1.0", content)
        if scroll_to_end:
            window.text_widget.see("end")
        window.text_widget.config(state="disabled")

    def show_command_error(self, result: subprocess.CompletedProcess[str]) -> None:
        output = "\n".join(part.strip() for part in [result.stdout, result.stderr] if part.strip())
        self.log_error(output or f"Commande terminée avec le code {result.returncode}")
        self.show_text_window("Erreur détectée", output or "Erreur détectée.", text_color=COLOR_ERROR)

    def show_error(self, exc: Exception) -> None:
        self.log_error(str(exc))
        self.show_error_message(APP_NAME, str(exc))


def main() -> None:
    root = tk.Tk()
    GitDTLApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


