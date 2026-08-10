
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from datetime import datetime
from tkinter import messagebox

CSV_FILE = "patient_data.csv"
WINDOW_SIZE = 30

# buffers
time_buf = deque(maxlen=WINDOW_SIZE)
hr_buf = deque(maxlen=WINDOW_SIZE)
spo2_buf = deque(maxlen=WINDOW_SIZE)
rr_buf = deque(maxlen=WINDOW_SIZE)
temp_buf = deque(maxlen=WINDOW_SIZE)
sys_buf = deque(maxlen=WINDOW_SIZE)
dia_buf = deque(maxlen=WINDOW_SIZE)

last_row = 0
play_state = False

root = tk.Tk()
root.title("Central Monitoring System")
root.state("zoomed")


# =====================
# FIXED PRINT FUNCTION
# =====================
def print_report():
    try:
        if len(time_buf) == 0:
            messagebox.showwarning("Print Error", "No data available to print.")
            return

        # Create a dedicated figure for the PDF/PNG report
        # This avoids the "Black Image" issue by drawing a fresh set of axes
        fig_report, axs = plt.subplots(3, 2, figsize=(10, 12))
        fig_report.suptitle(f"Patient Vital Signs Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                            fontsize=16, fontweight='bold')

        # Map data to report axes
        data_map = [
            (axs[0, 0], list(hr_buf), "Heart Rate (BPM)", "red"),
            (axs[0, 1], list(spo2_buf), "SpO2 (%)", "blue"),
            (axs[1, 0], list(rr_buf), "Respiratory Rate", "green"),
            (axs[1, 1], list(temp_buf), "Temperature (°C)", "orange")
        ]

        for ax, data, title, color in data_map:
            ax.plot(list(time_buf), data, color=color, linewidth=1.5)
            ax.set_title(title)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)

        # BP (Special case for dual lines)
        axs[2, 0].plot(list(time_buf), list(sys_buf), color="purple", label="SYS")
        axs[2, 0].plot(list(time_buf), list(dia_buf), color="magenta", label="DIA")
        axs[2, 0].set_title("Blood Pressure (mmHg)")
        axs[2, 0].legend()
        axs[2, 0].tick_params(axis='x', rotation=45)

        # Remove empty subplot
        fig_report.delaxes(axs[2, 1])

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        # Save filename with timestamp
        filename = f"Report_{datetime.now().strftime('%H%M%S')}.png"
        fig_report.savefig(filename, dpi=200)
        plt.close(fig_report) # Close to free up memory
        
        messagebox.showinfo("Success", f"Report saved as: {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to print: {e}")


# ======================
# TOP CONTROL BAR
# ======================

top_bar = tk.Frame(root,bg="lightgray",height=60)
top_bar.pack(fill=tk.X)

def toggle_play():
    global play_state

    play_state = not play_state

    if play_state:
        play_btn.config(text="Pause")
        play_data()
    else:
        play_btn.config(text="Play")

play_btn = tk.Button(top_bar,text="Play",font=("Arial",12, "bold"),command=toggle_play)
tk.Button(top_bar, text="🖨 PRINT TO PNG", command=print_report, bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)

play_btn.pack(side=tk.LEFT,padx=20,pady=10)


timeline = tk.Scale(
    top_bar,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    length=800,
    label="Timeline",
    command=lambda x: jump_to(int(x))
)

timeline.pack(side=tk.LEFT,padx=20)

# ======================
# GRAPH AREA
# ======================

graph_frame = ttk.Frame(root)
graph_frame.pack(fill=tk.BOTH,expand=True)

fig, axs = plt.subplots(3,2,figsize=(12,8))

canvas = FigureCanvasTkAgg(fig,master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

# ======================
# FUNCTIONS
# ======================

def jump_to(index):
    global last_row
    last_row = index
    update_graph()

def update_graph():

    global last_row

    try:
        df = pd.read_csv(CSV_FILE)
    except:
        return

    timeline.config(to=len(df)-1)

    if last_row >= len(df):
        return

    row = df.iloc[last_row]

    time_buf.append(datetime.now())

    hr = int(row["HR"])
    spo2 = int(row["SpO2"])
    rr = int(row["RR"])
    temp = float(row["Temp"])
    sys, dia = map(int,row["BP"].split("/"))

    hr_buf.append(hr)
    spo2_buf.append(spo2)
    rr_buf.append(rr)
    temp_buf.append(temp)
    sys_buf.append(sys)
    dia_buf.append(dia)

    # HEART RATE
    axs[0,0].clear()
    axs[0,0].plot(time_buf,hr_buf)
    axs[0,0].set_title("Heart Rate")

    # SPO2
    axs[0,1].clear()
    axs[0,1].plot(time_buf,spo2_buf)
    axs[0,1].set_title("SpO₂")

    # RR
    axs[1,0].clear()
    axs[1,0].plot(time_buf,rr_buf)
    axs[1,0].set_title("Respiratory Rate")

    # TEMP
    axs[1,1].clear()
    axs[1,1].plot(time_buf,temp_buf)
    axs[1,1].set_title("Temperature")

    # BP
    axs[2,0].clear()
    axs[2,0].plot(time_buf,sys_buf,label="SYS")
    axs[2,0].plot(time_buf,dia_buf,label="DIA")
    axs[2,0].legend()
    axs[2,0].set_title("Blood Pressure")

    # ======================
    # ALERT PANEL
    # ======================

    axs[2,1].clear()
    axs[2,1].axis("off")

    alerts = []

    if hr < 60 or hr > 100:
        alerts.append("Heart Rate Abnormal")

    if spo2 < 94:
        alerts.append("Low SpO₂")

    if rr < 12 or rr > 20:
        alerts.append("Respiration Abnormal")

    if temp < 36 or temp > 38:
        alerts.append("Temperature Abnormal")

    if sys < 90 or sys > 140 or dia < 60 or dia > 90:
        alerts.append("Blood Pressure Abnormal")

    if alerts:
        alert_text = "ALERTS\n\n" + "\n".join(alerts)
        axs[2,1].text(
            0.05,0.9,
            alert_text,
            fontsize=14,
            color="red",
            verticalalignment="top"
        )
    else:
        axs[2,1].text(
            0.25,0.5,
            "All vitals normal",
            fontsize=14,
            color="green"
        )

    canvas.draw()

def play_data():

    global last_row

    if not play_state:
        return

    try:
        df = pd.read_csv(CSV_FILE)
    except:
        return

    if last_row < len(df)-1:

        last_row += 1

        timeline.set(last_row)

        update_graph()

        root.after(500,play_data)

update_graph()

root.mainloop()
