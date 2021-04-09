from flask import *  
from fpdf import FPDF
import sqlite3  
  
app = Flask(__name__)  
 
@app.route("/")  
def index():  
    return render_template("index.html");  
 
@app.route("/add")
def add():
    return render_template("add.html")
 
@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            no_registrasi = request.form["no_registrasi"]
            nama = request.form["nama"]
            tempat_tanggal_lahir = request.form["tempat_tanggal_lahir"]
            nik_nip = request.form["nik_nip"]
            email = request.form["email"]
            hp = request.form["hp"]
            hp_wali_atasan = request.form["hp_wali_atasan"]
            pekerjaan = request.form["pekerjaan"]
            alamat = request.form["alamat"]
            program_akademi = request.form["program_akademi"]
            tema_pelatihan = request.form["tema_pelatihan"]
            mitra_pelatihan = request.form["mitra_pelatihan"]     
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan) values (?,?,?,?,?,?,?,?,?,?,?,?)",(no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html",msg = msg)
            con.close()
 
@app.route("/view")  
def view():  
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)  
 
@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id_employees = request.form["id_employees"]
    with sqlite3.connect("database.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Employees where id_employees = ?",(id_employees,))  
            msg = "Employees successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)  

@app.route("/pdf",methods = ["POST"])
def pdf():
    id_employees = request.form["id_employees"]
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees where id_employees = ?",(id_employees,))   
    rows = cur.fetchall()
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Form Komitmen", ln=1, align="C")
    
    for row in rows:
        pdf.cell(200, 10, txt=row["nama"], ln=1)
        pdf.cell(200, 10, txt=row["tempat_tanggal_lahir"], ln=1)
        pdf.cell(200, 10, txt=row["nik_nip"], ln=1)
        pdf.cell(200, 10, txt=row["email"], ln=1)
        pdf.cell(200, 10, txt=row["hp"], ln=1)
        pdf.cell(200, 10, txt=row["hp_wali_atasan"], ln=1)
        pdf.cell(200, 10, txt=row["pekerjaan"], ln=1)
        pdf.cell(200, 10, txt=row["alamat"], ln=1)
        pdf.cell(200, 10, txt=row["program_akademi"], ln=1)
        pdf.cell(200, 10, txt=row["tema_pelatihan"], ln=1)
        pdf.cell(200, 10, txt=row["mitra_pelatihan"], ln=1)
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=form_komitmen.pdf'})
  
if __name__ == "__main__":  
    app.run(debug = True)  