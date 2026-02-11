# ! Bu araç @ayhankucuk için "Tek Tıkla Güncelleme" ve Repo Yönetimi amacıyla hazırlanmıştır.

import os
import re
import json
import base64
import requests
import urllib3
from cloudscraper import CloudScraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# SSL Uyarılarını kapat (Self-signed sertifikalı siteler için)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AyhanManage:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.oturum = CloudScraper()
        # Ana kategoriler ve içerdikleri eklentiler
        self.categories_map = {
            "TR-Cinema": ["FullHDFilm", "FilmMakinesi", "DiziBox", "Dizilla", "JetFilmizle", "WebteIzle", "FilmModu", "HDFilmCehennemi", "FullHDFilmizlesene", "SetFilmIzle", "UgurFilm", "KultFilmler", "SuperFilmGeldi", "RareFilmm", "SinemaCX", "SezonlukDizi", "DiziYou", "DiziMom", "DiziPal", "DiziKorea", "KoreanTurk"],
            "TR-Anime": ["TurkAnime", "AnimeciX", "CizgiMax"],
            "TR-TV": ["CanliTV", "InatBox", "RecTV", "GolgeTV"],
            "Global-Mixed": ["YouTube", "NetflixMirror", "YoTurkish", "Watch2Movies", "IzleAI"],
            "Belgesel": ["BelgeselX"]
        }

    def get_all_plugins(self):
        """Tüm eklenti klasörlerini ve kategorilerini dinamik olarak bulur."""
        plugins = []
        for root, dirs, files in os.walk(self.base_dir):
            # Gizli klasörleri ve sistem klasörlerini atla
            dirs[:] = [d for d in dirs if not d.startswith((".", "gradle", "__Temel", "build", "src"))]
            
            if "build.gradle.kts" in files:
                # Ana klasörün kendisini eklenti olarak sayma
                if os.path.abspath(root) == os.path.abspath(self.base_dir):
                    continue
                    
                plugin_name = os.path.basename(root)
                # Eğer root ana dizin değilse, ana dizinin bir altındaki klasör kategoridir
                rel_path = os.path.relpath(root, self.base_dir)
                parts = rel_path.split(os.sep)
                
                category = "Genel"
                if len(parts) > 1:
                    category = parts[0] # Klasör ismini kategori yap (Örn: TR-Cinema/Dizilla -> TR-Cinema)
                
                plugins.append({
                    "name": plugin_name,
                    "path": root,
                    "category": category
                })
        return plugins

    def _rectv_ver(self):
        istek = self.oturum.post(
            url     = "https://firebaseremoteconfig.googleapis.com/v1/projects/791583031279/namespaces/firebase:fetch",
            headers = {
                "X-Goog-Api-Key"    : "AIzaSyBbhpzG8Ecohu9yArfCO5tF13BQLhjLahc",
                "X-Android-Package" : "com.rectv.shot",
                "User-Agent"        : "Dalvik/2.1.0 (Linux; U; Android 12)",
            },
            json    = {
                "appBuild"      : "81",
                "appInstanceId" : "evON8ZdeSr-0wUYxf0qs68",
                "appId"         : "1:791583031279:android:1",
            },
            verify  = False
        )
        return istek.json().get("entries", {}).get("api_url", "").replace("/api/", "")

    def _golgetv_ver(self):
        istek = self.oturum.get("https://raw.githubusercontent.com/sevdaliyim/sevdaliyim/refs/heads/main/ssl2.key", verify=False).text
        cipher = AES.new(b"trskmrskslmzbzcnfstkcshpfstkcshp", AES.MODE_CBC, b"trskmrskslmzbzcn")
        encrypted_data = base64.b64decode(istek)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode("utf-8")
        return json.loads(decrypted_data, strict=False)["apiUrl"]

    def update_main_urls(self):
        print("[*] Bağlantılar kontrol ediliyor...")
        plugins = self.get_all_plugins()
        for p_info in plugins:
            p = p_info["name"]
            kt_path = self._find_kt_file(p_info["path"], p)
            if not kt_path: continue
            
            with open(kt_path, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'override\s+var\s+mainUrl\s*=\s*"([^"]+)"', content)
                if match:
                    old_url = match.group(1)
                    try:
                        if p == "RecTV":
                            new_url = self._rectv_ver().rstrip("/")
                        elif p == "GolgeTV":
                            new_url = self._golgetv_ver().rstrip("/")
                        else:
                            res = self.oturum.get(old_url, timeout=10, allow_redirects=True, verify=False)
                            new_url = res.url.rstrip("/")
                        
                        if old_url.rstrip("/") != new_url:
                            print(f"[+] {p}: {old_url} -> {new_url}")
                            self._replace_in_file(kt_path, old_url, new_url)
                            self._bump_version(p_info["path"])
                    except Exception as e:
                        print(f"[!] {p}: {old_url} bağlantısı başarısız! Hata: {e}")

    def _find_kt_file(self, plugin_dir, plugin_name):
        for root, dirs, files in os.walk(plugin_dir):
            if f"{plugin_name}.kt" in files:
                return os.path.join(root, f"{plugin_name}.kt")
        return None

    def _replace_in_file(self, path, old, new):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.replace(old, new))

    def _bump_version(self, plugin_dir):
        gradle_path = os.path.join(plugin_dir, "build.gradle.kts")
        if os.path.exists(gradle_path):
            with open(gradle_path, "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r'version\s*=\s*(\d+)', content)
            if match:
                new_ver = int(match.group(1)) + 1
                new_content = re.sub(r'version\s*=\s*\d+', f'version = {new_ver}', content)
                with open(gradle_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

    def status(self):
        print("\n--- MEVCUT REPO DURUMU (AKILLI KEŞİF) ---")
        plugins = self.get_all_plugins()
        cat_summary = {}
        for p in plugins:
            cat = p["category"]
            if cat not in cat_summary: cat_summary[cat] = []
            cat_summary[cat].append(p["name"])
        
        for cat, list_p in cat_summary.items():
            print(f"[{cat}]: {', '.join(list_p)}")

    def generate_repo_json(self, news_msg=None):
        print("[*] Akıllı repo.json oluşturuluyor...")
        plugins = self.get_all_plugins()
        categories = sorted(list(set(p["category"] for p in plugins)))
        
        cat_map = {
            "TR-Cinema": {"name": "Sinema & Dizi", "description": "Film ve dizi siteleri"},
            "TR-Anime": {"name": "Anime", "description": "Anime platformları"},
            "TR-TV": {"name": "Spor & Canlı TV", "description": "Canlı yayınlar"},
            "Global-Mixed": {"name": "Global & Karışık", "description": "Evrensel kaynaklar"},
            "Belgesel": {"name": "Belgesel", "description": "Belgesel kanalları"},
            "Exxen": {"name": "Exxen", "description": "Exxen orijinal içerikleri"},
            "Gain": {"name": "Gain", "description": "Gain orijinal içerikleri"},
            "Netflix": {"name": "Netflix", "description": "Netflix içerikleri"},
            "Disney": {"name": "Disney+", "description": "Disney+ içerikleri"},
            "NSFW": {"name": "Yetişkin", "description": "Yetişkin içerikler (+18)"}
        }

        cat_list = []
        for cat in categories:
            info = cat_map.get(cat, {"name": cat, "description": f"{cat} içeriği"})
            cat_list.append({
                "name": info["name"],
                "description": info["description"],
                "category": cat
            })

        # V3: Aile Duyuru Sistemi
        news = []
        if os.path.exists("news.json"):
            with open("news.json", "r", encoding="utf-8") as f:
                news = json.load(f)
        
        if news_msg:
            from datetime import datetime
            news.insert(0, {
                "title": "Ayhan'dan Mesaj",
                "description": news_msg,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            news = news[:5] # Son 5 mesajı tut
            with open("news.json", "w", encoding="utf-8") as f:
                json.dump(news, f, indent=4, ensure_ascii=False)

        # 1. Aile Dostu Repo (Safe)
        repo_data_safe = {
            "name": "Ayhan'ın Özel Deposu",
            "description": "Kişisel CloudStream eklenti koleksiyonu - Arkadaşlar için",
            "manifestVersion": 1,
            "pluginLists": [
                f"https://raw.githubusercontent.com/ayhankucuk/ayhn/builds/plugins.json"
            ],
            "categoryList": cat_list,
            "news": news
        }
        
        # 2. Yetişkin Repo (NSFW)
        repo_data_nsfw = {
            "name": "Ayhan NSFW Deposu (+18)",
            "description": "Yetişkin içerik koleksiyonu - Sadece davetliler için",
            "manifestVersion": 1,
            "pluginLists": [
                f"https://raw.githubusercontent.com/ayhankucuk/ayhn/builds/nsfw.json"
            ],
            "categoryList": [],
            "news": []
        }

        # Aile Reposu Kayıt
        with open("repo.json", "w", encoding="utf-8") as f:
            json.dump(repo_data_safe, f, indent=4, ensure_ascii=False)
            
        # NSFW Reposu Kayıt
        with open("nsfw_repo.json", "w", encoding="utf-8") as f:
            json.dump(repo_data_nsfw, f, indent=4, ensure_ascii=False)
            
        print(f"[+] repo.json (Aile) ve nsfw_repo.json (Gizli) başarıyla oluşturuldu.")

    def sync_github(self):
        """Tüm değişiklikleri GitHub'a otomatik pushlar."""
        print("[*] GitHub senkronizasyonu başlatılıyor...")
        import subprocess
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Otomatik güncelleme (ayhan_update)"], check=True)
            subprocess.run(["git", "push", "origin", "master"], check=True)
            print("[+] Değişiklikler GitHub'a başarıyla gönderildi!")
        except Exception as e:
            print(f"[!] Git hatası: {e}. Lütfen reponuzun doğru bağlandığından emin olun.")

if __name__ == "__main__":
    import sys
    manage = AyhanManage()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "update":
            manage.update_main_urls()
            manage.generate_repo_json()
        elif cmd == "status":
            manage.status()
        elif cmd == "build":
            manage.generate_repo_json()
        elif cmd == "news":
            msg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else input("Mesajınızı yazın: ")
            manage.generate_repo_json(news_msg=msg)
        elif cmd == "sync":
            manage.sync_github()
        elif cmd == "all":
            manage.update_main_urls()
            manage.generate_repo_json()
            manage.sync_github()
    else:
        print("\n--- AYHAN CLOUDSTREAM YÖNETİCİ ---")
        print("update : Linkleri güncelle ve repo.json yap")
        print("status : Eklenti durumlarını gör")
        print("news   : Aileye/arkadaşlara mesaj gönder")
        print("sync   : Değişiklikleri GitHub'a yolla")
        print("all    : Her şeyi yap (Güncelle + Build + Sync)")
