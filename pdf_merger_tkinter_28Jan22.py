import datetime
from tkinter import *
import os
import tkinter.messagebox
import PyPDF2 as pd
from PyPDF2 import PdfFileMerger
import logging
import datetime

# Logging info
formatter= logging.Formatter('%(asctime)s:%(levelname)s: %(name)s : %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler=logging.FileHandler('main.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Initializing Tkinter Window
root= Tk()
root.geometry('900x433')
root.title('File Explorer')
root.minsize(200,100)

name_var= StringVar()


def error_msg(msg):
    '''
    Function to show messagebox.
    '''
    tkinter.messagebox.showinfo("Error Occurred.", msg)


def file(x):
    '''
    :param x: path which we enter
    :return: list of files on path x i.e. res
    '''
    if os.path.exists(x):
        res=[]
        for r,d,f in os.walk(x):
            for l in f:
                l=str(l)
                if l.endswith('.pdf'):
                    res.append(str(os.path.join(str(r),l)))
        return res
    else:
        logger.error(f'User has entered a wrong path {x} .')
        error_msg('Enter a valid path')
        name_var.set("")
        return

def submit():
    '''
    Function which show file names on the path.
    '''

    name = name_var.get()
    logger.info(f'{name} has been searched')
    res= file(name)

    if type(res)==list:
        if len(res)!=0:
            scrollbar = Scrollbar(root)
            mylist = Listbox(root, yscrollcommand=scrollbar.set)
            F2 = Frame(root)
            F2.pack(side=LEFT)
            side_res = Label(F2, text='Here is the Result')
            side_res.pack(side=LEFT)

            mylist = Listbox(root,height = 15, width = 40,  yscrollcommand=scrollbar.set)

            # Printing filenames on the screen
            for i in res:

                mylist.insert(END, str(i))
                logger.info(f'file {i} is found on path {name}')
            mylist.pack(side=LEFT, fill=BOTH)
            scrollbar.pack(side=LEFT, fill=Y)
            scrollbar.config(command=mylist.yview)
            F4= Frame(root)
            F4.pack(side=BOTTOM)
            b1= Button(F4,text='Want to merge all files',padx=5,command= lambda : merge(res))
            b2 = Button(F4, text='Reset',padx=5, command=lambda: reset(mylist,b1,b2,scrollbar,side_res,F2,F4))
            b1.pack(side=LEFT)
            b2.pack(side=BOTTOM)

        else:
            error_msg('No file is found on this path')
            logger.error(f'No file is found on the path {name}')
            name_var.set("")



def reset(mylist,b1,b2,scrollbar,side_res,F2,F4):
    '''
    Function to reset everything.
    '''

    logger.info('Reset button has been clicked')
    mylist.pack_forget()
    name_var.set("")
    b1.pack_forget()
    b2.pack_forget()
    scrollbar.pack_forget()
    side_res.pack_forget()
    F2.pack_forget()
    F4.pack_forget()
    logger.info('Everything has been resetted.')


def merge(res):
    '''
    Function to print the merged file content.
    '''
    logger.info('Merge has been clicked.')

    # merging all the pdf files
    merger = PdfFileMerger()
    for pdf in res:
        merger.append(pdf)

    date= datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    finalres= f'D:/final{date}.pdf'
    merger.write(finalres)
    merger.close()


    mer=Tk()
    mer.geometry('500x500')
    mer.title('Final File Content')
    mer.minsize(200, 100)
    F5 = Frame(mer,borderwidth=6)
    F5.pack(side=LEFT)

    scroll = Scrollbar(F5)
    final_data = Listbox(F5, yscrollcommand=scroll.set)
    final_data = Listbox(F5, height=50, width=150, yscrollcommand=scroll.set,bd=4)

    obj = open(finalres, 'rb')
    pd_reader = pd.PdfFileReader(obj)
    n = pd_reader.numPages
    try:
        for i in range(n):
            pageObj = pd_reader.getPage(i)
            data=pageObj.extractText()
            data= data.split('\n')

            for d in data:
                final_data.insert(END, d)
    except:
        logger.error('An error has been occurred while merging the data')
        error_msg(f'An error has occurred while merging the data')
    else:
        logger.info(f'Merged file is {finalres}')
        tkinter.messagebox.showinfo("Info", f"Merged file is at location {finalres}")


    obj.close()
    final_data.pack(side=LEFT, fill=BOTH)
    scroll.pack(side=RIGHT, fill=BOTH)
    scroll.config(command=final_data.yview)

# basic Tkinter window
F1= Frame(root,bg='white',padx=5,pady=5)
F1.pack()
name_label = Label(F1, text='Enter the Path', font=('calibre', 10, 'bold'),relief=SUNKEN)
name_entry = Entry(F1, textvariable=name_var, font=('calibre', 10, 'normal'),width=88,relief=SUNKEN)

btn = Button(F1, text="Submit", fg="red",padx=60,command=submit)

name_label.pack(padx=5,pady=5,anchor=CENTER,side=LEFT,fill=X)
name_entry.pack(padx=5,pady=5,anchor=CENTER,side=LEFT,fill=X)
btn.pack(anchor=CENTER,side=RIGHT,fill=X)

root.mainloop()