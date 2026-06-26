# # import socket
# # import time

# # BROADCAST_IP = "255.255.255.255"
# # PORT = 5005

# # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# # print("Patient Simulator Active. Press Ctrl+C to stop.")

# # while True:
# #     input("Press Enter to SIMULATE A CRITICAL HEART RATE...")
# #     msg = "BED 04: Heart Rate > 150 BPM!"
# #     sock.sendto(msg.encode(), (BROADCAST_IP, PORT))
# #     print("Alert broadcasted to all monitors.")



# import socket
# import pandas as pd
# from datetime import datetime
# import time

# BROADCAST_IP = "255.255.255.255"
# BROADCAST_IP2 = "192.168.1.255"
# PORT = 5005
# CSV_FILE = "patient_data.csv"

# last_row = 0

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# print("Patient Simulator Active. Press Ctrl+C to stop.")

# while True:
#     # input("Press Enter to SEND LATEST PATIENT DATA...")

#     try:
#         df = pd.read_csv(CSV_FILE)

#         if last_row >= len(df):
#             print("Waiting for new data...")
#             continue

#         row = df.iloc[last_row]
#         last_row += 1

#         hr = int(row["HR"])
#         spo2 = int(row["SpO2"])
#         rr = int(row["RR"])
#         temp = float(row["Temp"])
#         bp_sys, bp_dia = map(int, row["BP"].split("/"))
#         bp = f"{bp_sys}/{bp_dia}"

#         alerts = []

#         if hr < 60 or hr > 100:
#             alerts.append("Heart Rate Abnormal")
#         if spo2 < 95:
#             alerts.append("Low SpO2")
#         if rr < 12 or rr > 20:
#             alerts.append("Respiratory Rate Abnormal")
#         if temp < 36 or temp > 38:
#             alerts.append("Temperature Abnormal")
#         if bp_sys < 90 or bp_sys > 140 or bp_dia < 60 or bp_dia > 90:
#             alerts.append("Blood Pressure Abnormal")
  
#         if alerts:
#             alert_summary = "; ".join(alerts)
#             msg = f"BED 04 | HR:{hr} | SpO2:{spo2} | RR:{rr} | Temp:{temp} | BP:{bp} \n {alert_summary}"
#             sock.sendto(msg.encode(), (BROADCAST_IP, PORT))
#             sock.sendto(msg.encode(), (BROADCAST_IP2, PORT))
#             print("Broadcasted:", msg)

#         time.sleep(0.5)    

#     except Exception as e:
#         print("Error:", e)

import socket
import pandas as pd
import time

BROADCAST_IP = "255.255.255.255"
BROADCAST_IP2 = "192.168.1.255"
PORT = 5005
CSV_FILE = "patient_data1.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

last_row = 0

print("Patient Simulator Active")

while True:

    try:

        df = pd.read_csv(CSV_FILE)

        if last_row >= len(df):
            time.sleep(1)
            continue

        row = df.iloc[last_row]
        last_row += 1

        required_cols = ["HR", "SpO2", "RR", "Temp", "BP"]

        if row[required_cols].isnull().any():
            print("Skipping row with NaN values")
            continue

        hr = int(row["HR"])
        spo2 = int(row["SpO2"])
        rr = int(row["RR"])
        temp = float(row["Temp"])
        sys, dia = map(int,row["BP"].split("/"))

        alerts = []

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

            msg = f"BED04 | HR:{hr} | SpO2:{spo2} | RR:{rr} | Temp:{temp} | BP:{sys}/{dia}\n" + "; ".join(alerts)

            # sock.sendto(msg.encode(), (BROADCAST_IP, PORT))
            # sock.sendto(msg.encode(), (BROADCAST_IP2, PORT))
            # print("Broadcasted:",msg)

        time.sleep(2)

    except Exception as e:
        print(e)


