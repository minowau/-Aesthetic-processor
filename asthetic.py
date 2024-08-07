
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageEnhance, ImageFilter
import os
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import queue

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processor and Email Sender")
        master.geometry("700x500")
        master.configure(bg="#0f0f0f")

        self.folder_paths = {
            "aesthetic": tk.StringVar(),
            "greyscale": tk.StringVar()
        }
        self.gmail_id = tk.StringVar()

        self.queue = queue.Queue()
        self.create_widgets()
        self.master.after(100, self.process_queue)

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="#0f0f0f", foreground="#00ff00", font=("Courier New", 14, "bold"))
        style.configure("TEntry", background="#2b2b2b", foreground="#00ff00", fieldbackground="#2b2b2b", font=("Courier New", 14, "bold"))
        style.configure("TButton", background="#2b2b2b", foreground="#00ff00", font=("Courier New", 14, "bold"), padding=10)
        style.configure("TFrame", background="#0f0f0f")
        style.configure("TProgressbar", background="#00ff00", troughcolor="#2b2b2b")

        frame = ttk.Frame(self.master, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title_label = ttk.Label(frame, text="Image Processor and Email Sender", font=("Courier New", 20, "bold"), foreground="#00ff00")
        title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        ttk.Label(frame, text="Aesthetic Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(frame, textvariable=self.folder_paths["aesthetic"], width=40).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_folder("aesthetic")).grid(row=1, column=2, padx=10, pady=10)

        ttk.Label(frame, text="Greyscale Folder:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(frame, textvariable=self.folder_paths["greyscale"], width=40).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_folder("greyscale")).grid(row=2, column=2, padx=10, pady=10)

        ttk.Label(frame, text="Gmail ID:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(frame, textvariable=self.gmail_id, width=40).grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(frame, text="Start Monitoring", command=self.start_monitoring).grid(row=4, column=1, padx=10, pady=20)

        self.status_label = ttk.Label(frame, text="Status: Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def browse_folder(self, folder_type):
        folder_selected = filedialog.askdirectory()
        self.folder_paths[folder_type].set(folder_selected)

    def process_image(self, input_path, output_path, process_type):
        with Image.open(input_path) as img:
            if process_type == "aesthetic":
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.4)
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.1)
                img = img.filter(ImageFilter.SHARPEN)
                width, height = img.size
                mask = Image.new('L', (width, height), 255)
                for x in range(width):
                    for y in range(height):
                        distance = min(x, y, width-x, height-y)
                        mask.putpixel((x, y), max(0, 255 - (255 - distance)))
                blurred_mask = mask.filter(ImageFilter.GaussianBlur(30))
                img = Image.composite(img, Image.new('RGB', (width, height), (0, 0, 0)), blurred_mask)
            elif process_type == "greyscale":
                img = img.convert('L')

            img.save(output_path)

    def send_email(self, email_id, attachment_paths):
        sender_email = "jupalliprabhas@gmail.com"
        sender_password = "prug timh zjqh akey"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_id
        msg['Subject'] = "Processed Images"

        body = "Please find attached the processed images."
        msg.attach(MIMEText(body, 'plain'))

        for attachment in attachment_paths:
            filename = os.path.basename(attachment)
            attachment_part = MIMEBase('application', 'octet-stream')
            with open(attachment, 'rb') as f:
                attachment_part.set_payload(f.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(attachment_part)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, email_id, text)
                self.queue.put("Status: Email sent successfully!")
        except Exception as e:
            self.queue.put(f"Status: Failed to send email. Error: {str(e)}")

    def monitor_folders(self):
        while True:
            for process_type, folder_path_var in self.folder_paths.items():
                folder_path = folder_path_var.get()
                if folder_path:
                    for filename in os.listdir(folder_path):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                            input_path = os.path.join(folder_path, filename)
                            output_folder = os.path.join(folder_path, f"{process_type}_processed")
                            os.makedirs(output_folder, exist_ok=True)
                            output_path = os.path.join(output_folder, filename)
                            self.process_image(input_path, output_path, process_type)
                            self.send_email(self.gmail_id.get(), [output_path])
                            if os.path.exists(input_path):
                                os.remove(input_path)

            time.sleep(60)

    def start_monitoring(self):
        gmail_id = self.gmail_id.get()
        if not gmail_id:
            messagebox.showerror("Error", "Please enter Gmail ID.")
            return

        threading.Thread(target=self.monitor_folders).start()
        self.queue.put("Status: Monitoring started...")

    def process_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                self.status_label.config(text=msg)
        except queue.Empty:
            self.master.after(100, self.process_queue)

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
