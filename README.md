# proton
# Proton SMS CLI

<img width="1024" height="1024" alt="psc" src="https://github.com/user-attachments/assets/199b4b4f-cb58-44fd-9941-5df6cfb1d1f7" />

Send free SMS messages via your ProtonMail account using the ProtonMail Bridge and CLI Python tool.

## Features
- TUI interface (menu-driven)
- Contact nicknames
- ProtonMail Bridge integration (no third-party APIs)
- Config and contacts stored locally
- Free, private, and open source

## Requirements

- Python 3
- ProtonMail Bridge (GUI or CLI)
- Linux (tested on Arch)
- ProtonMail account

## Installation (Arch Linux)

```bash
sudo pacman -S protonmail-bridge
Or get the .deb from proton.me and convert using debtap.

Usage

python3 proton.py

You'll be prompted to enter your ProtonMail Bridge SMTP credentials once, and it will be saved securely (base64).
Reset Credentials

rm ~/.smsender_config

License

MIT License


---

## ✅ Step 5: Add `LICENSE` (MIT Recommended)

```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy...
[standard MIT text continues]
EOF
