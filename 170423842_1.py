import tkinter as tk
import json
from tkinter import messagebox
from datetime import datetime



class YapilacaklarListesi:
    def __init__(self,pencere):
        #Oncelikle Butun butonları ve menuleri ekledik ve pencere tasarımı yaptık
        self.pencere = pencere

        #Gorevlerin tutulacağı liste:
        self.gorevlerListe = []
        self.gorevleriAcFonksiyon()

        #Bir adet Label oluşturulması
        l1 = tk.Label(text="Gorevlerim:")
        l1.place(x=10,y=10)

        #Gorevlerin goruntuleneceği listbox
        #Burada tamamlanmış ve tamamlanmamış butun gorevler bulunmakta
        self.gorevGoruntulemeListbox = tk.Listbox(pencere,width=40)
        self.gorevGoruntulemeListbox.place(x=10, y=30)

        #Tamamla ve Sil butonlarının oluşturulması
        tamamlaButton = tk.Button(pencere, text="Tamamla",command=self.gorevTamamlaFonksiyon,bg="yellow")
        tamamlaButton.place(x=30, y=250)

        silButton = tk.Button(pencere, text="sil",command=self.gorevSilFonksiyon,bg="red")
        silButton.place(x=150, y=250)

        #Menu oluşturma ve içerisine Tamamlanan Menuler - Gorev Ekleme - Çıkış alt menuleri eklenmesi
        menuButon = tk.Menu(self.pencere,tearoff=0) #Menu buton oluşturduk
        pencere.config(menu=menuButon) #Pencerenin içine bir menu buton bolumu açtık (konum ayarlamamıza gerek yok)

        menuBar = tk.Menu(menuButon, tearoff=0)
        gorevEkleMenu = tk.Menu(menuButon,tearoff=0)
        cikisyapMenu = tk.Menu(menuButon, tearoff=0)
        AraMenu = tk.Menu(menuButon,tearoff=0)

        menuBar.add_command(label="Gorev Ekle", command=self.gorevEklePencereFonksiyon)
        menuBar.add_separator()
        menuButon.add_cascade(label="Secenekler", menu=menuBar)
        menuBar.add_command(label="Tamamlanan Gorevler", command=self.tamalanmisGorevleriGosterFonksiyon)
        menuBar.add_separator()
        menuBar.add_command(label="Görev Ara", command=self.gorevAraPencereFonksiyon)
        menuBar.add_separator()
        menuBar.add_command(label="Tarih Ekle", command=self.tarihEklePencereFonksiyon)
        menuBar.add_separator()
        menuBar.add_command(label="Tarih Görüntüle", command=self.tarihleriGoruntule)
        menuBar.add_separator() #Araya ayırma çubuğu çeker
        menuBar.add_command(label="Çıkış", command=self.uygulamadanCikisYapFonksiyon)

        # Json dosyasındaki butun ogelerin listbox ilk açıldığında gozukmesi için gorevListBoxYukle foksiyonunun Çağırılması
        self.gorevListBoxYukleFonksiyon()


    def gorevEklePencereFonksiyon(self):
        #TopLevel widgetı bize pencere üstüne pencere açar
        gorevEklePencere = tk.Toplevel(self.pencere)
        gorevEklePencere.geometry("300x100")
        gorevEklePencere.title("Gorev Ekle")
        self.gorevYukleEntry = tk.Entry(gorevEklePencere,width=30)
        self.gorevYukleEntry.place(x=10, y=10)
        ekleButon = tk.Button(gorevEklePencere, text="Ekle",command=self.gorevEkleFonksiyon)
        ekleButon.place(x=220, y=8)

    # Her gorevimizi bir sozluk olarak ekliyoruz.
    # Bu sozluğun iki anahtar kelimesi var
    # Bunlardan bir tanesi gorevin kendisini
    # Diğeri tamamlanmış olup olamıdğını belirtiyor
    def gorevEkleFonksiyon(self):
        yeniGorev = self.gorevYukleEntry.get() #get() ile Entry den girdi aldık

        if yeniGorev == "":
            messagebox.showwarning("Error", "Boş görev ekleyemezsiniz.")
        else:
            self.gorevlerListe.append({"gorev":yeniGorev,"tamamlanmışlık":False})
            self.gorevleriKaydetFonksiyon()
            self.gorevListBoxYukleFonksiyon()
            self.gorevYukleEntry.delete(0,tk.END)#Entry nin içini temizledik

    def gorevTamamlaFonksiyon(self):
        secilmisOgelerinIndisleri = self.gorevGoruntulemeListbox.curselection()
        for indis in secilmisOgelerinIndisleri:#Burada birden fazla seçim i aynı anda tamamla yapmaya çalıştım
            self.gorevlerListe[indis]["tamamlanmışlık"] = True
            self.gorevlerListe[indis]["gorev"]+=" ✓" #Tamamlanan görevlerin tanında tik işareti gözükecek

        self.gorevleriKaydetFonksiyon()
        self.gorevListBoxYukleFonksiyon()
    def tamalanmisGorevleriGosterFonksiyon(self):
        tamamlananGorevlerPencere = tk.Toplevel(self.pencere)
        tamamlananGorevlerPencere.geometry("350x300")
        tamamlananGorevlerPencere.title("Tamamlanmış Gorevler")
        self.tamamlananGorevlerListBox = tk.Listbox(tamamlananGorevlerPencere,width=50)
        self.tamamlananGorevlerListBox.place(x=10,y=10)

        #Burada tk.END her sefer ListBox ın en sonuna gorevleri ekler
        # task_text ise foreach dongusu ile gorevlerin içersinde dolaşır
        for gorev in self.gorevlerListe:
            if gorev["tamamlanmışlık"]:
                task_text = f"{gorev['gorev']}"
                task_text = task_text[:-2] #Sonuna eklediğimiz boşluk ve tik karakterlerini sildik
                self.tamamlananGorevlerListBox.insert(tk.END, task_text)
    def gorevAraPencereFonksiyon(self):
        gorevAraPencere = tk.Toplevel(pencere)
        gorevAraPencere.geometry("300x100")
        gorevAraPencere.title("Search")
        gorevAraLabel = tk.Label(gorevAraPencere,text="Ara: ")
        gorevAraLabel.place(x=10,y=10)
        self.gorevAraEntry = tk.Entry(gorevAraPencere,width=30)
        self.gorevAraEntry.place(x=60,y=10)
        gorevAraButon = tk.Button(gorevAraPencere,text="Ara",command=self.gorevAraFonksiyon)
        gorevAraButon.place(x=250,y=8)

    def gorevAraFonksiyon(self):
        text = self.gorevAraEntry.get()
        for indis, gorev in enumerate(self.gorevlerListe): #Hem indisi hem görevi döndürmesi için enumarate kulanıldı
            if gorev['tamamlanmışlık']==True:
                metin = gorev['gorev']
                metin = metin[:-2]
                if metin== text:
                    messagebox.showinfo("", f"Aradığınız görev {indis + 1} indeksinde bulundu")
                    return
            else:
                if gorev['gorev'] == text:
                    messagebox.showinfo("", f"Aradığınız görev {indis + 1} indeksinde bulundu")
                    return  # Eğer değer bulunursa bu fonksiyondan çıkar
        messagebox.showwarning("","Böyle bir görev yok")


    def gorevSilFonksiyon(self):
        secilmisOgeninIndisi = self.gorevGoruntulemeListbox.curselection() #curselection seçilen indisleri içeren bir tuple döndürür
        if secilmisOgeninIndisi: #Kullanıcının bir öğe seçtiğini varsaydığımız için 0. indisi alırız her sefer
            gorevIndis = secilmisOgeninIndisi[0]
            del self.gorevlerListe[gorevIndis]
            self.gorevleriKaydetFonksiyon()
            self.gorevListBoxYukleFonksiyon()
    def tarihEklePencereFonksiyon(self):
        tarihEklePencere = tk.Toplevel(self.pencere)
        tarihEklePencere.geometry("200x100")
        tarihEklePencere.title("Tarih Ekle")
        tk.Label(tarihEklePencere, text="Tarih (GG/AA/YYYY):").place(x=10, y=10)
        self.tarihEntry = tk.Entry(tarihEklePencere, width=20)
        self.tarihEntry.place(x=10, y=30)
        tk.Button(tarihEklePencere, text="Ekle", command=self.tarihEkleFonksiyon).place(x=10, y=60)

    def tarihEkleFonksiyon(self):
        secilmisOgelerinIndisleri = self.gorevGoruntulemeListbox.curselection()
        if secilmisOgelerinIndisleri:
            gorevIndis = secilmisOgelerinIndisleri[0]
            tarih_girisi = self.tarihEntry.get()
            try:
                tarih_objesi = datetime.strptime(tarih_girisi, "%d/%m/%Y")#tarih_girisini strptime fonksiyonu ile datetimea dönüştürüldü
                self.gorevlerListe[gorevIndis]["tarih"] = tarih_objesi.strftime("%d/%m/%Y")#Gün ay yıl bilgisini strftime fonksiyonu ile yeniden düzenleyip tarih anahtar kelimesine atadık
                messagebox.showinfo("", f"Tarih başarıyla eklendi: {tarih_objesi.strftime('%d/%m/%Y')}")
                self.gorevleriKaydetFonksiyon()
                self.gorevListBoxYukleFonksiyon()
            except ValueError:
                messagebox.showwarning("", "Geçersiz tarih formatı. Lütfen GG/AA/YYYY formatında girin.")
        else:
            messagebox.showwarning("", "Lütfen bir görev seçin.")
    def tarihleriGoruntule(self):
        tarihGoruntulePencere = tk.Toplevel(self.pencere)
        tarihGoruntulePencere.geometry("300x100")
        tarihGoruntulePencere.title("Tarihleri Görüntüle")

        # Seçilen görevin indisini al
        secilmisOgeIndisi = self.gorevGoruntulemeListbox.curselection()
        if not secilmisOgeIndisi:
            messagebox.showwarning("Hata", "Lütfen bir görev seçin.")
            return

        seciliGorev = self.gorevlerListe[secilmisOgeIndisi[0]]
        if 'tarih' in seciliGorev and seciliGorev['tarih']: #Öncelikle seçili görevde tarih anahtar kelimesinin varlığı kontrol edilir. Ardından var ise bu değerin varlığını kontrol eder.
            tarihLabel = tk.Label(tarihGoruntulePencere, text=f"Görev Tarihi: {seciliGorev['tarih']}")
            tarihLabel.place(x=10, y=10)
        else:
            tarihLabel = tk.Label(tarihGoruntulePencere, text="Tarih Bilgisi Yok")
            tarihLabel.place(x=10, y=10)


    def gorevListBoxYukleFonksiyon(self):
        # ListBox widgetındaki butun gorevleri siler ve yeniden ekler
        self.gorevGoruntulemeListbox.delete(0,tk.END)
        for gorev in self.gorevlerListe:
            task_text = f"{gorev['gorev']}"
            self.gorevGoruntulemeListbox.insert(tk.END,task_text) #tk.END her zmaan listboxın en sonuna ekleyeceğimizi belirtir

    def gorevleriAcFonksiyon(self):
        try:
            with open('gorevler.json', 'r') as dosya:
                self.gorevlerListe = json.load(dosya)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showwarning("Dosya Bulunamadı","Lutfen belirttiğiniz dosyayı oluşturunuz...")
            return [ ]
    def gorevleriKaydetFonksiyon(self):
        # Yaptığımız işlemleri Json a kaydeder
        with open("gorevler.json","w") as dosya:
            json.dump(self.gorevlerListe,dosya)
    def uygulamadanCikisYapFonksiyon(self):
        self.pencere.destroy()


pencere = tk.Tk()
pencere.geometry("300x300")
pencere.config(bg="gray")
pencere.title("Yapılacaklar Listesi")
YapilacaklarListesi(pencere)
pencere.mainloop()