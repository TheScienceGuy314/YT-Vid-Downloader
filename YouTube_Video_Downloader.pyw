# This imports the time, threading, and tkinter modules.
from threading import Thread
from time import sleep
from tkinter import Tk, StringVar, IntVar, Label, CENTER, DISABLED, Entry, NORMAL, Button, Radiobutton

# This sets the root window, the link variable, and the intVar variable.
root, link, intVar = Tk(), StringVar(), IntVar()

# This sets the icon, size, and title of the root window.
root.iconbitmap(r"C:\Users\School\Pictures\YubTub Favicon.ico")
root.minsize(width=550, height=375)
root.geometry('550x375')
root.resizable(False, False)
root.title("YubTub Video Downloader")

# This creates a label widget with the text "YubTub Video Downloading Mechanism" in the center of the root window.
Label(root, text="YubTub Video Downloading Mechanism", font="arial 20 bold").place(anchor=CENTER, relx=0.5, rely=0.3)
# This creates a label widget with the text "Insert Link Below" in the center of the root window.
label1 = Label(root, text="Insert Link Below", font="arial 15 bold")
label1.place(anchor=CENTER, relx=0.5, rely=0.4)

# This creates an entry widget where the user can input a link, and the text in the entry widget is linked to the
# link variable.
subLink = Entry(root, width=70, textvariable=link, exportselection=False)
subLink.place(anchor=CENTER, relx=0.5, rely=0.465)


# This defines a function that creates a thread that runs the Downloader_Inator function with an input of True.
def threading1():
    thread1 = Thread(target=Downloader_Inator(True))
    thread1.start()


# This defines a function that creates a thread that runs the Downloader_Inator function with an input of False.
def threading2():
    thread2 = Thread(target=Downloader_Inator(False))
    thread2.start()


# This defines a function that creates a thread that runs the progressBar function.
def threading3():
    thread3 = Thread(target=progressBar)
    thread3.start()


# This defines a function that checks the intVar variable. If the value is 0, it runs the threading1 function.
# Otherwise, it runs the threading2 function.
def videoFormat():
    if intVar.get() == 0:
        threading1()
    else:
        threading2()


# This defines a function that disables the button1 and subLink widgets, and changes the text in label1 to 
# "DOWNLOADING" plus whatever the title of the video is. It also has a loop that repeats 4 times and adds a dot after
# "DOWNLOADING" each time it loops. 
def progressBar():
    button1["state"] = DISABLED
    subLink["state"] = DISABLED
    label1["text"] = "DOWNLOADING"
    while incomplete:
        for repeats in range(4):
            dots = repeats * "."
            title = url.title
            label1["text"] = "DOWNLOADING " + title + dots
            if not incomplete:
                break
            sleep(1)
        label1["text"] = "Download Complete"


# This defines a function that takes in a name. It then creates a list of illegal characters and another list with
# the name. It then loops through the name list and removes any illegal characters. Finally, it returns the name
# without any illegal characters.
def allowedFileChars(name):
    illegalChars = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    chars = list(name)
    for letters in chars:
        for illChars in illegalChars:
            if letters == illChars:
                chars.remove(letters)
    safeName = ""
    for totalChars in chars:
        safeName += totalChars
    return safeName


# This defines a function that downloads a video. It first checks if isDASH is True. If it is, it downloads the video
# in 1080p and the audio in 160kbps. If not, it downloads the video in 720p with included audio. It also has a
# try/except/finally statement that checks for illegal characters in the title and renames the video if there are
# any. It also makes a folder to store the DASH tracks (The audio and video are downloaded separately as a byproduct
# of using DASH).
def Downloader_Inator(isDASH):
    try:
        # noinspection PyGlobalUndefined
        global url, progressive, incomplete
        from pytube import YouTube
        url = YouTube(link.get())
        incomplete = True
        threading3()
        if isDASH:
            # noinspection PyBroadException
            try:
                url.streams.filter(resolution="1080p", progressive=False).first().download(
                    output_path=r"C:\Users\School\Downloads",
                    filename="Video.mp4")
                url.streams.filter(abr="160kbps", progressive=False).first().download(
                    output_path=r"C:\Users\School\Downloads",
                    filename="Audio.mp3")
                progressive = False
            except:
                url.streams.get_highest_resolution().download(output_path=r"C:\Users\School\Downloads")
                progressive = True
            finally:
                if not progressive:
                    from os import path, makedirs, replace
                    newDir = "C:\\Users\\School\\Downloads\\" + allowedFileChars(url.title)
                    if not path.exists(newDir):
                        makedirs(newDir)

                    replace("C:\\Users\\School\\Downloads\\Video.mp4",
                            "C:\\Users\\School\\Downloads\\" + allowedFileChars(url.title) + "\\Video.mp4")
                    replace("C:\\Users\\School\\Downloads\\Audio.mp3",
                            "C:\\Users\\School\\Downloads\\" + allowedFileChars(url.title) + "\\Audio.mp3")
        else:
            # This downloads the video if isDASH is False.
            url.streams.get_highest_resolution().download(output_path=r"C:\Users\School\Downloads")

    finally:
        # This enables the button1 and subLink widgets, changes the text in label1 to "Download Complete!",
        # and changes it back to "Insert Link Below" after 5 seconds.
        button1["state"] = NORMAL
        subLink["state"] = NORMAL
        incomplete = False
        label1["text"] = "Download Complete!"
        sleep(5)
        label1["text"] = "Insert Link Below"


# This creates a button widget that runs the videoFormat function when clicked.
button1 = Button(root, text="Download Video", font="arial 15 bold", padx=2, command=videoFormat)
button1.place(anchor=CENTER, relx=0.5, rely=0.575)

# This creates radio buttons that the user can select to choose between Dash and Progressive. Progressive is selected
# by default.
radioButton1 = Radiobutton(root, text="Dash", variable=intVar, value=0)
radioButton1.place(relx=0.425, rely=0.65)
radioButton2 = Radiobutton(root, text="Progressive", variable=intVar, value=1)
radioButton2.select()
radioButton2.place(relx=0.425, rely=0.7)

# This creates a button widget that destroys the root window when clicked.
Button(root, text="Exit Program", command=root.destroy, font="arial 10 bold").place(anchor=CENTER, relx=0.5, rely=0.825)
root.mainloop()
