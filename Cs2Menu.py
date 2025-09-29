import os
import customtkinter as ctk
import pymem
import tkinter as tk

# ========== CONFIGURATION ==========
APP_TITLE = "CS2 Health Trainer"
APP_SIZE = "600x300"

# Style
FONT = ("Helvetica", 14)
BTN_FONT = ("Helvetica", 13)
STATUS_FONT = ("Helvetica", 12)
PRIMARY_COLOR = "#1E90FF"
SUCCESS_COLOR = "lightgreen"
ERROR_COLOR = "red"
BG_COLOR = "black"

# Game settings
PROCESS_NAME = "cs2.exe"
HEALTH_ADDRESS = 0x5AF03B862D0
HEALTH_VALUE = 99999
# ===================================

# Try to attach to process
try:
    pm = pymem.Pymem(PROCESS_NAME)
except Exception as e:
    pm = None
    attach_error = str(e)

# Function to write health
def set_health():
    if pm is None:
        status.set("Process not attached")
        status_label.configure(text_color=ERROR_COLOR)
        return

    try:
        pm.write_int(HEALTH_ADDRESS, HEALTH_VALUE)
        status.set(f"Health set to {HEALTH_VALUE}")
        status_label.configure(text_color=SUCCESS_COLOR)
    except Exception as e:
        status.set(f"Error: {e}")
        status_label.configure(text_color=ERROR_COLOR)

# Specify the exact images in order
IMAGE_FILES = ["frame1.gif", "frame2.gif", "frame3.gif", "frame4.gif",
               "frame5.gif", "frame6.gif", "frame7.gif", "frame8.gif", "frame9.gif",
               "frame10.gif", "frame11.gif", "frame12.gif", "frame13.gif", "frame14.gif",
               "frame15.gif", "frame16.gif", "frame17.gif", "frame18.gif", "frame19.gif",
               "frame20.gif", "frame21.gif", "frame22.gif", "frame23.gif", "frame24.gif",
               "frame25.gif", "frame26.gif", "frame27.gif", "frame28.gif", "frame29.gif",
               "frame30.gif", "frame31.gif", "frame32.gif", "frame33.gif", "frame34.gif",
               "frame35.gif", "frame36.gif", "frame37.gif"]
IMAGE_FOLDER = "frames"  # folder containing these images

def load_images_in_order(folder, filenames):
    images = []
    for filename in filenames:
        img_path = os.path.join(folder, filename)
        if not os.path.exists(img_path):
            raise RuntimeError(f"Image file '{img_path}' not found.")
        img = tk.PhotoImage(file=img_path)
        images.append(img)
    return images

# UI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title(APP_TITLE)
app.geometry(APP_SIZE)
app.resizable(False, False)

# Load images for background animation in specified order
images = load_images_in_order(IMAGE_FOLDER, IMAGE_FILES)

# Background label
bg_label = tk.Label(app)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame_index = 1
def animate():
    global frame_index
    bg_label.configure(image=images[frame_index])
    frame_index = (frame_index + 1) % len(images)
    app.after(100, animate)  # 300ms delay = 0.3 seconds between frames

animate()

# UI frame on top of background
frame = ctk.CTkFrame(app, corner_radius=10, fg_color="red")  # semi-transparent black
frame.place(relx=0.5, rely=0.5, anchor="center")

status = ctk.StringVar(value="Ready")
status_label = ctk.CTkLabel(frame, textvariable=status, font=STATUS_FONT, text_color=SUCCESS_COLOR)
status_label.pack(pady=(10, 5))

ctk.CTkButton(
    frame,
    text=f"Set Health to {HEALTH_VALUE}",
    font=BTN_FONT,
    fg_color=PRIMARY_COLOR,
    hover_color="#104E8B",
    command=set_health
).pack(pady=10, padx=20)

# Disable button if process not attached
if pm is None:
    status.set(f"Could not attach to {PROCESS_NAME}")
    status_label.configure(text_color=ERROR_COLOR)
    for w in frame.winfo_children():
        try:
            w.configure(state="disabled")
        except Exception:
            pass

app.mainloop()
