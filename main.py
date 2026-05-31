import tkinter as tk
from tkinter import filedialog, scrolledtext
import io
import sys
import traceback

# ---------------- WINDOW ---------------- #

root = tk.Tk()
root.title("⚡ VS Code Lite - Neon Edition")
root.geometry("1100x720")
root.config(bg="#0b0f1a")

current_file = None

# ---------------- COLORS ---------------- #

BG = "#0b0f1a"
EDITOR_BG = "#111827"
SIDEBAR = "#0f172a"
TERMINAL_BG = "#050816"

ACCENT = "#00ffd5"
BLUE = "#38bdf8"
PURPLE = "#a78bfa"
GREEN = "#22c55e"
RED = "#ef4444"

TEXT = "white"

# ---------------- FUNCTIONS ---------------- #

def open_file():
    global current_file

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python Files", "*.py"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        current_file = file_path

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        editor.delete("1.0", tk.END)
        editor.insert(tk.END, code)

        set_status(f"Opened: {file_path}")


def save_file():
    global current_file

    if current_file:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", tk.END))

        set_status("File saved ✓")
    else:
        save_as()


def save_as():
    global current_file

    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python Files", "*.py")]
    )

    if file_path:
        current_file = file_path

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", tk.END))

        set_status(f"Saved: {file_path}")


def run_code():
    code = editor.get("1.0", tk.END)

    output.delete("1.0", tk.END)
    output.insert(tk.END, "⚡ Running Code...\n\n")

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    redirected_output = io.StringIO()

    sys.stdout = redirected_output
    sys.stderr = redirected_output

    try:
        exec(code, {})
    except Exception:
        traceback.print_exc()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    result = redirected_output.getvalue()

    if result.strip():
        output.insert(tk.END, result)
    else:
        output.insert(tk.END, "✅ Code executed successfully (No Output)")

    set_status("Execution complete ✓")


def clear_terminal():
    output.delete("1.0", tk.END)


def clear_editor():
    editor.delete("1.0", tk.END)
    set_status("Editor cleared")


def set_status(message):
    status_label.config(text=f"  {message}")


# ---------------- UI ---------------- #

# Sidebar
sidebar = tk.Frame(root, bg=SIDEBAR, width=240)
sidebar.pack(side="left", fill="y")

logo = tk.Label(
    sidebar,
    text="⚡ NEON IDE",
    font=("Consolas", 18, "bold"),
    fg=ACCENT,
    bg=SIDEBAR
)
logo.pack(pady=25)


def neon_button(text, command, color):
    btn = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=color,
        fg="black",
        font=("Consolas", 11, "bold"),
        relief="flat",
        bd=0,
        padx=12,
        pady=10,
        cursor="hand2",
        activebackground=PURPLE,
        activeforeground="white"
    )
    return btn


neon_button("📂 Open File", open_file, ACCENT).pack(
    fill="x", padx=15, pady=6
)

neon_button("💾 Save", save_file, BLUE).pack(
    fill="x", padx=15, pady=6
)

neon_button("💾 Save As", save_as, PURPLE).pack(
    fill="x", padx=15, pady=6
)

neon_button("▶ Run Code", run_code, GREEN).pack(
    fill="x", padx=15, pady=(20, 6)
)

neon_button("🧹 Clear Editor", clear_editor, "#f59e0b").pack(
    fill="x", padx=15, pady=6
)

neon_button("🗑 Clear Terminal", clear_terminal, RED).pack(
    fill="x", padx=15, pady=6
)

# Main area
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True)

# Editor title
editor_title = tk.Label(
    main_frame,
    text="Editor",
    bg=BG,
    fg=ACCENT,
    font=("Arial", 12, "bold")
)
editor_title.pack(anchor="w", padx=12, pady=(10, 0))

# Code editor
editor = scrolledtext.ScrolledText(
    main_frame,
    bg=EDITOR_BG,
    fg="white",
    insertbackground=ACCENT,
    font=("Consolas", 13),
    relief="flat",
    borderwidth=0,
    padx=12,
    pady=12
)
editor.pack(fill="both", expand=True, padx=12, pady=8)

# Terminal title
terminal_title = tk.Label(
    main_frame,
    text="Terminal Output",
    bg=BG,
    fg=GREEN,
    font=("Arial", 12, "bold")
)
terminal_title.pack(anchor="w", padx=12)

# Output terminal
output = scrolledtext.ScrolledText(
    main_frame,
    height=12,
    bg=TERMINAL_BG,
    fg=ACCENT,
    font=("Consolas", 11),
    relief="flat",
    borderwidth=0,
    padx=12,
    pady=12
)
output.pack(fill="x", padx=12, pady=(8, 12))

# Status bar
status_label = tk.Label(
    root,
    text="  Ready",
    bg="#111827",
    fg="white",
    anchor="w",
    font=("Arial", 10)
)
status_label.pack(fill="x", side="bottom")

# Starter code
editor.insert(
    "1.0",
    '''print("hello world!")
'''
)

root.mainloop()