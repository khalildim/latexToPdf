import shutil
import platform
import subprocess
import customtkinter as ctk
from converting import LaTeXConverter
from tkinter import filedialog, messagebox


class Interface:
    def __init__(self):
        self.main_frame = ctk.CTk()
        self.converter = LaTeXConverter()
        self.main_frame.title("Latex to PDF converter")
        self.main_frame.geometry("1200x600")
        self.main_frame.minsize(1200, 600)
        self.main_frame.configure(fg_color="#2f333d")

        # configure grid for dynamic resizing
        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)

        # left frame
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.configure(fg_color="#232a3a")
        self.left_frame.grid(column=0, row=0, sticky='nswe')
        self.left_frame.columnconfigure(0, weight=3)
        self.left_frame.rowconfigure(0, weight=3)

        # left frame component
        self.text_box = ctk.CTkTextbox(self.left_frame, width=500, height=500)
        self.text_box.grid(column=0, row=0, sticky="nswe", padx=5, pady=5)

        self.button_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.button_frame.grid(column=0, row=1, pady=10)
        self.compile_btn = ctk.CTkButton(self.button_frame, text="Compile", width=130, command=self.compiler_preview)
        self.compile_btn.grid(row=0, column=0, padx=10)
        self.download_btn = ctk.CTkButton(self.button_frame, text="Download", width=130, command=self.download_pdf)
        self.download_btn.grid(row=0, column=1, padx=10)

        # right frame
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.right_frame.configure(fg_color="#2f333d")
        self.right_frame.grid(column=1, row=0, sticky="nswe")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(0, weight=1)

        self.main_frame.mainloop()

    def compiler_preview(self):
        latex_code = self.text_box.get("0.0", "end").strip()

        # Cleanup old previews
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        images = self.converter.compile_and_preview(latex_code)

        for idx, image in enumerate(images):
            img = ctk.CTkImage(light_image=image, dark_image=image, size=(827, 1170))
            label = ctk.CTkLabel(self.right_frame, image=img, text="")
            label.image = img  # Prevent garbage collection
            label.grid(column=0, row=idx, pady=10)

        self.main_frame.update()

    def download_pdf(self):
        if not self.converter or not self.converter.pdf_path:
            messagebox.showerror("Error", "No PDF to download.")
            return

        # Ask user where to save the PDF
        download_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as..."
        )

        if download_path:
            try:
                if platform.system() == "linux":
                    subprocess.run(["sudo","mv",self.converter.pdf_path, " ", download_path])
                else:
                    shutil.copy(self.converter.pdf_path, download_path)
                    messagebox.showinfo("Success", f"PDF saved to:\n{download_path}")
                self.converter.cleanup()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF:\n{e}")


if __name__ == "__main__":
    Interface()
