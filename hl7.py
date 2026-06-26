# from datetime import datetime, timedelta
# import random

# HL7_FILE = "patient_data.hl7"

# def generate_hl7_message(obs_time):
#     patient_id = "P12345"
#     patient_name = "Surekha^Sharma"
#     dob = "19990101"
#     gender = "F"

#     # heart_rate = random.randint(40, 180)
#     # systolic = random.randint(80, 200)
#     # diastolic = random.randint(70, 150)
#     # spo2 = random.randint(75, 100)
#     # temperature = round(random.uniform(34.5, 42.5), 1)
#     # respiratory_rate = random.randint(9, 29)

#     abnormal_case = random.random() < 0.15   # only 15% abnormal

#     if not abnormal_case:
#         # Normal values
#         heart_rate = random.randint(65, 95)
#         systolic = random.randint(110, 125)
#         diastolic = random.randint(70, 85)
#         spo2 = random.randint(96, 100)
#         temperature = round(random.uniform(36.4, 37.2), 1)
#         respiratory_rate = random.randint(12, 18)

#     else:
#         # Abnormal event
#         heart_rate = random.randint(40, 140)
#         systolic = random.randint(80, 180)
#         diastolic = random.randint(60, 120)
#         spo2 = random.randint(80, 94)
#         temperature = round(random.uniform(35.0, 40.5), 1)
#         respiratory_rate = random.randint(8, 28)

#     timestamp = obs_time.strftime("%Y%m%d%H%M%S")

#     return f"""MSH|^~\\&|MONITOR|ICU|EHR|HOSPITAL|{timestamp}||ORU^R01|MSG{timestamp}|P|2.3
# PID|1||{patient_id}||{patient_name}||{dob}|{gender}
# OBR|1|||VITALSIGNS|||{timestamp}
# OBX|1|NM|HR^Heart Rate||{heart_rate}|bpm
# OBX|2|NM|BP^Blood Pressure||{systolic}/{diastolic}|mmHg
# OBX|3|NM|SPO2^Oxygen Saturation||{spo2}|%
# OBX|4|NM|TEMP^Body Temperature||{temperature}|C
# OBX|5|NM|RR^Respiratory Rate||{respiratory_rate}|breaths/min
# """

# start_time = datetime.now()
# num_records = 25   # readings

# with open(HL7_FILE, "a") as f:
#     for i in range(num_records):
#         obs_time = start_time + timedelta(minutes=0.2 * i)
#         f.write(generate_hl7_message(obs_time))
#         f.write("\n")


from datetime import datetime
import random
import time

HL7_FILE = "patient_data.hl7"

def generate_hl7_message():

    patient_id = "P12345"
    patient_name = "Surekha^Sharma"
    dob = "19990101"
    gender = "F"

    abnormal_case = random.random() < 0.15

    if not abnormal_case:
        heart_rate = random.randint(65,95)
        systolic = random.randint(110,125)
        diastolic = random.randint(70,85)
        spo2 = random.randint(96,100)
        temperature = round(random.uniform(36.4,37.2),1)
        respiratory_rate = random.randint(12,18)
    else:
        heart_rate = random.randint(40,140)
        systolic = random.randint(80,180)
        diastolic = random.randint(60,120)
        spo2 = random.randint(80,94)
        temperature = round(random.uniform(35,40.5),1)
        respiratory_rate = random.randint(8,28)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    return f"""MSH|^~\\&|MONITOR|ICU|EHR|HOSPITAL|{timestamp}||ORU^R01|MSG{timestamp}|P|2.3
PID|1||{patient_id}||{patient_name}||{dob}|{gender}
OBR|1|||VITALSIGNS|||{timestamp}
OBX|1|NM|HR^Heart Rate||{heart_rate}|bpm
OBX|2|NM|BP^Blood Pressure||{systolic}/{diastolic}|mmHg
OBX|3|NM|SPO2^Oxygen Saturation||{spo2}|%
OBX|4|NM|TEMP^Body Temperature||{temperature}|C
OBX|5|NM|RR^Respiratory Rate||{respiratory_rate}|breaths/min
"""

print("HL7 Generator Started")

while True:

    with open(HL7_FILE,"a") as f:
        f.write(generate_hl7_message())
        f.write("\n")

    time.sleep(3)