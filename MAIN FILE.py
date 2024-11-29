from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from employee import employeeClass
from supplier import SupplierClass
from category import categoryClass
from product import productClass

class IMS:
    def __init__(self,root):
       self.root=root
       self.root.geometry("1350x700+160+80")
       self.root.title("INVENTORY MANAGEMENT SYSTEM")
       self.root.config(bg="orange")

       #===title====
       self.icon_title=PhotoImage(file="c:\\Users\\great\\OneDrive\\Desktop\\Inventory Mangement\\images.png")
       title=Label(self.root,text="INVENTORY MANAGEMENT SYSTEM",image = self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="red",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=110)

       #===Project name====
       self.lbl_name=Label(self.root,text="INVENTORY MANAGEMENT SYSTEM\t\t NAME: AAKASH TIWARI\t\t CLASS:XII-A(COMPUTER SCIENCE)",font=("times new roman",15,"bold"),bg="#4d636d",fg="white")
       self.lbl_name.place(x=0,y=120,relwidth=1,height=30)

       #====Left Menu=======
       LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
       LeftMenu.place(x=30,y=200,width=220,height=320)
       lbl_MENU=Label(LeftMenu,text="MENU",font=("times new roman",20,"bold"),bg="red",bd=3).pack(side=TOP,fill="x")

       btn_employee=Button(LeftMenu,text="Employee",command=self.employee,font=("times new roman",20,"bold"),bg="silver",bd=3,cursor="hand2").pack(side=TOP,fill="x")
       btn_Supplier=Button(LeftMenu,text="Suppliers",command=self.supplier,font=("times new roman",20,"bold"),bg="silver",bd=3,cursor="hand2").pack(side=TOP,fill="x")
       btn_Categories=Button(LeftMenu,text="Categories",command=self.category,font=("times new roman",20,"bold"),bg="silver",bd=3,cursor="hand2").pack(side=TOP,fill="x")
       btn_Product=Button(LeftMenu,text="Product",command=self.product,font=("times new roman",20,"bold"),bg="silver",bd=3,cursor="hand2").pack(side=TOP,fill="x")
       btn_Exit=Button(LeftMenu,text="Exit",command=quit,font=("times new roman",20,"bold"),bg="silver",bd=3,cursor="hand2").pack(side=TOP,fill="x")
       #===============================================================================================================================
       #=========image==========
       self.im1=Image.open("C:\\Users\\great\\OneDrive\\Desktop\\Inventory Mangement\\inventory-management-dashboard-1.jpg")
       self.im1=self.im1.resize((1000,430),Image.Resampling.LANCZOS)
       self.im1=ImageTk.PhotoImage(self.im1)

       self.lbl_im1=Label(self.root,image=self.im1,bd=3,relief=RIDGE)
       self.lbl_im1.place(x=300,y=150)

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SupplierClass(self.new_win)
    
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
        
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
       
if __name__=="__main__":
   root=Tk()
   obj=IMS(root)
   root.mainloop()