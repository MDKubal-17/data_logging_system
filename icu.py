# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
# import matplotlib.dates as mdates

# # ----------------------
# # Load CSV
# # ----------------------
# df = pd.read_csv("patient_data.csv")

# # Convert timestamp
# df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y%m%d%H%M%S")

# # Split BP
# df[["SYS","DIA"]] = df["BP"].str.split("/", expand=True).astype(int)

# WINDOW = 20   # points visible
# index_pointer = 1
# running = True


# # ----------------------
# # Tkinter Window
# # ----------------------
# root = tk.Tk()
# root.title("Patient Monitor")

# # FULLSCREEN
# root.state("zoomed")


# # ----------------------
# # Matplotlib Figure
# # ----------------------
# fig, axs = plt.subplots(3,2, figsize=(12,7))

# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# # ----------------------
# # Graph Update
# # ----------------------
# def draw_graph(index):

#     index = int(index)

#     start = max(0, index-WINDOW)
#     data = df.iloc[start:index]

#     for ax in axs.flat:
#         ax.clear()

#     axs[0,0].plot(data["Timestamp"], data["HR"], color="red")
#     axs[0,0].set_title("Heart Rate")

#     axs[0,1].plot(data["Timestamp"], data["SpO2"], color="blue")
#     axs[0,1].set_title("SpO2")

#     axs[1,0].plot(data["Timestamp"], data["RR"], color="green")
#     axs[1,0].set_title("Respiratory Rate")

#     axs[1,1].plot(data["Timestamp"], data["Temp"], color="orange")
#     axs[1,1].set_title("Temperature")

#     axs[2,0].plot(data["Timestamp"], data["SYS"], label="SYS")
#     axs[2,0].plot(data["Timestamp"], data["DIA"], label="DIA")
#     axs[2,0].legend()
#     axs[2,0].set_title("Blood Pressure")

#     axs[2,1].axis("off")

#     for ax in axs.flat:
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
#         ax.tick_params(axis='x', rotation=30)

#     canvas.draw()


# # ----------------------
# # Slider Control
# # ----------------------
# def slider_update(val):
#     global running
#     running = False
#     draw_graph(val)

# slider = tk.Scale(
#     root,
#     from_=1,
#     to=len(df),
#     orient="horizontal",
#     length=1200,
#     label="Timeline Scroll (Doctor can go back anytime)",
#     command=slider_update
# )

# slider.pack(pady=10)

# slider.set(1)


# # ----------------------
# # Real Time Simulation
# # ----------------------
# def realtime():

#     global index_pointer, running

#     if running:

#         if index_pointer < len(df):

#             slider.set(index_pointer)
#             draw_graph(index_pointer)

#             index_pointer += 1

#     root.after(1000, realtime)   # 1 sec update


# # ----------------------
# # Resume Live Button
# # ----------------------
# def resume_live():
#     global running
#     running = True


# live_button = tk.Button(root, text="Resume Live Monitoring", command=resume_live)
# live_button.pack()


# # ----------------------
# # Start
# # ----------------------
# realtime()

# root.mainloop()





# import tkinter as tk
# from tkinter import ttk
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from collections import deque
# from datetime import datetime

# CSV_FILE = "patient_data.csv"
# WINDOW_SIZE = 30

# # buffers
# time_buf = deque(maxlen=WINDOW_SIZE)
# hr_buf = deque(maxlen=WINDOW_SIZE)
# spo2_buf = deque(maxlen=WINDOW_SIZE)
# rr_buf = deque(maxlen=WINDOW_SIZE)
# temp_buf = deque(maxlen=WINDOW_SIZE)
# sys_buf = deque(maxlen=WINDOW_SIZE)
# dia_buf = deque(maxlen=WINDOW_SIZE)

# last_row = 0
# play_state = False

# root = tk.Tk()
# root.title("Central Monitoring System")
# root.state("zoomed")

# # ======================
# # TOP CONTROL BAR
# # ======================

# top_bar = tk.Frame(root,bg="lightgray",height=60)
# top_bar.pack(fill=tk.X)

# def toggle_play():
#     global play_state

#     play_state = not play_state

#     if play_state:
#         play_btn.config(text="Pause")
#         play_data()
#     else:
#         play_btn.config(text="Play")

# play_btn = tk.Button(top_bar,text="Play",font=("Arial",12),command=toggle_play)
# play_btn.pack(side=tk.LEFT,padx=20,pady=10)

# timeline = tk.Scale(
#     top_bar,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=800,
#     label="Timeline",
#     command=lambda x: jump_to(int(x))
# )

# timeline.pack(side=tk.LEFT,padx=20)

# # ======================
# # GRAPH AREA
# # ======================

# graph_frame = ttk.Frame(root)
# graph_frame.pack(fill=tk.BOTH,expand=True)

# fig, axs = plt.subplots(3,2,figsize=(12,8))

# canvas = FigureCanvasTkAgg(fig,master=graph_frame)
# canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

# # ======================
# # FUNCTIONS
# # ======================

# def jump_to(index):
#     global last_row
#     last_row = index
#     update_graph()

# def update_graph():

#     global last_row

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     timeline.config(to=len(df)-1)

#     if last_row >= len(df):
#         return

#     row = df.iloc[last_row]

#     time_buf.append(datetime.now())

#     hr = int(row["HR"])
#     spo2 = int(row["SpO2"])
#     rr = int(row["RR"])
#     temp = float(row["Temp"])
#     sys, dia = map(int,row["BP"].split("/"))

#     hr_buf.append(hr)
#     spo2_buf.append(spo2)
#     rr_buf.append(rr)
#     temp_buf.append(temp)
#     sys_buf.append(sys)
#     dia_buf.append(dia)

#     # HEART RATE
#     axs[0,0].clear()
#     axs[0,0].plot(time_buf,hr_buf)
#     axs[0,0].set_title("Heart Rate")

#     # SPO2
#     axs[0,1].clear()
#     axs[0,1].plot(time_buf,spo2_buf)
#     axs[0,1].set_title("SpO₂")

#     # RR
#     axs[1,0].clear()
#     axs[1,0].plot(time_buf,rr_buf)
#     axs[1,0].set_title("Respiratory Rate")

#     # TEMP
#     axs[1,1].clear()
#     axs[1,1].plot(time_buf,temp_buf)
#     axs[1,1].set_title("Temperature")

#     # BP
#     axs[2,0].clear()
#     axs[2,0].plot(time_buf,sys_buf,label="SYS")
#     axs[2,0].plot(time_buf,dia_buf,label="DIA")
#     axs[2,0].legend()
#     axs[2,0].set_title("Blood Pressure")

#     canvas.draw()

# def play_data():

#     global last_row

#     if not play_state:
#         return

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     if last_row < len(df)-1:

#         last_row += 1

#         timeline.set(last_row)

#         update_graph()

#         root.after(500,play_data)

# update_graph()

# root.mainloop()


# import tkinter as tk
# from tkinter import ttk
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from collections import deque
# from datetime import datetime
# from tkinter import messagebox

# CSV_FILE = "patient_data.csv"
# WINDOW_SIZE = 30

# # buffers
# time_buf = deque(maxlen=WINDOW_SIZE)
# hr_buf = deque(maxlen=WINDOW_SIZE)
# spo2_buf = deque(maxlen=WINDOW_SIZE)
# rr_buf = deque(maxlen=WINDOW_SIZE)
# temp_buf = deque(maxlen=WINDOW_SIZE)
# sys_buf = deque(maxlen=WINDOW_SIZE)
# dia_buf = deque(maxlen=WINDOW_SIZE)

# last_row = 0
# play_state = False

# root = tk.Tk()
# root.title("Central Monitoring System")
# root.state("zoomed")


# # =====================
# # FIXED PRINT FUNCTION
# # =====================
# def print_report():
#     try:
#         if len(time_buf) == 0:
#             messagebox.showwarning("Print Error", "No data available to print.")
#             return

#         # Create a dedicated figure for the PDF/PNG report
#         # This avoids the "Black Image" issue by drawing a fresh set of axes
#         fig_report, axs = plt.subplots(3, 2, figsize=(10, 12))
#         fig_report.suptitle(f"Patient Vital Signs Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
#                             fontsize=16, fontweight='bold')

#         # Map data to report axes
#         data_map = [
#             (axs[0, 0], list(hr_buf), "Heart Rate (BPM)", "red"),
#             (axs[0, 1], list(spo2_buf), "SpO2 (%)", "blue"),
#             (axs[1, 0], list(rr_buf), "Respiratory Rate", "green"),
#             (axs[1, 1], list(temp_buf), "Temperature (°C)", "orange")
#         ]

#         for ax, data, title, color in data_map:
#             ax.plot(list(time_buf), data, color=color, linewidth=1.5)
#             ax.set_title(title)
#             ax.tick_params(axis='x', rotation=45)
#             ax.grid(True, alpha=0.3)

#         # BP (Special case for dual lines)
#         axs[2, 0].plot(list(time_buf), list(sys_buf), color="purple", label="SYS")
#         axs[2, 0].plot(list(time_buf), list(dia_buf), color="magenta", label="DIA")
#         axs[2, 0].set_title("Blood Pressure (mmHg)")
#         axs[2, 0].legend()
#         axs[2, 0].tick_params(axis='x', rotation=45)

#         # Remove empty subplot
#         fig_report.delaxes(axs[2, 1])

#         plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
#         # Save filename with timestamp
#         filename = f"Report_{datetime.now().strftime('%H%M%S')}.png"
#         fig_report.savefig(filename, dpi=200)
#         plt.close(fig_report) # Close to free up memory
        
#         messagebox.showinfo("Success", f"Report saved as: {filename}")
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to print: {e}")


# # ======================
# # TOP CONTROL BAR
# # ======================

# top_bar = tk.Frame(root,bg="lightgray",height=60)
# top_bar.pack(fill=tk.X)

# def toggle_play():
#     global play_state

#     play_state = not play_state

#     if play_state:
#         play_btn.config(text="Pause")
#         play_data()
#     else:
#         play_btn.config(text="Play")

# play_btn = tk.Button(top_bar,text="Play",font=("Arial",12, "bold"),command=toggle_play)
# tk.Button(top_bar, text="🖨 PRINT TO PNG", command=print_report, bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)

# play_btn.pack(side=tk.LEFT,padx=20,pady=10)


# timeline = tk.Scale(
#     top_bar,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=800,
#     label="Timeline",
#     command=lambda x: jump_to(int(x))
# )

# timeline.pack(side=tk.LEFT,padx=20)

# # ======================
# # GRAPH AREA
# # ======================

# graph_frame = ttk.Frame(root)
# graph_frame.pack(fill=tk.BOTH,expand=True)

# fig, axs = plt.subplots(3,2,figsize=(12,8))

# canvas = FigureCanvasTkAgg(fig,master=graph_frame)
# canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

# # ======================
# # FUNCTIONS
# # ======================

# def jump_to(index):
#     global last_row
#     last_row = index
#     update_graph()

# def update_graph():

#     global last_row

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     timeline.config(to=len(df)-1)

#     if last_row >= len(df):
#         return

#     row = df.iloc[last_row]

#     time_buf.append(datetime.now())

#     hr = int(row["HR"])
#     spo2 = int(row["SpO2"])
#     rr = int(row["RR"])
#     temp = float(row["Temp"])
#     sys, dia = map(int,row["BP"].split("/"))

#     hr_buf.append(hr)
#     spo2_buf.append(spo2)
#     rr_buf.append(rr)
#     temp_buf.append(temp)
#     sys_buf.append(sys)
#     dia_buf.append(dia)

#     # HEART RATE
#     axs[0,0].clear()
#     axs[0,0].plot(time_buf,hr_buf)
#     axs[0,0].set_title("Heart Rate")

#     # SPO2
#     axs[0,1].clear()
#     axs[0,1].plot(time_buf,spo2_buf)
#     axs[0,1].set_title("SpO₂")

#     # RR
#     axs[1,0].clear()
#     axs[1,0].plot(time_buf,rr_buf)
#     axs[1,0].set_title("Respiratory Rate")

#     # TEMP
#     axs[1,1].clear()
#     axs[1,1].plot(time_buf,temp_buf)
#     axs[1,1].set_title("Temperature")

#     # BP
#     axs[2,0].clear()
#     axs[2,0].plot(time_buf,sys_buf,label="SYS")
#     axs[2,0].plot(time_buf,dia_buf,label="DIA")
#     axs[2,0].legend()
#     axs[2,0].set_title("Blood Pressure")

#     # ======================
#     # ALERT PANEL
#     # ======================

#     axs[2,1].clear()
#     axs[2,1].axis("off")

#     alerts = []

#     if hr < 60 or hr > 100:
#         alerts.append("Heart Rate Abnormal")

#     if spo2 < 94:
#         alerts.append("Low SpO₂")

#     if rr < 12 or rr > 20:
#         alerts.append("Respiration Abnormal")

#     if temp < 36 or temp > 38:
#         alerts.append("Temperature Abnormal")

#     if sys < 90 or sys > 140 or dia < 60 or dia > 90:
#         alerts.append("Blood Pressure Abnormal")

#     if alerts:
#         alert_text = "ALERTS\n\n" + "\n".join(alerts)
#         axs[2,1].text(
#             0.05,0.9,
#             alert_text,
#             fontsize=14,
#             color="red",
#             verticalalignment="top"
#         )
#     else:
#         axs[2,1].text(
#             0.25,0.5,
#             "All vitals normal",
#             fontsize=14,
#             color="green"
#         )

#     canvas.draw()

# def play_data():

#     global last_row

#     if not play_state:
#         return

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     if last_row < len(df)-1:

#         last_row += 1

#         timeline.set(last_row)

#         update_graph()

#         root.after(500,play_data)

# update_graph()

# root.mainloop()




# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
# import matplotlib.dates as mdates

# # ----------------------
# # Load CSV
# # ----------------------
# df = pd.read_csv("patient_data.csv")

# # Convert timestamp
# df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y%m%d%H%M%S")

# # Split BP
# df[["SYS","DIA"]] = df["BP"].str.split("/", expand=True).astype(int)

# WINDOW = 20   # points visible
# index_pointer = 1
# running = True


# # ----------------------
# # Tkinter Window
# # ----------------------
# root = tk.Tk()
# root.title("Patient Monitor")

# # FULLSCREEN
# root.state("zoomed")


# # ----------------------
# # Matplotlib Figure
# # ----------------------
# fig, axs = plt.subplots(3,2, figsize=(12,7))

# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# # ----------------------
# # Graph Update
# # ----------------------
# def draw_graph(index):

#     index = int(index)

#     start = max(0, index-WINDOW)
#     data = df.iloc[start:index]

#     for ax in axs.flat:
#         ax.clear()

#     axs[0,0].plot(data["Timestamp"], data["HR"], color="red")
#     axs[0,0].set_title("Heart Rate")

#     axs[0,1].plot(data["Timestamp"], data["SpO2"], color="blue")
#     axs[0,1].set_title("SpO2")

#     axs[1,0].plot(data["Timestamp"], data["RR"], color="green")
#     axs[1,0].set_title("Respiratory Rate")

#     axs[1,1].plot(data["Timestamp"], data["Temp"], color="orange")
#     axs[1,1].set_title("Temperature")

#     axs[2,0].plot(data["Timestamp"], data["SYS"], label="SYS")
#     axs[2,0].plot(data["Timestamp"], data["DIA"], label="DIA")
#     axs[2,0].legend()
#     axs[2,0].set_title("Blood Pressure")

#     axs[2,1].axis("off")

#     for ax in axs.flat:
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
#         ax.tick_params(axis='x', rotation=30)

#     canvas.draw()


# # ----------------------
# # Slider Control
# # ----------------------
# def slider_update(val):
#     global running
#     running = False
#     draw_graph(val)

# slider = tk.Scale(
#     root,
#     from_=1,
#     to=len(df),
#     orient="horizontal",
#     length=1200,
#     label="Timeline Scroll (Doctor can go back anytime)",
#     command=slider_update
# )

# slider.pack(pady=10)

# slider.set(1)


# # ----------------------
# # Real Time Simulation
# # ----------------------
# def realtime():

#     global index_pointer, running

#     if running:

#         if index_pointer < len(df):

#             slider.set(index_pointer)
#             draw_graph(index_pointer)

#             index_pointer += 1

#     root.after(1000, realtime)   # 1 sec update


# # ----------------------
# # Resume Live Button
# # ----------------------
# def resume_live():
#     global running
#     running = True


# live_button = tk.Button(root, text="Resume Live Monitoring", command=resume_live)
# live_button.pack()


# # ----------------------
# # Start
# # ----------------------
# realtime()

# root.mainloop()





# import tkinter as tk
# from tkinter import ttk
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from collections import deque
# from datetime import datetime

# CSV_FILE = "patient_data.csv"
# WINDOW_SIZE = 30

# # buffers
# time_buf = deque(maxlen=WINDOW_SIZE)
# hr_buf = deque(maxlen=WINDOW_SIZE)
# spo2_buf = deque(maxlen=WINDOW_SIZE)
# rr_buf = deque(maxlen=WINDOW_SIZE)
# temp_buf = deque(maxlen=WINDOW_SIZE)
# sys_buf = deque(maxlen=WINDOW_SIZE)
# dia_buf = deque(maxlen=WINDOW_SIZE)

# last_row = 0
# play_state = False

# root = tk.Tk()
# root.title("Central Monitoring System")
# root.state("zoomed")

# # ======================
# # TOP CONTROL BAR
# # ======================

# top_bar = tk.Frame(root,bg="lightgray",height=60)
# top_bar.pack(fill=tk.X)

# def toggle_play():
#     global play_state

#     play_state = not play_state

#     if play_state:
#         play_btn.config(text="Pause")
#         play_data()
#     else:
#         play_btn.config(text="Play")

# play_btn = tk.Button(top_bar,text="Play",font=("Arial",12),command=toggle_play)
# play_btn.pack(side=tk.LEFT,padx=20,pady=10)

# timeline = tk.Scale(
#     top_bar,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=800,
#     label="Timeline",
#     command=lambda x: jump_to(int(x))
# )

# timeline.pack(side=tk.LEFT,padx=20)

# # ======================
# # GRAPH AREA
# # ======================

# graph_frame = ttk.Frame(root)
# graph_frame.pack(fill=tk.BOTH,expand=True)

# fig, axs = plt.subplots(3,2,figsize=(12,8))

# canvas = FigureCanvasTkAgg(fig,master=graph_frame)
# canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

# # ======================
# # FUNCTIONS
# # ======================

# def jump_to(index):
#     global last_row
#     last_row = index
#     update_graph()

# def update_graph():

#     global last_row

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     timeline.config(to=len(df)-1)

#     if last_row >= len(df):
#         return

#     row = df.iloc[last_row]

#     time_buf.append(datetime.now())

#     hr = int(row["HR"])
#     spo2 = int(row["SpO2"])
#     rr = int(row["RR"])
#     temp = float(row["Temp"])
#     sys, dia = map(int,row["BP"].split("/"))

#     hr_buf.append(hr)
#     spo2_buf.append(spo2)
#     rr_buf.append(rr)
#     temp_buf.append(temp)
#     sys_buf.append(sys)
#     dia_buf.append(dia)

#     # HEART RATE
#     axs[0,0].clear()
#     axs[0,0].plot(time_buf,hr_buf)
#     axs[0,0].set_title("Heart Rate")

#     # SPO2
#     axs[0,1].clear()
#     axs[0,1].plot(time_buf,spo2_buf)
#     axs[0,1].set_title("SpO₂")

#     # RR
#     axs[1,0].clear()
#     axs[1,0].plot(time_buf,rr_buf)
#     axs[1,0].set_title("Respiratory Rate")

#     # TEMP
#     axs[1,1].clear()
#     axs[1,1].plot(time_buf,temp_buf)
#     axs[1,1].set_title("Temperature")

#     # BP
#     axs[2,0].clear()
#     axs[2,0].plot(time_buf,sys_buf,label="SYS")
#     axs[2,0].plot(time_buf,dia_buf,label="DIA")
#     axs[2,0].legend()
#     axs[2,0].set_title("Blood Pressure")

#     canvas.draw()

# def play_data():

#     global last_row

#     if not play_state:
#         return

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     if last_row < len(df)-1:

#         last_row += 1

#         timeline.set(last_row)

#         update_graph()

#         root.after(500,play_data)

# update_graph()

# root.mainloop()


# import tkinter as tk
# from tkinter import ttk
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from collections import deque
# from datetime import datetime
# from tkinter import messagebox

# CSV_FILE = "patient_data.csv"
# WINDOW_SIZE = 30

# # buffers
# time_buf = deque(maxlen=WINDOW_SIZE)
# hr_buf = deque(maxlen=WINDOW_SIZE)
# spo2_buf = deque(maxlen=WINDOW_SIZE)
# rr_buf = deque(maxlen=WINDOW_SIZE)
# temp_buf = deque(maxlen=WINDOW_SIZE)
# sys_buf = deque(maxlen=WINDOW_SIZE)
# dia_buf = deque(maxlen=WINDOW_SIZE)

# last_row = 0
# play_state = False

# root = tk.Tk()
# root.title("Central Monitoring System")
# root.state("zoomed")


# # =====================
# # FIXED PRINT FUNCTION
# # =====================
# def print_report():
#     try:
#         if len(time_buf) == 0:
#             messagebox.showwarning("Print Error", "No data available to print.")
#             return

#         # Create a dedicated figure for the PDF/PNG report
#         # This avoids the "Black Image" issue by drawing a fresh set of axes
#         fig_report, axs = plt.subplots(3, 2, figsize=(10, 12))
#         fig_report.suptitle(f"Patient Vital Signs Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
#                             fontsize=16, fontweight='bold')

#         # Map data to report axes
#         data_map = [
#             (axs[0, 0], list(hr_buf), "Heart Rate (BPM)", "red"),
#             (axs[0, 1], list(spo2_buf), "SpO2 (%)", "blue"),
#             (axs[1, 0], list(rr_buf), "Respiratory Rate", "green"),
#             (axs[1, 1], list(temp_buf), "Temperature (°C)", "orange")
#         ]

#         for ax, data, title, color in data_map:
#             ax.plot(list(time_buf), data, color=color, linewidth=1.5)
#             ax.set_title(title)
#             ax.tick_params(axis='x', rotation=45)
#             ax.grid(True, alpha=0.3)

#         # BP (Special case for dual lines)
#         axs[2, 0].plot(list(time_buf), list(sys_buf), color="purple", label="SYS")
#         axs[2, 0].plot(list(time_buf), list(dia_buf), color="magenta", label="DIA")
#         axs[2, 0].set_title("Blood Pressure (mmHg)")
#         axs[2, 0].legend()
#         axs[2, 0].tick_params(axis='x', rotation=45)

#         # Remove empty subplot
#         fig_report.delaxes(axs[2, 1])

#         plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
#         # Save filename with timestamp
#         filename = f"Report_{datetime.now().strftime('%H%M%S')}.png"
#         fig_report.savefig(filename, dpi=200)
#         plt.close(fig_report) # Close to free up memory
        
#         messagebox.showinfo("Success", f"Report saved as: {filename}")
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to print: {e}")


# # ======================
# # TOP CONTROL BAR
# # ======================

# top_bar = tk.Frame(root,bg="lightgray",height=60)
# top_bar.pack(fill=tk.X)

# def toggle_play():
#     global play_state

#     play_state = not play_state

#     if play_state:
#         play_btn.config(text="Pause")
#         play_data()
#     else:
#         play_btn.config(text="Play")

# play_btn = tk.Button(top_bar,text="Play",font=("Arial",12, "bold"),command=toggle_play)
# tk.Button(top_bar, text="🖨 PRINT TO PNG", command=print_report, bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)

# play_btn.pack(side=tk.LEFT,padx=20,pady=10)


# timeline = tk.Scale(
#     top_bar,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=800,
#     label="Timeline",
#     command=lambda x: jump_to(int(x))
# )

# timeline.pack(side=tk.LEFT,padx=20)

# # ======================
# # GRAPH AREA
# # ======================

# graph_frame = ttk.Frame(root)
# graph_frame.pack(fill=tk.BOTH,expand=True)

# fig, axs = plt.subplots(3,2,figsize=(12,8))

# canvas = FigureCanvasTkAgg(fig,master=graph_frame)
# canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

# # ======================
# # FUNCTIONS
# # ======================

# def jump_to(index):
#     global last_row
#     last_row = index
#     update_graph()

# def update_graph():

#     global last_row

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     timeline.config(to=len(df)-1)

#     if last_row >= len(df):
#         return

#     row = df.iloc[last_row]

#     time_buf.append(datetime.now())

#     hr = int(row["HR"])
#     spo2 = int(row["SpO2"])
#     rr = int(row["RR"])
#     temp = float(row["Temp"])
#     sys, dia = map(int,row["BP"].split("/"))

#     hr_buf.append(hr)
#     spo2_buf.append(spo2)
#     rr_buf.append(rr)
#     temp_buf.append(temp)
#     sys_buf.append(sys)
#     dia_buf.append(dia)

#     # HEART RATE
#     axs[0,0].clear()
#     axs[0,0].plot(time_buf,hr_buf)
#     axs[0,0].set_title("Heart Rate")

#     # SPO2
#     axs[0,1].clear()
#     axs[0,1].plot(time_buf,spo2_buf)
#     axs[0,1].set_title("SpO₂")

#     # RR
#     axs[1,0].clear()
#     axs[1,0].plot(time_buf,rr_buf)
#     axs[1,0].set_title("Respiratory Rate")

#     # TEMP
#     axs[1,1].clear()
#     axs[1,1].plot(time_buf,temp_buf)
#     axs[1,1].set_title("Temperature")

#     # BP
#     axs[2,0].clear()
#     axs[2,0].plot(time_buf,sys_buf,label="SYS")
#     axs[2,0].plot(time_buf,dia_buf,label="DIA")
#     axs[2,0].legend()
#     axs[2,0].set_title("Blood Pressure")

#     # ======================
#     # ALERT PANEL
#     # ======================

#     axs[2,1].clear()
#     axs[2,1].axis("off")

#     alerts = []

#     if hr < 60 or hr > 100:
#         alerts.append("Heart Rate Abnormal")

#     if spo2 < 94:
#         alerts.append("Low SpO₂")

#     if rr < 12 or rr > 20:
#         alerts.append("Respiration Abnormal")

#     if temp < 36 or temp > 38:
#         alerts.append("Temperature Abnormal")

#     if sys < 90 or sys > 140 or dia < 60 or dia > 90:
#         alerts.append("Blood Pressure Abnormal")

#     if alerts:
#         alert_text = "ALERTS\n\n" + "\n".join(alerts)
#         axs[2,1].text(
#             0.05,0.9,
#             alert_text,
#             fontsize=14,
#             color="red",
#             verticalalignment="top"
#         )
#     else:
#         axs[2,1].text(
#             0.25,0.5,
#             "All vitals normal",
#             fontsize=14,
#             color="green"
#         )

#     canvas.draw()

# def play_data():

#     global last_row

#     if not play_state:
#         return

#     try:
#         df = pd.read_csv(CSV_FILE)
#     except:
#         return

#     if last_row < len(df)-1:

#         last_row += 1

#         timeline.set(last_row)

#         update_graph()

#         root.after(500,play_data)

# update_graph()

# root.mainloop()






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

#==========================

# 🔊 Init TTS

# 🔊 Initialize TTS
# engine = pyttsx3.init('sapi5')
# engine.setProperty('rate', 160)

# # 🧵 Speech Queue
# speech_queue = queue.Queue()

# def speech_worker():
#     while True:
#         text = speech_queue.get()
#         if text is None:
#             speech_queue.task_done()
#             break

#         print(f"🔊 AI Speaking: {text}")

#         try:
#             # 🔥 Recreate engine EVERY TIME (key fix)
#             engine = pyttsx3.init('sapi5')
#             engine.setProperty('rate', 160)

#             engine.say(text)
#             engine.runAndWait()

#             # 🔥 Explicit cleanup
#             engine.stop()
#             del engine

#         except Exception as e:
#             print("TTS Error:", e)

#         time.sleep(0.2)  # allow driver to release
#         speech_queue.task_done()

# # Start speech thread
# threading.Thread(target=speech_worker, daemon=True).start()

# def speak(text):
#     print("Assistant:", text)

#     filename = f"voice_{uuid.uuid4().hex}.mp3"
#     tts = gTTS(text)
#     tts.save(filename)

#     playsound(filename)   # 🔥 plays in background (no popup)

#     os.remove(filename)   # cleanup


# # 🧠 Convert speech → HHMM
# def extract_time_from_text(text):
#     text = text.lower().replace(":", " ").replace(".", " ")
#     nums = re.findall(r'\d+', text)

#     if not nums:
#         return None

#     hour = int(nums[0])
#     minute = int(nums[1]) if len(nums) > 1 else 0

#     if "pm" in text and hour != 12:
#         hour += 12
#     elif "am" in text and hour == 12:
#         hour = 0

#     if hour > 23 or minute > 59:
#         return None

#     return f"{hour:02d}{minute:02d}"


# def voice_status_check():
#     recognizer = sr.Recognizer()

#     # 🔊 Speak first (non-blocking now)
#     speak("I am listening. Which time should I check?")
#     speech_queue.join()
#     time.sleep(2)  # let speech finish

#     try:
#         # 🎤 Listen
#         with sr.Microphone() as source:
#             recognizer.adjust_for_ambient_noise(source, duration=0.5)
#             audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)

#         user_input = recognizer.recognize_google(audio)
#         print("User said:", user_input)

#         # 🧠 Parse time
#         clean_time = extract_time_from_text(user_input)

#         if not clean_time:
#             speak("I couldn't understand the time.")
#             return

#         print("Parsed time:", clean_time)

#         # 📂 Load CSV
#         df = pd.read_csv(CSV_FILE)
#         df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
#         df = df.dropna(subset=['Timestamp'])

#         # 🎯 Convert input time
#         input_time = datetime.strptime(clean_time, "%H%M")

#         # ⏱ Find closest match
#         df['time_diff'] = df['Timestamp'].apply(
#             lambda x: abs((x.replace(year=1900, month=1, day=1) - input_time).total_seconds())
#         )

#         row = df.loc[df['time_diff'].idxmin()]

#         hr = int(float(row['HR']))
#         spo2 = int(float(row['SpO2']))
#         temp = float(row['Temp'])

#         report = (f"At around {clean_time[:2]}:{clean_time[2:]}, "
#                   f"Heart Rate was {hr} BPM, "
#                   f"Oxygen was {spo2} percent, "
#                   f"and Temperature was {temp} degrees.")

#         print(report)

#         # 🔊 Speak result (will ALWAYS work now)
#         speak(report)

#     except sr.UnknownValueError:
#         speak("I couldn't understand what you said.")
#     except sr.RequestError:
#         speak("Network error.")
#     except Exception as e:
#         print("Error:", e)
#         speak("Sorry, I had trouble finding that data.")
# # #==========================
# #Ai summary
# #==========================

# import tkinter as tk
# from tkinter import scrolledtext

# def show_formatted_analysis(title, content):
#     # Create a popup window
#     result_window = tk.Toplevel()
#     result_window.title(title)
#     result_window.geometry("500x400")
    
#     # Header Label
#     header = tk.Label(result_window, text="Clinical Insights", font=("Helvetica", 14, "bold"), pady=10)
#     header.pack()

#     # Scrollable Text Area
#     text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, font=("Consolas", 11), padx=10, pady=10)
#     text_area.insert(tk.INSERT, content)
#     text_area.configure(state='disabled') # Make it read-only
#     text_area.pack(expand=True, fill='both')

#     # Close Button
#     btn = tk.Button(result_window, text="Dismiss", command=result_window.destroy, width=15)
#     btn.pack(pady=10)

# #Gemini API Key  ==   AIzaSyBNYq7li5zGtBEC6jF8h2e289le_vpYLQc (do not share it)
# # Initialize Gemini
# genai.configure(api_key='AIzaSyBNYq7li5zGtBEC6jF8h2e289le_vpYLQc')
# model = genai.GenerativeModel('gemini-2.5-flash')
# def run_ai_analysis():
#     try:
#         if not hr_buf:
#             messagebox.showwarning("AI Error", "No data visible on timeline to analyze.")
#             return

#         # --- Data Preparation ---
#         hr_list, spo2_list, temp_list = list(hr_buf), list(spo2_buf), list(temp_buf)
        
#         avg_hr = sum(hr_list) / len(hr_list)
#         min_spo2 = min(spo2_list)
#         max_temp = max(temp_list)
#         current_bp = f"{sys_buf[-1]}/{dia_buf[-1]}" if sys_buf and dia_buf else "N/A"

#         # --- Professional Prompting ---
#         # We ask for Markdown formatting to make the AI output structured
#         prompt = f"""
#         Role: Clinical Data Analyst
#         Task: Analyze the following patient vitals:
        
#         DATA SUMMARY:
#         - Heart Rate: Avg {avg_hr:.1f} BPM (Latest: {hr_list[-1]})
#         - SpO2: Min {min_spo2}% (Latest: {spo2_list[-1]}%)
#         - Temp: Max {max_temp:.1f}°C
#         - BP: {current_bp}
        
#         REQUIREMENTS:
#         1. Use a 'STATUS' header (e.g., STABLE or CRITICAL).
#         2. Provide a 3-sentence summary of trends.
#         3. Identify any physiological correlations between SpO2 and HR.
#         """

#         response = model.generate_content(prompt)
        
#         # --- Formatted Display ---
#         # Construct the final display string
#         display_text = f"ANALYSIS REPORT\n{'='*20}\n\n{response.text}"
        
#         # Call our custom popup instead of messagebox.showinfo
#         show_formatted_analysis("AI Live Timeline Analysis", display_text)

#     except Exception as e:
#         messagebox.showerror("AI Error", f"Buffer Analysis Failed: {str(e)}")

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
#     subprocess.Popen(["python", "AI_summary.py"])    

play_btn = tk.Button(top_bar, text="PAUSE", font=("Arial", 10, "bold"), command=toggle_play, 
                     bg="#ffc107", fg="black", width=10, relief="flat")
play_btn.pack(side=tk.LEFT, padx=10)

# Change your existing AI Summary button to this:
# ai_btn = tk.Button(top_bar, text="AI Summary", font=("Arial", 10, "bold"), 
#                    command=run_ai_analysis, # Points to the function above
#                    bg="#ffc107", fg="black", width=12, relief="flat")
# ai_btn.pack(side=tk.LEFT, padx=10)

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

# At the top of your main script, ONLY import
# Load your data here
# from multiprocessing import Process, Queue
# import ecg  # your module

# ecg_queue = Queue()
# ecg_process = None

# def start_ecg():
#     global ecg_process

#     if ecg_process is None or not ecg_process.is_alive():
#         ecg_process = Process(target=ecg.animate_live, args=(ecg_queue,))
#         ecg_process.start()


# def send_data():
#     if len(hr_buf) > 0:
#         hr = hr_buf[-1]   # latest HR value
#         ecg_queue.put(hr)

#     root.after(500, send_data)  # send every 0.5 sec


# The button triggers the subprocess function
# ecg_btn = tk.Button(
#     root, 
#     text="ECG VIEW", 
#     command=start_ecg,
#     bg="#ffc107", 
#     fg="black",
#     font=("Arial", 12, "bold"),
#     width=15
# )
# ecg_btn.pack(pady=10)


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