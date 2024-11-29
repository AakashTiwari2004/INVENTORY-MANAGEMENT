from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("INVENTORY MANAGEMENT SYSTEM")
        self.root.config(bg="orange")
        self.root.focus_force()

        # All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()

        # Options
        lbl_search = ttk.Label(self.root, text="Invoice No.", font=("times new roman", 15))
        lbl_search.place(x=700, y=80)

        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightblue")
        txt_search.place(x=800, y=80, width=140)
        btn_search = Button(self.root, text="Search", command=self.Search, font=("goudy old style", 15),
                            bg="silver", fg="black", cursor="hand2")
        btn_search.place(x=950, y=79, width=100, height=30)

        # Title
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 20, "bold"), bg="red", fg="white")
        title.place(x=50, y=10, width=1000, height=40)

        # Content - Row 1 to Row 4
        Label(self.root, text="Invoice No.", font=("goudy old style", 15), bg="orange").place(x=50, y=80)
        Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=80, width=180)
        Label(self.root, text="Name", font=("goudy old style", 15), bg="orange").place(x=50, y=120)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)
        Label(self.root, text="Contact", font=("goudy old style", 15), bg="orange").place(x=50, y=160)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)
        Label(self.root, text="Description", font=("goudy old style", 15), bg="orange").place(x=50, y=200)

        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=90)

        # Buttons
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=180, y=320, width=110, height=35)
        Button(self.root, text="Update", command=self.Update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=300, y=320, width=110, height=35)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=420, y=320, width=110, height=35)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=540, y=320, width=110, height=35)

        # Supplier Details Table
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        scroll_y = Scrollbar(emp_frame, orient=VERTICAL)
        scroll_x = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.supplierTable.xview)
        scroll_y.config(command=self.supplierTable.yview)

        # Table Headings
        self.supplierTable.heading("invoice", text="Invoice No.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        self.supplierTable["show"] = "headings"
        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Methods
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice number already assigned, try a different one", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier (invoice, name, contact, desc) VALUES (?, ?, ?, ?)",
                                (self.var_sup_invoice.get(), self.var_name.get(), self.var_contact.get(),
                                 self.txt_desc.get('1.0', END)))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, event):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

    def Update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice number must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid invoice number", parent=self.root)
                else:
                    cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",
                                (self.var_name.get(), self.var_contact.get(),
                                 self.txt_desc.get('1.0', END), self.var_sup_invoice.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice number must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid invoice number", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.show()

    def Search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice number should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)  
    root.mainloop()
