## ✅ **What Da Nerkh Bot – Systemd Notes**

### **1. Systemd service file location**

* **Path:** `/etc/systemd/system/whatdanerkhbot.service`
* To edit:

```bash
sudo nano /etc/systemd/system/whatdanerkhbot.service
```

Inside, it should look like:

```
[Unit]
Description=What Da Nerkh Telegram Bot
After=network.target

....

[Install]
WantedBy=multi-user.target
```

---

### **2. Basic Commands**

| Action                      | Command                                 |
| --------------------------- | --------------------------------------- |
| **Start the bot**           | `sudo systemctl start whatdanerkhbot`   |
| **Stop the bot**            | `sudo systemctl stop whatdanerkhbot`    |
| **Restart (after updates)** | `sudo systemctl restart whatdanerkhbot` |
| **Check if running**        | `sudo systemctl status whatdanerkhbot`  |

---

### **3. Logs**

* **Live logs (follow):**

```bash
journalctl -u whatdanerkhbot -f
```

* **Full logs (scroll):**

```bash
journalctl -u whatdanerkhbot
```

Press `Ctrl+C` to exit logs.

---

### **4. After Editing Service File**

If you ever change the `.service` file:

```bash
sudo systemctl daemon-reexec
sudo systemctl restart whatdanerkhbot
```
