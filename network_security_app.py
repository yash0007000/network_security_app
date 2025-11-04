import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import random
import string
import subprocess
import requests
from urllib.parse import urlparse
import sys

# --------------------------
# PASSWORD MANAGER
# --------------------------
def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except:
        passwords = {}
    return passwords

def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

def add_password():
    website = simpledialog.askstring("Website", "Enter website:")
    if not website:
        return
    username = simpledialog.askstring("Username", "Enter username:")
    if not username:
        return
    choice = messagebox.askyesno("Password", "Generate random password?")
    if choice:
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(chars) for i in range(10))
    else:
        password = simpledialog.askstring("Password", "Enter password:", show="*")
    passwords[website] = {"username": username, "password": password}
    save_passwords(passwords)
    messagebox.showinfo("Saved", "Password saved!")

def view_passwords():
    passwords = load_passwords()
    if not passwords:
        messagebox.showinfo("Passwords", "No passwords saved")
        return
    result = ""
    for site in passwords:
        result += f"Website: {site}\nUsername: {passwords[site]['username']}\nPassword: {passwords[site]['password']}\n\n"
    messagebox.showinfo("Saved Passwords", result)

def search_password():
    website = simpledialog.askstring("Search", "Enter website to search:")
    if not website:
        return
    passwords = load_passwords()
    if website in passwords:
        data = passwords[website]
        messagebox.showinfo("Found", f"Website: {website}\nUsername: {data['username']}\nPassword: {data['password']}")
    else:
        messagebox.showinfo("Not Found", "Password not found")

# --------------------------
# FIREWALL CHECKER
# --------------------------
firewall_rules = [
    {"ip": "192.168.1.100", "port": 80, "action": "allow"},
    {"ip": "192.168.1.200", "port": 22, "action": "allow"},
    {"ip": "0.0.0.0", "port": 0, "action": "block"}
]

def check_firewall():
    ip = simpledialog.askstring("IP", "Enter IP address:")
    port = simpledialog.askinteger("Port", "Enter port:")
    action = "block"
    for rule in firewall_rules:
        if rule["ip"] == ip and rule["port"] == port:
            action = rule["action"]
            break
    messagebox.showinfo("Result", f"The IP {ip}:{port} is {action.upper()}.")

# --------------------------
# URL SCANNER
# --------------------------
def scan_url():
    url = simpledialog.askstring("URL", "Enter URL (http:// or https://):")
    if not url:
        return
    if urlparse(url).scheme == "https":
        result = "URL uses HTTPS.\n"
        try:
            r = requests.head(url, timeout=5)
            if r.status_code < 400:
                result += "SSL certificate seems OK.\n"
            else:
                result += "SSL certificate may not be valid.\n"
        except:
            result += "Could not check SSL.\n"
    else:
        result = "URL does not use HTTPS.\n"
    harmful_words = ["phishing","malware","spam","fraud","attack","danger"]
    if any(word in url.lower() for word in harmful_words):
        result += "This URL may be harmful!"
    else:
        result += "URL seems safe."
    messagebox.showinfo("Scan Result", result)

# --------------------------
# WIFI PASSWORD RETRIEVER
# --------------------------
def get_wifi_password():
    if not sys.platform.startswith("win"):
        messagebox.showinfo("Error", "Only works on Windows")
        return
    ssid = simpledialog.askstring("SSID", "Enter Wi-Fi SSID:")
    if not ssid:
        return
    try:
        command = f'netsh wlan show profile name="{ssid}" key=clear'
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        for line in output.splitlines():
            if "Key Content" in line:
                pwd = line.split(":")[1].strip()
                messagebox.showinfo("Wi-Fi Password", f"Password for {ssid}: {pwd}")
                return
        messagebox.showinfo("Wi-Fi Password", "Password not found")
    except:
        messagebox.showinfo("Error", "SSID not found or error")

# --------------------------
# MAIN GUI
# --------------------------
passwords = load_passwords()

root = tk.Tk()
root.title("Security Toolkit")
root.geometry("400x400")

tk.Label(root, text="Security Toolkit", font=("Arial",16,"bold")).pack(pady=10)

tk.Button(root, text="Add Password", width=20, command=add_password).pack(pady=5)
tk.Button(root, text="View Passwords", width=20, command=view_passwords).pack(pady=5)
tk.Button(root, text="Search Password", width=20, command=search_password).pack(pady=5)

tk.Button(root, text="Check Firewall", width=20, command=check_firewall).pack(pady=10)
tk.Button(root, text="Scan URL", width=20, command=scan_url).pack(pady=10)
tk.Button(root, text="Get Wi-Fi Password", width=20, command=get_wifi_password).pack(pady=10)

root.mainloop()
