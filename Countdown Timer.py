import tkinter as tk
from tkinter import messagebox
import time
import os
import pickle

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer and Stopwatch")

        self.load_config()

        self.running = False
        self.paused = False
        self.time_left = 0
        self.start_time = 0
        self.pause_time = 0
        self.laps = []

        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT)

        self.lap_button = tk.Button(root, text="Lap", command=self.lap)
        self.lap_button.pack(side=tk.LEFT)

        self.switch_button = tk.Button(root, text="Switch to Countdown", command=self.switch_mode)
        self.switch_button.pack(side=tk.LEFT)

        self.lap_listbox = tk.Listbox(root)
        self.lap_listbox.pack(fill=tk.BOTH, expand=True)

        self.update_time()

    def update_time(self):
        if self.running:
            if not self.paused:
                if self.mode == "stopwatch":
                    elapsed_time = int(time.time() - self.start_time)
                    self.display_time(elapsed_time)
                elif self.mode == "countdown":
                    if self.time_left > 0:
                        elapsed_time = int(time.time() - self.start_time)
                        remaining_time = self.time_left - elapsed_time
                        if remaining_time <= 0:
                            self.running = False
                            remaining_time = 0
                            self.play_sound()
                            messagebox.showinfo("Time's up", "The countdown has finished!")
                        self.display_time(remaining_time)
                    else:
                        self.running = False

        self.root.after(1000, self.update_time)

    def display_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.start_time = time.time()
            if self.mode == "countdown" and self.time_left == 0:
                self.set_countdown_time()
            self.save_config()

    def stop(self):
        if self.running:
            self.running = False
            if self.mode == "countdown":
                elapsed_time = int(time.time() - self.start_time)
                self.time_left -= elapsed_time
            self.save_config()

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_time = time.time()
        elif self.running and self.paused:
            self.paused = False
            self.start_time += time.time() - self.pause_time
        self.save_config()

    def reset(self):
        self.running = False
        self.paused = False
        self.laps = []
        self.lap_listbox.delete(0, tk.END)
        if self.mode == "stopwatch":
            self.time_label.config(text="00:00:00")
        elif self.mode == "countdown":
            self.time_left = 0
            self.time_label.config(text="00:00:00")
        self.save_config()

    def lap(self):
        if self.mode == "stopwatch" and self.running:
            elapsed_time = int(time.time() - self.start_time)
            self.laps.append(elapsed_time)
            self.lap_listbox.insert(tk.END, f"Lap {len(self.laps)}: {elapsed_time // 3600:02}:{(elapsed_time % 3600) // 60:02}:{elapsed_time % 60:02}")

    def switch_mode(self):
        self.running = False
        self.paused = False
        self.laps = []
        self.lap_listbox.delete(0, tk.END)
        if self.mode == "stopwatch":
            self.mode = "countdown"
            self.switch_button.config(text="Switch to Stopwatch")
            self.time_label.config(text="00:00:00")
        else:
            self.mode = "stopwatch"
            self.switch_button.config(text="Switch to Countdown")
            self.time_label.config(text="00:00:00")
        self.save_config()

    def set_countdown_time(self):
        def set_time():
            try:
                hours = int(hours_entry.get())
                minutes = int(minutes_entry.get())
                seconds = int(seconds_entry.get())
                self.time_left = hours * 3600 + minutes * 60 + seconds
                set_time_window.destroy()
                self.start()
                self.save_config()
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers.")

        set_time_window = tk.Toplevel(self.root)
        set_time_window.title("Set Countdown Time")

        tk.Label(set_time_window, text="Hours:").pack()
        hours_entry = tk.Entry(set_time_window)
        hours_entry.pack()

        tk.Label(set_time_window, text="Minutes:").pack()
        minutes_entry = tk.Entry(set_time_window)
        minutes_entry.pack()

        tk.Label(set_time_window, text="Seconds:").pack()
        seconds_entry = tk.Entry(set_time_window)
        seconds_entry.pack()

        tk.Button(set_time_window, text="Set Time", command=set_time).pack()

    def play_sound(self):
        try:
            import winsound
            winsound.Beep(1000, 1000)
        except ImportError:
            print("Sound not supported on this platform.")

    def save_config(self):
        config = {
            'mode': self.mode,
            'time_left': self.time_left,
        }
        with open('config.pkl', 'wb') as f:
            pickle.dump(config, f)

    def load_config(self):
        if os.path.exists('config.pkl'):
            with open('config.pkl', 'rb') as f:
                config = pickle.load(f)
                self.mode = config.get('mode', 'stopwatch')
                self.time_left = config.get('time_left', 0)
        else:
            self.mode = 'stopwatch'
            self.time_left = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
