# ☁️ Ayhan CloudStream Deposu

[![Private Repository](https://img.shields.io/badge/🔒-Private%20Repo-red)](#)
[![Güncelleme](https://img.shields.io/badge/📅-Ayda%202%20Kez-blue)](#)

**Kişisel CloudStream eklenti koleksiyonu - Arkadaşlar için**

---

## 🔐 Özel Depo - Sadece Davetliler

Bu repository **private** (özel) bir depodur. Sadece davet edilen kişiler erişebilir.

### 📱 Kurulum (Arkadaşlar İçin)

#### Adım 1: Token Alın
Repository sahibinden (Ayhan) **Personal Access Token (PAT)** alın.

#### Adım 2: CloudStream'e Ekleyin

**CloudStream Uygulaması:**
1. Settings → Extensions → Repositories
2. "Add Repository" butonuna tıklayın
3. **URL:**
   ```
   https://raw.githubusercontent.com/ayhankucuk/ayhn/master/repo.json
   ```
4. **Headers ekleyin:**
   - Key: `Authorization`
   - Value: `token SIZE_VERILEN_TOKEN`

5. Repository eklenecek ve eklentiler görünecek!

---

## 🎯 NSFW Deposu (Yetişkin İçerik +18)

**URL:**
```
https://raw.githubusercontent.com/ayhankucuk/ayhn/master/nsfw_repo.json
```

Aynı token ile erişilebilir.

---

## 📂 Mevcut Kategoriler

### 🎬 Film & Dizi
- **TR-Cinema** - Türkçe film ve dizi siteleri
- **Disney** - Disney+ içerikleri
- **Exxen** - Exxen orijinal içerikleri
- **Gain** - Gain orijinal içerikleri
- **Netflix** - Netflix Mirror

### 📺 TV & Canlı Yayın
- **TR-TV** - Canlı TV ve spor kanalları
- **Belgesel** - Belgesel platformları

### 🎭 Anime & Çizgi
- **TR-Anime** - Türkçe anime siteleri

### 🌐 Global
- **Global-Mixed** - Uluslararası platformlar

### 🔞 Yetişkin
- **NSFW** - Yetişkin içerik (+18)

---

## 🔧 Yönetim (Sadece Repo Sahibi)

### Eklentileri Güncelleme

```bash
# Tüm işlemleri otomatik yap
python ayhan_update.py all

# Sadece linkleri güncelle
python ayhan_update.py update

# Durumu göster
python ayhan_update.py status

# GitHub'a yükle
python ayhan_update.py sync
```

---

## 🔒 Gizlilik ve Güvenlik

- ✅ Repository **private** olarak ayarlanmıştır
- ✅ Sadece collaborator olarak eklenen kişiler görebilir
- ✅ Token paylaşıldığı kişiler erişebilir
- ⚠️ Token'ınızı kimseyle paylaşmayın (veya sadece güvendiğiniz kişilerle)
- ⚠️ Token sızdırılırsa yeni token oluşturup eskisini iptal edin

---

## 📅 Güncelleme Programı

Eklentiler **ayda 2 kez** güncellenir:
- Çalışmayan siteler kaldırılır
- Yeni siteler eklenir
- Link değişiklikleri güncellenir

---

## 🌐 Telif Hakkı ve Lisans

* *Copyright (C) 2026 by Ayhan*
* Kişisel kullanım için
* Orijinal proje: [keyiflerolsun/Kekik-cloudstream](https://github.com/keyiflerolsun/Kekik-cloudstream)

---

## 📞 İletişim

Sorularınız için Ayhan ile iletişime geçin.
