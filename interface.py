import tkinter
from database import BookstoreDB
from tkinter import messagebox

class BookstoreGUI:

    def __init__(self, name: str) -> None:
        self.__app_state = "read"  # keeps track of what action the user is trying to perform
        self.__database = BookstoreDB(name)

        # create the main window
        self.root = tkinter.Tk()

        # create the title and geometry
        self.root.title("CFCC Bookstore Inventory Management System")
        self.root.geometry("900x500")

        # create frames
        self.crud_frame = tkinter.Frame(self.root)
        self.dropdown_frame = tkinter.Frame(self.root)
        self.book_info_frame = tkinter.Frame(self.root)
        self.label_frame = tkinter.Frame(self.book_info_frame)
        self.info_frame = tkinter.Frame(self.book_info_frame)
        self.save_or_clear_frame = tkinter.Frame(self.root)

        # create widgets
        self.create_button = tkinter.Button(self.crud_frame, text="Add Book", command=self.__create)
        self.read_button = tkinter.Button(self.crud_frame, text="View Details", command=self.__read)
        self.update_button = tkinter.Button(self.crud_frame, text="Update Book", command=self.__update)
        self.delete_button = tkinter.Button(self.crud_frame, text="Delete Book", command=self.__delete)

        # create StringVars for dropdown option
        self.__selection = tkinter.StringVar()
        self.__titles = self.__get_titles()

        try:
            self.__selection.set(self.__titles[0])
        except IndexError:
            tkinter.messagebox.showwarning("Warning", message="Your inventory is empty!")
            self.__selection.set("")
            self.__titles = [""]

        # create dropdown_menu object
        self.dropdown_menu = tkinter.OptionMenu(self.dropdown_frame, self.__selection, *self.__titles)
        self.dropdown_menu.config(width=20)

        # create description label widgets
        self.isbn_descr_label = tkinter.Label(self.label_frame, text="ISBN:")
        self.title_descr_label = tkinter.Label(self.label_frame, text="Title:")
        self.author_descr_label = tkinter.Label(self.label_frame, text="Author:")
        self.edition_descr_label = tkinter.Label(self.label_frame, text="Edition:")
        self.price_descr_label = tkinter.Label(self.label_frame, text="Price:")
        self.publisher_descr_label = tkinter.Label(self.label_frame, text="Publisher:")

        # StringVars
        self.__isbn = tkinter.StringVar()
        self.__title = tkinter.StringVar()
        self.__author = tkinter.StringVar()
        self.__edition = tkinter.StringVar()
        self.__price = tkinter.StringVar()
        self.__publisher = tkinter.StringVar()

        # Label & entry widgets
        self.isbn_label = tkinter.Label(self.info_frame, textvariable=self.__isbn, width=40)
        self.title_label = tkinter.Label(self.info_frame, textvariable=self.__title, width=40)
        self.author_label = tkinter.Label(self.info_frame, textvariable=self.__author, width=40)
        self.edition_label = tkinter.Label(self.info_frame, textvariable=self.__edition, width=40)
        self.price_label = tkinter.Label(self.info_frame, textvariable=self.__price, width=40)
        self.publisher_label = tkinter.Label(self.info_frame, textvariable=self.__publisher, width=40)

        self.isbn_entry = tkinter.Entry(self.info_frame, width=40, textvariable=self.__isbn)
        self.title_entry = tkinter.Entry(self.info_frame, width=40, textvariable=self.__title)
        self.author_entry = tkinter.Entry(self.info_frame, width=40, textvariable=self.__author)
        self.edition_entry = tkinter.Entry(self.info_frame, width=40, textvariable=self.__edition)
        self.price_entry = tkinter.Entry(self.info_frame, width=40, textvariable=self.__price)
        self.publisher_entry = tkinter.Entry(self.info_frame, width=40, textvariable=self.__publisher)

        # save and clear buttons
        self.save_button = tkinter.Button(self.save_or_clear_frame, text="Save", command=self.__save)
        self.clear_button = tkinter.Button(self.save_or_clear_frame, text="Clear", command=self.__clear)

        # pack crud buttons
        self.create_button.pack(side="left", ipadx=40, padx=10, pady=10)
        self.read_button.pack(side="left", ipadx=40, padx=10, pady=10)
        self.update_button.pack(side="left", ipadx=40, padx=10, pady=10)
        self.delete_button.pack(side="left", ipadx=40, padx=10, pady=10)

        # pack option menu
        self.dropdown_menu.pack(side="top", ipadx=220, pady=5)

        # pack label and entry widgets
        self.isbn_descr_label.pack(side="top", ipadx=5)
        self.isbn_label.pack(side="top", ipadx=5)
        self.title_descr_label.pack(side="top", ipadx=5)
        self.title_label.pack(side="top", ipadx=5)
        self.author_descr_label.pack(side="top", ipadx=5)
        self.author_label.pack(side="top", ipadx=5)
        self.edition_descr_label.pack(side="top", ipadx=5)
        self.edition_label.pack(side="top", ipadx=5)
        self.price_descr_label.pack(side="top", ipadx=5)
        self.price_label.pack(side="top", ipadx=5)
        self.publisher_descr_label.pack(side="top", ipadx=5)
        self.publisher_label.pack(side="top", ipadx=5)

        # pack bottom buttons
        self.clear_button.pack(side="right", ipadx=40, padx=5)
        self.save_button.pack(side="right", ipadx=40, padx=5)

        # pack frames
        self.crud_frame.pack(side="top", ipadx=5)
        self.dropdown_frame.pack(side="top")
        self.book_info_frame.pack(side="top", ipadx=5, pady=20)
        self.label_frame.pack(side="left", ipadx=5)
        self.info_frame.pack(side="left", ipadx=5)
        self.save_or_clear_frame.pack(side="right", ipadx=5, padx=120)

        # set all selected StringVars
        # populate info area with first book
        self.__read()

        # main loop
        tkinter.mainloop()

    def __get_title_isbn_pair(self) -> list[tuple[str, str]]:
        """
        Retrieves all titles, isbns from database
        :return: list[tuple[str, str] list of title, isbn tuple
        """
        # query database for titles and isbns
        titles_list = self.__database.get_titles()
        return titles_list

    def __get_titles(self) -> list[str]:
        """
        Returns a list of titles
        :return: list[str] list of titles
        """
        titles = []
        for title, isbn in self.__get_title_isbn_pair():
            titles.append(title)

        # update list for dropdown widget
        self.__titles = titles

        return titles

    def __get_isbn(self) -> int:
        """
        Retrieves isbn of currently selected title
        :return: int isbn
        """
        try:
            # get the list index of the current selection
            index = self.__titles.index(self.__selection.get())
            # get isbn from the title/isbn tuple
            try:
                isbn_to_read = int(self.__get_title_isbn_pair()[index][1])
            except IndexError:
                self.__app_state = "empty inventory"
                isbn_to_read = 0
            return isbn_to_read
        except ValueError:
            self.__app_state = "empty inventory"
            return 0


    def __show_entry_widgets(self) -> None:
        """
        Hides label widgets and displays entry widgets
        :return: None
        """
        # get rid of label widgets
        self.isbn_label.pack_forget()
        self.title_label.pack_forget()
        self.author_label.pack_forget()
        self.edition_label.pack_forget()
        self.price_label.pack_forget()
        self.publisher_label.pack_forget()

        # get rid of entry widgets because going from update to create is broken otherwise
        self.title_entry.pack_forget()
        self.author_entry.pack_forget()
        self.edition_entry.pack_forget()
        self.price_entry.pack_forget()
        self.publisher_entry.pack_forget()

        # pack entry widgets
        if self.__app_state == "create":
            self.isbn_entry.pack()
        else:
            self.isbn_label.pack()
        self.title_entry.pack()
        self.author_entry.pack()
        self.edition_entry.pack()
        self.price_entry.pack()
        self.publisher_entry.pack()

    def __show_read_only_widgets(self) -> None:
        """
        Hides entry widgets and displays label widgets
        :return: None
        """
        # get rid of entry widgets
        self.isbn_entry.pack_forget()
        self.title_entry.pack_forget()
        self.author_entry.pack_forget()
        self.edition_entry.pack_forget()
        self.price_entry.pack_forget()
        self.publisher_entry.pack_forget()

        # pack label widgets
        self.isbn_label.pack()
        self.title_label.pack()
        self.author_label.pack()
        self.edition_label.pack()
        self.price_label.pack()
        self.publisher_label.pack()

    def __update_dropdown(self) -> None:
        """
        Updates dropdown menu to reflect changes
        :return: None
        """
        if self.__app_state == "delete":
            # get index of current selection
            menu_index = self.__titles.index(self.__selection.get())
            # access menu from dropdown widget
            menu = self.dropdown_menu["menu"]
            # remove selected title from dropdown menu
            menu.delete(menu_index)
        else:
            # access menu from dropdown widget
            menu = self.dropdown_menu["menu"]
            # remove all titles from dropdown menu
            menu.delete(0, "end")
            # rebuild the dropdown menu
            for book in self.__get_titles():
                menu.add_command(label=book, command=lambda value=book: self.__selection.set(value))

    def __create(self) -> None:
        """
        Sets up application state to create a new book record
        :return: None
        """
        self.__app_state = "create"
        self.__show_entry_widgets()
        self.__clear()

    def __read(self) -> None:
        """
        Sets up application state to read a book record
        :return: None
        """
        self.__app_state = "read"
        isbn_to_read = self.__get_isbn()

        # set StringVars
        book_details = self.__database.read(isbn_to_read)
        try:
            self.__isbn.set(book_details[0])
            self.__title.set(book_details[1])
            self.__author.set(book_details[2])
            self.__edition.set(book_details[3])
            self.__price.set(book_details[4])
            self.__publisher.set(book_details[5])
        except TypeError:
            tkinter.messagebox.showerror("Error", "No book details!")
            self.__app_state = "empty inventory"

        self.__show_read_only_widgets()

    def __update(self) -> None:
        """
        Sets up application state to update a book record
        :return: None
        """
        self.__read()
        if self.__app_state == "empty inventory":
            tkinter.messagebox.showerror("Error", "No book to update!")
            self.__show_read_only_widgets()
        else:
            self.__app_state = "update"
            # show details for selected book
            self.__show_entry_widgets()

    def __delete(self) -> None:  # how to remove deleted books from dropdown list???
        """
        Sets up application state to delete a book record
        :return: None
        """
        # display info for book record selected for deletion
        self.__read()
        self.__app_state = "delete"
        isbn_to_delete = self.__get_isbn()

        # ask user to confirm deletion
        if self.__app_state != "empty inventory":
            title_to_delete = self.__database.read(isbn_to_delete)[1]
            confirm = tkinter.messagebox.askokcancel(title="Confirm Deletion", message=f"Are you sure you want to delete\n'{title_to_delete}'\nISBN: {isbn_to_delete}?")
            if confirm:
                self.__database.delete(isbn_to_delete)
                # if deleting the only book
                if len(self.__titles) == 1:
                    self.__app_state = "empty inventory"
                    self.__clear()
                    self.__selection.set("")
                    menu = self.dropdown_menu["menu"]
                    menu.delete(0)
                else:
                    self.__update_dropdown()
                    self.__get_titles()
                    self.__selection.set(self.__titles[0])
                    self.__read()
                message = f"You deleted:\n'{title_to_delete}'\nISBN: {isbn_to_delete}"
                # display the message
                tkinter.messagebox.showinfo("Book Deleted", message)
        else:
            tkinter.messagebox.showerror("Error", message="No book to delete!")

    def __save(self) -> None:
        """
        Saves book record according to application state
        :return: None
        """
        if self.__app_state == "create" or self.__app_state == "update":
            index = self.__titles.index(self.__selection.get())

            # error flags
            duplicate_isbn = False
            valid_record = False
            no_empty_fields = True

            error_message = ""

            # make a list of book details
            record = [self.__isbn.get(), self.__title.get(), self.__author.get(), self.__edition.get(), self.__price.get(), self.__publisher.get()]

            # check for empty fields
            for field in record:
                if field == "":
                    error_message = "Please fill out all fields"
                    no_empty_fields = False

            # set book details variables to StringVars
            if no_empty_fields:
                isbn = record[0]
                title = record[1]
                author = record[2]
                edition = record[3]
                price = record[4]
                publisher = record[5]

                # check for duplicate ISBN
                if self.__app_state == "create":
                    for pair in self.__get_title_isbn_pair():
                        if isbn == str(pair[1]):
                            duplicate_isbn = True

                # check ISBN validity
                if duplicate_isbn:
                    error_message += "\nISBN already exists."
                elif not isbn.isdigit():
                    error_message += "\nInvalid ISBN, must be integer."
                elif not (len(isbn) == 10 or len(isbn) == 13):
                    error_message += "\nInvalid ISBN, number of digits must be 10 or 13."
                # prevent inputs containing only whitespace characters
                elif title.replace(" ", "") == "":  # replace() allows for spaces between words
                    error_message += "\nInvalid Title"
                elif author.replace(" ", "") == "":
                    error_message += "\nInvalid Author"
                elif publisher.replace(" ", "") == "":
                    error_message += "\nInvalid Publisher"
                else:
                    # check for correct type
                    try:
                        int(isbn)
                    except ValueError:
                        error_message += "\nInvalid ISBN, must be integer."
                    try:
                        int(edition)
                    except ValueError:
                        error_message += "\nInvalid Edition, must be integer."
                    try:
                        float(price)
                    except ValueError:
                        error_message += "\nInvalid Price, must be float."
                    if error_message == "":
                        # all checks passed
                        valid_record = True

                if valid_record and self.__app_state == "create":
                    self.__database.create(int(isbn), title, author, int(edition), float(price), publisher)
                    self.__update_dropdown()
                    success_message = f"You added a record for:\n'{title}'\nISBN: {isbn}"

                    # display the message
                    tkinter.messagebox.showinfo("Book Created", success_message)
                    self.__selection.set(self.__titles[0])
                    self.__read()
                elif valid_record and self.__app_state == "update":
                    self.__database.update(int(isbn), title, author, int(edition), float(price), publisher)
                    self.__update_dropdown()
                    success_message = f"You updated the record for:\n'{title}'\nISBN: {isbn}"

                    # display the message
                    tkinter.messagebox.showinfo("Book Updated", success_message)
                    self.__selection.set(self.__titles[index])
                    self.__read()
                else:
                    tkinter.messagebox.showerror("Error", error_message)
            else:
                tkinter.messagebox.showerror("Error", error_message)

    def __clear(self) -> None:
        """
        Clears entries/labels
        :return: None
        """
        if self.__app_state == "create" or self.__app_state == "empty inventory":
            self.__isbn.set("")
            self.__title.set("")
            self.__author.set("")
            self.__edition.set("")
            self.__price.set("")
            self.__publisher.set("")
        elif self.__app_state == "update":
            self.__title.set("")
            self.__author.set("")
            self.__edition.set("")
            self.__price.set("")
            self.__publisher.set("")
