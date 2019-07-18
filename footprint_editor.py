from tkinter import * 
import tkinter.filedialog
import tkinter.messagebox
import os # for handling file operations
root=Tk()
root.title("Haithem's Editor")
#functions
def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return 'break'
def copy():
    content_text.event_generate("<<Copy>>")
    on_content_changed()
    return 'break'
def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed
    return 'break'
def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed
    return 'break'
def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return 'break'
def select_all(event=None):
    content_text.tag_add('sel','1.0',END)
    return'break'
       
def find_text(event=None):
    ignore_case_value=BooleanVar()
    search_toplevel=Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    Label(search_toplevel,text='Find All:').grid(row=0,column=0,sticky='e')
    e=Entry(search_toplevel,width=25)
    e.grid(row=0,column=1,sticky='we')
    b=Button(search_toplevel,text='Find All',width=8,command=lambda:search_output(e.get(),ignore_case_value.get(),content_text,search_toplevel,e))
    b.grid(row=0,column=2,sticky='ew',padx=2,pady=2)
    ch=Checkbutton(search_toplevel,text='Ignore Case',variable=ignore_case_value)
    ch.grid(row=1,column=1,sticky='se')
    def close_search():
        content_text.tag_remove('match','1.0','end')
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW',close_search)
        

def search_output(needle,if_ignore_case,content_text,search_toplevel,e):
    content_text.tag_remove('match','1.0',END)
    matches_found=0
    if needle:
       start_pos='1.0'
       while True:
         start_pos=content_text.search(needle,start_pos,nocase=if_ignore_case,stopindex=END)
         if not start_pos:
             break
         end_pos='{}+{}c'.format(start_pos,len(needle))
         content_text.tag_add('match',start_pos,end_pos)
         matches_found+=1
         start_pos=end_pos
       content_text.tag_config('match',foreground='red',background='yellow')
    e.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found)) 

def open_file(event=None):
    input_file_name=tkinter.filedialog.askopenfilename(defaultextension='*.txt',filetypes=[('All Files:','*.*'),('Text Documents:','*.txt')])
    if input_file_name:
        global file_name
        file_name = input_file_name 
        root.title('{} '.format(os.path.basename(file_name)))
        content_text.delete(1.0,END)
        with open(file_name) as _file:
            content_text.insert(1.0,_file.read())
    on_content_changed()
    return 'break'
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
        
def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension='.txt',filetypes=[('All Files :','*.*'),(' Text Documents :','*.txt')])
    if input_file_name:
        global file_name
        file_name=input_file_name
        write_to_file(file_name)
        root.title('{}'.format(os.path.basename(file_name)))
        return 'break'
def write_to_file(file_name):
    try:
        content = content_text.get(1.0,END)
        with open(file_name,'w') as the_file:
            the_file.write(content)
    except IOError:
        pass
def new_file(event=None):
    root.title('Untitled')
    global file_name
    file_name = None
    content_text.delete(1.0,END)
    on_content_changed()
    return 'break'
def display_about_messagebox(event=None):
    tkinter.messagebox.showinfo("About","{}".format("\nTkinter GUI Application \n Developement Bluprints"))
def display_help_messagebox(event=None):
    tkinter.messagebox.showinfo("Help","Help Book : \nTkinter GUI Application \n Developement Bluprints",icon='question') 
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel('Quit','Do you really want to quit?'):
        root.destroy()
root.protocol('WM_DELETE_WINDOW',exit_editor)
def get_line_numbers():
    output=''
    if show_line_number.get():
        row,col=content_text.index('end').split('.')
        for i in range(1,int(row)):
            output+=str(i)+'\n'
    return output
def update_line_numbers(event=None):
    line_numbers=get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0','end')
    line_number_bar.insert('1.0',line_numbers)
    line_number_bar.config(state='disabled')
def highlight_line(interval=100):
	 content_text.tag_remove("active_line",	1.0,	"end")
	 content_text.tag_add("active_line","insert	linestart","insert	lineend+1c")
	 content_text.after(interval,toggle_highlight)																																																																														
def undo_highlight():
	 content_text.tag_remove("active_line",	1.0,	"end")
def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()
def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()
def show_cursor_info_bar():
    show_cursor_info_checked=show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no',fill=None,side='right',anchor='se')
    else:
        cursor_info_bar.pack_forget()
def update_cursor_info_bar(event=None):
    row,col=content_text.index(INSERT).split('.')
    line_num,col_num=str(int(row)),str(int(col)+1) # col starts at 0
    infotext="Line : {0} | Column : {1}".format(line_num,col_num)
    cursor_info_bar.config(text=infotext)
def change_theme(event=None):
    selected_theme = theme_name.get()
    fg_bg_color = color_schemes.get(selected_theme)
    foreground,background = fg_bg_color.split('.')
    content_text.config(bg=background,fg=foreground)
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root,event.y_root)

           
            
#File menu
menu_bar=Menu(root)
file_menu=Menu(menu_bar,tearoff=0)
#all file menu_items will be added here next
menu_bar.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='New',accelerator='CTRL + N',compound='left',command=new_file)
file_menu.add_command(label='Open',accelerator='CTRL + O',compound='left',command=open_file)
file_menu.add_command(label='Save',accelerator='CTRL + S',compound='left',command=save)
file_menu.add_command(label='Save as ',accelerator='Shift + Ctrl + S',compound='left',command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit',accelerator='Alt + F4',command=exit_editor)
root.config(menu=menu_bar)
#Edit Menu
edit_menu=Menu(menu_bar,tearoff=0)
#all edit menu_items will be added here next
menu_bar.add_cascade(label='Edit',menu=edit_menu)
edit_menu.add_command(label='Undo',accelerator='CTRL + Z',compound='left',command=undo)
edit_menu.add_command(label='Redo',accelerator='CTRL + Y',compound='left',command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut',accelerator='CTRL + X',compound='left',command=cut)
edit_menu.add_command(label='Copy',accelerator='CTRL + C',compound='left',command=copy)
edit_menu.add_command(label='Paste',accelerator='CTRL + V',compound='left',command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find',accelerator='CTRL + F',compound='left',command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All',accelerator='CTRL + A',compound='left',command=select_all)
root.config(menu=menu_bar)
#View Menu
view_menu=Menu(menu_bar,tearoff=0)
#all view menu_items will be added here next
menu_bar.add_cascade(label='View',menu=view_menu)
show_line_number=IntVar()
show_line_number.set(1) 
view_menu.add_checkbutton(label='Show Line Number',variable=show_line_number)
show_cursor_info=BooleanVar()
view_menu.add_checkbutton(label='Show Cursor Info',variable=show_cursor_info,command=show_cursor_info_bar)
to_highlight_line=BooleanVar()
view_menu.add_checkbutton(label='Highlight Current Line',onvalue=1,offvalue=0,variable=to_highlight_line,command=toggle_highlight)
themes_menu=Menu(view_menu,tearoff=0)
view_menu.add_cascade(label='Themes',menu=themes_menu)
theme_name=StringVar()
themes_menu.add_radiobutton(label='Aquamarine',variable=theme_name,command=change_theme)
themes_menu.add_radiobutton(label='Bold Beige',variable=theme_name,command=change_theme)
themes_menu.add_radiobutton(label='Cobalt Blue',variable=theme_name,command=change_theme)
themes_menu.add_radiobutton(label='Default',variable=theme_name,command=change_theme)
themes_menu.add_radiobutton(label='Grey garious',variable=theme_name,command=change_theme)
themes_menu.add_radiobutton(label='Night Mode',variable=theme_name,command=change_theme)
themes_menu.add_radiobutton(label='Olive Green',variable=theme_name,command=change_theme)

root.config(menu=menu_bar)
#About Menu
about_menu=Menu(menu_bar,tearoff=0)
#all about menu_items will be added here next
menu_bar.add_cascade(label='About',menu=about_menu)
about_menu.add_command(label='About',command=display_about_messagebox)
about_menu.add_command(label='Help',command=display_help_messagebox)
root.config(menu=menu_bar)
shortcut_bar=Frame(root,height=25,background='light sea green')
shortcut_bar.pack(expand='no',fill='x')
line_number_bar=Text(root,width=4,border=0,padx=3,takefocus=0,background='yellow')
line_number_bar.pack(side='left',fill='y')
content_text=Text(root)
content_text.pack(expand='yes',fill='both')
scrollbar1=Scrollbar(content_text,orient=VERTICAL)
content_text.config(yscrollcommand=scrollbar1.set)
scrollbar1.configure(command=content_text.yview)
scrollbar1.pack(side='right',fill='y')
scrollbar2=Scrollbar(content_text,orient=HORIZONTAL)
content_text.config(xscrollcommand=scrollbar2.set)
scrollbar2.configure(command=content_text.xview)
scrollbar2.pack(side='bottom',fill='x')
cursor_info_bar=Label(content_text,text='Line : 1 | Column : 1')
cursor_info_bar.pack(expand='no',fill=None,side=RIGHT,anchor='se')
#bindings 
content_text.bind("<Control -y>",redo)
content_text.bind("<Control -Y>",redo)
content_text.bind("<Control -a>",select_all)
content_text.bind("<Control -A>",select_all)
content_text.bind("<Control -f>",find_text)
content_text.bind("<Control -F>",find_text)
content_text.bind("<Control -O>",open_file)
content_text.bind("<Control -o>",open_file)
content_text.bind("<Control -S>",save)
content_text.bind("<Control -s>",save)
content_text.bind("<Control -N>",new_file)
content_text.bind("<Control -n>",new_file)
content_text.bind("<Control -Shift -S>",save_as)
content_text.bind("<Control -Shift -s>",save_as)
content_text.bind("<KeyPress- F1>",display_help_messagebox)
content_text.bind("<Any-KeyPress>",on_content_changed)
content_text.bind('<Button-3>',show_popup_menu)
#icons
icons=('new_file','open_file','find_text','save','undo','redo','copy','paste','cut')
for i,icon in enumerate(icons):
    tool_bar_icon=PhotoImage(file='icons/{}.png'.format(icon))
    cmd=eval(icon)
    tool_bar=Button(shortcut_bar,image=tool_bar_icon,command=cmd)
    tool_bar.image=tool_bar_icon
    tool_bar.pack(side='left')
    
content_text.tag_configure('active_line',background='ivory2')  
color_schemes = {'Default':'#000000.#FFFFFF', 'Grey garious':'#83406A.#D1D4D1', 'Aquamarine':	'#5B8340.#D1E7E0','Bold Beige':'#4B4620.#FFF0E1','Cobalt Blue':'#ffffBB.#3333aa', 'Olive Green':	'#D1E7E0.#5B8340', 'Night Mode':'#FFFFFF.#000000', }
# pop-up menu
popup_menu=Menu(content_text)
for i in ('cut','copy','paste','undo','redo'):
    cmd=eval(i)
    popup_menu.add_command(label=i,compound='left',command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All',command=select_all)



    
root.mainloop()