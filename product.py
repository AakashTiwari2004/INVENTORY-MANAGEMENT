from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("INVENTORY MANAGEMENT SYSTEM ")
        self.root.config(bg="orange")
        self.root.focus_force()

        # All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        # Fetch categories and suppliers
        self.fetch_cat_sup()

        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # Title
        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="red", fg="white").pack(side=TOP, fill=X)

        # Column labels
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_Frame, text="Suppliers", font=("goudy old style", 18), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30, y=160)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=210)
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30, y=260)
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white").place(x=30, y=310)

        # Category ComboBox
        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_cat.place(x=150, y=60, width=200)
        if self.cat_list:  # Only set current if there are values
            cmb_cat.current(0)

        # Supplier ComboBox
        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_sup.place(x=150, y=110, width=200)
        if self.sup_list:  # Only set current if there are values
            cmb_sup.current(0)

        # Other Entry fields
        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("times new roman", 15), bg='lightyellow').place(x=150, y=160, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("times new roman", 15), bg='lightyellow').place(x=150, y=210, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("times new roman", 15), bg='lightyellow').place(x=150, y=260, width=200)

        # Status ComboBox
        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # Buttons
        btn_add = Button(product_Frame, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", command=self.Update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", command=self.Clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg='white')
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # Search options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightblue").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", command=self.Search, font=("goudy old style", 15), bg="silver", fg="black", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # Product Details
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        Scrolly = Scrollbar(p_frame, orient=VERTICAL)
        Scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Supplier", "Category", "name", "price", "qty", "status"), yscrollcommand=Scrolly.set, xscrollcommand=Scrollx.set)
        Scrollx.pack(side=BOTTOM, fill=X)
        Scrolly.pack(side=RIGHT, fill=Y)
        Scrollx.config(command=self.product_table.xview)
        Scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Fetch Categories and Suppliers
    def fetch_cat_sup(self):
        self.sup_list.append("Empty")
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from category")
            cat = cur.fetchall()
            self.cat_list.append("Empty")
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # Add Product
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" or self.var_sup.get() == "Empty":
                messagebox.showerror("Error", "Please select category and supplier", parent=self.root)
            else:
                cur.execute("Insert into product (category, supplier, name, price, qty, status) values(?, ?, ?, ?, ?, ?)", (
                    self.var_cat.get(),
                    self.var_sup.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get(),
                ))
                con.commit()
                messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Update Product
    def Update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("Update product set category=?, supplier=?, name=?, price=?, qty=?, status=? where pid=?", (
                    self.var_cat.get(),
                    self.var_sup.get(),
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get(),
                    self.var_pid.get(),
                ))
                con.commit()
                messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Delete Product
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("Delete from product where pid=?", (self.var_pid.get(),))
                con.commit()
                messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Clear Fields
    def Clear(self):
        self.var_pid.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")

    # Show Products
    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows = cur.fetchall()
            if len(rows) != 0:
                del self.product_table[:]
                for row in rows:
                    self.product_table.insert("", END, values=row)
                con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Get data from table
    def get_data(self, ev):
     selected_row = self.product_table.focus()
     if not selected_row:  # Check if a row is selected
      return  # Exit if no row is selected
      data = self.product_table.item(selected_row)
      row = data['values']
    
    # Check if row is not empty
      if row:
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])



    # Search Product
    def Search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Please select search option", parent=self.root)
            else:
                cur.execute("Select * from product where " + self.var_searchby.get().lower() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    del self.product_table[:]
                    for row in rows:
                        self.product_table.insert("", END, values=row)
                    con.commit()
                else:
                    messagebox.showinfo("No Data", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
