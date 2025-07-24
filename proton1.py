#!/usr/bin/env python3

import smtplib
import json
import os
import sys
import base64
from pathlib import Path

CONFIG_PATH = Path.home() / ".smsender_config"
CONTACTS_PATH = Path.home() / ".smsender_contacts.json"
SMTP_SERVER = "127.0.0.1"
SMTP_PORT = 1025

CARRIER_GATEWAYS = [
    ("AT&T", "@txt.att.net"),
    ("T-Mobile", "@tmomail.net"),
    ("Verizon", "@vtext.com"),
    ("Sprint", "@messaging.sprintpcs.com"),
    ("Boost Mobile", "@myboostmobile.com"),
    ("US Cellular", "@email.uscc.net")
]

def encode(val): return base64.b64encode(val.encode()).decode()
def decode(val): return base64.b64decode(val.encode()).decode()

def save_config():
    print("[Setup] ProtonMail Bridge configuration:")
    from_email = input("Your ProtonMail address: ").strip()
    username = input("Bridge SMTP username: ").strip()
    password = input("Bridge SMTP password: ").strip()

    config = {
        "from_email": encode(from_email),
        "username": encode(username),
        "password": encode(password)
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)
    print("[Info] Configuration saved.\n")

def load_config():
    if not CONFIG_PATH.exists():
        save_config()
    with open(CONFIG_PATH, "r") as f:
        c = json.load(f)
    return {
        "from_email": decode(c["from_email"]),
        "username": decode(c["username"]),
        "password": decode(c["password"])
    }

def load_contacts():
    if not CONTACTS_PATH.exists():
        return {}
    with open(CONTACTS_PATH, "r") as f:
        return json.load(f)

def save_contacts(contacts):
    with open(CONTACTS_PATH, "w") as f:
        json.dump(contacts, f, indent=2)

def add_contact():
    name = input("Enter nickname: ").strip().lower()
    number = input("Phone number (digits only): ").strip()
    for i, (name_c, _) in enumerate(CARRIER_GATEWAYS, 1):
        print(f"{i}. {name_c}")
    try:
        carrier_idx = int(input("Select carrier number: ")) - 1
        _, gateway = CARRIER_GATEWAYS[carrier_idx]
    except:
        print("[Error] Invalid choice.")
        return
    contacts = load_contacts()
    contacts[name] = {"number": number, "gateway": gateway}
    save_contacts(contacts)
    print(f"[Info] Contact '{name}' added.")

def list_contacts():
    contacts = load_contacts()
    if not contacts:
        print("[Info] No contacts saved.")
        return
    print("\nSaved Contacts:")
    for name, info in contacts.items():
        print(f"- {name}: {info['number']} ({info['gateway']})")

def send_sms(config, number, gateway, message):
    to_address = number + gateway
    email_message = f"Subject:\n\n{message}"
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(config["username"], config["password"])
            server.sendmail(config["from_email"], to_address, email_message)
        print(f"[Success] SMS sent to {number}")
    except Exception as e:
        print(f"[Error] Failed to send message: {e}")

def send_to_contact(config):
    contacts = load_contacts()
    if not contacts:
        print("[Info] No contacts saved.")
        return
    print("Select contact to message:")
    names = list(contacts.keys())
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")
    try:
        idx = int(input("Enter choice: ")) - 1
        selected = names[idx]
        msg = input("Type your message: ")
        contact = contacts[selected]
        send_sms(config, contact["number"], contact["gateway"], msg)
    except:
        print("[Error] Invalid selection.")

def menu():
    config = load_config()
    while True:
        print("\n=== SMSender TUI ===")
        print("1. Send SMS to a contact")
        print("2. Add a contact")
        print("3. List contacts")
        print("4. Reset ProtonMail config")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            send_to_contact(config)
        elif choice == "2":
            add_contact()
        elif choice == "3":
            list_contacts()
        elif choice == "4":
            CONFIG_PATH.unlink(missing_ok=True)
            print("[Info] Config reset.")
            save_config()
            config = load_config()
        elif choice == "5":
            print("[Exit] Goodbye.")
            break
        else:
            print("[Error] Invalid option.")

if __name__ == "__main__":
    menu()
