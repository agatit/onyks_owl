import tkinter as tk


# todo: zastąpić dekoratorem
class LoadingScreen(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("LoadingScreen.py")

        self.label = tk.Label(self, text="Loading...")
        self.label.pack()

        self.update()
