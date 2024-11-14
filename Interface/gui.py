import tkinter as tk
from tkinter import messagebox, scrolledtext
from Classes.rsa import RSA
from Classes.hashing import SimpleHash
from data.database import Database

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Criptografia RSA")
        self.geometry("600x500")

        self.rsa = RSA()
        self.db = Database()

  
        tk.Label(self, text="Chave Pública (e, n):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.public_key_entry = tk.Entry(self, width=50, state='readonly')
        self.public_key_entry.grid(row=0, column=1, padx=10)
        self.public_key_entry.config(state='normal')
        self.public_key_entry.insert(0, str(self.rsa.public_key))
        self.public_key_entry.config(state='readonly')

        tk.Label(self, text="Chave Privada (d, n):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.private_key_entry = tk.Entry(self, width=50, state='readonly')
        self.private_key_entry.grid(row=1, column=1, padx=10)
        self.private_key_entry.config(state='normal')
        self.private_key_entry.insert(0, str(self.rsa.private_key))
        self.private_key_entry.config(state='readonly')

        tk.Label(self, text="Digite a Mensagem:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.grid(row=2, column=1, padx=10)

        
        self.encrypt_button = tk.Button(self, text="Criptografar", command=self.encrypt_message)
        self.encrypt_button.grid(row=3, column=1, pady=5)

       
        tk.Label(self, text="Mensagem Criptografada:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.encrypted_message_entry = tk.Entry(self, width=50, state='readonly')
        self.encrypted_message_entry.grid(row=4, column=1, padx=10)

       
        self.decrypt_button = tk.Button(self, text="Decriptar Última", command=self.decrypt_message)
        self.decrypt_button.grid(row=5, column=1, pady=5)

        
        tk.Label(self, text="Mensagem Decriptada:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.decrypted_message_entry = tk.Entry(self, width=50, state='readonly')
        self.decrypted_message_entry.grid(row=6, column=1, padx=10)

        
        tk.Label(self, text="Histórico de Mensagens Criptografadas e Descriptografadas:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.history_box = scrolledtext.ScrolledText(self, width=70, height=10, state='disabled')
        self.history_box.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

       
        self.load_history()

    def encrypt_message(self):
        """Criptografa a mensagem digitada e exibe o texto criptografado."""
        message = self.message_entry.get()
        if message:
            encrypted = self.rsa.encrypt(message, self.rsa.public_key)
            encrypted_str = ' '.join(map(str, encrypted))  
            hash_value = SimpleHash.hash_message(message)
            
           
            self.db.save_message(message, encrypted_str, hash_value)
            messagebox.showinfo("Encriptado", f"Mensagem encriptada: {encrypted_str}")
            
          
            self.encrypted_message_entry.config(state='normal')
            self.encrypted_message_entry.delete(0, tk.END)
            self.encrypted_message_entry.insert(0, encrypted_str)
            self.encrypted_message_entry.config(state='readonly')
            self.load_history()  
        else:
            messagebox.showwarning("Aviso", "Digite uma mensagem para encriptar!")

    def decrypt_message(self):
        """Decripta a última mensagem no banco de dados e exibe o texto original."""
        messages = self.db.get_messages()
        if messages:
            last_message = messages[-1]  
            encrypted_list = list(map(int, last_message[2].split()))  
            decrypted = self.rsa.decrypt(encrypted_list, self.rsa.private_key)
            
            
            self.decrypted_message_entry.config(state='normal')
            self.decrypted_message_entry.delete(0, tk.END)
            self.decrypted_message_entry.insert(0, decrypted)
            self.decrypted_message_entry.config(state='readonly')
            messagebox.showinfo("Decriptado", f"Mensagem decriptada: {decrypted}")
        else:
            messagebox.showwarning("Aviso", "Nenhuma mensagem para decriptar!")

    def load_history(self):
        """Carrega o histórico de mensagens criptografadas no campo de histórico."""
        self.history_box.config(state='normal')
        self.history_box.delete(1.0, tk.END) 

        messages = self.db.get_messages()
        for msg in messages:
            self.history_box.insert(tk.END, f"ID: {msg[0]}, Mensagem: {msg[1]}, Criptografada: {msg[2]}, Hash: {msg[3]}\n")
        
        self.history_box.config(state='disabled') 

    def on_closing(self):
        """Fecha a conexão com o banco de dados ao fechar a aplicação."""
        self.db.close()
        self.destroy()
