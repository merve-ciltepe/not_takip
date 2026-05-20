import sqlite3
import os


DB_YOLU = os.path.join(os.path.dirname(__file__), 'data.db')

def get_db():
    """Veritabanı bağlantısı oluşturur ve döndürür."""
    conn = sqlite3.connect(DB_YOLU)
    conn.row_factory = sqlite3.Row  
    conn.execute('PRAGMA foreign_keys = ON')  
    return conn

def init_db():
    """schema.sql dosyasını okuyarak tabloları oluşturur."""
    conn = get_db()
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print("Veritabanı başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        conn.close()


def ogrenci_listele():
    """Tüm öğrencileri listeler."""
    conn = get_db()
    try:
        rows = conn.execute('SELECT * FROM ogrenciler ORDER BY soyad').fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def ogrenci_getir(ogrenci_id):
    """ID'ye göre tek öğrenci getirir."""
    conn = get_db()
    try:
        row = conn.execute('SELECT * FROM ogrenciler WHERE id=?', (ogrenci_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def ogrenci_ekle(ad, soyad, email, ogrenci_no):
    """Yeni öğrenci ekler."""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO ogrenciler (ad, soyad, email, ogrenci_no) VALUES (?,?,?,?)',
            (ad, soyad, email, ogrenci_no)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception('Bu email veya öğrenci no zaten kayıtlı!')
    finally:
        conn.close()

def ogrenci_guncelle(ogrenci_id, ad, soyad, email):
    """Öğrenci bilgilerini günceller."""
    conn = get_db()
    try:
        conn.execute(
            'UPDATE ogrenciler SET ad=?, soyad=?, email=? WHERE id=?',
            (ad, soyad, email, ogrenci_id)
        )
        conn.commit()
    finally:
        conn.close()
def ogrenci_sil(ogrenci_id):
    """Öğrenciyi ve bağlı tüm notlarını siler."""
    conn = get_db()
    try:
        # Önce öğrenciye ait notları sil
        conn.execute('DELETE FROM notlar WHERE ogrenci_id=?', (ogrenci_id,))
        # Sonra öğrenciyi sil
        conn.execute('DELETE FROM ogrenciler WHERE id=?', (ogrenci_id,))
        conn.commit()
    finally:
        conn.close()




def ders_listele():
    """Tüm dersleri listeler."""
    conn = get_db()
    try:
        rows = conn.execute('SELECT * FROM dersler ORDER BY ders_adi').fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
def ders_getir(ders_id):
    """ID'ye göre tek ders getirir."""
    conn = get_db()
    try:
        row = conn.execute('SELECT * FROM dersler WHERE id=?', (ders_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()        

def ders_ekle(ders_adi, kredi, ogretmen):
    """Yeni ders ekler."""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO dersler (ders_adi, kredi, ogretmen) VALUES (?,?,?)',
            (ders_adi, kredi, ogretmen)
        )
        conn.commit()
    finally:
        conn.close()

def ders_guncelle(ders_id, ders_adi, kredi, ogretmen):
    """Ders bilgilerini günceller."""
    conn = get_db()
    try:
        conn.execute(
            'UPDATE dersler SET ders_adi=?, kredi=?, ogretmen=? WHERE id=?',
            (ders_adi, kredi, ogretmen, ders_id)
        )
        conn.commit()
    finally:
        conn.close()

def ders_sil(ders_id):
    """Dersi ve bağlı tüm notlarını siler."""
    conn = get_db()
    try:
        # Önce derse ait notları sil
        conn.execute('DELETE FROM notlar WHERE ders_id=?', (ders_id,))
        # Sonra dersi sil
        conn.execute('DELETE FROM dersler WHERE id=?', (ders_id,))
        conn.commit()
    finally:
        conn.close()



def not_listele(ogrenci_id=None):
    """Tüm notları listeler, ogrenci_id verilirse sadece o öğrencinin notları."""
    conn = get_db()
    try:
        if ogrenci_id:
            rows = conn.execute('''
                SELECT notlar.*, ogrenciler.ad, ogrenciler.soyad, dersler.ders_adi
                FROM notlar
                JOIN ogrenciler ON notlar.ogrenci_id = ogrenciler.id
                JOIN dersler ON notlar.ders_id = dersler.id
                WHERE notlar.ogrenci_id=?
            ''', (ogrenci_id,)).fetchall()
        else:
            rows = conn.execute('''
                SELECT notlar.*, ogrenciler.ad, ogrenciler.soyad, dersler.ders_adi
                FROM notlar
                JOIN ogrenciler ON notlar.ogrenci_id = ogrenciler.id
                JOIN dersler ON notlar.ders_id = dersler.id
            ''').fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def not_ekle(ogrenci_id, ders_id, not_degeri, not_turu):
    """Yeni not ekler."""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO notlar (ogrenci_id, ders_id, not_degeri, not_turu) VALUES (?,?,?,?)',
            (ogrenci_id, ders_id, not_degeri, not_turu)
        )
        conn.commit()
    finally:
        conn.close()

def not_guncelle(not_id, not_degeri, not_turu):
    """Notu günceller."""
    conn = get_db()
    try:
        conn.execute(
            'UPDATE notlar SET not_degeri=?, not_turu=? WHERE id=?',
            (not_degeri, not_turu, not_id)
        )
        conn.commit()
    finally:
        conn.close()

def not_sil(not_id):
    """Notu siler."""
    conn = get_db()
    try:
        conn.execute('DELETE FROM notlar WHERE id=?', (not_id,))
        conn.commit()
    finally:
        conn.close()        


def not_getir(not_id):
    """ID'ye göre tek not getirir."""
    conn = get_db()
    try:
        row = conn.execute('SELECT * FROM notlar WHERE id=?', (not_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
def seed_data():
    """Örnek verileri veritabanına ekler."""
    conn = get_db()
    try:
        
        ogrenciler = [
            ('Merve', 'Çiltepe', 'merve@gmail.com', '2024001'),
            ('Ali', 'Yılmaz', 'ali@gmail.com', '2024002'),
            ('Ayşe', 'Kaya', 'ayse@gmail.com', '2024003'),
            ('Mehmet', 'Demir', 'mehmet@gmail.com', '2024004'),
            ('Zeynep', 'Şahin', 'zeynep@gmail.com', '2024005'),
        ]
        for o in ogrenciler:
            try:
                conn.execute('INSERT INTO ogrenciler (ad, soyad, email, ogrenci_no) VALUES (?,?,?,?)', o)
            except:
                pass

        
        dersler = [
            ('Programlamaya Giriş', 3, 'Dr. Ahmet Yılmaz'),
            ('Matematik', 4, 'Prof. Elif Kaya'),
            ('Fizik', 3, 'Dr. Can Demir'),
            ('Veri Yapıları', 3, 'Dr. Selin Çelik'),
            ('Web Geliştirme', 2, 'Öğr. Gör. Murat Arslan'),
        ]
        for d in dersler:
            try:
                conn.execute('INSERT INTO dersler (ders_adi, kredi, ogretmen) VALUES (?,?,?)', d)
            except:
                pass

        
        notlar = [
            (1, 1, 85.0, 'Vize'),
            (1, 2, 72.0, 'Final'),
            (2, 1, 90.0, 'Vize'),
            (2, 3, 65.0, 'Ödev'),
            (3, 2, 78.0, 'Final'),
            (3, 4, 88.0, 'Quiz'),
            (4, 1, 55.0, 'Vize'),
            (4, 5, 92.0, 'Final'),
            (5, 3, 45.0, 'Ödev'),
            (5, 4, 70.0, 'Vize'),
        ]
        for n in notlar:
            try:
                conn.execute('INSERT INTO notlar (ogrenci_id, ders_id, not_degeri, not_turu) VALUES (?,?,?,?)', n)
            except:
                pass

        conn.commit()
        print("Örnek veriler başarıyla eklendi!")
    finally:
        conn.close()
def istatistik_getir():
    """Pandas ile istatistik hesaplar."""
    import pandas as pd
    conn = get_db()
    try:
        
        rows = conn.execute('''
            SELECT ogrenciler.ad, ogrenciler.soyad, dersler.ders_adi, 
                   notlar.not_degeri, notlar.not_turu
            FROM notlar
            JOIN ogrenciler ON notlar.ogrenci_id = ogrenciler.id
            JOIN dersler ON notlar.ders_id = dersler.id
        ''').fetchall()
        
        df = pd.DataFrame([dict(r) for r in rows], 
                          columns=['ad', 'soyad', 'ders_adi', 'not_degeri', 'not_turu'])
        
        
        ders_ortalama = df.groupby('ders_adi')['not_degeri'].mean().round(2).to_dict()
        
        
        tur_ortalama = df.groupby('not_turu')['not_degeri'].mean().round(2).to_dict()
        
        
        genel = {
            'ortalama': round(df['not_degeri'].mean(), 2),
            'en_yuksek': df['not_degeri'].max(),
            'en_dusuk': df['not_degeri'].min(),
            'toplam_not': len(df)
        }
        
        df['ad_soyad'] = df['ad'] + ' ' + df['soyad']
        ogrenci_ortalama = df.groupby('ad_soyad')['not_degeri'].mean().round(2).to_dict()
        
        harf_notlari = {ogrenci: harf_notu_hesapla(ort) for ogrenci, ort in ogrenci_ortalama.items()}
        return ders_ortalama, tur_ortalama, genel, ogrenci_ortalama, harf_notlari
    finally:
        conn.close()  


def harf_notu_hesapla(not_degeri):
    """
    Özyinelemeli fonksiyon: Not değerine göre harf notu hesaplar.
    Not 0'ın altına düşerse FF döndürür.
    """
    if not_degeri < 0:
        return 'FF'
    elif not_degeri >= 90:
        return 'AA'
    elif not_degeri >= 80:
        return 'BA'
    elif not_degeri >= 70:
        return 'BB'
    elif not_degeri >= 60:
        return 'CB'
    elif not_degeri >= 50:
        return 'CC'
    else:
        return harf_notu_hesapla(not_degeri - 1)           
                  