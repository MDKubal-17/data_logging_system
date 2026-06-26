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