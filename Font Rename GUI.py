import os, shutil
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, RIGHT, Y, END
from fontTools.ttLib import TTFont

class FontRenamerApp:
    def __init__(self, master):
        self.master = master
        master.title("Font Renamer & Mover")

        Button(master, text="Select Source Folder", command=self.select_source_folder).pack(pady=5)
        Button(master, text="Select Destination Folder", command=self.select_dest_folder).pack(pady=5)
        Button(master, text="Start Rename & Move", command=self.rename_and_move_fonts).pack(pady=10)

        self.text = Text(master, height=20, width=80); self.text.pack(padx=10, pady=5)
        Scrollbar(master, command=self.text.yview).pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=lambda f, l: self.text.yview_moveto(f))

        self.source_folder = ""; self.dest_folder = ""

    def log(self, message):
        self.text.insert(END, message + "\n"); self.text.see(END)

    def select_source_folder(self):
        self.source_folder = filedialog.askdirectory(); self.log(f"Source: {self.source_folder}")

    def select_dest_folder(self):
        self.dest_folder = filedialog.askdirectory(); self.log(f"Destination: {self.dest_folder}")

    def rename_and_move_fonts(self):
        if not self.source_folder or not self.dest_folder:
            self.log("❌ Please select both source & destination folders."); return
        for fn in os.listdir(self.source_folder):
            if fn.lower().endswith(".ttf"):
                path = os.path.join(self.source_folder, fn)
                try:
                    font = TTFont(path)
                    name = next((r.string.decode('utf-16-be') if b'\x00' in r.string else r.string.decode('utf-8')
                                 for r in font['name'].names if r.nameID == 4), None)
                    if name:
                        clean = "".join(c for c in name if c.isalnum() or c in " _-").strip()
                        new = clean + ".ttf"; dst = os.path.join(self.dest_folder, new)
                        cnt = 1
                        while os.path.exists(dst):
                            new = f"{clean}_{cnt}.ttf"; dst = os.path.join(self.dest_folder, new); cnt += 1
                        shutil.copy(path, dst); self.log(f"✅ {fn} → {new}")
                except Exception as e:
                    self.log(f"❌ Error {fn}: {e}")

if __name__ == "__main__":
    root = Tk()
    FontRenamerApp(root)
    root.mainloop()
