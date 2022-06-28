from tkinter import *
import sqlite3


class Library_Managemant:
    def __init__(self) -> None:
        self.MainPage = Tk()
        self.MainPage.title(" Library Managemant ")
        self.MainPage.geometry('800x380')
        self.MainPage.resizable(width=False, height=False)
        self.MainPage.configure(bg='sky blue')
# ////////////////////////////////////////////////////////
        self.library_labels("Title", 20, 5)
        self.library_labels('Author', 410, 5)
        self.library_labels('Year', 20, 30)
        self.library_labels('  ISBN  ', 410, 30)
# ////////////////////////////////////////////////////////
        self.title_input = StringVar()
        self.author_input = StringVar()
        self.year_input = StringVar()
        self.isbn_input = StringVar()
        self.library_entries(self.title_input, 90, 8)
        self.library_entries(self.author_input, 490, 8)
        self.library_entries(self.year_input, 90, 43)
        self.library_entries(self.isbn_input, 490, 43)
# ////////////////////////////////////////////////////////
        self.ListBox_and_Scrollbar()
# //////////////////////////////////////////////////////////
        self.library_buttons("Show books",460 , 150 , self.Show_All_Books_in_LibraryBox)
        self.library_buttons("Add book",600 , 150 , self.Add_a_Book_in_LibraryBox)
        self.library_buttons("Delete a book",460 , 200 , self.Delete_book_From_LibraryBox)
        self.library_buttons("Update a book",600 , 200 , self.Update_book_From_LibraryBox)
        self.library_buttons("Search book",460 , 250 , self.Search_book_From_LibraryBox)
        self.library_buttons("Close",600 , 250 , lambda : self.MainPage.destroy())
# //////////////////////////////////////////////////////////
        self.Db_and_Library_Connection()
# //////////////////////////////////////////////////////////
        self.Show_All_Books_in_LibraryBox()
# //////////////////////////////////////////////////////////
        self.libraryListBox.bind("<<ListboxSelect>>", self.Create_Information_from_LibraryBox)
        self.MainPage = mainloop()
# //////////////////////////////////////////////////////////
    def library_labels(self, Text, X, Y):
        label = Label(self.MainPage, text=Text, pady=10, padx=10)
        label.place(x=X,y=Y)
# //////////////////////////////////////////////////////////
    def library_entries(self, myInput, X, Y):
        entry = Entry(self.MainPage, width=45, textvariable=myInput)
        entry.place(x=X,y=Y)
# //////////////////////////////////////////////////////////
    def ListBox_and_Scrollbar(self):
        self.libraryListBox = Listbox(self.MainPage, width=65, height=17)
        self.libraryListBox.place(x=20,y=80)
        libraryScrollBar = Scrollbar(self.MainPage, width=20)
        libraryScrollBar.place(x=420,y=180)
        self.libraryListBox.configure(yscrollcommand=libraryScrollBar.set)
        libraryScrollBar.configure(command=self.libraryListBox.yview)

# //////////////////////////////////////////////////////////   
    def library_buttons(self, Text, X, Y, Command):
        button = Button(self.MainPage, text=Text, width=18, command=Command)
        button.place(x=X, y=Y)
# //////////////////////////////////////////////////////////
    def Db_and_Library_Connection(self):
        connection = sqlite3.connect('./LibraryDataBase.db')
        cursor = connection.cursor()
        sql = """
            Create Table If Not Exists book (
            id INTEGER PRIMARY key ,
            title text ,
            author text ,
            year INTEGER ,
            isbn INTEGER 
            );
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()

# //////////////////////////////////////////////////////////
    def Bring_All_Books_From_DataBase(self):
        connection = sqlite3.connect('./LibraryDataBase.db')
        cursor = connection.cursor()
        sql = """
            select * from book
        """
        cursor.execute(sql)
        AllBooks = cursor.fetchall()
        connection.commit()
        connection.close()
        return AllBooks

    def Show_All_Books_in_LibraryBox(self):
       AllBooks = self.Bring_All_Books_From_DataBase()
       if len(AllBooks) == 0:
           self.Clear_listBox()
           self.libraryListBox.insert(END, "\
                                                    Empty")
       else:
        self.Clear_listBox()
        self.Clear_Entries()
        for book in AllBooks:
            self.libraryListBox.insert(END, book)

# //////////////////////////////////////////////////////////
    def Add_a_Book_in_LibraryBox(self):
        self.Add_book_in_Database(self.title_input.get(),self.author_input.get(),self.year_input.get(),self.isbn_input.get())
        self.Clear_Entries()
        self.Clear_listBox()
        self.Show_All_Books_in_LibraryBox()
    
    def Add_book_in_Database(self, title, author, year, isbn):
        connection = sqlite3.connect('./LibraryDataBase.db')
        cursor = connection.cursor()
        sql = """
            Insert into book values (NULL,? , ? , ? ,?)
        """
        cursor.execute(sql, (title, author, year, isbn))
        connection.commit()
        connection.close()
 # //////////////////////////////////////////////////////////
    def Create_Information_from_LibraryBox(self,event):
        global Item
        if len(self.libraryListBox.curselection()) > 0:
            index = self.libraryListBox.curselection()
            Item = self.libraryListBox.get(index[0])
            self.title_input.set(Item[1])
            self.author_input.set(Item[2])
            self.year_input.set(Item[3])
            self.isbn_input.set(Item[4])
 # //////////////////////////////////////////////////////////
    def Delete_book_From_LibraryBox(self):
        self.Delete_book_From_DataBase(Item[0])
        self.Clear_Entries()
        self.Clear_listBox()
        self.Show_All_Books_in_LibraryBox()

    def Delete_book_From_DataBase(self, id):
        connection = sqlite3.connect('./LibraryDataBase.db')
        cursor = connection.cursor()
        sql = """
            delete from book where id=?
        """
        cursor.execute(sql, (id,))
        connection.commit()
        connection.close()
# //////////////////////////////////////////////////////////
    def Update_book_From_LibraryBox(self):
        self.Update_book_From_DataBase(self.title_input.get(), self.author_input.get(), self.year_input.get(), self.isbn_input.get(), Item[0])
        self.Clear_Entries()
        self.Clear_listBox()
        self.Show_All_Books_in_LibraryBox()       

    def Update_book_From_DataBase(self,title, author, year, isbn, id):
        connection = sqlite3.connect('./LibraryDataBase.db')
        cursor = connection.cursor()
        sql = """
            update book set title=?,author=?,year=?,isbn=? where id = ?
        """
        cursor.execute(sql, (title, author, year, isbn, id))
        connection.commit()
        connection.close()
# //////////////////////////////////////////////////////////
    def Search_book_From_LibraryBox(self):
        Findes = self.Search_book_From_DataBase(self.title_input.get(), self.author_input.get(), self.year_input.get(), self.isbn_input.get())
        if len(Findes) == 0:
            self.Clear_listBox()
            self.libraryListBox.insert(END, "\
                                      Not Found Any Book")
        else:
            self.Clear_Entries()
            self.Clear_listBox()
            for book in Findes:
                self.libraryListBox.insert(END ,book)

    def Search_book_From_DataBase(self, title='', author='', year='', isbn=''):
        connection = sqlite3.connect('./LibraryDataBase.db')
        cursor = connection.cursor()
        sql = """
            select * from book where title = ? or author = ? or year = ? or isbn = ?
        """
        cursor.execute(sql, (title, author, year, isbn))
        AllBooks = cursor.fetchall()
        connection.commit()
        connection.close()
        return AllBooks

# //////////////////////////////////////////////////////////    
    def Clear_Entries(self):
        self.title_input.set('')
        self.author_input.set('')
        self.year_input.set('')
        self.isbn_input.set('')
# //////////////////////////////////////////////////////////
    def Clear_listBox(self):
        self.libraryListBox.delete(0,END)



Library_Managemant()