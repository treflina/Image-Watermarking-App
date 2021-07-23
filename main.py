from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import filedialog, messagebox
import os
window = Tk()
window.geometry("900x750+300+0")
window.resizable(width=True, height=True)
window.title("Watermarks App")


def set_path():
    filename = filedialog.askopenfilename(title='open')
    return filename
def open_img():
    x = set_path()
    img = Image.open(x)
    img.save("original_image.jpg")
    if img.size[0]>700 or img.size[1]>750:
        baseheight = 500
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save("image_to_watermark.jpg")
    else:
        img.save("image_to_watermark.jpg")
    im=Image.open("image_to_watermark.jpg")
    canvas.delete("all")
    canvas.image=ImageTk.PhotoImage(im)
    canvas.create_image(449,325,image=canvas.image)

def add_logo():
    try:
        im = Image.open("image_to_watermark.jpg")
        y = set_path()
        watermark = Image.open(y)
    except:
        canvas_id = canvas.create_text(400, 325, anchor="center", font=("Arial", 16, "normal"), fill="red")
        canvas.itemconfig(canvas_id, text="Select an image to watermark first.\n (use: 'OPEN IMAGE')")

    try:
        watermark = watermark.convert("RGBA")
    except:
        pass

    if im.size[0]/3<watermark.size[0]:
        basewidth = int(im.size[0]/3)
        wpercent = (basewidth/float(watermark.size[0]) )
        hsize = int((float(watermark.size[1]) * float(wpercent)))
        watermark = watermark.resize((basewidth,hsize), Image.ANTIALIAS)
        watermark.save("watermark.png")
        print(f"after:{watermark.size}")
    else:
        watermark.save("watermark.png")


    watermark_logo = Image.open("watermark.png")
    base_image = Image.new('RGBA', (im.size[0], im.size[1]), (0, 0, 0, 0))
    base_image.paste(im, (0, 0))
    base_image.paste(watermark_logo, (0,im.size[1]-watermark_logo.size[1]), mask=watermark_logo)
    base_image.save("finalimg.png")
    canvas.delete("all")
    canvas.image = ImageTk.PhotoImage(file="finalimg.png")
    canvas.create_image(449, 325, image=canvas.image)


def add_text():
    try:
        im = Image.open("image_to_watermark.jpg")
    except:
        canvas_id = canvas.create_text(400, 325, anchor="center", font=("Arial", 16, "normal"), fill="red")
        canvas.itemconfig(canvas_id, text="Select an image to watermark first.\n (use: 'OPEN IMAGE')")

    text=user_text.get()
    text_insert = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 40)
    text_insert.text((10, im.size[1]-50), text=text, fill="black", font=font)
    im.save("final_img.png")

    canvas.delete("all")
    canvas.image = ImageTk.PhotoImage(file="final_img.png")
    canvas.create_image(449, 325, image=canvas.image)

def save():

    image_to_save=Image.open("final_img.png")
    dimensions=Image.open("original_image.jpg")
    image_to_save.resize((dimensions.size[0], dimensions.size[1]),Image.ANTIALIAS)
    rgb_image_to_save = image_to_save.convert('RGB')
    f = filedialog.asksaveasfile(mode='wb', defaultextension=".jpg", filetypes=(("JPG file", "*.jpg"),("All Files", "*.*") ))
    if f:
        rgb_image_to_save.save(f)
        os.remove("image_to_watermark.jpg")
        os.remove("watermark.png")
        messagebox.showinfo("Saved", "The image has been successfully saved.")
    if f is None:
        return


btn = Button(window, text='OPEN IMAGE (.jpg)', command=open_img)
btn.grid(row=0, column=1, columnspan=3, ipadx=40, ipady=10)

btn_next=Button(window, text="SAVE", bg="green", fg="white", command=save)
btn_next.grid(row=0, column=4, ipadx=30, ipady=10)


canvas = Canvas(window, width=898, height=650)
canvas.grid(row=1, column=0, columnspan=5)

btn_text=Button(window, text='ADD TEXT', command=add_text)
btn_text.grid(row=2, column=3, ipadx=20, ipady=10)

btn_logo=Button(window, text='ADD LOGO (.jpg, .png)', command=add_logo)
btn_logo.grid(row=2, column=1, ipadx=20, ipady=10)

labeli=Label(window, text="or")
labeli.grid(row=2, column=2)

user_text = StringVar()
entry = Entry(window, textvariable=user_text, width=20)
entry.config(font=("Helvetica", 16, "normal"))
entry.insert(0,"Insert a text to add")
entry.grid(row=2, column=4)


window.mainloop()


