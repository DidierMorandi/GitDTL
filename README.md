# GitDTL v1.0-7

June 2026 - Didier DTL Morandi - https://netdtl.com/

**A simplified Windows menu for managing Git projects**

GitDTL is a Python/Tkinter desktop application for everyday Git work. It is designed for users who want to use Git without typing command-line instructions.

The interface follows the NetDTL "DEC VT100 terminal" style: black background, phosphor-green text, and the Courier New monospace font.

---

## Overview

GitDTL exposes common Git operations through a numbered graphical menu. It can manage an existing local repository or help initialize a new one when the selected folder is not yet a Git repository.

The application focuses on clear, guided actions: checking project status, adding files, committing changes, publishing to GitHub, creating tags, cloning repositories, reading logs, and scanning folders for Git projects.

---

## Requirements

- Windows 10 or later
- Python 3.10 or later
- Git installed and available in the Windows `PATH`

GitDTL uses only Python standard-library modules, including `tkinter`, `subprocess`, `pathlib`, and `shutil`.

---

## Installation

```powershell
git clone https://github.com/DidierMorandi/gitdtl.git
cd gitdtl
python GitDTL.py
```

No external Python dependency is required.

---

## Launch

```powershell
python GitDTL.py
```

GitDTL starts from the current folder. The managed project folder can be changed at any time with the **Change project** button in the application.

---

## Main Menu

| No. | Action | Git equivalent |
|-----|--------|----------------|
| 1 | Project status: what should I do now? | `git status` |
| 2 | View changes | `git diff` |
| 3 | Add a new file to the project | `git add` |
| 4 | Save a modified file into the project | `git add` |
| 5 | Remove a file or folder | `git rm` |
| 6 | Commit changes | `git commit` |
| 7 | Publish the project to GitHub | `git push` |
| 8 | Create a release | `git tag` + `git push` |
| 9 | Version history | `git log` |
| 10 | Sync the project from GitHub | `git pull` |
| 11 | Technical repository diagnostic | `git status`, branch, remote, latest commit |
| 12 | Read the log | Opens `logs/gitdtl.log` |
| 13 | View the project on GitHub | Opens the configured GitHub page |
| 14 | Documentation | Opens the Markdown documentation |
| 15 | Magic command: GitScan | Scans a folder and summarizes detected Git repositories |
| 16 | Clone a GitHub repository | `git clone` |
| 17 | Publish a GitHub Release without kit | local tag + GitHub publication without installer kit |
| 18 | Build a kit and publish a GitHub Release | PyInstaller if needed + ZIP + manuals + GitHub publishing |

---

## Notable Behavior

**Automatic repository initialization.** If the current folder is not a Git repository, GitDTL offers to run `git init` before Git-specific operations.

**Initial project detection.** GitDTL tries to identify the most useful project folder at startup and can guide the user through choosing or creating a project.

**Remote setup.** If no `origin` remote is configured when publishing, GitDTL asks for the GitHub repository URL and stores it automatically.

**Upstream handling.** On the first push of a new branch, GitDTL detects a missing upstream and runs `git push --set-upstream origin <branch>` when appropriate.

**File removal choices.** When removing a file or folder, GitDTL can either delete it from disk and Git, or stop tracking it while keeping it locally and adding it to `.gitignore`.

**README reminder before commit.** Before committing, GitDTL asks whether the English documentation in `README.md` should be updated. If the user chooses yes, GitDTL opens `README.md`, waits for confirmation after the file is saved, and automatically runs `git add README.md` so the English documentation is included in the commit.

**Commit assistance.** Before option 6 asks for the commit message, GitDTL displays the current diff and status summary in a separate visible window. This helps the user write a meaningful commit message. The diff window stays visible while the commit-message prompt is open.

**Publish warning.** If local changes are not yet committed, GitDTL lists them and asks for confirmation before running `git push`.

**Visual guidance.** GitDTL highlights the next useful action after reading the project status, after adding files, after committing, or after publishing.

**Command feedback.** A discreet line at the bottom of the window shows the latest Git command actually executed by GitDTL.

**Silent Windows execution.** Git commands are run without opening extra console windows.

**First-run welcome.** On first launch, GitDTL shows a welcome screen. A local `.gitdtl_welcome_seen` marker prevents it from appearing again.

**Common Python ignore suggestions.** When common generated Python folders such as `__pycache__/` or `logs/` appear as untracked files, GitDTL can offer to add them to `.gitignore`.

**GitScan.** The GitScan tool scans a selected root folder, detects Git repositories, and summarizes their state.

**GitHub clone flow.** After cloning a GitHub repository, GitDTL detects the cloned folder and can immediately switch to managing it.

**Release creation.** The release action creates a version commit, creates an annotated tag such as `v1.2.3`, pushes the commit, and pushes the tag.

**Publish a GitHub Release without kit.** Option 17 starts from an existing local tag. It does not create a tag and does not prepare an installer kit. GitDTL checks that the repository is clean, that `origin` points to GitHub, that the tag exists locally, and that no GitHub Release already uses that tag. GitDTL pushes the tag if needed and creates the Release with GitHub CLI `gh`.

**Build a kit and publish a GitHub Release.** Option 18 runs the complete chain: PyInstaller compilation when a `.spec` file exists, ZIP creation, addition of the reference manual and user guide in the ZIP `documentation\` folder, then GitHub publication. It uses an existing local tag and refuses to publish if the repository is not clean or if a GitHub Release already exists for that tag.

**Application log.** Git commands and errors are written to `logs/gitdtl.log` with timestamps. The log can be viewed, cleared, or exported from the interface.

**Context help.** Dialog windows include a help button. Help text can be customized through `aide.md`.

**Expert advice.** Unexpected Git messages can be enriched with advice loaded from local rules in `expert_git.md`.

---

## Custom Help

Create or edit `aide.md` in the GitDTL folder. Sections are identified by keys:

```markdown
## commit_message

Briefly describe the change.
Example: Fix the HTML header calculation.

## release_version

Enter the version number using the X.Y.Z format.
The v prefix will be added automatically.
```

Common keys include:

`welcome`, `first_project_choice`, `create_git_repository`, `remove_file_action`, `commit_message`, `release_version`, `release_confirmation`, `clear_log`, `publish_with_uncommitted_changes`, `github_remote_url`, `clone_repository_url`, `common_python_ignores`, `stage_modified_files`.

If the file is missing, or if a key is not defined, GitDTL uses the built-in default help text.

---

## Custom Expert Rules

Create or edit `expert_git.md` in the GitDTL folder. Each rule contains Git message fragments to detect and advice to display:

```markdown
## Branch without upstream

Patterns:
- has no upstream branch
- --set-upstream

Advice:
The local branch is not connected to its GitHub branch yet.
GitDTL can fix this with git push --set-upstream origin <branch>.
```

---

## Building a Windows Executable

The repository includes `GitDTL.spec` for PyInstaller:

```powershell
python -m PyInstaller GitDTL.spec
```

If the build fails with an access-denied error on `dist\GitDTL.exe`, close every running GitDTL window first. Windows cannot replace the executable while it is still open.

---

## Project Structure

```text
gitdtl/
|-- GitDTL.py                         Main application
|-- GitDTL.spec                       PyInstaller build file
|-- aide.md                           Optional custom help text
|-- expert_git.md                     Optional expert-advice rules
|-- README.md                         English README
|-- README_Fr.md                      French README
|-- GitDTL_User_Guide.html            English user guide
|-- GitDTL_Reference_Manual.html      English reference manual
|-- GitDTL_Guide_Utilisateur.html     French user guide
|-- GitDTL_Manuel_de_Reference.html   French reference manual
|-- netdtl_logo.png                   NetDTL logo asset
|-- netdtl_logo_small.png             Small NetDTL logo asset
`-- logs/
    `-- gitdtl.log                    Application log, created automatically
```

---

## License

MIT - see `LICENSE`.

---

*In Memoriam Jean-Claude BELLAMY (1937-2015)*
