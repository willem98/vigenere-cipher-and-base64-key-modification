from flask import Flask, render_template, request, send_file
import backend as bk
from backend import analisa as Uji, plot, Save

app = Flask(__name__)
#app.config["SECRET_KEY"] = "iniSecretKeywillem"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enkripsi", methods=["POST","GET"])
def enkripsi():
    if request.method == 'POST':
        plain = request.form['plaintext']
        kunci = request.form['kunci']
        if plain and kunci :
            res = bk.encode(kunci,plain)
            save = Save(plain,kunci,res,"enk")
            return render_template("enkripsi.html",result=res,plain=plain,key=kunci,save=save)
        elif plain : return render_template("enkripsi.html",result=plain,plain=plain)
        elif kunci : return render_template("enkripsi.html",key=kunci)
    return render_template("enkripsi.html")

@app.route("/deskripsi",methods=["POST","GET"])
def deskripsi():
    if request.method == 'POST':
        plain = request.form['chipertext']
        kunci = request.form['kunci']
        if plain and kunci :
            res = bk.decode(kunci,plain)
            save = Save(plain,kunci,res,"des")
            return render_template("deskripsi.html",result=res,cipher=plain,key=kunci,save=save)
        elif plain : return render_template("deskripsi.html",result=plain, cipher=plain)
        elif kunci : return render_template("deskripsi.html", key=kunci)
    return render_template("deskripsi.html")

@app.route("/pengujian", methods=["POST","GET"])
def pengujian():
    if request.method == 'POST':
        p = request.form['plain']
        c = request.form['cipher']
        if p and c:
            analisap = Uji(p)
            analisac = Uji(c)
            nalisap = analisap['data']
            nalisac = analisac['data']
            plotdir = plot(nalisap,nalisac)
            analisa = []
            rp = []
            rc = []
            while len(nalisap) != 0:
                i = nalisap.pop(0)
                j = nalisac.pop(0)
                dict = {"huruf":str(i['huruf']),"fp":str(i['frekuensi']),"pp":str(i['persentase']),"fc":str(j['frekuensi']),"pc":str(j['persentase'])}
                rp.append(i["frekuensi"])
                rc.append(i["frekuensi"])
                analisa.append(dict)
            rps = str("%.2f"%(float(sum(rp)/len(rp)*100))+"%")
            rcs = str("%.2f"%(float(sum(rc)/len(rc)*100))+"%")
            return render_template("pengujian.html",analisa=analisa,totalp=analisap['len'],totalc=analisac['len'],ratap=rps,ratac=rcs,filepath=plotdir)
        else: return render_template("pengujian.html",plain=p,cipher=c)
    return render_template("pengujian.html")

@app.route('/download/<name>', methods=["POST",'GET'])
def download(name):
    try : return send_file(f"static\\plots\\{name}", mimetype='jpg',download_name="Chart.png",as_attachment=True)
    except : return send_file(f"static\\txt\\{name}", mimetype='txt',download_name="Output.txt",as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5002)