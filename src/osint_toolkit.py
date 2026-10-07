import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import subprocess
import threading
import webbrowser

# ============================================================
# OSINT TOOLKIT - GUI
# A launcher/catalogue for legitimate OSINT tools.
# It does not bypass authentication or access private data.
# ============================================================

TOOLS = [
    {
        "name": "Sherlock",
        "command": "sherlock",
        "category": "Username",
        "description": "Sucht nach einem Benutzernamen auf vielen öffentlich erreichbaren Webseiten.",
        "usage": "sherlock USERNAME",
        "url": "https://github.com/sherlock-project/sherlock",
    },
    {
        "name": "SpiderFoot",
        "command": "spiderfoot",
        "category": "OSINT",
        "description": "Automatisiert OSINT-Recherche und verbindet öffentlich verfügbare Informationen.",
        "usage": "spiderfoot -l 127.0.0.1:5001",
        "url": "https://github.com/smicallef/spiderfoot",
    },
    {
        "name": "theHarvester",
        "command": "theHarvester",
        "category": "Domain",
        "description": "Sammelt öffentlich verfügbare Informationen zu Domains, z. B. Suchmaschinen-Treffer und E-Mail-Adressen.",
        "usage": "theHarvester -d example.com -b bing",
        "url": "https://github.com/laramies/theHarvester",
    },
    {
        "name": "Recon-ng",
        "command": "recon-ng",
        "category": "OSINT",
        "description": "Modulares Framework für strukturierte OSINT-Recherche.",
        "usage": "recon-ng",
        "url": "https://github.com/lanmaster53/recon-ng",
    },
    {
        "name": "Amass",
        "command": "amass",
        "category": "Domain",
        "description": "Recherchiert Domains, Subdomains und öffentlich erkennbare Netzwerkbeziehungen.",
        "usage": "amass enum -passive -d example.com",
        "url": "https://github.com/owasp-amass/amass",
    },
    {
        "name": "ExifTool",
        "command": "exiftool",
        "category": "Metadaten",
        "description": "Liest Metadaten aus Bildern, PDFs und zahlreichen anderen Dateiformaten.",
        "usage": "exiftool bild.jpg",
        "url": "https://exiftool.org/",
    },
    {
        "name": "GHunt",
        "command": "ghunt",
        "category": "Accounts",
        "description": "Untersucht öffentlich sichtbare Informationen rund um Google-Konten.",
        "usage": "ghunt --help",
        "url": "https://github.com/mxrch/GHunt",
    },
    {
        "name": "Nmap",
        "command": "nmap",
        "category": "Netzwerk",
        "description": "Analysiert erreichbare Netzwerkdienste und Ports. Nur auf Systemen verwenden, für die du autorisiert bist.",
        "usage": "nmap -sV example.com",
        "url": "https://nmap.org/",
    },
    {
        "name": "WHOIS",
        "command": "whois",
        "category": "Domain",
        "description": "Zeigt öffentlich verfügbare Registrierungsinformationen zu Domains und IP-Netzen.",
        "usage": "whois example.com",
        "url": "https://www.iana.org/whois",
    },
    {
        "name": "dig",
        "command": "dig",
        "category": "DNS",
        "description": "Fragt öffentliche DNS-Informationen wie A-, MX- oder TXT-Records ab.",
        "usage": "dig example.com",
        "url": "https://bind9.readthedocs.io/",
    },
]

CATEGORIES = ["Alle", "Username", "OSINT", "Domain", "Metadaten", "Accounts", "Netzwerk", "DNS"]


class OSINTToolkit(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OSINT Toolkit")
        self.geometry("1180x720")
        self.minsize(900, 600)

        self.bg = "#111827"
        self.panel = "#1f2937"
        self.panel2 = "#273449"
        self.text = "#f3f4f6"
        self.muted = "#9ca3af"
        self.accent = "#60a5fa"
        self.success = "#34d399"
        self.danger = "#f87171"

        self.configure(bg=self.bg)
        self.selected_tool = None

        self.setup_style()
        self.build_ui()
        self.refresh_tools()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.panel,
            foreground=self.text,
            fieldbackground=self.panel,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.panel2,
            foreground=self.text,
            font=("Segoe UI Semibold", 10),
            padding=8,
        )
        style.map(
            "Treeview",
            background=[("selected", "#334155")],
            foreground=[("selected", self.text)],
        )
        style.configure(
            "TCombobox",
            fieldbackground=self.panel,
            background=self.panel2,
            foreground=self.text,
        )

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=self.bg)
        header.pack(fill="x", padx=24, pady=(20, 12))

        tk.Label(
            header,
            text="OSINT Toolkit",
            font=("Segoe UI", 25, "bold"),
            bg=self.bg,
            fg=self.text,
        ).pack(side="left")

        tk.Label(
            header,
            text="Open-Source Intelligence • Tool Manager",
            font=("Segoe UI", 10),
            bg=self.bg,
            fg=self.muted,
        ).pack(side="left", padx=16, pady=(10, 0))

        # Search/filter row
        controls = tk.Frame(self, bg=self.bg)
        controls.pack(fill="x", padx=24, pady=(0, 12))

        tk.Label(
            controls, text="Suche", bg=self.bg, fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(side="left")

        self.search_var = tk.StringVar()
        search = tk.Entry(
            controls,
            textvariable=self.search_var,
            bg=self.panel,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            font=("Segoe UI", 11),
        )
        search.pack(side="left", fill="x", expand=True, padx=(8, 16), ipady=8)
        search.bind("<KeyRelease>", lambda e: self.refresh_tools())

        tk.Label(
            controls, text="Kategorie", bg=self.bg, fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(side="left")

        self.category_var = tk.StringVar(value="Alle")
        category = ttk.Combobox(
            controls,
            textvariable=self.category_var,
            values=CATEGORIES,
            state="readonly",
            width=15,
        )
        category.pack(side="left", padx=(8, 0))
        category.bind("<<ComboboxSelected>>", lambda e: self.refresh_tools())

        # Main area
        main = tk.Frame(self, bg=self.bg)
        main.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        left = tk.Frame(main, bg=self.panel)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(main, bg=self.panel, width=390)
        right.pack(side="right", fill="both", padx=(14, 0))
        right.pack_propagate(False)

        # Tool list
        columns = ("tool", "category", "status")
        self.tree = ttk.Treeview(left, columns=columns, show="headings")
        self.tree.heading("tool", text="Tool")
        self.tree.heading("category", text="Kategorie")
        self.tree.heading("status", text="Status")
        self.tree.column("tool", width=180)
        self.tree.column("category", width=130)
        self.tree.column("status", width=120)

        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Details
        self.detail_title = tk.Label(
            right, text="Tool auswählen",
            bg=self.panel, fg=self.text,
            font=("Segoe UI", 19, "bold"),
            anchor="w",
        )
        self.detail_title.pack(fill="x", padx=20, pady=(22, 6))

        self.detail_category = tk.Label(
            right, text="",
            bg=self.panel, fg=self.accent,
            font=("Segoe UI Semibold", 10),
            anchor="w",
        )
        self.detail_category.pack(fill="x", padx=20)

        self.detail_text = tk.Text(
            right,
            bg=self.panel,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            wrap="word",
            height=10,
            font=("Segoe UI", 10),
        )
        self.detail_text.pack(fill="both", expand=True, padx=20, pady=15)
        self.detail_text.configure(state="disabled")

        self.command_label = tk.Label(
            right, text="Beispiel:",
            bg=self.panel, fg=self.muted,
            font=("Segoe UI Semibold", 9),
            anchor="w",
        )
        self.command_label.pack(fill="x", padx=20)

        self.command_var = tk.StringVar()
        command_entry = tk.Entry(
            right,
            textvariable=self.command_var,
            bg="#0b1220",
            fg="#dbeafe",
            insertbackground=self.text,
            relief="flat",
            font=("Consolas", 10),
        )
        command_entry.pack(fill="x", padx=20, pady=(5, 15), ipady=7)

        buttons = tk.Frame(right, bg=self.panel)
        buttons.pack(fill="x", padx=20, pady=(0, 20))

        self.start_button = tk.Button(
            buttons,
            text="▶  Tool starten",
            command=self.start_tool,
            bg=self.accent,
            fg="#08111f",
            activebackground="#93c5fd",
            relief="flat",
            font=("Segoe UI Semibold", 10),
            padx=12,
            pady=9,
            cursor="hand2",
        )
        self.start_button.pack(side="left", fill="x", expand=True)

        tk.Button(
            buttons,
            text="Dokumentation",
            command=self.open_docs,
            bg=self.panel2,
            fg=self.text,
            activebackground="#334155",
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=9,
            cursor="hand2",
        ).pack(side="left", padx=(8, 0))

        # Output
        output_frame = tk.Frame(self, bg=self.bg)
        output_frame.pack(fill="x", padx=24, pady=(0, 18))

        tk.Label(
            output_frame,
            text="Status",
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI Semibold", 9),
        ).pack(anchor="w")

        self.status_var = tk.StringVar(value="Bereit.")
        tk.Label(
            output_frame,
            textvariable=self.status_var,
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x", pady=(3, 0))

    def refresh_tools(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_var.get().lower().strip()
        category = self.category_var.get()

        for tool in TOOLS:
            if category != "Alle" and tool["category"] != category:
                continue

            searchable = (
                tool["name"] + " " +
                tool["category"] + " " +
                tool["description"]
            ).lower()

            if search and search not in searchable:
                continue

            installed = shutil.which(tool["command"]) is not None
            status = "✓ installiert" if installed else "✗ fehlt"

            self.tree.insert(
                "",
                "end",
                iid=tool["name"],
                values=(tool["name"], tool["category"], status),
            )

    def get_selected_tool(self):
        selection = self.tree.selection()
        if not selection:
            return None

        name = selection[0]
        return next((t for t in TOOLS if t["name"] == name), None)

    def on_select(self, _event=None):
        tool = self.get_selected_tool()
        if not tool:
            return

        self.selected_tool = tool

        self.detail_title.config(text=tool["name"])
        self.detail_category.config(text=tool["category"])

        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert(
            "1.0",
            tool["description"] +
            "\n\nWofür geeignet:\n" +
            self.category_explanation(tool["category"]) +
            "\n\nBeispielbefehl:\n" +
            tool["usage"]
        )
        self.detail_text.configure(state="disabled")

        self.command_var.set(tool["usage"])

        installed = shutil.which(tool["command"]) is not None
        if installed:
            self.start_button.config(
                state="normal",
                bg=self.accent,
                text="▶  Tool starten"
            )
            self.status_var.set(f"{tool['name']} ist installiert.")
        else:
            self.start_button.config(
                state="disabled",
                bg="#475569",
                text="✗  Nicht installiert"
            )
            self.status_var.set(
                f"{tool['name']} wurde nicht im PATH gefunden."
            )

    def category_explanation(self, category):
        explanations = {
            "Username": "Suche nach öffentlich sichtbaren Profilen, die einen bestimmten Benutzernamen verwenden.",
            "OSINT": "Breit angelegte Recherche und Verknüpfung öffentlich zugänglicher Informationen.",
            "Domain": "Analyse öffentlich zugänglicher Informationen rund um Domains und deren Infrastruktur.",
            "Metadaten": "Untersuchung technischer Metadaten, die in öffentlich bereitgestellten Dateien enthalten sein können.",
            "Accounts": "Recherche öffentlich sichtbarer Account-Informationen.",
            "Netzwerk": "Technische Analyse erreichbarer Netzwerkdienste. Nur mit entsprechender Berechtigung verwenden.",
            "DNS": "Abfrage und Analyse öffentlich erreichbarer DNS-Informationen.",
        }
        return explanations.get(category, "Öffentlich zugängliche Informationen recherchieren.")

    def start_tool(self):
        if not self.selected_tool:
            return

        tool = self.selected_tool
        command = self.command_var.get().strip()

        if not command:
            return

        executable = command.split()[0]

        if shutil.which(executable) is None:
            messagebox.showerror(
                "Tool nicht gefunden",
                f"'{executable}' wurde nicht gefunden.\n\n"
                "Installiere das Tool und stelle sicher, dass es im PATH liegt."
            )
            return

        self.status_var.set(f"Starte {tool['name']} ...")

        def run():
            try:
                # shell=False: keine Shell-Auswertung.
                args = command.split()
                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                output = process.communicate()[0]

                self.after(
                    0,
                    lambda: self.show_output(tool["name"], output)
                )
            except Exception as exc:
                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "Fehler",
                        f"Das Tool konnte nicht gestartet werden:\n{exc}"
                    )
                )
            finally:
                self.after(
                    0,
                    lambda: self.status_var.set(
                        f"{tool['name']} beendet."
                    )
                )

        threading.Thread(target=run, daemon=True).start()

    def show_output(self, name, output):
        window = tk.Toplevel(self)
        window.title(f"{name} – Output")
        window.geometry("900x550")
        window.configure(bg=self.bg)

        text = tk.Text(
            window,
            bg="#080d16",
            fg="#d1d5db",
            insertbackground=self.text,
            relief="flat",
            font=("Consolas", 10),
            wrap="none",
        )
        text.pack(fill="both", expand=True, padx=12, pady=12)
        text.insert("1.0", output or "(Kein Output)")
        text.configure(state="disabled")

    def open_docs(self):
        if self.selected_tool:
            webbrowser.open(self.selected_tool["url"])


if __name__ == "__main__":
    app = OSINTToolkit()
    app.mainloop()
