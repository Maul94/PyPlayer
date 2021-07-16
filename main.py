from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
from tinytag import TinyTag
from random import randint
import os
import pygame
import ntpath
import time
from mutagen.mp3 import MP3

# Function durasi song
def song_time():
    global song_duration, convert_song_duration, paused, timeloop, repeated, current_song

    current_time = pygame.mixer.music.get_pos()/1000
    convert_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    # Get Currently playing song
    sourcesong = sourcelist.activate(current_song)
    sourcesong = sourcelist.get(ACTIVE)

    # load sourcesong mutagen
    song_mut = MP3(sourcesong)
    song_duration = song_mut.info.length
    convert_song_duration = time.strftime('%H:%M:%S', time.gmtime(song_duration))

    current_time +=1

    if int(song_slider.get()) == int(song_duration):
        song_slider.config(value=0)
        time_label.config(text="00:00:00")
        pygame.mixer.music.stop()
        PlayBtn['image'] = PlayBtnImg
        paused = False

        if repeated == 0 and current_song+1 == playlist.size():
            pass
        elif repeated == 2:
            play('<Double-1>')
        else:
            next()

    elif int(song_slider.get()) == int(current_time) or paused:
        song_slider.config(to=int(song_duration), value=int(current_time))
        time_label.config(text=convert_current_time)
        timeloop = time_label.after(1000, song_time)
    else:
        convert_current_time = time.strftime('%H:%M:%S', time.gmtime(int(song_slider.get())))
        song_slider.config(to=int(song_duration), value=int(song_slider.get()+1))
        time_label.config(text=convert_current_time)
        timeloop = time_label.after(1000, song_time)

    print('song time : '+convert_current_time)
                
# Function add song
def add_song():
    songs = filedialog.askopenfilenames(initialdir='mp3/', title='Pilih lagu', filetypes=(('mp3 Files', '*.mp3'), ('wav Files', '*.wav')))
    
    for song in songs:
        sourcelist.insert(END, song)
        
        #Get filename
        os.path.dirname(os.path.abspath(song))
        song = ntpath.basename(song)
        song = song.replace(".mp3", "")

        playlist.insert(END, song)

# Function play song
def play(event):
    if playlist.size() > 0:
        global paused, timeloop, current_song

        current_song = sum(playlist.curselection())

        sourcesong = sourcelist.activate(current_song)
        sourcesong = sourcelist.get(ACTIVE)

        playlist.select_clear(0, 'end')
        playlist.select_set(ACTIVE)

        pygame.mixer.music.load(sourcesong)
        pygame.mixer.music.play(loops=0)

        if timeloop != None:
            time_label.after_cancel(timeloop)
            timeloop = None

        song_time()

        song_slider.config(value=0, state=NORMAL,takefocus=1)

        time_label.config(text="00:00:00")
        PlayBtn['image'] = PauseBtnImg
        paused = False
        
        print('playing now : '+playlist.get(ACTIVE))
        TitleSong.config(text=playlist.get(ACTIVE))
        duration_label.config(text=convert_song_duration)
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di putar")

# Function pause song
def pause(is_paused):
    if playlist.size() > 0:
        global paused, timeloop

        if is_paused:
            pygame.mixer.music.unpause()
            PlayBtn['image'] = PauseBtnImg      
            paused = False
            song_slider.config(state=NORMAL,takefocus=1)

            song_time()
        else:
            if timeloop != None:
                pygame.mixer.music.pause()
                PlayBtn['image'] = PlayBtnImg
                paused = True
                song_slider.config(state=DISABLED,takefocus=0)
                time_label.after_cancel(timeloop)
                timeloop = None
            else:
                play('<Double-1>')
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di putar")

# Function previous song
def prev():
    if playlist.size() > 0:
        global timeloop, current_song
        
        if timeloop != None:
            prevsong = current_song
            if prevsong != 0:
                prevsong = prevsong-1
            else:
                prevsong = playlist.size()-1

            playlist.selection_clear(0, END)
            playlist.selection_set(prevsong, last=None)
            
            playlist.activate(prevsong)
            sourcelist.activate(prevsong)

            play('<Double-1>')
        else:
            play('<Double-1>')
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di putar")

# Function next song       
def next():
    if playlist.size() > 0:
        global timeloop, current_song
        
        if timeloop != None:
            nextsong = current_song

            if nextsong+1 != playlist.size():
                nextsong = nextsong+1
            else:
                nextsong = 0

            playlist.selection_clear(0, END)
            playlist.selection_set(nextsong, last=None)

            playlist.activate(nextsong)
            sourcelist.activate(nextsong)

            play('<Double-1>')
        else:
            play('<Double-1>')
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di putar")

def repeat():
    global repeated
    if repeated==0:
        RepeatBtn.config(bg='light grey')
        repeated = 1
    elif repeated==1:
        RepeatBtn['image'] = Repeat1BtnImg      
        repeated = 2
    elif repeated==2:
        RepeatBtn['image'] = RepeatBtnImg
        RepeatBtn.config(bg=defaultbg)
        repeated = 0

def delete():
    if playlist.size() > 0:
        global timeloop, paused, current_song

        if current_song == sum(playlist.curselection()):
            pygame.mixer.music.stop()

            if timeloop != None:
                time_label.after_cancel(timeloop)
                timeloop = None

            PlayBtn['image'] = PlayBtnImg
            paused = False

            TitleSong.config(text="_ _ _ _ _ _ _ _ _ _ _ _")
            song_slider.config(state=DISABLED, takefocus=0, value=0)
            time_label.config(text="00:00:00")
            duration_label.config(text="00:00:00")


        print(current_song)
        print(sum(playlist.curselection()))
        if current_song > sum(playlist.curselection()):
            current_song = current_song - 1
            print('lebih besar')

        print(current_song)
        nextsong = sum(playlist.curselection())

        if nextsong+1 != playlist.size():
            pass
        else:
            nextsong -= 1

        playlist.select_clear(ACTIVE)
        sourcelist.select_clear(ACTIVE)

        playlist.delete(ACTIVE)
        sourcelist.delete(ACTIVE)

        playlist.selection_set(nextsong, last=None)

        playlist.activate(nextsong)
        sourcelist.activate(nextsong)
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di hapus")

def delete_all():
    if playlist.size() > 0:
        global timeloop, paused

        pygame.mixer.music.stop()

        if timeloop != None:
            time_label.after_cancel(timeloop)
            timeloop = None

        PlayBtn['image'] = PlayBtnImg
        paused = False

        TitleSong.config(text="_ _ _ _ _ _ _ _ _ _ _ _")
        song_slider.config(state=DISABLED, takefocus=0, value=0)
        time_label.config(text="00:00:00")
        duration_label.config(text="00:00:00")

        playlist.delete(0, END)
        sourcelist.delete(0, END)
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di hapus")

# Function slider
def slider(event):
    if playlist.size() > 0:
        global timeloop, paused, current_song

        if paused != True:
            current_song

            sourcesong = sourcelist.activate(current_song)
            sourcesong = sourcelist.get(ACTIVE)

            playlist.select_clear(0, 'end')
            playlist.select_set(ACTIVE)

            pygame.mixer.music.load(sourcesong)
            pygame.mixer.music.play(loops=0, start=int(song_slider.get()))

            if timeloop != None:
                time_label.after_cancel(timeloop)
                timeloop = None

            song_time()
    else:
        messagebox.showerror("Error", "Tidak ada lagu untuk di putar")

# Setting Volume
def volume(event):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    volume_frame.config(text="Volume : %i" % int (current_volume * 100))
    # volume_label.config(text =int (current_volume * 100))

# Function about PyPlayer
def about():
    messagebox.showinfo("Tentang PyPlayer", "PyPlayer merupakan Project Akhir Kelompok Q \nyang di bangun menggunakan Bahasa Pemrograman Python \n\nKelompok Q : \n1. Putra Edi Sujito \n2. Maulana Akhmady Arief \n3. Fatmil Dwi Pambudi \n4. Yogiek Indra Kurniawan")

# Function Exit Program
def menuExit():
    menuExit = messagebox.askyesno("PyPlayer","Do you want to exit ?")
    if menuExit>0:
        pygame.mixer.music.stop()
        playlist.select_clear(ACTIVE)
        app.destroy()
        return

def ubahAbu():
    playlist.configure(bg='grey')

def ubahHitam():
    playlist.configure(bg='black')

def ubahMerah():
    playlist.configure(bg='red')

def ubahBiru():
    playlist.configure(bg='blue')

# ROOT_DIR untuk mengetahui lokasi project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Tk()
app.title("PyPlayer")
app.call('wm', 'iconphoto', app._w, PhotoImage(file=ROOT_DIR+'\\assets\\icon.png'))
app.geometry("410x600")
defaultbg = app.cget('bg')

# Inisialisasi pygame mixer, module memutar lagu
pygame.mixer.init()

# Inisialisasi
global puased, song_duration, convert_song_duration, timeloop, repeated, current_song
current_song = None
repeated = 0
paused = False
timeloop = None

# =============================================
# Create PyPlayer Info Song Frame
info_frame = Frame(app)
info_frame.pack(pady=20, ipady=5)

TitleSong = Label(info_frame, text="_ _ _ _ _ _ _ _ _ _ _ _", font='bold 10', wraplength=300, justify=CENTER)
TitleSong.grid(row=0, column=0, columnspan=2)

# Create Song slider
slider_frame = Frame(app)
slider_frame.pack(pady=10)

time_label = Label(slider_frame, text="00:00:00")
song_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL,command=slider, value=0, length=250, state=DISABLED, takefocus=0)
duration_label = Label(slider_frame, text="00:00:00")

time_label.grid(row=0, column=0, padx=5)
song_slider.grid(row=0, column=1, padx=5)
duration_label.grid(row=0, column=2, padx=5)

# Create PyPlayer Control Frame
control_frame = Frame(app)
control_frame.pack()

# Create PyPlayer Playlist display
playlist = Listbox(app, bg='black', fg='white', selectbackground='grey', width=65)
playlist.pack(side = LEFT, fill = BOTH)

scrollbar = Scrollbar(app)
scrollbar.pack(side = RIGHT, fill = BOTH)

playlist.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = playlist.yview)

# Create SourceList, untuk menyimpan lokasi file lagu
sourcelist = Listbox()
sourcelist.pack_forget()

# Double click lagu di playlist, untuk memutar lagi
playlist.bind('<Double-1>', play)

# PyPlayer Control Button Images
PrevBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\back.png')
PauseBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\pause.png')
PlayBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\play.png')
NextBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\forward.png')
RepeatBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\repeat.png')
Repeat1BtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\repeat1.png')
DelBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\del.png')
DelAllBtnImg = PhotoImage(file=ROOT_DIR+'\\assets\\del_all.png')

# Create PyPlayer Control Buttons
PrevBtn = Button(control_frame, image=PrevBtnImg, borderwidth=0, command=prev)
PlayBtn = Button(control_frame, image=PlayBtnImg, borderwidth=0, command=lambda: pause(paused))
NextBtn = Button(control_frame, image=NextBtnImg, borderwidth=0, command=next)
RepeatBtn = Button(control_frame, image=RepeatBtnImg, borderwidth=0, command=repeat)
DelAllBtn = Button(control_frame, image=DelAllBtnImg, borderwidth=0, command=delete_all)
DelBtn = Button(control_frame, image=DelBtnImg, borderwidth=0, command=delete)

PrevBtn.grid(row=0, column=0, padx=10, rowspan=2)
PlayBtn.grid(row=0, column=1, padx=10, rowspan=2)
NextBtn.grid(row=0, column=2, padx=10, rowspan=2)
RepeatBtn.grid(row=0, column=3, padx=10, rowspan=2)
DelAllBtn.grid(row=0, column=5, padx=10)
DelBtn.grid(row=1, column=5, padx=10)

#Volume label Frame
volume_frame = LabelFrame(control_frame, text="Volume : 100")
volume_frame.grid(row=0, column=4, padx=10, rowspan=2)

# Volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# ========= Create Menu =========
AppMenu = Menu(app)
app.config(menu=AppMenu)

# Add Song Menu
AddSongMenu = Menu(AppMenu, tearoff=0)
AppMenu.add_cascade(label='Option', menu=AddSongMenu)
AddSongMenu.add_command(label='Add song to playlist', command=add_song)
AddSongMenu.add_command(label='Exit', command=menuExit)

# Ubah Background
changeBack= Menu(AppMenu,tearoff=0)
AppMenu.add_cascade(label='Playlist Background', menu=changeBack)
changeBack.add_command(label='Abu-Abu', command=ubahAbu)
changeBack.add_command(label='Hitam', command=ubahHitam)
changeBack.add_command(label='Merah', command=ubahMerah)
changeBack.add_command(label='Biru', command=ubahBiru)

# Menu Help
Help = Menu(AppMenu, tearoff=0)
AppMenu.add_cascade(label='Help', menu=Help)
Help.add_command(label='About', command=about)

app.mainloop()