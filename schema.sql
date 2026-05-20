-- schema.sql
CREATE TABLE IF NOT EXISTS ogrenciler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    ogrenci_no TEXT NOT NULL UNIQUE,
    kayit_tarihi TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS dersler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ders_adi TEXT NOT NULL,
    kredi INTEGER NOT NULL,
    ogretmen TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER NOT NULL REFERENCES ogrenciler(id),
    ders_id INTEGER NOT NULL REFERENCES dersler(id),
    not_degeri REAL NOT NULL,
    not_turu TEXT NOT NULL,
    tarih TEXT DEFAULT (date('now'))
);