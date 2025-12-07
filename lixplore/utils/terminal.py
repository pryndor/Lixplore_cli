# lixplore/utils/terminal.py

import platform
import shutil
import subprocess

def open_in_new_terminal(text: str):
    system = platform.system()

    if system == "Linux":
        for term in ["xfce4-terminal", "gnome-terminal", "konsole", "xterm"]:
            if shutil.which(term):
                if term == "xfce4-terminal":
                    subprocess.Popen([term, "--hold", "-e", f"bash -c 'echo \"{text}\"; read -p \"Press Enter...\"'"])
                elif term == "gnome-terminal":
                    subprocess.Popen([term, "--", "bash", "-c", f"echo \"{text}\"; read -p 'Press Enter...'"])
                elif term == "konsole":
                    subprocess.Popen([term, "-e", f"bash -c 'echo \"{text}\"; read -p \"Press Enter...\"'"])
                else:  # xterm fallback
                    subprocess.Popen([term, "-hold", "-e", f"bash -c 'echo \"{text}\"; read'"])
                return

    elif system == "Darwin":  # macOS
        subprocess.Popen([
            "osascript", "-e",
            f'tell application "Terminal" to do script "echo \\"{text}\\"; read"'
        ])

    elif system == "Windows":
        subprocess.Popen(["start", "cmd", "/k", f"echo {text} && pause"], shell=True)

    else:
        print(text)

