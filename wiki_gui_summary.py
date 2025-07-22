
import wikipedia
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import threading  # 🧵 For concurrent voice + GUI output

# ✅ Voice output using pyttsx3 (runs in separate thread)
def speak_async(text):
    def run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # Optional: Adjust speech rate
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"🔇 Voice error: {e}")
    threading.Thread(target=run, daemon=True).start()  # 🔧 daemon=True ensures thread exits with GUI

# ✅ Fetch summary with error handling
def simple_summary(topic, bullet_count=5):
    try:
        wikipedia.set_lang("en")  # Ensure English articles
        return wikipedia.summary(topic, sentences=bullet_count)
    except wikipedia.exceptions.DisambiguationError as e:
        return "⚠️ Disambiguation error. Try one of these:\n- " + "\n- ".join(e.options[:5])
    except wikipedia.exceptions.PageError:
        return "❌ No page found for that topic. Please try another."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ GUI with simultaneous voice + text
def create_gui():
    def on_search():
        topic = entry.get().strip()
        if not topic:
            messagebox.showwarning("Input Error", "Please enter a topic.")
            return
        summary = simple_summary(topic)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, summary)
        speak_async(summary)  # 🔊 Launch voice in parallel

    window = tk.Tk()
    window.title("📘 Wikipedia Summary Tool")
    window.geometry("650x450")  # Optional: Set window size

    tk.Label(window, text="Enter a topic:", font=("Arial", 12)).pack(pady=10)

    entry = tk.Entry(window, width=50, font=("Arial", 12))
    entry.pack(pady=5)

    search_btn = tk.Button(window, text="Summarize", command=on_search, font=("Arial", 12))
    search_btn.pack(pady=10)

    text_box = tk.Text(window, wrap=tk.WORD, width=70, height=15, font=("Arial", 11))
    text_box.pack(pady=10)

    window.mainloop()

# 🚀 Launch the GUI
if __name__ == "__main__":
    create_gui()