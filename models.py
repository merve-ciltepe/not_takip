

class Ogrenci:
    """Öğrenci modelini temsil eden sınıf."""

    def __init__(self, ad, soyad, email, ogrenci_no):
        self.ad = ad.strip().title()        
        self.soyad = soyad.strip().title()  
        self.email = email.strip().lower()  
        self.ogrenci_no = ogrenci_no.strip()

    def dogrula(self):
        """Verilerin geçerli olup olmadığını kontrol eder."""
        hatalar = []
        if not self.ad:
            hatalar.append("Ad boş olamaz.")
        if not self.soyad:
            hatalar.append("Soyad boş olamaz.")
        if '@' not in self.email:
            hatalar.append("Geçerli bir email giriniz.")
        if not self.ogrenci_no:
            hatalar.append("Öğrenci no boş olamaz.")
        return hatalar

    def __repr__(self):
        return f"<Ogrenci {self.ogrenci_no}: {self.ad} {self.soyad}>"


class Ders:
    """Ders modelini temsil eden sınıf."""

    def __init__(self, ders_adi, kredi, ogretmen):
        self.ders_adi = ders_adi.strip()
        self.kredi = int(kredi)
        self.ogretmen = ogretmen.strip().title()

    def dogrula(self):
        """Verilerin geçerli olup olmadığını kontrol eder."""
        hatalar = []
        if not self.ders_adi:
            hatalar.append("Ders adı boş olamaz.")
        if self.kredi < 1 or self.kredi > 8:
            hatalar.append("Kredi 1 ile 8 arasında olmalıdır.")
        if not self.ogretmen:
            hatalar.append("Öğretmen adı boş olamaz.")
        return hatalar

    def __repr__(self):
        return f"<Ders {self.ders_adi} ({self.kredi} kredi)>"


class Not:
    """Not modelini temsil eden sınıf."""

    NOT_TURLERI = ['Vize', 'Final', 'Ödev', 'Quiz']

    def __init__(self, ogrenci_id, ders_id, not_degeri, not_turu):
        self.ogrenci_id = ogrenci_id
        self.ders_id = ders_id
        self.not_degeri = float(not_degeri)
        self.not_turu = not_turu

    def dogrula(self):
        """Verilerin geçerli olup olmadığını kontrol eder."""
        hatalar = []
        if self.not_degeri < 0 or self.not_degeri > 100:
            hatalar.append("Not 0 ile 100 arasında olmalıdır.")
        if self.not_turu not in self.NOT_TURLERI:
            hatalar.append(f"Not türü şunlardan biri olmalı: {self.NOT_TURLERI}")
        return hatalar

    def harf_notu(self):
        """Not değerine göre harf notu döndürür."""
        if self.not_degeri >= 90:
            return 'AA'
        elif self.not_degeri >= 80:
            return 'BA'
        elif self.not_degeri >= 70:
            return 'BB'
        elif self.not_degeri >= 60:
            return 'CB'
        elif self.not_degeri >= 50:
            return 'CC'
        else:
            return 'FF'

    def __repr__(self):
        return f"<Not {self.not_turu}: {self.not_degeri} ({self.harf_notu()})>"
