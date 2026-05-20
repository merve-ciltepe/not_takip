from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import database as db
from models import Ogrenci, Ders, Not


app = Flask(__name__)
app.secret_key = 'gizli_anahtar_123'  # Flash mesajları için zorunlu


db.init_db()


KULLANICILAR = {
    'admin': {'sifre': 'admin123', 'rol': 'admin'},
    'ogrenci': {'sifre': 'ogrenci123', 'rol': 'ogrenci'}
}



def giris_gerekli(f):
    """Giriş yapılmamışsa login sayfasına yönlendir."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'kullanici' not in session:
            flash('Bu sayfayı görmek için giriş yapmalısınız!', 'warning')
            return redirect(url_for('giris'))
        return f(*args, **kwargs)
    return decorated

def admin_gerekli(f):
    """Admin değilse ana sayfaya yönlendir."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('rol') != 'admin':
            flash('Bu işlem için admin yetkisi gereklidir!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


@app.route('/giris', methods=['GET', 'POST'])
def giris():
    """Kullanıcı giriş sayfası."""
    if 'kullanici' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        kullanici_adi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        if kullanici_adi in KULLANICILAR and KULLANICILAR[kullanici_adi]['sifre'] == sifre:
            session['kullanici'] = kullanici_adi
            session['rol'] = KULLANICILAR[kullanici_adi]['rol']
            flash(f'Hoş geldiniz, {kullanici_adi}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'danger')
    return render_template('giris.html')

@app.route('/cikis')
def cikis():
    """Oturumu kapatır."""
    session.clear()
    flash('Başarıyla çıkış yapıldı!', 'success')
    return redirect(url_for('giris'))


@app.route('/')
@giris_gerekli
def index():
    """Ana sayfa — özet istatistikler gösterir."""
    ogrenciler = db.ogrenci_listele()
    dersler = db.ders_listele()
    notlar = db.not_listele()
    return render_template('index.html',
                           ogrenci_sayisi=len(ogrenciler),
                           ders_sayisi=len(dersler),
                           not_sayisi=len(notlar))



@app.route('/ogrenciler')
@giris_gerekli
def ogrenciler():
    """Tüm öğrencileri listeler."""
    liste = db.ogrenci_listele()
    return render_template('ogrenciler.html', ogrenciler=liste)

@app.route('/ogrenci/ekle', methods=['GET', 'POST'])
@giris_gerekli
@admin_gerekli
def ogrenci_ekle():
    """GET: formu göster, POST: formu işle."""
    if request.method == 'POST':
        try:
            o = Ogrenci(
                request.form['ad'],
                request.form['soyad'],
                request.form['email'],
                request.form['ogrenci_no']
            )
            hatalar = o.dogrula()
            if hatalar:
                for h in hatalar:
                    flash(h, 'danger')
                return redirect(url_for('ogrenci_ekle'))
            db.ogrenci_ekle(o.ad, o.soyad, o.email, o.ogrenci_no)
            flash('Öğrenci başarıyla eklendi!', 'success')
            return redirect(url_for('ogrenciler'))
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('ogrenci_ekle'))
    return render_template('ogrenci_ekle.html')

@app.route('/ogrenci/duzenle/<int:ogrenci_id>', methods=['GET', 'POST'])
@giris_gerekli
@admin_gerekli
def ogrenci_duzenle(ogrenci_id):
    """Öğrenci bilgilerini günceller."""
    ogrenci = db.ogrenci_getir(ogrenci_id)
    if not ogrenci:
        flash('Öğrenci bulunamadı!', 'danger')
        return redirect(url_for('ogrenciler'))
    if request.method == 'POST':
        try:
            o = Ogrenci(
                request.form['ad'],
                request.form['soyad'],
                request.form['email'],
                ogrenci['ogrenci_no']
            )
            hatalar = o.dogrula()
            if hatalar:
                for h in hatalar:
                    flash(h, 'danger')
                return redirect(url_for('ogrenci_duzenle', ogrenci_id=ogrenci_id))
            db.ogrenci_guncelle(ogrenci_id, o.ad, o.soyad, o.email)
            flash('Öğrenci güncellendi!', 'success')
            return redirect(url_for('ogrenciler'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('ogrenci_duzenle.html', ogrenci=ogrenci)

@app.route('/ogrenci/sil/<int:ogrenci_id>', methods=['POST'])
@giris_gerekli
@admin_gerekli
def ogrenci_sil(ogrenci_id):
    """Öğrenciyi siler."""
    try:
        db.ogrenci_sil(ogrenci_id)
        flash('Öğrenci silindi!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('ogrenciler'))



@app.route('/dersler')
@giris_gerekli
def dersler():
    """Tüm dersleri listeler."""
    liste = db.ders_listele()
    return render_template('dersler.html', dersler=liste)

@app.route('/ders/ekle', methods=['GET', 'POST'])
@giris_gerekli
@admin_gerekli
def ders_ekle():
    """Yeni ders ekler."""
    if request.method == 'POST':
        try:
            d = Ders(
                request.form['ders_adi'],
                request.form['kredi'],
                request.form['ogretmen']
            )
            hatalar = d.dogrula()
            if hatalar:
                for h in hatalar:
                    flash(h, 'danger')
                return redirect(url_for('ders_ekle'))
            db.ders_ekle(d.ders_adi, d.kredi, d.ogretmen)
            flash('Ders başarıyla eklendi!', 'success')
            return redirect(url_for('dersler'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('ders_ekle.html')

@app.route('/ders/sil/<int:ders_id>')
@giris_gerekli
@admin_gerekli
def ders_sil(ders_id):
    """Dersi siler."""
    try:
        db.ders_sil(ders_id)
        flash('Ders silindi!', 'success')
    except Exception as e:
        flash('Bu derse ait notlar var, önce notları silin!', 'danger')
    return redirect(url_for('dersler'))
@app.route('/ders/duzenle/<int:ders_id>', methods=['GET', 'POST'])
@giris_gerekli
@admin_gerekli
def ders_duzenle(ders_id):
    """Ders bilgilerini günceller."""
    ders = db.ders_getir(ders_id)
    if not ders:
        flash('Ders bulunamadı!', 'danger')
        return redirect(url_for('dersler'))
    if request.method == 'POST':
        try:
            d = Ders(
                request.form['ders_adi'],
                request.form['kredi'],
                request.form['ogretmen']
            )
            hatalar = d.dogrula()
            if hatalar:
                for h in hatalar:
                    flash(h, 'danger')
                return redirect(url_for('ders_duzenle', ders_id=ders_id))
            db.ders_guncelle(ders_id, d.ders_adi, d.kredi, d.ogretmen)
            flash('Ders güncellendi!', 'success')
            return redirect(url_for('dersler'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('ders_duzenle.html', ders=ders)



@app.route('/notlar')
@giris_gerekli
def notlar():
    """Tüm notları listeler."""
    liste = db.not_listele()
    return render_template('notlar.html', notlar=liste)

@app.route('/not/ekle', methods=['GET', 'POST'])
@giris_gerekli
@admin_gerekli
def not_ekle():
    """Yeni not ekler."""
    ogrenciler = db.ogrenci_listele()
    dersler = db.ders_listele()
    if request.method == 'POST':
        try:
            n = Not(
                request.form['ogrenci_id'],
                request.form['ders_id'],
                request.form['not_degeri'],
                request.form['not_turu']
            )
            hatalar = n.dogrula()
            if hatalar:
                for h in hatalar:
                    flash(h, 'danger')
                return redirect(url_for('not_ekle'))
            db.not_ekle(n.ogrenci_id, n.ders_id, n.not_degeri, n.not_turu)
            flash('Not başarıyla eklendi!', 'success')
            return redirect(url_for('notlar'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('not_ekle.html', ogrenciler=ogrenciler, dersler=dersler)

@app.route('/not/sil/<int:not_id>', methods=['POST'])
@giris_gerekli
@admin_gerekli
def not_sil(not_id):
    """Notu siler."""
    try:
        db.not_sil(not_id)
        flash('Not silindi!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('notlar'))
@app.route('/not/duzenle/<int:not_id>', methods=['GET', 'POST'])
@giris_gerekli
@admin_gerekli
def not_duzenle(not_id):
    """Notu günceller."""
    not_kaydi = db.not_getir(not_id)
    if not not_kaydi:
        flash('Not bulunamadı!', 'danger')
        return redirect(url_for('notlar'))
    if request.method == 'POST':
        try:
            n = Not(
                not_kaydi['ogrenci_id'],
                not_kaydi['ders_id'],
                request.form['not_degeri'],
                request.form['not_turu']
            )
            hatalar = n.dogrula()
            if hatalar:
                for h in hatalar:
                    flash(h, 'danger')
                return redirect(url_for('not_duzenle', not_id=not_id))
            db.not_guncelle(not_id, n.not_degeri, n.not_turu)
            flash('Not güncellendi!', 'success')
            return redirect(url_for('notlar'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('not_duzenle.html', not_kaydi=not_kaydi)


@app.route('/istatistik')
@giris_gerekli
def istatistik():
    """Pandas ve Matplotlib ile istatistik sayfası."""
    import matplotlib
    matplotlib.use('Agg')  
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    ders_ortalama, tur_ortalama, genel, ogrenci_ortalama, harf_notlari = db.istatistik_getir()
    
    
    not_degerleri = [n['not_degeri'] for n in db.not_listele()]
    np_dizi = np.array(not_degerleri)
    numpy_istatistik = {
        'standart_sapma': round(float(np.std(np_dizi)), 2),
        'medyan': round(float(np.median(np_dizi)), 2),
        'varyans': round(float(np.var(np_dizi)), 2)
    }

    # Grafik 1: Ders bazında çubuk grafik
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#09090b')
    ax.set_facecolor('#09090b')
    dersler = list(ders_ortalama.keys())
    ortalamalar = list(ders_ortalama.values())
    renkler = ['#ec4899', '#a855f7', '#d946ef', '#f43f5e', '#8b5cf6']
    bars = ax.bar(dersler, ortalamalar, color=renkler[:len(dersler)], 
                  edgecolor='none', width=0.5)
    ax.set_title('Ders Bazında Ortalama Notlar', color='white', fontsize=14, pad=15)
    ax.set_ylabel('Ortalama Not', color='#f9a8d4')
    ax.tick_params(colors='#f9a8d4')
    ax.set_ylim(0, 100)
    for bar, val in zip(bars, ortalamalar):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}', ha='center', va='bottom', color='white', fontsize=10)
    for spine in ax.spines.values():
        spine.set_edgecolor('#ec4899')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    grafik1_yolu = os.path.join('static', 'img', 'grafik1.png')
    plt.savefig(grafik1_yolu, facecolor='#09090b', dpi=100)
    plt.close()
    

    # Grafik 2: Not türü pasta grafik
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    fig2.patch.set_facecolor('#09090b')
    ax2.set_facecolor('#09090b')
    turler = list(tur_ortalama.keys())
    degerler = list(tur_ortalama.values())
    renkler2 = ['#ec4899', '#a855f7', '#d946ef', '#f43f5e']
    ax2.pie(degerler, labels=turler, colors=renkler2[:len(turler)],
            autopct='%1.1f%%', textprops={'color': 'white'})
    ax2.set_title('Not Türü Ortalamaları', color='white', fontsize=14)
    plt.tight_layout()
    grafik2_yolu = os.path.join('static', 'img', 'grafik2.png')
    plt.savefig(grafik2_yolu, facecolor='#09090b', dpi=100)
    plt.close()

    return render_template('istatistik.html',
                           genel=genel,
                           ders_ortalama=ders_ortalama,
                           tur_ortalama=tur_ortalama,
                           ogrenci_ortalama=ogrenci_ortalama,
                           numpy_istatistik=numpy_istatistik,
                           harf_notlari=harf_notlari)


@app.route('/csv/indir')
@giris_gerekli
@admin_gerekli
def csv_indir():
    """Tüm notları CSV dosyası olarak indirir."""
    import csv
    import io
    from flask import Response

    notlar = db.not_listele()

    
    output = io.StringIO()
    writer = csv.writer(output)

    
    writer.writerow(['Öğrenci No', 'Ad', 'Soyad', 'Ders', 'Not Türü', 'Not', 'Tarih'])

    
    for n in notlar:
        writer.writerow([
            '',
            n['ad'],
            n['soyad'],
            n['ders_adi'],
            n['not_turu'],
            n['not_degeri'],
            n['tarih']
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=notlar.csv'}
    )    



@app.errorhandler(404)
def bulunamadi(e):
    """404 hata sayfası."""
    return render_template('hata.html', kod=404, mesaj='Sayfa bulunamadı!'), 404

@app.errorhandler(500)
def sunucu_hatasi(e):
    """500 hata sayfası."""
    return render_template('hata.html', kod=500, mesaj='Sunucu hatası!'), 500

if __name__ == '__main__':
    app.run(debug=True)
