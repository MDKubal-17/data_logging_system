import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
import os
import threading
import time
from collections import deque
import math


class ECGMonitor:
    def __init__(self):
        self.fs = 500
        self.duration = 5
        self.buffer_size = self.fs * self.duration

        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.line, = self.ax.plot([], [], lw=1.5, color='#00FF00')

        # X-axis (fixed time window)
        self.x_data = np.linspace(0, self.duration, self.buffer_size)

        # Y buffer (sliding window)
        self.y_data = deque([0.0] * self.buffer_size, maxlen=self.buffer_size)

        self.sample_index = 0
        self.current_hr = 70
        self.running = True

        # HR history for condition detection
        self.hr_history = deque(maxlen=20)
        self.condition = "Normal Sinus Rhythm"

        # Graph styling
        self.ax.set_ylim(-0.5, 1.5)
        self.ax.set_xlim(0, self.duration)
        self.ax.set_facecolor("black")
        self.ax.grid(True, linestyle='--', alpha=0.2, color='white')
        self.ax.set_title("Live ECG Monitor", color='white')
        self.ax.tick_params(colors='white')

        # Condition text
        self.text = self.ax.text(
            0.02, 0.9, "",
            transform=self.ax.transAxes,
            fontsize=12,
            fontweight='bold'
        )

    # ---------- ECG SIGNAL ----------
    def get_signal_point(self, index, hr):
        bps = hr / 60.0
        t = (index * bps / self.fs) % 1.0

        # P-QRS-T wave
        p = 0.1 * np.exp(-((t - 0.2)**2) / (2 * 0.01**2))
        qrs = 1.0 * np.exp(-((t - 0.4)**2) / (2 * 0.005**2))
        t_w = 0.25 * np.exp(-((t - 0.7)**2) / (2 * 0.02**2))

        return p + qrs + t_w

    def classify(self):
        # 1. Validation: Handle NaN or empty history immediately
        if math.isnan(self.current_hr) or not self.hr_history:
            return "No Data"

        hr = self.current_hr
        condition = "Normal Sinus Rhythm"

        # 2. Rate-based Classification (Priority logic)
        if hr > 150:
            condition = "Ventricular Tachycardia"
        elif hr > 100:
            condition = "Tachycardia"
        elif hr < 60:
            condition = "Bradycardia"

        # 3. Variability-based Classification (Arrhythmia check)
        # We filter NaNs out of the history to prevent math errors
        clean_history = [x for x in self.hr_history if not math.isnan(x)]

        if len(clean_history) > 5:
            variability = max(clean_history) - min(clean_history)
            
            # If variability is high, we flag it as Atrial Fibrillation,
            # BUT we don't overwrite if it's already a high-priority VT.
            if variability > 20 and condition != "Ventricular Tachycardia":
                condition = "Atrial Fibrillation"

        return condition

    # ---------- FILE READER ----------
    def file_reader_thread(self):
        while self.running:
            if os.path.exists("live_data.json"):
                try:
                    with open("live_data.json", "r") as f:
                        data = json.load(f)
                        hr_list = data.get("hr", [])

                        if hr_list:
                            self.current_hr = hr_list[-1]
                            self.hr_history.append(self.current_hr)

                except:
                    pass

            time.sleep(0.5)

    # ---------- ANIMATION ----------
    def update(self, frame):
        samples_per_frame = 25

        for _ in range(samples_per_frame):
            val = self.get_signal_point(self.sample_index, self.current_hr)
            self.y_data.append(val)
            self.sample_index += 1

        self.line.set_data(self.x_data, list(self.y_data))

        # Update condition
        self.condition = self.classify()

        self.text.set_text(f"Condition: {self.condition} | HR: {self.current_hr}")

        # Color logic
        if "Normal" in self.condition:
            self.text.set_color("green")
        else:
            self.text.set_color("red")

        return self.line, self.text

    # ---------- RUN ----------
    def run(self):
        threading.Thread(target=self.file_reader_thread, daemon=True).start()

        self.ani = FuncAnimation(
            self.fig,
            self.update,
            interval=50,
            blit=True,
            cache_frame_data=False
        )

        plt.show()
        self.running = False


# ---------- MAIN ----------
if __name__ == "__main__":
    monitor = ECGMonitor()
    monitor.run()