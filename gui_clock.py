# Edward Mawuko Samlafo-Adams
# A GUI clock implemented with tkninter module



import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import time


class GUIClock(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Digital Clock')
        self.resizable(0, 0)
        self.geometry('1000x620')
        self['bg'] = 'lemon chiffon'

        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='lemon chiffon',
            foreground='red')

        # clock label
        self.clock_label = ttk.Label(
            self,
            text=self.time_string(),
            font=('Digital-7', 40))

        self.clock_label.pack()

        # Day display
        self.day_label = ttk.Label(self, text=self.day_string(), font=('Digital-7', 30))
        self.day_label.pack(pady=5)

        #display date
        self.date_label = ttk.Label(self, text=self.date_string(), font=('Digital-7', 30))
        self.date_label.pack(pady=5)

        #display timer start time
        self.start_label = ttk.Label(self, text="Timer Start: ")
        self.start_label.pack(pady=5)

        # display timer stop time
        self.stop_label = ttk.Label(self, text="Timer End: ")
        self.stop_label.pack(pady=5)

        #display duration
        self.duration_label = ttk.Label(self, text='Duration: ')
        self.duration_label.pack(pady=5)

        # timer button
        self.button = ttk.Button(self, text='Start Timer', command=self.toggle_timer)
        self.button.pack(pady=5)

        # location definition text field
        self.file_path_str = ttk.Entry(self, width=50)
        self.file_path_str.pack(pady=5)

        # save button
        self.save_button = ttk.Button(self, text="Save", command=self.save_file_as)
        self.save_button.pack(pady=5)

        self.timer_running = False

        #coundtdown

        countdown_frame = ttk.Frame(self)
        countdown_frame.pack(pady=20, side=tk.BOTTOM)

        self.countdown_label = ttk.Label(countdown_frame, text='Countdown', font=('Digital-7', 20))
        self.countdown_label.pack(pady=5)

        self.min_var = tk.StringVar()
        self.sec_var = tk.StringVar()

        countdown_minutes_frame = ttk.Frame(countdown_frame)
        countdown_minutes_frame.pack()

        self.countdown_minutes_label = ttk.Label(countdown_minutes_frame, text="Minutes:")
        self.countdown_minutes_label.pack(side=tk.LEFT)

        self.countdown_minutes = ttk.Entry(countdown_minutes_frame, textvariable=self.min_var, width=5)
        self.countdown_minutes.pack(side=tk.LEFT, padx=5)

        countdown_seconds_frame = ttk.Frame(countdown_frame)
        countdown_seconds_frame.pack()

        self.countdown_seconds_label = ttk.Label(countdown_seconds_frame, text="Seconds:")
        self.countdown_seconds_label.pack(side=tk.LEFT)

        self.countdown_seconds = ttk.Entry(countdown_seconds_frame, textvariable=self.sec_var, width=5)
        self.countdown_seconds.pack(side=tk.LEFT, padx=5)

        self.countdown_button = ttk.Button(countdown_frame, text='Start Countdown', command=self.start_countdown)
        self.countdown_button.pack(pady=5)

        self.countdown_end_label = ttk.Label(countdown_frame, text='', font=('Digital-7', 10))
        self.countdown_end_label.pack(pady=5)

        self.countdown_running = False


    def time_string(self):
        self.after(1000, self.update)
        return time.strftime('%H:%M:%S')

    def update(self):
        #update the label every 1 second

        self.clock_label.configure(text=self.time_string())

        # schedule another timer
        self.clock_label.after(1000, self.update)

    def day_string(self):
        return time.strftime('%A')

    def date_string(self):
        return time.strftime("%B %d, %Y")

    def toggle_timer(self):
        """Toggle between starting and stopping the timer"""
        if not self.timer_running:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        self.start_time = time.time()
        self.start_time_str = time.strftime('%H:%M:%S')
        self.start_label.config(text=f"Timer Start: {self.start_time_str}")
        self.timer_running = True
        self.button.config(text='Stop Timer')

    def stop_timer(self):
        self.stop_time = time.time()
        self.stop_time_str = time.strftime('%H:%M:%S')
        self.stop_label.config(text=f"Timer End: {self.stop_time_str}")
        self.button.config(text='Start Timer')
        duration = self.stop_time - self.start_time
        duration_str = time.strftime('%H:%M:%S', time.gmtime(duration))
        self.duration_label.config(text=f'Duration: {duration_str}')
        self.timer_running = False
        self.write_timer_to_file(
            f"Timer starts {self.start_time_str} and Timer ends {self.stop_time_str}. Duration is {duration_str}")

    def save_file_as(self):
        file_path = fd.asksaveasfilename(defaultextension=".txt")
        if file_path:
            self.file_path_str.delete(0, tk.END)
            self.file_path_str.insert(0, file_path)
            self.file_path = file_path

    def write_timer_to_file(self, text):
        self.file_path = self.file_path_str.get()
        if self.file_path:
            with open(self.file_path, "a") as file:
                file.write(text + "\n")
        else:
            print('File path is not specified')

    def start_countdown(self):
        try:
            minutes = int(self.min_var.get())
            seconds = int(self.sec_var.get())
        except ValueError:
            print("Invalid input for minutes or seconds")
            return

        self.countdown_seconds = minutes * 60 + seconds
        self.countdown_running = True
        self.countdown_button.config(text="Counting Down")
        self.update_countdown()

    def update_countdown(self):
        if self.countdown_running:
            if self.countdown_seconds > 0:
                minutes, seconds = divmod(self.countdown_seconds, 60)
                self.min_var.set(f"{minutes:02d}")
                self.sec_var.set(f"{seconds:02d}")
                self.countdown_seconds -= 1
                self.after(1000, self.update_countdown)
            else:
                self.countdown_running = False
                self.countdown_button.config(text="Start Countdown")
                self.min_var.set("00")
                self.sec_var.set("00")
                self.countdown_end_label.config(text="Countdown has ended")
                self.after(3000, self.clear_countdown_end_message)

    def clear_countdown_end_message(self):
        self.countdown_end_label.config(text='')


if __name__ == "__main__":
    clock = GUIClock()
    clock.mainloop()
