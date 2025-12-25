# lixplore/utils/terminal.py

import platform
import shutil
import subprocess
import tempfile
import os


def _supports_unicode_output() -> bool:
    import sys
    try:
        "📄".encode(sys.stdout.encoding or "utf-8")
        return True
    except Exception:
        return False


def _label(unicode_ok: bool, emoji: str, ascii_label: str) -> str:
    return f"{emoji} {ascii_label}:" if unicode_ok else f"{ascii_label.upper()}:"


def format_article_for_review(article: dict, article_number: int = None) -> str:
    """
    Format article data for detailed review in a separate terminal.

    Args:
        article: Dictionary containing article data
        article_number: Optional article number in the results list

    Returns:
        Formatted text for display
    """
    unicode_ok = _supports_unicode_output()

    # Get terminal width dynamically, with fallback to 100
    try:
        import shutil
        width = shutil.get_terminal_size().columns
        # Use reasonable limits: minimum 80, maximum 120
        width = max(80, min(width, 120))
    except:
        width = 100  # fallback default

    lines = []
    lines.append("=" * width)
    if article_number:
        lines.append(f"ARTICLE #{article_number} - DETAILED REVIEW".center(width))
    else:
        lines.append("ARTICLE DETAILED REVIEW".center(width))
    lines.append("=" * width)
    lines.append("")
    
    # Title
    if article.get('title'):
        lines.append(_label(unicode_ok, "📄", "Title"))
        lines.append("-" * width)
        lines.append(article['title'])
        lines.append("")

    # Authors
    if article.get('authors'):
        lines.append(_label(unicode_ok, "👥", "Authors"))
        lines.append("-" * width)
        if isinstance(article['authors'], list):
            for i, author in enumerate(article['authors'], 1):
                lines.append(f"  {i}. {author}")
        else:
            lines.append(f"  {article['authors']}")
        lines.append("")

    # Publication Info
    lines.append(_label(unicode_ok, "📚", "Publication Info"))
    lines.append("-" * width)
    if article.get('journal'):
        lines.append(f"  Journal: {article['journal']}")
    if article.get('year'):
        lines.append(f"  Year: {article['year']}")
    if article.get('source'):
        lines.append(f"  Source: {article['source']}")
    lines.append("")
    
    # DOI and URL
    if article.get('doi') or article.get('url'):
        lines.append(_label(unicode_ok, "🔗", "Links"))
        lines.append("-" * width)
        if article.get('doi'):
            lines.append(f"  DOI: {article['doi']}")
            lines.append(f"  DOI URL: https://doi.org/{article['doi']}")
        if article.get('url'):
            lines.append(f"  URL: {article['url']}")
        lines.append("")

    # Abstract
    if article.get('abstract'):
        lines.append(_label(unicode_ok, "📝", "Abstract"))
        lines.append("-" * width)
        # Wrap abstract text for better readability
        abstract = article['abstract']
        words = abstract.split()
        current_line = ""
        wrap_width = width - 2  # Leave 2 chars margin
        for word in words:
            if len(current_line) + len(word) + 1 <= wrap_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        lines.append("")

    lines.append("=" * width)
    lines.append("Press 'q' or Ctrl+C to close this window...".center(width))
    lines.append("=" * width)
    
    return "\n".join(lines)


def open_article_in_terminal(article: dict, article_number: int = None):
    """
    Open an article in a new terminal window for detailed review.
    
    Args:
        article: Dictionary containing article data
        article_number: Optional article number in the results list
    """
    formatted_text = format_article_for_review(article, article_number)
    
    # Create a temporary script file for better display
    system = platform.system()
    
    if system == "Linux":
        # Create a temporary script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write('#!/bin/bash\n')
            f.write('clear\n')
            f.write(f'cat << \'EOF\'\n{formatted_text}\nEOF\n')
            f.write('echo ""\n')  # Add blank line
            f.write('# Wait for q or Ctrl+C\n')
            f.write('while true; do\n')
            f.write('    read -n 1 -s -r key\n')
            f.write('    if [ "$key" = "q" ] || [ "$key" = "Q" ]; then\n')
            f.write('        break\n')
            f.write('    fi\n')
            f.write('done\n')
            f.write('echo ""\n')  # Add blank line after exit
            f.write(f'rm -f {f.name}\n')
            script_path = f.name
        
        os.chmod(script_path, 0o755)
        
        # Try different terminal emulators
        for term in ["xfce4-terminal", "gnome-terminal", "konsole", "xterm", "alacritty", "kitty"]:
            if shutil.which(term):
                try:
                    if term == "xfce4-terminal":
                        # xfce4-terminal: run script directly without --hold
                        subprocess.Popen([term, "-e", f"bash {script_path}"])
                    elif term == "gnome-terminal":
                        subprocess.Popen([term, "--", "bash", script_path])
                    elif term == "konsole":
                        subprocess.Popen([term, "--hold", "-e", f"bash {script_path}"])
                    elif term in ["alacritty", "kitty"]:
                        subprocess.Popen([term, "-e", "bash", script_path])
                    else:  # xterm fallback
                        subprocess.Popen([term, "-hold", "-e", f"bash {script_path}"])
                    return
                except Exception:
                    continue
        
        # Fallback: print to console
        print("\n" + formatted_text + "\n")
        try:
            os.remove(script_path)
        except:
            pass

    elif system == "Darwin":  # macOS
        # Create a temporary script for macOS
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write('#!/bin/bash\n')
            f.write('clear\n')
            f.write(f'cat << \'EOF\'\n{formatted_text}\nEOF\n')
            f.write('read -p ""\n')
            f.write(f'rm -f {f.name}\n')
            script_path = f.name
        
        os.chmod(script_path, 0o755)
        
        subprocess.Popen([
            "osascript", "-e",
            f'tell application "Terminal" to do script "{script_path}"'
        ])

    elif system == "Windows":
        # Create a temporary batch file for Windows
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as f:
            f.write('@echo off\n')
            f.write('cls\n')
            f.write(f'echo {formatted_text}\n')
            f.write('pause\n')
            f.write(f'del {f.name}\n')
            script_path = f.name
        
        subprocess.Popen(["start", "cmd", "/c", script_path], shell=True)
    
    else:
        # Fallback: print to console
        print("\n" + formatted_text + "\n")


def open_in_new_terminal(text: str):
    """
    Open text in a new terminal window.
    
    Args:
        text: Text to display
    """
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

