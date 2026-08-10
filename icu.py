
import importlib
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import queue
import re
from gtts import gTTS
import uuid
from playsound import playsound
import time
from IPython.display import Markdown
import os
import subprocess
import threading 
import sys
import json
import socket

# Configuration
CSV_FILE = "patient_data1.csv"
WINDOW_SIZE = 30
BG_COLOR = "#121212"      # Dark background
PANEL_COLOR = "#1e1e1e"   # Slightly lighter dark for panels
ACCENT_COLOR = "#00d4ff"  # Cyan accent

# Buffers
time_buf = deque(maxlen=WINDOW_SIZE)
hr_buf = deque(maxlen=WINDOW_SIZE)
spo2_buf = deque(maxlen=WINDOW_SIZE)
rr_buf = deque(maxlen=WINDOW_SIZE)
temp_buf = deque(maxlen=WINDOW_SIZE)
sys_buf = deque(maxlen=WINDOW_SIZE)
dia_buf = deque(maxlen=WINDOW_SIZE)

last_row = 0
play_state = True # Auto-starts

# =========================
# UI SETUP
# =========================
root = tk.Tk()
root.title("VITAL-CORE | Central Monitoring System")
root.state("zoomed")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background=BG_COLOR)



# =========================
# PRINT FUNCTION
# =========================
def print_report():
    try:
        if len(time_buf) == 0:
            messagebox.showwarning("Print Error", "No data available.")
            return

        fig_report, axs = plt.subplots(3, 2, figsize=(10, 12))
        fig_report.suptitle(f"Patient Vital Signs Report\nGenerated: {datetime.now()}", fontsize=16)

        data_map = [
            (axs[0, 0], list(hr_buf), "Heart Rate (BPM)", "red"),
            (axs[0, 1], list(spo2_buf), "SpO2 (%)", "#00d4ff"),
            (axs[1, 0], list(rr_buf), "Resp Rate", "lime"),
            (axs[1, 1], list(temp_buf), "Temp (°C)", "orange")
        ]

        for ax, data, title, color in data_map:
            ax.plot(list(time_buf), data, color=color)
            ax.set_title(title)
            ax.grid(True, alpha=0.3)

        axs[2, 0].plot(list(time_buf), list(sys_buf), color="purple", label="SYS")
        axs[2, 0].plot(list(time_buf), list(dia_buf), color="magenta", label="DIA")
        axs[2, 0].legend()
        axs[2, 0].set_title("Blood Pressure")

        fig_report.delaxes(axs[2, 1])
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        filename = f"Report_{datetime.now().strftime('%H%M%S')}.png"
        fig_report.savefig(filename)
        plt.close(fig_report)
        messagebox.showinfo("Success", f"Report saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# =========================
# TOP CONTROL BAR
# =========================
top_bar = tk.Frame(root, bg=PANEL_COLOR, height=70, relief="raised", bd=1)
top_bar.pack(fill=tk.X, side=tk.TOP)

title_label = tk.Label(top_bar, text="VITAL-CORE", font=("Verdana", 18, "bold"), bg=PANEL_COLOR, fg=ACCENT_COLOR)
title_label.pack(side=tk.LEFT, padx=20)

def toggle_play():
    global play_state
    play_state = not play_state
    play_btn.config(text="PAUSE" if play_state else "PLAY", bg="#ffc107" if play_state else "#28a745")
    if play_state:
        play_data()


def open_ecg_program():
    subprocess.Popen(["python", "ecg.py"])

# def AI_Summary():


load_dotenv() # This loads the variables from the .env file
Gemini_API_Key = os.getenv("Gemini_API_Key")
genai.configure(api_key=Gemini_API_Key)
model = genai.GenerativeModel('gemini-2.5-flash')
summary_module = importlib.import_module("AI_summary")

ai_btn = tk.Button(
    top_bar, 
    text="AI Summary", 
    font=("Arial", 10, "bold"), 
    # Pass all the required variables into the function here
    command=lambda: threading.Thread(
        target=summary_module.run_ai_analysis, 
        args=(hr_buf, spo2_buf, temp_buf, sys_buf, dia_buf, model), # Pass data here!
        daemon=True
    ).start(), 
    bg="#4CAF50", 
    fg="white", 
    width=12, 
    relief="flat"
)
ai_btn.pack(side=tk.LEFT, padx=10)

def update_data_file():
    if len(hr_buf) > 0:
        data = {
            "hr": list(hr_buf)   # 🔥 FIX HERE
        }

        with open("live_data.json", "w") as f:
            json.dump(data, f)

    root.after(500, update_data_file)

def open_ecg():
    subprocess.Popen([sys.executable, "ecg.py"])

tk.Button(top_bar, text="ECG VIEW", command=open_ecg,
          bg=ACCENT_COLOR, fg="black",
          font=("Arial", 10, "bold"), relief="flat").pack(side=tk.LEFT, padx=5)


voice_module = importlib.import_module("AI_voice_assistence")
voice_btn = tk.Button(
    top_bar, 
    text="Voice Assitence", 
    font=("Arial", 10, "bold"), 
    # Calling the function from your separate file inside a thread
    command=lambda: threading.Thread(
        target=voice_module.start_voice_assistant, 
        daemon=True
    ).start(), 
    bg="#4CAF50", 
    fg="white", 
    width=12, 
    relief="flat"
)
voice_btn.pack(side=tk.LEFT, padx=10)

timeline = tk.Scale(top_bar, from_=0, to=100, orient=tk.HORIZONTAL, length=500, 
                    bg=PANEL_COLOR, fg="white", highlightthickness=0, 
                    command=lambda x: jump_to(int(x)))
timeline.pack(side=tk.RIGHT, padx=30)

# =========================
# GRAPH AREA
# =========================
graph_frame = tk.Frame(root, bg=BG_COLOR)
graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Matplotlib Dark Theme Setup
plt.style.use('dark_background')
fig, axs = plt.subplots(3, 2, figsize=(12, 8))
fig.patch.set_facecolor(BG_COLOR)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# =========================
# LOGIC
# =========================
def jump_to(index):
    global last_row
    last_row = index
    update_graph()

def safe_int(val):
    try:
        if pd.isna(val):
            return np.nan
        return int(val)
    except:
        return np.nan

def safe_float(val):
    try:
        if pd.isna(val):
            return np.nan
        return float(val)
    except:
        return np.nan

def update_graph():
    global last_row
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty: return
    except: return

    timeline.config(to=len(df)-1)
    if last_row >= len(df): return

    row = df.iloc[last_row]
    raw_ts = str(row["Timestamp"])
    try:
        # Standard HL7: YYYYMMDDHHMMSS (14 chars) or YYYYMMDDHHMM (12 chars)
        # We take the first 12 or 14 digits to be safe
        ts_clean = raw_ts.split('.')[0] # Remove sub-seconds if they exist
        
        if len(ts_clean) >= 14:
            # Parse the string into a datetime object
            dt_obj = datetime.strptime(ts_clean[:14], "%Y%m%d%H%M%S")
            # Convert to a friendly format
            display_time = dt_obj.strftime("%H:%M:%S")
        elif len(ts_clean) >= 12:
            # Fallback if only minutes are available
            dt_obj = datetime.strptime(ts_clean[:12], "%Y%m%d%H%M")
            display_time = dt_obj.strftime("%H:%M:00")
        else:
            display_time = raw_ts
    except Exception:
        display_time = raw_ts # Fallback for non-standard formats
        
    time_buf.append(display_time)

    try:
        hr, spo2, rr, temp = safe_int(row["HR"]), safe_int(row["SpO2"]), safe_int(row["RR"]), safe_float(row["Temp"])
        try:
            sys, dia = map(int, str(row["BP"]).split("/"))
        except:
            sys, dia = np.nan, np.nan
        
        hr_buf.append(hr); spo2_buf.append(spo2); rr_buf.append(rr)
        temp_buf.append(temp); sys_buf.append(sys); dia_buf.append(dia)
    except: return

    # Plotting
    configs = [
        (axs[0,0], hr_buf, "HEART RATE", "red"),
        (axs[0,1], spo2_buf, "SpO2 %", ACCENT_COLOR),
        (axs[1,0], rr_buf, "RESPIRATION", "lime"),
        (axs[1,1], temp_buf, "TEMPERATURE", "orange")
    ]

    for ax, buf, title, col in configs:
        ax.clear()
        ax.plot(list(buf), color=col, linewidth=2)
        ax.set_title(title, fontsize=9, color="grey")
        ax.set_facecolor(PANEL_COLOR)
        
        # ADD THIS: Show only a few time labels to avoid clutter
        ticks = list(time_buf)
        if len(ticks) > 0:
            ax.set_xticks([0, len(ticks)//2, len(ticks)-1])
            ax.set_xticklabels([ticks[0], ticks[len(ticks)//2], ticks[-1]], fontsize=7)
            
        ax.grid(True, alpha=0.1)

    # Blood Pressure Plot
    axs[2,0].clear()
    axs[2,0].plot(list(sys_buf), color="#e100ff", label="SYS", linewidth=2)
    axs[2,0].plot(list(dia_buf), color="#00ffcc", label="DIA", linewidth=2)
    axs[2,0].set_facecolor(PANEL_COLOR)
    axs[2,0].set_title("BLOOD PRESSURE", fontsize=9, color="grey")
    
    # ADDED: X-Axis Time Labels
    if len(time_buf) > 0:
        indices = [0, len(time_buf)//2, len(time_buf)-1]
        labels = [list(time_buf)[i] for i in indices]
        axs[2,0].set_xticks(indices)
        axs[2,0].set_xticklabels(labels, fontsize=7, color="#888")
    
    axs[2,0].legend(prop={'size': 7}, loc="upper right")
    axs[2,0].grid(True, alpha=0.1)

    # Alert Panel
    axs[2,1].clear()
    axs[2,1].axis("off")
    axs[2,1].set_facecolor(PANEL_COLOR)
    
    alerts = []
    # if hr < 60 or hr > 100: alerts.append("⚠️ HEART RATE")
    # if spo2 < 94: alerts.append("⚠️ LOW OXYGEN")
    # if rr < 12 or rr > 20: alerts.append("⚠️ RESPIRATION")
    # if sys > 140 or dia > 90: alerts.append("⚠️ HYPERTENSION")

    BROADCAST_IP = "255.255.255.255"
    BROADCAST_IP2 = "192.168.1.255"
    PORT = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    if hr < 60 or hr > 100:
        alerts.append("Heart Rate Abnormal")

    if spo2 < 95:
        alerts.append("Low SpO2")

    if rr < 12 or rr > 20:
        alerts.append("Respiration Abnormal")

    if temp < 36 or temp > 38:
        alerts.append("Temperature Abnormal")

    if sys < 90 or sys > 140 or dia < 60 or dia > 90:
        alerts.append("Blood Pressure Abnormal")

    if alerts:
        axs[2,1].text(0.5, 0.5, "\n".join(alerts), color="#ff4444", fontsize=14, 
                      weight="bold", ha="center", va="center", bbox=dict(facecolor='black', alpha=0.5))
        msg = f"BED04 | HR:{hr} | SpO2:{spo2} | RR:{rr} | Temp:{temp} | BP:{sys}/{dia}\n" + "; ".join(alerts)
        sock.sendto(msg.encode(), (BROADCAST_IP, PORT))
        sock.sendto(msg.encode(), (BROADCAST_IP2, PORT))
        print("Broadcasted:",msg)

    else:
        axs[2,1].text(0.5, 0.5, "SYSTEMS NORMAL", color="#00ff88", fontsize=14, 
                      weight="bold", ha="center", va="center")

    canvas.draw()

def play_data():
    global last_row
    if not play_state: return
    
    try:
        df = pd.read_csv(CSV_FILE)
        if last_row < len(df)-1:
            last_row += 1
            timeline.set(last_row)
            update_graph()
    except: pass
    
    root.after(800, play_data)

    

# Start
update_graph()
play_data()
update_data_file()
root.mainloop()
