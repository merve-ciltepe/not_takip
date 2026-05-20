# 🎓 Öğrenci Not Takip Sistemi
Python Flask ve SQLite3 ile geliştirilmiş web tabanlı öğrenci not takip uygulaması.

## 🚀 Kurulum

### Gereksinimler
- Python 3.10+
- pip

### Adımlar

1. Sanal ortamı oluşturun ve aktif edin:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

4. Tarayıcıda açın: `http://127.0.0.1:5000`

## 👤 Giriş Bilgileri

- **Admin**: kullanıcı adı: `admin` / şifre: `admin123`
- **Öğrenci**: kullanıcı adı: `ogrenci` / şifre: `ogrenci123`

## ✨ Özellikler

- Öğrenci Yönetimi: Ekle, listele, düzenle, sil
- Ders Yönetimi: Ekle, listele, düzenle, sil
- Not Yönetimi: Ekle, listele, düzenle, sil
- Admin/User Sistemi: Rol bazlı yetkilendirme
- İstatistik Sayfası: Pandas ve Matplotlib ile grafikler
- CSV Dışa Aktarma: Notları CSV olarak indir

## 🗄️ Veritabanı
3 tablo ve aralarında foreign key ilişkileri:

- `ogrenciler`: id, ad, soyad, email, ogrenci_no, kayit_tarihi
- `dersler`: id, ders_adi, kredi, ogretmen
- `notlar`: id, ogrenci_id (FK), ders_id (FK), not_degeri, not_turu, tarih

## 🛠️ Kullanılan Teknolojiler

- **Backend**: Python, Flask, SQLite3
- **Frontend**: HTML, CSS, Bootstrap 5
- **Veri Analizi**: Pandas, Matplotlib, NumPy
- **Tasarım**: Antigravity (AI tasarım aracı)
