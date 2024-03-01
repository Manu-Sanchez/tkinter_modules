import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, END


class AutocompleteEntry(ctk.CTkEntry):

    def __init__(self, parent, known_values):


        super().__init__(parent)

        self.display_status = 0
        self.entry_value = tk.StringVar(self)
        self.configure(textvariable=self.entry_value)
        self.configure(corner_radius=0)

        # parent.bind("<Configure>", self.get_pos)
        self.frame = tk.Frame(parent, background="white")
        self.scrollbar = ctk.CTkScrollbar(self.frame, width=10)
        self.labels = []
        self.known_values = known_values
        self.parent = parent

        self.bind("<KeyRelease>", self.toggle_visibility)

        self.parent.bind("<Button-1>", self.toggle)


    def clean_labels(self):

        for label in self.labels:
            label.pack_forget()

        self.labels = []

    def toggle(self, event):
        print(event)
        print(self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height())
        if (event.x < self.frame.winfo_x() or event.x > self.frame.winfo_x() + self.frame.winfo_height() or \
        event.y < self.frame.winfo_y() or event.y > self.frame.winfo_y() + self.frame.winfo_width()):
            
            self.frame.place_forget()
            self.display_status = 0

    def toggle_visibility(self, event):
        print(event)
        print(self.winfo_y(), self.winfo_x())
        print(self.winfo_rooty(), self.winfo_rootx())
        print(self.frame.winfo_width(), self.frame.winfo_height())
        print(self.winfo_width(), self.winfo_height())
        
        self.clean_labels()
        self.update()

        filtered_values = []
        for value in self.known_values:
            if self.entry_value.get() in value:
                filtered_values.append(value)

        print(self.entry_value.get())
        print(filtered_values)
        for idx, value in enumerate(filtered_values):
            self.labels.append(ctk.CTkLabel(self.frame, text=value, text_color="black", anchor="w", padx=10))
            self.labels[-1].bind("<Enter>", self.highlight("enter", idx))
            self.labels[-1].bind("<Leave>", self.highlight("leave", idx))
            self.labels[-1].bind("<Button-1>", self.highlight("click", idx))

            self.labels[-1].pack(expand=True, fill="both")

        if filtered_values:

            self.frame.place(x = self.winfo_x() + self.winfo_width() + 10, y = self.winfo_height() + self.winfo_y(), width=self.winfo_width() + 10, anchor="ne")
            self.frame.lift()   
            self.scrollbar.place(x=self.winfo_width()+10, y=0, relheight=1, anchor="ne")
            self.scrollbar.lift()
            self.display_status = 1

        else:
            self.frame.place_forget()
            self.display_status = 0

    def get_pos(self, event):
        print(event)
        print(self.winfo_y(), self.winfo_x())
        print(self.winfo_rooty(), self.winfo_rootx())

        # self.frame.place(x = self.winfo_x() + self.frame.winfo_width(), y = self.winfo_height() + self.winfo_y(), width=self.winfo_width(), anchor="ne" )

        
    def highlight(self, method, idx):
        
        def hightlight_trigger(event):
            self.labels[idx].configure(bg_color="black", text_color="white")

        def unhightlight_trigger(event):
            self.labels[idx].configure(bg_color="white", text_color="black")

        def click_trigger(event):
            self.delete(0, END)
            self.insert(0, self.labels[idx].cget("text"))
            self.frame.place_forget()
            
            self.display_status = 0

        if method == "enter":
            return hightlight_trigger
        elif method == "leave":
            return unhightlight_trigger
        elif method == "click":
            return click_trigger
    


known_values = ["test", "test_masup", "test_app", "mytest", "filter"]

window = ctk.CTk()
window.geometry("600x400")
AutocompleteEntry(window, known_values).pack()


ctk.CTkEntry(window).pack()

window.mainloop()
