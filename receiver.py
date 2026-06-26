# # import socket
# # import tkinter as tk
# # from threading import Thread

# # # Network Config
# # PORT = 5005

# # class HospitalDashboard:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Hospital Alert System - Ward A")
# #         self.root.geometry("600x400")
        
# #         # UI Elements
# #         self.status_label = tk.Label(root, text="SYSTEM NORMAL", font=("Arial", 30), bg="green", fg="white")
# #         self.status_label.pack(expand=True, fill="both")
        
# #         self.message_label = tk.Label(root, text="Waiting for data...", font=("Arial", 14))
# #         self.message_label.pack(pady=20)

# #         # Start the background listener thread
# #         self.listener_thread = Thread(target=self.listen_for_alerts, daemon=True)
# #         self.listener_thread.start()

# #     def listen_for_alerts(self):
# #         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #         sock.bind(("0.0.0.0", PORT))
        
# #         while True:
# #             data, addr = sock.recvfrom(1024)
# #             message = data.decode()
# #             # Update the UI from the background thread
# #             self.root.after(0, self.trigger_alert, message, addr)

# #     def trigger_alert(self, message, addr):
# #         self.status_label.config(text="🚨 EMERGENCY 🚨", bg="red")
# #         self.message_label.config(text=f"From {addr}: {message}")
# #         # Automatically reset after 5 seconds
# #         self.root.after(5000, self.reset_status)

# #     def reset_status(self):
# #         self.status_label.config(text="SYSTEM NORMAL", bg="green")

# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = HospitalDashboard(root)
# #     root.mainloop()

# # import socket
# # import tkinter as tk
# # from threading import Thread
# # import winsound

# # PORT = 5005

# # class HospitalDashboard:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Hospital Alert System - Ward A")
# #         self.root.geometry("600x400")

# #         self.flash = False

# #         # UI
# #         self.status_label = tk.Label(
# #             root, text="SYSTEM NORMAL",
# #             font=("Arial", 30), bg="green", fg="white"
# #         )
# #         self.status_label.pack(expand=True, fill="both")

# #         self.message_label = tk.Label(
# #             root, text="Waiting for data...",
# #             font=("Arial", 14)
# #         )
# #         self.message_label.pack(pady=20)

# #         # Start listening thread
# #         self.listener_thread = Thread(target=self.listen_for_alerts, daemon=True)
# #         self.listener_thread.start()

# #     def listen_for_alerts(self):
# #         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #         sock.bind(("0.0.0.0", PORT))

# #         while True:
# #             data, addr = sock.recvfrom(1024)
# #             message = data.decode()

# #             self.root.after(0, self.trigger_alert, message, addr)

# #     def trigger_alert(self, message, addr):

# #         # 🔊 Alarm sound
# #         winsound.Beep(2000, 500)

# #         self.status_label.config(text="🚨 EMERGENCY 🚨")
# #         self.message_label.config(text=f"From {addr}: {message}")

# #         self.flash_alert()

# #         self.root.after(5000, self.reset_status)

# #     def flash_alert(self):

# #         if self.flash:
# #             self.status_label.config(bg="red")
# #         else:
# #             self.status_label.config(bg="darkred")

# #         self.flash = not self.flash
# #         self.root.after(500, self.flash_alert)

# #     def reset_status(self):
# #         self.status_label.config(text="SYSTEM NORMAL", bg="green")
# #         self.message_label.config(text="Waiting for data...")
# #         self.flash = False


# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = HospitalDashboard(root)
# #     root.mainloop()

# import socket
# import tkinter as tk
# from threading import Thread, Lock
# import winsound

# PORT = 5005

# class HospitalDashboard:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Hospital Alert System")
#         self.root.geometry("600x400")
        
#         self.flash_job = None
#         self.reset_job = None
#         self.lock = Lock() # Prevents multiple threads from hitting the UI at once

#         # UI Elements
#         self.status_label = tk.Label(root, text="SYSTEM NORMAL", font=("Arial", 30), bg="green", fg="white")
#         self.status_label.pack(expand=True, fill="both")
#         self.message_label = tk.Label(root, text="Waiting for data...", font=("Arial", 14))
#         self.message_label.pack(pady=20)

#         # Start listening
#         Thread(target=self.listen_for_alerts, daemon=True).start()

#     def listen_for_alerts(self):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.bind(("0.0.0.0", PORT))
#         while True:
#             data, addr = sock.recvfrom(1024)
#             msg = data.decode()
#             # Use .after to ensure UI changes happen on the Main Thread
#             self.root.after(0, self.trigger_alert, msg, addr)

#     def trigger_alert(self, message, addr):
#         with self.lock:
#             # 1. Beep immediately
#             winsound.Beep(2000, 200)

#             # 2. Cancel ANY pending resets or flashes to "start fresh"
#             if self.reset_job:
#                 self.root.after_cancel(self.reset_job)
#             if self.flash_job:
#                 self.root.after_cancel(self.flash_job)
#                 self.flash_job = None

#             # 3. Update Text
#             self.status_label.config(text="🚨 EMERGENCY 🚨", bg="red")
#             self.message_label.config(text=f"From {addr[0]}: {message}")

#             # 4. Start Flashing and Schedule Reset (5 seconds)
#             self.flash_alert(True)
#             self.reset_job = self.root.after(2000, self.reset_status)

#     def flash_alert(self, is_red):
#         color = "red" 
#         self.status_label.config(bg=color)
#         # Schedule next flash toggle in 500ms
#         self.flash_job = self.root.after(500, self.flash_alert, not is_red)

#     def reset_status(self):
#         with self.lock:
#             if self.flash_job:
#                 self.root.after_cancel(self.flash_job)
#                 self.flash_job = None
            
#             self.status_label.config(text="SYSTEM NORMAL", bg="green")
#             self.message_label.config(text="Patient is OK. Do not worry")
#             self.reset_job = None

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = HospitalDashboard(root)
#     root.mainloop()

import socket
import tkinter as tk
from threading import Thread
import winsound

PORT = 5005

class Dashboard:

    def __init__(self,root):

        self.root = root

        root.title("Hospital Alert System")
        root.geometry("600x400")

        self.status = tk.Label(root,text="SYSTEM NORMAL",font=("Arial",30),bg="green",fg="white")
        self.status.pack(fill="both",expand=True)

        self.msg = tk.Label(root,text="Waiting for alerts",font=("Arial",14))
        self.msg.pack(pady=20)

        Thread(target=self.listen,daemon=True).start()

    def listen(self):

        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0",PORT))

        while True:

            data,addr = sock.recvfrom(1024)

            message = data.decode()

            self.root.after(0,self.trigger,message)

    def trigger(self,message):

        winsound.Beep(2000,200)

        self.status.config(text="🚨 EMERGENCY 🚨",bg="red")

        self.msg.config(text=message)

        self.root.after(4000,self.reset)

    def reset(self):

        self.status.config(text="SYSTEM NORMAL",bg="green")

        self.msg.config(text="Patient OK")

root = tk.Tk()
Dashboard(root)
root.mainloop()