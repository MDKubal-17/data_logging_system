import subprocess

# subprocess.Popen(["python","hl7.py"])
# subprocess.Popen(["python","convertion.py"])
subprocess.Popen(["python","sender.py"])
subprocess.Popen(["python","receiver.py"])
subprocess.Popen(["python","icu.py"])
print("Hospital Monitoring System Started")