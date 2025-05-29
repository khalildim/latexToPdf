import os
import shutil
import subprocess
import tempfile
from pdf2image import convert_from_path
from tkinter import messagebox


class LaTeXConverter:
    """
    Class to compile LaTeX code to PDF and convert PDF to images.
    Temporary files are managed automatically.
    """

    def __init__(self):
        self.temp_dir = None
        self.tex_path = None
        self.pdf_path = None

    def write_latex_file(self, latex_code: str):
        """Create a temp directory and write LaTeX code to a .tex file."""
        self.cleanup()  # Clean up previous temp directory if exists
        self.temp_dir = tempfile.mkdtemp()
        self.tex_path = os.path.join(self.temp_dir, "main.tex")
        self.pdf_path = os.path.join(self.temp_dir, "main.pdf")

        with open(self.tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        print(f"📄 LaTeX written to: {self.tex_path}")

    def compile_latex(self) -> bool:
        """Compile the LaTeX file into a PDF."""
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", os.path.basename(self.tex_path)],
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                messagebox.showerror(title="compilation failed", message="Please check you code if something wrong")
                print("❌ Compilation failed.")
                print(result.stdout)
                print(result.stderr)
                return False

            print("✅ Compilation succeeded.")
            return True
        except Exception as e:
            messagebox.showerror(title="Exception during compilation", message=str(e))
            print(f"❌ Exception during compilation: {e}")
            return False

    def get_pdf_preview_images(self, dpi=100):
        """Convert the compiled PDF into a list of images."""
        if not os.path.exists(self.pdf_path):
            messagebox.showerror(title="Error", message="PDF file not found. try to compile again")
            print("❌ PDF file not found.")
            return []

        try:
            images = convert_from_path(self.pdf_path, dpi=dpi)
            print(f"🖼️ Generated {len(images)} preview image(s).")
            return images
        except Exception as e:
            messagebox.showerror(title="Error", message="Failed to convert PDF to images")
            print(f"❌ Failed to convert PDF to images: {e}")
            return []

    def compile_and_preview(self, latex_code: str):
        """Compile LaTeX and return preview images."""
        self.write_latex_file(latex_code)
        if self.compile_latex():
            return self.get_pdf_preview_images()
        return []

    def cleanup(self):
        """Remove the temporary directory and all contents."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Removed temp dir: {self.temp_dir}")
            self.temp_dir = None

    def __del__(self):
        """Destructor to ensure cleanup on deletion."""
        self.cleanup()

# # Example usage
# if __name__ == "__main__":
#     sample_latex = r"""
#     \documentclass{article}
#     \begin{document}
#     Hello \LaTeX! I'm Khalil.
#     \newpage
#     This is page 2.
#     \end{document}
#     """
#
#     converter = LaTeXConverter()
#     images = converter.compile_and_preview(sample_latex)
#     if images:
#         images[0].show()
#           # Show the first page as a preview
