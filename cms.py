# # # import tkinter as tk
# # # from tkinter import ttk
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # # from collections import deque
# # # from datetime import datetime

# # # # =====================
# # # # CONFIG
# # # # =====================
# # # CSV_FILE = "patient_data.csv"
# # # WINDOW_SIZE = 30
# # # REFRESH_MS = 200

# # # # =====================
# # # # BUFFERS
# # # # =====================
# # # time_buf   = deque(maxlen=WINDOW_SIZE)
# # # hr_buf     = deque(maxlen=WINDOW_SIZE)
# # # spo2_buf   = deque(maxlen=WINDOW_SIZE)
# # # rr_buf     = deque(maxlen=WINDOW_SIZE)
# # # temp_buf   = deque(maxlen=WINDOW_SIZE)
# # # bp_sys_buf = deque(maxlen=WINDOW_SIZE)
# # # bp_dia_buf = deque(maxlen=WINDOW_SIZE)

# # # # =====================
# # # # MAIN WINDOW
# # # # =====================
# # # root = tk.Tk()
# # # root.title("Central Monitoring System")
# # # root.state("zoomed")
# # # root.configure(bg="#f0f2f5")

# # # frame = ttk.Frame(root)
# # # frame.pack(fill=tk.BOTH, expand=True)

# # # frame.columnconfigure((0, 1), weight=1)
# # # frame.rowconfigure((0, 1, 2), weight=1)

# # # # =====================
# # # # GRAPH CREATOR
# # # # =====================
# # # def create_graph(title, ylabel, row, col, ylim):
# # #     fig, ax = plt.subplots(figsize=(6, 4))
# # #     ax.set_title(title, weight="bold")
# # #     ax.set_ylabel(ylabel)
# # #     ax.set_xlabel("Time (HH:MM:SS)")
# # #     ax.set_ylim(ylim)
# # #     ax.grid(True)

# # #     canvas = FigureCanvasTkAgg(fig, master=frame)
# # #     canvas.get_tk_widget().grid(
# # #         row=row, column=col, sticky="nsew", padx=8, pady=8
# # #     )

# # #     return ax, canvas

# # # # =====================
# # # # GRAPHS
# # # # =====================
# # # ax_hr,   canvas_hr   = create_graph("Heart Rate", "BPM", 0, 0, (50, 130))
# # # ax_spo2, canvas_spo2 = create_graph("SpO₂", "%", 0, 1, (90, 100))
# # # ax_rr,   canvas_rr   = create_graph("Respiratory Rate", "Breaths/min", 1, 0, (8, 30))
# # # ax_temp, canvas_temp = create_graph("Temperature", "°C", 1, 1, (35, 40))
# # # ax_bp,   canvas_bp   = create_graph("Blood Pressure", "mmHg", 2, 0, (50, 180))

# # # # =====================
# # # # ALERT PANEL
# # # # =====================
# # # alert_label = tk.Label(
# # #     frame,
# # #     text="✅ All vitals normal",
# # #     font=("Segoe UI", 16, "bold"),
# # #     bg="white",
# # #     fg="green",
# # #     relief="solid",
# # #     padx=20,
# # #     pady=20
# # # )
# # # alert_label.grid(row=2, column=1, sticky="nsew", padx=8, pady=8)

# # # # =====================
# # # # DATA STATE
# # # # =====================
# # # last_row = 0

# # # # =====================
# # # # UPDATE FUNCTION
# # # # =====================
# # # def update_graphs():
# # #     global last_row

# # #     try:
# # #         df = pd.read_csv(CSV_FILE)
# # #     except:
# # #         root.after(REFRESH_MS, update_graphs)
# # #         return

# # #     if last_row >= len(df):
# # #         alert_label.config(text="⏸ Waiting for new data...", fg="orange")
# # #         root.after(REFRESH_MS, update_graphs)
# # #         return

# # #     row = df.iloc[last_row]
# # #     last_row += 1

# # #     # Timestamp
# # #     time_buf.append(datetime.now())

# # #     # Read values
# # #     hr = int(row["HR"])
# # #     spo2 = int(row["SpO2"])
# # #     rr = int(row["RR"])
# # #     temp = float(row["Temp"])
# # #     bp_sys, bp_dia = map(int, row["BP"].split("/"))

# # #     hr_buf.append(hr)
# # #     spo2_buf.append(spo2)
# # #     rr_buf.append(rr)
# # #     temp_buf.append(temp)
# # #     bp_sys_buf.append(bp_sys)
# # #     bp_dia_buf.append(bp_dia)

# # #     # =====================
# # #     # ALERT LOGIC
# # #     # =====================
# # #     alerts = []

# # #     if hr < 60 or hr > 100:
# # #         alerts.append("Heart Rate Abnormal")
# # #     if spo2 < 94:
# # #         alerts.append("Low SpO₂")
# # #     if rr < 12 or rr > 20:
# # #         alerts.append("Respiratory Rate Abnormal")
# # #     if temp < 36 or temp > 38:
# # #         alerts.append("Temperature Abnormal")
# # #     if bp_sys < 90 or bp_sys > 140 or bp_dia < 60 or bp_dia > 90:
# # #         alerts.append("Blood Pressure Abnormal")

# # #     # =====================
# # #     # PLOTS
# # #     # =====================
# # #     def format_axis(ax):
# # #         ax.xaxis.set_major_formatter(
# # #             plt.matplotlib.dates.DateFormatter('%H:%M:%S')
# # #         )
# # #         ax.grid(True)

# # #     # HR
# # #     ax_hr.cla()
# # #     ax_hr.plot(time_buf, hr_buf, linewidth=2)
# # #     ax_hr.set_title("Heart Rate")
# # #     ax_hr.set_ylabel("BPM")
# # #     ax_hr.set_xlabel("Time (HH:MM:SS)")
# # #     ax_hr.set_ylim(50, 130)
# # #     format_axis(ax_hr)

# # #     # SpO2
# # #     ax_spo2.cla()
# # #     ax_spo2.plot(time_buf, spo2_buf, linewidth=2)
# # #     ax_spo2.set_title("SpO₂")
# # #     ax_spo2.set_ylabel("%")
# # #     ax_spo2.set_xlabel("Time (HH:MM:SS)")
# # #     ax_spo2.set_ylim(90, 100)
# # #     format_axis(ax_spo2)

# # #     # RR
# # #     ax_rr.cla()
# # #     ax_rr.plot(time_buf, rr_buf, linewidth=2)
# # #     ax_rr.set_title("Respiratory Rate")
# # #     ax_rr.set_ylabel("Breaths/min")
# # #     ax_rr.set_xlabel("Time (HH:MM:SS)")
# # #     ax_rr.set_ylim(8, 30)
# # #     format_axis(ax_rr)

# # #     # Temp
# # #     ax_temp.cla()
# # #     ax_temp.plot(time_buf, temp_buf, linewidth=2)
# # #     ax_temp.set_title("Temperature")
# # #     ax_temp.set_ylabel("°C")
# # #     ax_temp.set_xlabel("Time (HH:MM:SS)")
# # #     ax_temp.set_ylim(35, 40)
# # #     format_axis(ax_temp)

# # #     # BP
# # #     ax_bp.cla()
# # #     ax_bp.plot(time_buf, bp_sys_buf, label="SYS", linewidth=2)
# # #     ax_bp.plot(time_buf, bp_dia_buf, label="DIA", linewidth=2)
# # #     ax_bp.set_title("Blood Pressure")
# # #     ax_bp.set_ylabel("mmHg")
# # #     ax_bp.set_xlabel("Time (HH:MM:SS)")
# # #     ax_bp.set_ylim(50, 180)
# # #     ax_bp.legend()
# # #     format_axis(ax_bp)

# # #     # =====================
# # #     # ALERT PANEL UPDATE
# # #     # =====================
# # #     if alerts:
# # #         alert_label.config(
# # #             text="🚨 ALERT!\n" + "\n".join(alerts),
# # #             fg="red"
# # #         )
# # #     else:
# # #         alert_label.config(
# # #             text="✅ All vitals normal",
# # #             fg="green"
# # #         )

# # #     # Draw canvases
# # #     canvas_hr.draw()
# # #     canvas_spo2.draw()
# # #     canvas_rr.draw()
# # #     canvas_temp.draw()
# # #     canvas_bp.draw()

# # #     root.after(REFRESH_MS, update_graphs)

# # # # =====================
# # # # SAFE EXIT
# # # # =====================
# # # def on_close():
# # #     global after_id
# # #     if after_id is not None:
# # #         try:
# # #             root.after_cancel(after_id)
# # #         except:
# # #             pass
# # #     root.destroy()

# # # root.protocol("WM_DELETE_WINDOW", on_close)

# # # # =====================
# # # # START
# # # # =====================
# # # global after_id
# # # after_id = root.after(REFRESH_MS, update_graphs)

# # # root.mainloop()








# # import tkinter as tk
# # from tkinter import ttk, messagebox
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from collections import deque
# # from datetime import datetime
# # import os

# # # =====================
# # # CONFIG & CONSTANTS
# # # =====================
# # CSV_FILE = "patient_data.csv"
# # WINDOW_SIZE = 30
# # REFRESH_MS = 500  # Increased slightly for stability

# # # Thresholds for Alarms
# # THRESHOLDS = {
# #     "HR": (60, 100),
# #     "SpO2": (94, 100),
# #     "RR": (12, 20),
# #     "Temp": (36.1, 37.2),
# #     "BP_SYS": (90, 140)
# # }

# # class VitalMonitor:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Advanced Hospital Vital Monitor")
# #         self.root.state("zoomed")
# #         self.root.configure(bg="#f0f0f0")

# #         # Data Buffers
# #         self.buffers = {
# #             "time": deque(maxlen=WINDOW_SIZE),
# #             "HR": deque(maxlen=WINDOW_SIZE),
# #             "SpO2": deque(maxlen=WINDOW_SIZE),
# #             "RR": deque(maxlen=WINDOW_SIZE),
# #             "Temp": deque(maxlen=WINDOW_SIZE),
# #             "SYS": deque(maxlen=WINDOW_SIZE),
# #             "DIA": deque(maxlen=WINDOW_SIZE)
# #         }

# #         self.setup_ui()
# #         self.setup_plots()
# #         self.update_loop()

# #     def setup_ui(self):
# #         """Creates the top control panel."""
# #         self.cp = tk.Frame(self.root, bg="#2c3e50", pady=10)
# #         self.cp.pack(side=tk.TOP, fill=tk.X)

# #         # Print Button
# #         tk.Button(self.cp, text="📑 GENERATE REPORT", command=self.print_report, 
# #                   bg="#27ae60", fg="white", font=("Arial", 10, "bold"), relief="flat").pack(side=tk.LEFT, padx=20)

# #         # Live Toggle
# #         self.is_live = tk.BooleanVar(value=True)
# #         tk.Checkbutton(self.cp, text="LIVE FEED", variable=self.is_live, 
# #                        bg="#2c3e50", fg="white", selectcolor="#2c3e50", font=("Arial", 10)).pack(side=tk.LEFT)

# #         # Slider
# #         self.time_slider = tk.Scale(self.cp, from_=0, to=100, orient=tk.HORIZONTAL, 
# #                                     length=500, showvalue=False, bg="#2c3e50", fg="white", highlightthickness=0)
# #         self.time_slider.pack(side=tk.LEFT, padx=30)

# #         self.lbl_time = tk.Label(self.cp, text="Syncing...", bg="#2c3e50", fg="#ecf0f1", font=("Courier", 12, "bold"))
# #         self.lbl_time.pack(side=tk.RIGHT, padx=20)

# #     def setup_plots(self):
# #         """Initializes Matplotlib figures."""
# #         self.main_frame = ttk.Frame(self.root)
# #         self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
# #         self.main_frame.columnconfigure((0, 1), weight=1)
# #         self.main_frame.rowconfigure((0, 1, 2), weight=1)

# #         self.figs = {}
# #         self.axes = {}
# #         self.canvases = {}
# #         self.lines = {}

# #         plot_configs = [
# #             ("HR", "Heart Rate (BPM)", 0, 0, (40, 140), "red"),
# #             ("SpO2", "Oxygen Saturation (%)", 0, 1, (85, 105), "blue"),
# #             ("RR", "Respiration Rate", 1, 0, (5, 35), "green"),
# #             ("Temp", "Body Temp (°C)", 1, 1, (34, 41), "orange"),
# #         ]

# #         for key, title, r, c, ylim, color in plot_configs:
# #             fig, ax = plt.subplots(figsize=(5, 3))
# #             fig.patch.set_facecolor('#f0f0f0')
# #             ax.set_title(title, fontweight='bold')
# #             ax.set_ylim(ylim)
# #             line, = ax.plot([], [], color=color, linewidth=2)
            
# #             canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
# #             canvas.get_tk_widget().grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
            
# #             self.figs[key] = fig
# #             self.axes[key] = ax
# #             self.canvases[key] = canvas
# #             self.lines[key] = line

# #         # Special setup for Blood Pressure
# #         fig_bp, ax_bp = plt.subplots(figsize=(5, 3))
# #         fig_bp.patch.set_facecolor('#f0f0f0')
# #         ax_bp.set_title("Blood Pressure (mmHg)", fontweight='bold')
# #         ax_bp.set_ylim(40, 200)
# #         l_sys, = ax_bp.plot([], [], color="purple", label="SYS")
# #         l_dia, = ax_bp.plot([], [], color="#8e44ad", label="DIA")
# #         ax_bp.legend(loc="upper right", fontsize='small')
        
# #         canvas_bp = FigureCanvasTkAgg(fig_bp, master=self.main_frame)
# #         canvas_bp.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
# #         self.axes["BP"] = ax_bp
# #         self.canvases["BP"] = canvas_bp
# #         self.lines["SYS"] = l_sys
# #         self.lines["DIA"] = l_dia


# #     def check_alarms(self, key, value):
# #         """Changes plot background if values are out of range."""
# #         # Mapping the 'BP' graph to use 'BP_SYS' thresholds
# #         threshold_key = "BP_SYS" if key == "BP" else key
        
# #         if threshold_key not in THRESHOLDS: 
# #             return
            
# #         low, high = THRESHOLDS[threshold_key]
        
# #         if value < low or value > high:
# #             self.axes[key].set_facecolor('#fadbd8') # Light Red (Alarm)
# #         else:
# #             self.axes[key].set_facecolor('white') # Normal

# #     def update_loop(self):
# #         try:
# #             if os.path.exists(CSV_FILE):
# #                 df = pd.read_csv(CSV_FILE)
# #                 if not df.empty:
# #                     self.time_slider.config(to=len(df)-1)
# #                     idx = (len(df)-1) if self.is_live.get() else self.time_slider.get()
# #                     if self.is_live.get(): self.time_slider.set(idx)

# #                     # Get data window
# #                     view = df.iloc[max(0, idx-WINDOW_SIZE+1) : idx+1]
                    
# #                     # Reset buffers
# #                     for b in self.buffers.values(): b.clear()

# #                     for _, row in view.iterrows():
# #                         self.buffers["time"].append(str(row["Timestamp"]))
# #                         self.buffers["HR"].append(float(row["HR"]))
# #                         self.buffers["SpO2"].append(float(row["SpO2"]))
# #                         self.buffers["RR"].append(float(row["RR"]))
# #                         self.buffers["Temp"].append(float(row["Temp"]))
# #                         s, d = map(int, str(row["BP"]).split("/"))
# #                         self.buffers["SYS"].append(s)
# #                         self.buffers["DIA"].append(d)

# #                     # Update UI Label
# #                     self.lbl_time.config(text=f"TIME: {self.buffers['time'][-1]}")

# #                     # Update Plot Lines
# #                     x_axis = list(range(len(self.buffers["HR"])))
# #                     for key in ["HR", "SpO2", "RR", "Temp"]:
# #                         self.lines[key].set_data(x_axis, list(self.buffers[key]))
# #                         self.check_alarms(key, self.buffers[key][-1])
# #                         self.canvases[key].draw_idle()

# #                     self.lines["SYS"].set_data(x_axis, list(self.buffers["SYS"]))
# #                     self.lines["DIA"].set_data(x_axis, list(self.buffers["DIA"]))
# #                     self.check_alarms("BP", self.buffers["SYS"][-1])
# #                     self.canvases["BP"].draw_idle()

# #         except Exception as e:
# #             print(f"Sync Error: {e}")

# #         self.root.after(REFRESH_MS, self.update_loop)

# #     def print_report(self):
# #         """Generates a professional PNG report."""
# #         try:
# #             if not self.buffers["time"]:
# #                 messagebox.showwarning("No Data", "No data to export.")
# #                 return

# #             fig_rep, axs = plt.subplots(3, 2, figsize=(10, 12))
# #             fig_rep.suptitle(f"Patient Status Report\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fontsize=16)

# #             plots = [
# #                 (axs[0,0], "HR", "Heart Rate", "red"),
# #                 (axs[0,1], "SpO2", "SpO2", "blue"),
# #                 (axs[1,0], "RR", "Respiration", "green"),
# #                 (axs[1,1], "Temp", "Temperature", "orange")
# #             ]

# #             for ax, key, title, color in plots:
# #                 ax.plot(list(self.buffers["time"]), list(self.buffers[key]), color=color)
# #                 ax.set_title(title)
# #                 ax.tick_params(axis='x', rotation=45)

# #             axs[2,0].plot(list(self.buffers["time"]), list(self.buffers["SYS"]), label="SYS")
# #             axs[2,0].plot(list(self.buffers["time"]), list(self.buffers["DIA"]), label="DIA")
# #             axs[2,0].legend()
# #             axs[2,0].set_title("Blood Pressure")
            
# #             fig_rep.delaxes(axs[2,1])
# #             plt.tight_layout()
            
# #             fname = f"Report_{datetime.now().strftime('%H%M%S')}.png"
# #             fig_rep.savefig(fname)
# #             plt.close(fig_rep)
# #             messagebox.showinfo("Report Saved", f"Successfully saved as {fname}")
# #         except Exception as e:
# #             messagebox.showerror("Export Error", str(e))

# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = VitalMonitor(root)
# #     root.mainloop()

# # import tkinter as tk
# # from tkinter import ttk
# # from tkinter import messagebox
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from collections import deque
# # from datetime import datetime

# # CSV_FILE = "patient_data.csv"
# # WINDOW_SIZE = 30

# # # Buffers
# # time_buf = deque(maxlen=WINDOW_SIZE)
# # hr_buf = deque(maxlen=WINDOW_SIZE)
# # spo2_buf = deque(maxlen=WINDOW_SIZE)
# # rr_buf = deque(maxlen=WINDOW_SIZE)
# # temp_buf = deque(maxlen=WINDOW_SIZE)
# # sys_buf = deque(maxlen=WINDOW_SIZE)
# # dia_buf = deque(maxlen=WINDOW_SIZE)

# # last_row = 0

# # # =========================
# # # TKINTER WINDOW
# # # =========================

# # root = tk.Tk()
# # root.title("Central Monitoring System")
# # root.state("zoomed")

# # # =========================
# # # PRINT REPORT
# # # =========================

# # def print_report():

# #     try:

# #         if len(time_buf) == 0:
# #             messagebox.showwarning("Print Error","No data available")
# #             return

# #         fig_report,axs = plt.subplots(3,2,figsize=(10,12))

# #         fig_report.suptitle(
# #             f"Patient Vital Signs Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
# #             fontsize=16
# #         )

# #         data_map = [
# #             (axs[0,0],hr_buf,"Heart Rate","red"),
# #             (axs[0,1],spo2_buf,"SpO2","blue"),
# #             (axs[1,0],rr_buf,"Respiratory Rate","green"),
# #             (axs[1,1],temp_buf,"Temperature","orange")
# #         ]

# #         for ax,data,title,color in data_map:

# #             ax.plot(list(time_buf),list(data),color=color)
# #             ax.set_title(title)
# #             ax.tick_params(axis='x',rotation=45)
# #             ax.grid(True)

# #         axs[2,0].plot(list(time_buf),list(sys_buf),label="SYS")
# #         axs[2,0].plot(list(time_buf),list(dia_buf),label="DIA")
# #         axs[2,0].legend()
# #         axs[2,0].set_title("Blood Pressure")

# #         fig_report.delaxes(axs[2,1])

# #         plt.tight_layout()

# #         filename=f"Report_{datetime.now().strftime('%H%M%S')}.png"
# #         fig_report.savefig(filename,dpi=200)

# #         plt.close(fig_report)

# #         messagebox.showinfo("Success",f"Report saved as {filename}")

# #     except Exception as e:
# #         messagebox.showerror("Error",str(e))

# # # =========================
# # # TOP BAR
# # # =========================

# # top_bar=tk.Frame(root,bg="lightgray",height=60)
# # top_bar.pack(fill=tk.X)

# # print_btn=tk.Button(
# #     top_bar,
# #     text="🖨 PRINT REPORT",
# #     command=print_report,
# #     bg="#28a745",
# #     fg="white",
# #     font=("Arial",12,"bold")
# # )

# # print_btn.pack(side=tk.LEFT,padx=20,pady=10)

# # timeline=tk.Scale(
# #     top_bar,
# #     from_=0,
# #     to=100,
# #     orient=tk.HORIZONTAL,
# #     length=800,
# #     label="Timeline"
# # )

# # timeline.pack(side=tk.LEFT,padx=20)

# # # =========================
# # # GRAPH AREA
# # # =========================

# # graph_frame=ttk.Frame(root)
# # graph_frame.pack(fill=tk.BOTH,expand=True)

# # fig,axs=plt.subplots(3,2,figsize=(12,8))

# # canvas=FigureCanvasTkAgg(fig,master=graph_frame)
# # canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

# # # =========================
# # # GRAPH UPDATE
# # # =========================

# # def update_graph():

# #     global last_row

# #     try:
# #         df = pd.read_csv(CSV_FILE, dtype={"Timestamp": str})
# #     except:
# #         return

# #     timeline.config(to=len(df)-1)

# #     if last_row>=len(df):
# #         return

# #     row=df.iloc[last_row]

# #     timestamp=datetime.strptime(row["Timestamp"],"%Y%m%d%H%M%S")
# #     time_buf.append(timestamp)

# #     hr=int(row["HR"])
# #     spo2=int(row["SpO2"])
# #     rr=int(row["RR"])
# #     temp=float(row["Temp"])

# #     sys,dia=map(int,row["BP"].split("/"))

# #     hr_buf.append(hr)
# #     spo2_buf.append(spo2)
# #     rr_buf.append(rr)
# #     temp_buf.append(temp)
# #     sys_buf.append(sys)
# #     dia_buf.append(dia)

# #     # clear graphs
# #     for ax in axs.flatten():
# #         ax.clear()
# #         ax.grid(True)

# #     # HEART RATE
# #     axs[0,0].plot(time_buf,hr_buf,color="red")
# #     axs[0,0].set_title("Heart Rate")

# #     # SPO2
# #     axs[0,1].plot(time_buf,spo2_buf,color="blue")
# #     axs[0,1].set_title("SpO₂")

# #     # RR
# #     axs[1,0].plot(time_buf,rr_buf,color="green")
# #     axs[1,0].set_title("Respiratory Rate")

# #     # TEMP
# #     axs[1,1].plot(time_buf,temp_buf,color="orange")
# #     axs[1,1].set_title("Temperature")

# #     # BP
# #     axs[2,0].plot(time_buf,sys_buf,label="SYS",color="purple")
# #     axs[2,0].plot(time_buf,dia_buf,label="DIA",color="magenta")
# #     axs[2,0].legend()
# #     axs[2,0].set_title("Blood Pressure")

# #     # =========================
# #     # ALERT PANEL
# #     # =========================

# #     axs[2,1].axis("off")

# #     alerts=[]

# #     if hr<60 or hr>100:
# #         alerts.append("Heart Rate Abnormal")

# #     if spo2<94:
# #         alerts.append("Low SpO₂")

# #     if rr<12 or rr>20:
# #         alerts.append("Respiration Abnormal")

# #     if temp<36 or temp>38:
# #         alerts.append("Temperature Abnormal")

# #     if sys<90 or sys>140 or dia<60 or dia>90:
# #         alerts.append("Blood Pressure Abnormal")

# #     if alerts:

# #         text="ALERTS\n\n"+"\n".join(alerts)

# #         axs[2,1].text(
# #             0.05,0.9,
# #             text,
# #             fontsize=14,
# #             color="red",
# #             verticalalignment="top"
# #         )

# #     else:

# #         axs[2,1].text(
# #             0.25,0.5,
# #             "All Vitals Normal",
# #             fontsize=14,
# #             color="green"
# #         )

# #     canvas.draw()

# # # =========================
# # # REALTIME LOOP
# # # =========================

# # def realtime_update():

# #     global last_row

# #     try:
# #         df = pd.read_csv(CSV_FILE, dtype={"Timestamp": str})
# #     except:
# #         root.after(1000,realtime_update)
# #         return

# #     if last_row<len(df)-1:

# #         last_row+=1
# #         timeline.set(last_row)
# #         update_graph()

# #     root.after(1000,realtime_update)

# # # =========================
# # # START SYSTEM
# # # =========================

# # update_graph()
# # realtime_update()

# # root.mainloop()


# import tkinter as tk
# from tkinter import ttk, messagebox
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from collections import deque
# from datetime import datetime
# import os
# import random

# CSV_FILE = "patient_data.csv"
# WINDOW_SIZE = 30

# # Buffers to store the "sliding window" of data
# time_buf = deque(maxlen=WINDOW_SIZE)
# hr_buf = deque(maxlen=WINDOW_SIZE)
# spo2_buf = deque(maxlen=WINDOW_SIZE)
# rr_buf = deque(maxlen=WINDOW_SIZE)
# temp_buf = deque(maxlen=WINDOW_SIZE)
# sys_buf = deque(maxlen=WINDOW_SIZE)
# dia_buf = deque(maxlen=WINDOW_SIZE)

# last_row = 0

# # --- HELPER: Create Dummy Data if File Doesn't Exist ---
# def check_or_create_csv():
#     if not os.path.exists(CSV_FILE):
#         df = pd.DataFrame(columns=["Timestamp", "HR", "SpO2", "RR", "Temp", "BP"])
#         # Add one initial row so the script has something to read
#         new_row = {
#             "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
#             "HR": 75, "SpO2": 98, "RR": 16, "Temp": 36.6, "BP": "120/80"
#         }
#         df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
#         df.to_csv(CSV_FILE, index=False)

# # =========================
# # TKINTER UI SETUP
# # =========================
# root = tk.Tk()
# root.title("Medical Vital Signs Monitor")
# root.state("zoomed")

# # =========================
# # PRINT REPORT FUNCTION
# # =========================
# def print_report():
#     try:
#         if len(time_buf) == 0:
#             messagebox.showwarning("Print Error", "No data available in buffers.")
#             return

#         fig_report, axs = plt.subplots(3, 2, figsize=(10, 12))
#         fig_report.suptitle(
#             f"Patient Vital Signs Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#             fontsize=16
#         )

#         data_map = [
#             (axs[0, 0], hr_buf, "Heart Rate (bpm)", "red"),
#             (axs[0, 1], spo2_buf, "SpO2 (%)", "blue"),
#             (axs[1, 0], rr_buf, "Resp Rate (rpm)", "green"),
#             (axs[1, 1], temp_buf, "Temp (°C)", "orange")
#         ]

#         for ax, data, title, color in data_map:
#             ax.plot(list(time_buf), list(data), color=color, marker='o', markersize=3)
#             ax.set_title(title)
#             ax.grid(True)
#             plt.setp(ax.get_xticklabels(), rotation=45)

#         axs[2, 0].plot(list(time_buf), list(sys_buf), label="SYS", color="purple")
#         axs[2, 0].plot(list(time_buf), list(dia_buf), label="DIA", color="magenta")
#         axs[2, 0].legend()
#         axs[2, 0].set_title("Blood Pressure (mmHg)")
#         plt.setp(axs[2, 0].get_xticklabels(), rotation=45)

#         fig_report.delaxes(axs[2, 1]) # Remove the empty alert slot for the print
#         plt.tight_layout(rect=[0, 0.03, 1, 0.95])

#         filename = f"Report_{datetime.now().strftime('%H%M%S')}.png"
#         fig_report.savefig(filename, dpi=200)
#         plt.close(fig_report)
#         messagebox.showinfo("Success", f"Report saved as {filename}")

#     except Exception as e:
#         messagebox.showerror("Error", f"Report failed: {e}")

# # =========================
# # TOP NAVIGATION BAR
# # =========================
# top_bar = tk.Frame(root, bg="#f8f9fa", height=60, relief=tk.RAISED, borderwidth=1)
# top_bar.pack(fill=tk.X)

# print_btn = tk.Button(
#     top_bar, text="💾 SAVE REPORT", command=print_report,
#     bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=15
# )
# print_btn.pack(side=tk.LEFT, padx=20, pady=10)

# timeline = tk.Scale(
#     top_bar, from_=0, to=100, orient=tk.HORIZONTAL, 
#     length=600, label="Historical Seek (Rows)"
# )
# timeline.pack(side=tk.LEFT, padx=20)

# # =========================
# # GRAPHING AREA
# # =========================
# graph_frame = ttk.Frame(root)
# graph_frame.pack(fill=tk.BOTH, expand=True)

# fig, axs = plt.subplots(3, 2, figsize=(10, 7))
# fig.patch.set_facecolor('#f0f0f0')
# canvas = FigureCanvasTkAgg(fig, master=graph_frame)
# canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# # =========================
# # LOGIC & UPDATES
# # =========================
# def update_graph():
#     global last_row
#     try:
#         df = pd.read_csv(CSV_FILE, dtype={"Timestamp": str})
#         if df.empty: return
#     except:
#         return

#     # Update slider range
#     timeline.config(to=len(df)-1)
    
#     # Check if there is a new row to process
#     if last_row >= len(df):
#         return

#     row = df.iloc[last_row]
    
#     try:
#         ts = datetime.strptime(row["Timestamp"], "%Y%m%d%H%M%S")
#         time_buf.append(ts.strftime("%H:%M:%S"))
        
#         hr = int(row["HR"])
#         spo2 = int(row["SpO2"])
#         rr = int(row["RR"])
#         temp = float(row["Temp"])
#         sys, dia = map(int, str(row["BP"]).split("/"))

#         hr_buf.append(hr)
#         spo2_buf.append(spo2)
#         rr_buf.append(rr)
#         temp_buf.append(temp)
#         sys_buf.append(sys)
#         dia_buf.append(dia)
#     except Exception as e:
#         print(f"Data parse error at row {last_row}: {e}")
#         return

#     # Redraw logic
#     titles = ["Heart Rate", "SpO2", "Respiratory Rate", "Temperature"]
#     buffers = [hr_buf, spo2_buf, rr_buf, temp_buf]
#     colors = ["red", "blue", "green", "orange"]

#     for i, ax in enumerate(axs.flatten()[:4]):
#         ax.clear()
#         ax.plot(list(time_buf), list(buffers[i]), color=colors[i], linewidth=2)
#         ax.set_title(titles[i], fontsize=10, fontweight='bold')
#         ax.grid(True, linestyle='--', alpha=0.6)
#         ax.tick_params(axis='x', labelsize=8, rotation=30)

#     # BP Graph
#     axs[2, 0].clear()
#     axs[2, 0].plot(list(time_buf), list(sys_buf), label="SYS", color="purple")
#     axs[2, 0].plot(list(time_buf), list(dia_buf), label="DIA", color="magenta")
#     axs[2, 0].set_title("Blood Pressure", fontsize=10, fontweight='bold')
#     axs[2, 0].legend(loc='upper left', fontsize=8)
#     axs[2, 0].grid(True, linestyle='--', alpha=0.6)
#     axs[2, 0].tick_params(axis='x', labelsize=8, rotation=30)

#     # Alert Panel
#     axs[2, 1].clear()
#     axs[2, 1].axis("off")
#     alerts = []
#     if hr < 60 or hr > 100: alerts.append("• HR Abnormal")
#     if spo2 < 94: alerts.append("• Low SpO2")
#     if rr < 12 or rr > 20: alerts.append("• RR Abnormal")
#     if temp < 36 or temp > 38: alerts.append("• Temp Abnormal")
#     if sys > 140 or dia > 90: alerts.append("• Hypertension")

#     if alerts:
#         axs[2, 1].text(0.1, 0.8, "⚠️ ALERTS", color="red", weight="bold", fontsize=14)
#         axs[2, 1].text(0.1, 0.3, "\n".join(alerts), color="darkred", fontsize=12)
#     else:
#         axs[2, 1].text(0.2, 0.5, "✅ VITALS NORMAL", color="green", weight="bold", fontsize=12)

#     fig.tight_layout()
#     canvas.draw()

# def realtime_loop():
#     global last_row
#     try:
#         df = pd.read_csv(CSV_FILE)
#         if last_row < len(df) - 1:
#             last_row += 1
#             timeline.set(last_row)
#             update_graph()
#     except:
#         pass
    
#     root.after(1000, realtime_loop)

# # =========================
# # EXECUTION
# # =========================
# check_or_create_csv()
# update_graph() # Initial draw
# realtime_loop() # Start the 1s loop

# root.mainloop()





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