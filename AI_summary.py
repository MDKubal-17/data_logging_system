
#==========================
#Ai summary
#==========================
import google.generativeai as genai
from tkinter import messagebox
import tkinter as tk
from tkinter import scrolledtext
from IPython.display import Markdown
from collections import deque

def show_formatted_analysis(title, content):
    # Create a popup window
    result_window = tk.Toplevel()
    result_window.title(title)
    result_window.geometry("500x400")
    
    # Header Label
    header = tk.Label(result_window, text="Clinical Insights", font=("Helvetica", 14, "bold"), pady=10)
    header.pack()

    # Scrollable Text Area
    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, font=("Consolas", 11), padx=10, pady=10)
    text_area.insert(tk.INSERT, content)
    text_area.configure(state='disabled') # Make it read-only
    text_area.pack(expand=True, fill='both')

    # Close Button
    btn = tk.Button(result_window, text="Dismiss", command=result_window.destroy, width=15)
    btn.pack(pady=10)


def run_ai_analysis(hr_buf, spo2_buf, temp_buf, sys_buf, dia_buf, model):
    try:
        # Convert deques to lists
        hr_list = list(hr_buf)
        if not hr_list:
            messagebox.showwarning("AI Error", "No data visible on timeline to analyze.")
            return

        spo2_list = list(spo2_buf)
        temp_list = list(temp_buf)
        
        # Calculations
        avg_hr = sum(hr_list) / len(hr_list)
        min_spo2 = min(spo2_list)
        max_temp = max(temp_list)
        current_bp = f"{sys_buf[-1]}/{dia_buf[-1]}" if sys_buf else "N/A"

         # --- Professional Prompting ---
        # We ask for Markdown formatting to make the AI output structured
        prompt = f"""
        Role: Clinical Data Analyst
        Task: Analyze the following patient vitals:
        
        DATA SUMMARY:
        - Heart Rate: Avg {avg_hr:.1f} BPM (Latest: {hr_list[-1]})
        - SpO2: Min {min_spo2}% (Latest: {spo2_list[-1]}%)
        - Temp: Max {max_temp:.1f}°C
        - BP: {current_bp}
        
        REQUIREMENTS:
        1. Use a 'STATUS' header (e.g., STABLE or CRITICAL).
        2. Provide a 3-sentence summary of trends.
        3. Identify any physiological correlations between SpO2 and HR.
        """

        response = model.generate_content(prompt)
        
        # --- Formatted Display ---
        # Construct the final display string
        display_text = f"ANALYSIS REPORT\n{'='*20}\n\n{response.text}"
        
        # Call our custom popup instead of messagebox.showinfo
        show_formatted_analysis("AI Live Timeline Analysis", display_text)

    except Exception as e:
        messagebox.showerror("AI Error", f"Buffer Analysis Failed: {str(e)}")