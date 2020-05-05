import tkinter as t
import Personal_Assistant as jr

#To stop using button
def stop_ai():
    exit()

def GUI():
    window=t.Tk()
    window.title("Assistant")
    window.geometry('500x200')
    lbl1=t.Label(window,text="Your personal assistant to get your work done.")
    lbl1.grid(column=1, row=0)
    lbl2 = t.Label(window, text="Get your work done by pressing Call Assistant")
    lbl2.grid(column=1, row=1)
    lbl3=t.Label(window,text="")
    lbl3.grid(column=0,row=5)
    btn2 = t.Button(window, text="Call Assistant", bg="orange", fg="red", command=jr.main)
    btn2.grid(column=2, row=6)
    btn3=t.Button(window,text="Quit",bg="Red",fg="white",command=stop_ai)
    btn3.grid(column=2, row=3)
    window.mainloop()

if __name__ == "__main__":
    GUI()
