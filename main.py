import json
import re
import random_responses
import tkinter as tk
from tkinter import scrolledtext, messagebox
import webbrowser  # Import webbrowser untuk membuka URL
from emoticons import emoticons  # Import emoticons dari file emoticons.py

# Fungsi untuk memuat JSON
def load_json(file):
    try:
        with open(file) as bot_responses:
            print(f"Loaded '{file}' successfully!")
            return json.load(bot_responses)
    except FileNotFoundError:
        messagebox.showerror("File Error", f"'{file}' not found!")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("File Error", f"'{file}' has invalid JSON format!")
        return None

# Memuat data bot dari file JSON
response_data = load_json("D:\\Development\\chat-bot\\bot.json")

# Fungsi untuk mendapatkan respons dari bot
def get_response(input_string):
    if not response_data:
        # Menggunakan respons acak jika data tidak ada
        return random_responses.random_string()

    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Cek untuk kalimat sedih
    sad_words = ["sad", "upset", "hurt", "unhappy", "depressed", "down", "cry", "miss", "lost", "heartbroken", "bad", "nothing"]
    if any(word in split_message for word in sad_words):
        return "I'm really sorry to hear that. Remember, it's okay to feel sad sometimes. " + emoticons.get("sad")

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if input_string == "":
        return "Please type something so we can chat :("

    if best_response != 0:
        # Menambahkan emotikon acak ke respons bot
        emoticon = emoticons.get("happy")  # Anda bisa mengganti kunci sesuai kebutuhan
        return response_data[response_index]["bot_response"] + " " + emoticon

    return random_responses.random_string()

# Membuat antarmuka GUI dengan Tkinter
class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")

        # Ukuran jendela
        self.root.geometry("500x600")
        self.root.configure(bg="#ededed")

        # Area tampilan chat
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', bg="#fafafa", fg="#000")
        self.chat_display.place(x=10, y=10, width=480, height=450)

        # Entry untuk input user
        self.user_input = tk.Entry(self.root, font=("Arial", 14), bg="#ffffff")
        self.user_input.place(x=10, y=470, width=380, height=40)
        self.user_input.bind("<Return>", self.send_message)

        # Tombol untuk mengirim pesan
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, font=("Arial", 12), bg="#4caf50", fg="white")
        self.send_button.place(x=400, y=470, width=90, height=40)

        # Tombol untuk membersihkan chat
        self.clear_button = tk.Button(self.root, text="Clear Chat", command=self.clear_chat, font=("Arial", 12), bg="#f44336", fg="white")
        self.clear_button.place(x=10, y=520, width=230, height=40)

        # Tombol untuk keluar dari aplikasi
        self.quit_button = tk.Button(self.root, text="Quit", command=self.confirm_quit, font=("Arial", 12), bg="#f44336", fg="white")
        self.quit_button.place(x=250, y=520, width=230, height=40)

        # Tombol untuk mengaktifkan dark mode
        self.dark_mode_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode, font=("Arial", 12), bg="#4caf50", fg="white")
        self.dark_mode_button.place(x=10, y=570, width=480, height=40)

        # Menampilkan ucapan selamat datang
        self.welcome_message = "Selamat datang di chatbot! Saya di sini untuk membantu Anda. 😊"
        self.update_chat(f"Bot: {self.welcome_message}")

        # Menambahkan label untuk informasi pembuat
        self.credit_label = tk.Label(self.root, text="Dibuat oleh ", bg="#ededed", font=("Arial", 10))
        self.credit_label.place(x=10, y=610)

        # Menambahkan link untuk GitHub
        self.github_link = tk.Label(self.root, text="Alpian", bg="#ededed", font=("Arial", 10), fg="blue", cursor="hand2")
        self.github_link.place(x=70, y=610)  # Pindahkan posisi label ke bawah tombol
        self.github_link.bind("<Button-1>", self.open_github)  # Mengaitkan klik pada label

        # Variabel untuk menyimpan status dark mode
        self.is_dark_mode = False

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip() == "":
            messagebox.showwarning("Input Error", "Please type something to chat!")
            return

        self.user_input.delete(0, tk.END)
        self.update_chat(f"You: {user_message}")

        bot_response = get_response(user_message)
        self.update_chat(f"Bot: {bot_response}")

    def update_chat(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def clear_chat(self):
        # Menghapus semua teks dari area tampilan chat kecuali ucapan selamat datang
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)  # Menghapus semua teks
        self.update_chat(f"Bot: {self.welcome_message}")  # Menampilkan kembali ucapan selamat datang
        self.chat_display.configure(state='disabled')

    def confirm_quit(self):
        # Menampilkan konfirmasi sebelum keluar
        if messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?"):
            self.root.quit()  # Keluar dari aplikasi

    def toggle_dark_mode(self):
        if self.is_dark_mode:
            # Kembali ke mode terang
            self.root.configure(bg="#ededed")
            self.chat_display.configure(bg="#fafafa", fg="#000")
            self.user_input.configure(bg="#ffffff", fg="#000")
            self.send_button.configure(bg="#4caf50", fg="white")
            self.clear_button.configure(bg="#f44336", fg="white")
            self.quit_button.configure(bg="#f44336", fg="white")
            self.dark_mode_button.configure(bg="#4caf50", fg="white")
            self.credit_label.configure(bg="#ededed", fg="#000")  # Update warna label
            self.github_link.configure(bg="#ededed", fg="blue")  # Update warna label GitHub
            self.is_dark_mode = False
        else:
            # Aktifkan mode gelap
            self.root.configure(bg="#333333")
            self.chat_display.configure(bg="#555555", fg="#fff")
            self.user_input.configure(bg="#777777", fg="#fff")
            self.send_button.configure(bg="#007acc", fg="white")
            self.clear_button.configure(bg="#ff3333", fg="white")
            self.quit_button.configure(bg="#ff3333", fg="white")
            self.dark_mode_button.configure(bg="#007acc", fg="white")
            self.credit_label.configure(bg="#333333", fg="#fff")  # Update warna label
            self.github_link.configure(bg="#333333", fg="lightblue")  # Update warna label GitHub
            self.is_dark_mode = True

    def open_github(self, event):
        # Fungsi untuk membuka link GitHub
        webbrowser.open("https://github.com/AlpianPPLG")

# Inisialisasi aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
