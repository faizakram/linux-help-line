
# 🔐 Secure SSH Setup — Complete Guide

## 1. Install OpenSSH Server (on the server)

**Ubuntu/Debian**  
```bash
sudo apt update  
sudo apt install -y openssh-server  
sudo systemctl enable --now ssh
```

**RHEL / Rocky / Alma**  
```bash
sudo dnf install -y openssh-server  
sudo systemctl enable --now sshd
```

Check status:  
```bash
systemctl status ssh    # Ubuntu/Debian  
systemctl status sshd   # RHEL
```

✅ Should say active (running).

---

## 2. Create a Non-Root User

```bash
sudo adduser faiz
```

**OR on RHEL:**  
```bash
# sudo useradd -m -s /bin/bash faiz && sudo passwd faiz
```

### Optional: Give sudo rights:

**Ubuntu/Debian:**  
```bash
sudo usermod -aG sudo faiz
```

**RHEL:**  
```bash
sudo usermod -aG wheel faiz
```

---

## 3. Generate SSH Key on Client (laptop/workstation)

### Naming convention:
`id_ed25519_<username>_<servername>`

**Example** (user = faiz, server = server1):
```bash
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519_faiz_server1 -C "faiz@server1"
```

Creates:
- `~/.ssh/id_ed25519_faiz_server1` (private key)
- `~/.ssh/id_ed25519_faiz_server1.pub` (public key)

---

## 4. Copy Public Key to Server

### Preferred (if `ssh-copy-id` is available):
```bash
ssh-copy-id -i ~/.ssh/id_ed25519_faiz_server1.pub faiz@192.168.1.3
```

### Manual method:
```bash
cat ~/.ssh/id_ed25519_faiz_server1.pub | ssh faiz@192.168.1.3 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

---

## 5. Configure SSH Server for Key-Only Login

Edit server config:
```bash
sudo nano /etc/ssh/sshd_config
```

Ensure:
```plaintext
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PermitRootLogin no
```

Reload service:
```bash
sudo systemctl reload ssh   # Ubuntu  
sudo systemctl reload sshd  # RHEL
```

---

## 6. Client Convenience — ~/.ssh/config

On the client, create:
```bash
nano ~/.ssh/config
```

Example for domain + LAN IP:

### Public access (via domain):
```plaintext
Host esparks
  HostName esparksit.com
  User faiz
  IdentityFile ~/.ssh/id_ed25519_faiz_server1
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 2
  HashKnownHosts yes
  UpdateHostKeys yes
```

### LAN access (via local IP):
```plaintext
Host esparks-lan
  HostName 192.168.1.3
  User faiz
  IdentityFile ~/.ssh/id_ed25519_faiz_server1
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 2
  HashKnownHosts yes
  UpdateHostKeys yes
```

Set permissions:
```bash
chmod 600 ~/.ssh/config
```

---

## 7. Test Connection

From client:
```bash
ssh esparks        # connects via esparksit.com  
ssh esparks-lan    # connects via LAN
```

If you want verbose debug:
```bash
ssh -vvv esparks
```

---

## 8. Pre-Seed Known Hosts (optional)

To avoid host key prompts:
```bash
ssh-keyscan -t ed25519 esparksit.com >> ~/.ssh/known_hosts  
ssh-keyscan -t ed25519 192.168.1.3   >> ~/.ssh/known_hosts
```

---

## 9. Firewall & Brute-Force Protection

**UFW (Ubuntu/Debian):**
```bash
sudo apt install -y ufw  
sudo ufw allow OpenSSH  
sudo ufw enable
```

**Firewalld (RHEL):**
```bash
sudo firewall-cmd --permanent --add-service=ssh  
sudo firewall-cmd --reload
```

**Fail2Ban (both):**
```bash
sudo apt install -y fail2ban || sudo dnf install -y fail2ban  
sudo systemctl enable --now fail2ban
```

---

## 🔎 Example: Full Workflow

**Server:** Installed OpenSSH, created user faiz.  
**Client:** Generated key `~/.ssh/id_ed25519_faiz_server1` and `~/.ssh/id_ed25519_faiz_server1.pub`.  
Copied key to server with `ssh-copy-id`.  
Configured `/etc/ssh/sshd_config` to disallow passwords.  
Added `~/.ssh/config` entries for `esparks` and `esparks-lan`.  
Connected with:
```bash
ssh esparks  
ssh esparks-lan
```

---

## ✅ Recap

- Keys are unique per user/server → `id_ed25519_<username>_<servername>`
- Server accepts only keys, no passwords.
- Client has simple aliases in `~/.ssh/config`.
- Firewall and Fail2Ban block brute-force attempts.
- Both LAN IP and public domain access are configured.

👉 Do you want me to save this guide into a PDF or Markdown file so you can keep it as a reference document?