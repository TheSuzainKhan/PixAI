import customtkinter as ctk
from PIL import Image, ImageTk
import io
from api_helper import generate_image_from_prompt
import threading

# ---------- UI Setup ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PixAI - AI Image Generator App")
app.geometry("800x600") 

# ---------- Main Frames ----------
left_frame = ctk.CTkFrame(app, width=350)
left_frame.pack(side="left", fill="y", padx=20, pady=20)

right_frame = ctk.CTkFrame(app)
right_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

# ---------- Left Side Widgets ----------
ctk.CTkLabel(left_frame, text="Enter your prompt:", font=("Arial", 16, "bold")).pack(pady=(10,10))

prompt_entry = ctk.CTkEntry(left_frame, width=300, height=35, font=("Arial", 14))
prompt_entry.pack(pady=(0,20), padx=10)  # Added internal padding

ctk.CTkLabel(left_frame, text="Art Style:", font=("Arial", 14, "bold")).pack(pady=(0,5))

style_options = ["Realistic", "Cartoon", "Watercolor", "Digital Art", "Pixel Art"]
style_var = ctk.StringVar(value=style_options[0])
style_menu = ctk.CTkOptionMenu(left_frame, values=style_options, variable=style_var, width=200)
style_menu.pack(pady=(0,20))

status_label = ctk.CTkLabel(left_frame, text="", font=("Arial", 14))
status_label.pack(pady=(0,20))

# ---------- Generate Button ----------
def generate_threaded():
    threading.Thread(target=on_generate, daemon=True).start()

def on_generate():
    prompt = prompt_entry.get().strip()
    style = style_var.get()

    if not prompt:
        status_label.configure(text="⚠️ Please enter a prompt!", text_color="red")
        return

    full_prompt = f"{prompt}, {style} style"
    status_label.configure(text="🧠 Generating image... (~15-25 sec)", text_color="yellow")
    app.update()

    img_data = generate_image_from_prompt(full_prompt, token=None)

    if img_data:
        image = Image.open(io.BytesIO(img_data))
        image = image.resize((512, 512))
        img_tk = ImageTk.PhotoImage(image)

        image_label.configure(image=img_tk, text="")
        image_label.image = img_tk
        status_label.configure(text="✅ Image generated successfully!", text_color="lightgreen")
    else:
        status_label.configure(text="❌ Failed to generate image.", text_color="red")

generate_btn = ctk.CTkButton(left_frame, text="Generate Image", command=generate_threaded, width=200, height=40)
generate_btn.pack(pady=(0,15))

# ---------- Save Button ----------
def save_image():
    if hasattr(image_label, "image"):
        path = ctk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if path:
            image_label.image._PhotoImage__photo.write(path, format="png")
            status_label.configure(text=f"✅ Saved image to {path}", text_color="lightgreen")

save_btn = ctk.CTkButton(left_frame, text="Save Image", command=save_image, width=150, height=40)
save_btn.pack(pady=(0,15))

# ---------- Right Side (Image Display) ----------
image_label = ctk.CTkLabel(right_frame, text="Your generated image will appear here", font=("Arial", 14))
image_label.pack(expand=True)

# ---------- Run App ----------
app.mainloop()
