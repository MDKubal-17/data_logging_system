import serial
import csv
import os
import time
from datetime import datetime

# --- Configuration ---
PORT = 'COM9'
BAUD = 115200
CSV_FILE = "patient_data.csv"
TIMEOUT = 0.1  # Short timeout to allow "alive" dots to print

print(f"--- MCU Real-Time Logger Starting on {PORT} ---")

try:
    # Adding a timeout is crucial so readline() doesn't hang forever
    ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    ser.reset_input_buffer()
    print("Connection Successful. Waiting for data...")
except Exception as e:
    print(f"FATAL ERROR: Could not open {PORT}. {e}")
    print("Check if PuTTY or another Serial Monitor is using the port.")
    exit()

def save_to_csv(data_row):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "PatientID", "HR", "BP", "SpO2", "Temp", "RR"])
        writer.writerow(data_row)

while True:
    try:
        # 1. Read a full line from the buffer
        line_raw = ser.readline()
        
        if line_raw:
            # 2. Decode and Clean
            line = line_raw.decode('utf-8').strip()
            if not line:
                continue
                
            print(f"\n[RAW] {line}") # Debugging feedback
            
            # 3. Parse Fields (Expected: HR,SPO2,RR,TEMP,SYS,DIA)
            fields = line.split(",")
            
            if len(fields) >= 6:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Mapping fields based on your MCU UARTprintf order
                hr   = fields[0]
                spo2 = fields[1]
                rr   = fields[2]
                temp = fields[3]
                bp   = f"{fields[4]}/{fields[5]}" # Combine Systolic/Diastolic
                
                # 4. Prepare and Save Row
                row = [timestamp, "P101", hr, bp, spo2, temp, rr]
                save_to_csv(row)
                
                print(f"[{timestamp}] LOGGED: HR:{hr} | SpO2:{spo2}% | BP:{bp} | Temp:{temp}")
            else:
                print(f" [!] Malformed Data: Expected 6 fields, got {len(fields)}")
        
        else:
            # No data received during the timeout period
            print(".", end="", flush=True)
            
    except UnicodeDecodeError:
        print("\n [!] Decode Error: Received garbage bytes. Check Baud rate/Wiring.")
    except KeyboardInterrupt:
        print("\nStopping Logger...")
        ser.close()
        break
    except Exception as e:
        print(f"\n [!] Unexpected Error: {e}")