import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFileDialog, QProgressBar
from PyQt5.QtGui import QIcon
from instaloader import Instaloader, Post

class InstagramDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Pencere başlığı ve boyutu
        self.setWindowTitle("Instagram İndirici")
        self.setGeometry(100, 100, 400, 250)

        # Pencere ikonu
        self.setWindowIcon(QIcon("instagram_icon.png"))  # İkon dosyasını proje dizinine ekleyin

        # Layout oluştur
        layout = QVBoxLayout()

        # Label (Başlık)
        self.label = QLabel("Instagram Linki:")
        layout.addWidget(self.label)

        # Entry (Giriş Kutusu)
        self.entry = QLineEdit()
        layout.addWidget(self.entry)

        # Klasör Seç Butonu
        self.folder_button = QPushButton("Klasör Seç")
        self.folder_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.folder_button)

        # Seçilen Klasörü Gösteren Label
        self.folder_label = QLabel("Seçilen Klasör: Yok")
        layout.addWidget(self.folder_label)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)  # Başlangıç değeri 0
        layout.addWidget(self.progress_bar)

        # Button (İndir Butonu)
        self.button = QPushButton("İndir")
        self.button.clicked.connect(self.download_instagram_content)
        layout.addWidget(self.button)

        # Layout'u pencereye ekle
        self.setLayout(layout)

        # Seçilen klasörü saklamak için değişken
        self.download_folder = None

    def choose_directory(self):
        # Klasör seçme dialog'u aç
        folder = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if folder:
            self.download_folder = folder
            self.folder_label.setText(f"Seçilen Klasör: {folder}")

    def download_instagram_content(self):
        url = self.entry.text()
        if not url:
            QMessageBox.critical(self, "Hata", "Lütfen bir Instagram linki girin!")
            return

        if not self.download_folder:
            QMessageBox.critical(self, "Hata", "Lütfen bir klasör seçin!")
            return

        try:
            # Instaloader çıktısını engelle
            logging.basicConfig(level=logging.CRITICAL)  # Sadece kritik hataları göster
            L = Instaloader()

            shortcode = url.split("/")[-2]
            post = Post.from_shortcode(L.context, shortcode)

            # Progress bar'ı güncelle (%25)
            self.progress_bar.setValue(25)
            QApplication.processEvents()  # GUI'yi güncelle

            # İndirme işlemi için mutlak yol oluştur
            target_folder = os.path.join(self.download_folder, f"{post.owner_username}_{post.shortcode}")

            # İndirme işlemi
            L.download_post(post, target=target_folder)

            # Progress bar'ı güncelle (%100)
            self.progress_bar.setValue(100)
            QApplication.processEvents()  # GUI'yi güncelle

            # İndirilen dosyaları kontrol et
            if os.path.exists(target_folder) and os.listdir(target_folder):
                QMessageBox.information(self, "Başarılı", f"İndirme başarılı! Dosya şuraya kaydedildi: {target_folder}")
            else:
                QMessageBox.critical(self, "Hata", "İndirme başarısız! Dosyalar kaydedilmedi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")
        finally:
            self.progress_bar.setValue(0)  # Progress bar'ı sıfırla

# Uygulamayı başlat
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstagramDownloader()
    window.show()
    sys.exit(app.exec_())