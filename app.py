import sys
import json
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QGroupBox,
    QComboBox, QMessageBox, QHeaderView, QRadioButton, QButtonGroup,
    QFrame, QDialog, QFormLayout, QDialogButtonBox, QSpinBox, QSplitter,
    QCheckBox
)
from PyQt5.QtCore import Qt
from styling import app_stylesheet, title_font, subtitle_font

# Algoritma Pencarian Sekuensial
def sequential_search(data, target):
    langkah = 0
    steps_log = []
    for idx, item in enumerate(data):
        langkah += 1
        steps_log.append(f"Langkah {langkah}: Memeriksa indeks {idx} (ID: {item['id']}, {item['nama']})")
        if item["id"] == target:
            steps_log.append(f"-> <b>Cocok!</b> Target ditemukan di indeks {idx}.")
            return item, langkah, steps_log
        else:
            steps_log.append("-> Tidak cocok.")
    steps_log.append(f"-> Target {target} tidak ditemukan di seluruh data.")
    return None, langkah, steps_log

# Algoritma Pencarian Biner
def binary_search(data, target):
    kiri, kanan = 0, len(data) - 1
    langkah = 0
    steps_log = []
    while kiri <= kanan:
        langkah += 1
        tengah = (kiri + kanan) // 2
        item = data[tengah]
        steps_log.append(f"Langkah {langkah}: Rentang [{kiri} s/d {kanan}], Tengah = {tengah} (ID: {item['id']}, {item['nama']})")
        if item["id"] == target:
            steps_log.append(f"-> <b>Cocok!</b> Target ditemukan di indeks tengah {tengah}.")
            return item, langkah, steps_log
        elif item["id"] < target:
            steps_log.append(f"-> ID saat ini ({item['id']}) &lt; target ({target}). Cari bagian kanan.")
            kiri = tengah + 1
        else:
            steps_log.append(f"-> ID saat ini ({item['id']}) &gt; target ({target}). Cari bagian kiri.")
            kanan = tengah - 1
    steps_log.append(f"-> Target {target} tidak ditemukan dalam pencarian biner.")
    return None, langkah, steps_log

# Dialog CRUD untuk Tambah/Ubah/Hapus Data
class CRUDDialog(QDialog):
    def __init__(self, parent=None, item_data=None, next_id=None):
        super().__init__(parent)
        self.item_data = item_data
        self.next_id = next_id
        self.setWindowTitle("Tambah Barang Baru" if not item_data else "Ubah Data Barang")
        self.setMinimumWidth(360)
        self.setStyleSheet(app_stylesheet())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        form = QFormLayout()
        form.setSpacing(10)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Contoh: 1051")
        if self.item_data:
            self.input_id.setText(str(self.item_data["id"]))
            self.input_id.setEnabled(False)
        else:
            # Untuk item baru: toggle auto-generate ID
            self.chk_auto_id = QCheckBox("Isi ID otomatis")
            self.chk_auto_id.setChecked(True)
            # Isi next_id jika tersedia
            if self.next_id is not None:
                self.input_id.setText(str(self.next_id))
                self.input_id.setEnabled(False)
            else:
                self.input_id.setEnabled(True)
            self.chk_auto_id.stateChanged.connect(self.on_auto_id_toggled)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Contoh: Beras Segitiga 5kg")
        if self.item_data:
            self.input_nama.setText(self.item_data["nama"])

        self.input_kategori = QComboBox()
        self.input_kategori.setEditable(True)
        self.input_kategori.addItems([
            "Sembako", "Mie & Makanan Instan", "Bumbu & Penyedap",
            "Minuman Kemasan", "Susu & Olahan", "Perawatan Pribadi",
            "Kebutuhan Rumah", "Camilan & Biskuit", "Kopi & Teh"
        ])
        if self.item_data:
            self.input_kategori.setCurrentText(self.item_data.get("kategori", ""))

        self.input_stok = QSpinBox()
        self.input_stok.setRange(0, 100000)
        self.input_stok.setValue(10)
        if self.item_data:
            self.input_stok.setValue(int(self.item_data.get("stok", 0)))

        form.addRow("ID Barang:", self.input_id)
        form.addRow("Nama Barang:", self.input_nama)
        form.addRow("Kategori:", self.input_kategori)
        form.addRow("Stok:", self.input_stok)
        layout.addLayout(form)

        self.btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.btn_box.accepted.connect(self.validate_and_accept)
        self.btn_box.rejected.connect(self.reject)
        layout.addWidget(self.btn_box)

    def validate_and_accept(self):
        id_str = self.input_id.text().strip()
        nama = self.input_nama.text().strip()
        kategori = self.input_kategori.currentText().strip()
        stok = self.input_stok.value()

        if not id_str:
            QMessageBox.warning(self, "Input Kosong", "ID Barang tidak boleh kosong.")
            self.input_id.setFocus()
            return
        try:
            item_id = int(id_str)
        except ValueError:
            QMessageBox.warning(self, "Format Salah", "ID Barang harus berupa angka integer.")
            self.input_id.setFocus()
            return
        if not nama:
            QMessageBox.warning(self, "Input Kosong", "Nama Barang tidak boleh kosong.")
            self.input_nama.setFocus()
            return

        self.result_data = {"id": item_id, "nama": nama, "kategori": kategori, "stok": stok}
        self.accept()

    def on_auto_id_toggled(self, state):
        # Ketika auto dicentang, kunci dan isi field ID dengan next_id (jika tersedia)
        checked = (state == Qt.Checked)
        if checked and self.next_id is not None:
            self.input_id.setText(str(self.next_id))
            self.input_id.setEnabled(False)
        else:
            self.input_id.setEnabled(True)
            # jika dimatikan, kosongkan untuk prompt input manual
            if not checked:
                self.input_id.clear()

    def get_data(self):
        return getattr(self, "result_data", None)


# Dialog Detail Barang (Pop-up otomatis)
class ProductDetailDialog(QDialog):
    """Pop-up yang menampilkan detail barang hasil pencarian."""
    def __init__(self, parent=None, item_data=None, algoritma=""):
        super().__init__(parent)
        self.setWindowTitle("Detail Barang Ditemukan")
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build_ui(item_data, algoritma)

    def _build_ui(self, item, algo):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header banner
        header = QFrame()
        header.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            "stop:0 #0b5ed7, stop:1 #38bdf8);"
        )
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(20, 16, 20, 12)
        h_layout.setSpacing(4)

        title_lbl = QLabel("Barang Ditemukan")
        title_lbl.setStyleSheet(
            "color: #ffffff; font-size: 16px; font-weight: 700;"
            "background: transparent;"
        )
        title_lbl.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(title_lbl)

        algo_lbl = QLabel(f"Algoritma: {algo}")
        algo_lbl.setStyleSheet(
            "color: #dbeafe; font-size: 11px; font-weight: 500;"
            "background: transparent;"
        )
        algo_lbl.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(algo_lbl)

        layout.addWidget(header)

        # Body tabel data
        body = QFrame()
        body.setStyleSheet("background-color: #ffffff;")
        b_layout = QVBoxLayout(body)
        b_layout.setContentsMargins(16, 14, 16, 14)
        b_layout.setSpacing(12)

        # Tabel data
        ROW_HEIGHT    = 34   # px per baris data
        HEADER_HEIGHT = 36   # px header kolom

        rows_data = [
            ("ID Barang", str(item.get("id", "-"))),
            ("Nama Barang", item.get("nama", "-")),
            ("Kategori", item.get("kategori", "-")),
            ("Stok", str(item.get("stok", 0))),
        ]
        num_rows = len(rows_data)

        tbl = QTableWidget(num_rows, 2)
        tbl.setHorizontalHeaderLabels(["Field", "Nilai"])
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        tbl.horizontalHeader().setFixedHeight(HEADER_HEIGHT)
        tbl.verticalHeader().setVisible(False)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setSelectionMode(QTableWidget.NoSelection)
        tbl.setFocusPolicy(Qt.NoFocus)
        tbl.setAlternatingRowColors(True)
        tbl.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tbl.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for r, (field, val) in enumerate(rows_data):
            tbl.setRowHeight(r, ROW_HEIGHT)
            f_item = QTableWidgetItem(field)
            f_item.setFlags(f_item.flags() & ~Qt.ItemIsEditable)
            v_item = QTableWidgetItem(val)
            v_item.setFlags(v_item.flags() & ~Qt.ItemIsEditable)
            tbl.setItem(r, 0, f_item)
            tbl.setItem(r, 1, v_item)

        # Hitung tinggi pas: header + semua baris + 2px border
        exact_height = HEADER_HEIGHT + (ROW_HEIGHT * num_rows) + 2
        tbl.setFixedHeight(exact_height)

        b_layout.addWidget(tbl)

        # Stok status badge
        stok_val = int(item.get("stok", 0))
        if stok_val >= 30:
            stok_color, stok_bg, stok_label = "#16a34a", "#dcfce7", "Stok Aman"
        elif stok_val >= 10:
            stok_color, stok_bg, stok_label = "#ea580c", "#fff7ed", "Stok Menipis"
        else:
            stok_color, stok_bg, stok_label = "#dc2626", "#fef2f2", "Stok Kritis"

        badge = QLabel(f"{stok_label}  —  {stok_val} unit")
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"background-color: {stok_bg}; color: {stok_color};"
            f"border: 1px solid {stok_color}; border-radius: 10px;"
            "padding: 5px 14px; font-size: 12px; font-weight: 700;"
        )
        b_layout.addWidget(badge, alignment=Qt.AlignCenter)

        # Close button
        btn_close = QPushButton("Tutup")
        btn_close.setStyleSheet(
            "background-color: #0b5ed7; color: white; border-radius: 6px;"
            "padding: 8px 22px; font-weight: 600; font-size: 13px;"
        )
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        b_layout.addWidget(btn_close, alignment=Qt.AlignCenter)

        layout.addWidget(body)
        # Dialog menyesuaikan ukuran sendiri berdasarkan konten
        self.setMinimumWidth(460)
        self.adjustSize()


# Aplikasi GUI Utama
class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("SearchApp")
        self.setWindowTitle("Sistem Inventaris Gudang")
        self.setMinimumSize(1100, 680)
        self.setStyleSheet(app_stylesheet())

        # Holds the last search results for chart generation
        self._last_seq_result = None
        self._last_bin_result = None

        self.load_data()
        self.init_ui()

    def load_data(self):
        try:
            with open("gudang.json", "r", encoding="utf-8") as f:
                self.data_original = json.load(f)
            self.data = list(self.data_original)
            self.data.sort(key=lambda x: int(x["id"]))
        except Exception as e:
            QMessageBox.critical(self, "Gagal Muat File", f"Gagal membaca gudang.json:\n{e}")
            self.data_original = []
            self.data = []

    def save_data_to_json(self):
        try:
            with open("gudang.json", "w", encoding="utf-8") as f:
                json.dump(self.data_original, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Gagal Simpan", f"Gagal menyimpan ke gudang.json:\n{e}")
            return False

    def init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar kiri
        sidebar = QFrame()
        sidebar.setObjectName("sidebar_frame")
        sidebar.setFixedWidth(220)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(15, 20, 15, 20)
        sb.setSpacing(8)

        logo = QLabel("📦 SMART GUDANG")
        logo.setObjectName("sidebar_title")
        logo.setAlignment(Qt.AlignCenter)
        sb.addWidget(logo)

        desc = QLabel("Sistem Inventaris Gudang")
        desc.setStyleSheet("color:#94a3b8; font-size:11px; margin-bottom:8px;")
        desc.setAlignment(Qt.AlignCenter)
        sb.addWidget(desc)

        self.btn_side_load = QPushButton("🔄 Reset Data")
        self.btn_side_load.setObjectName("sidebar_btn")
        self.btn_side_load.clicked.connect(self.action_reset_data)
        sb.addWidget(self.btn_side_load)

        self.btn_side_step = QPushButton("🎮 Step by Step Mode")
        self.btn_side_step.setObjectName("sidebar_btn")
        self.btn_side_step.clicked.connect(self.action_toggle_step_mode)
        sb.addWidget(self.btn_side_step)

        sb.addSpacing(20)

        # Kontrol pengurutan di sidebar
        lbl_sort_hdr = QLabel("Pengurutan Data")
        lbl_sort_hdr.setStyleSheet("font-weight:700; color:#0b5ed7; font-size:12px;")
        sb.addWidget(lbl_sort_hdr)

        lbl_sortby = QLabel("Urutkan Berdasarkan:")
        lbl_sortby.setStyleSheet("color:#475569; font-size:11px;")
        sb.addWidget(lbl_sortby)
        self.cb_sort_by = QComboBox()
        self.cb_sort_by.addItems(["ID Barang", "Nama Barang"])
        sb.addWidget(self.cb_sort_by)

        lbl_order = QLabel("Metode Urutan:")
        lbl_order.setStyleSheet("color:#475569; font-size:11px;")
        sb.addWidget(lbl_order)
        self.cb_sort_order = QComboBox()
        self.cb_sort_order.addItems(["Ascending", "Descending"])
        sb.addWidget(self.cb_sort_order)

        btn_apply_sort = QPushButton("✅ Terapkan Urutan")
        btn_apply_sort.clicked.connect(self.apply_sorting)
        sb.addWidget(btn_apply_sort)

        sb.addStretch()

        root.addWidget(sidebar)

        # Konten utama
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(14)

        # Header
        hdr = QLabel("Dashboard Perbandingan Kecepatan Algoritma Pencarian")
        hdr.setObjectName("header_title")
        cl.addWidget(hdr)

        # Status Label
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #16a34a; font-weight: 500; font-size: 12px; margin-top: -5px; margin-bottom: 5px;")
        cl.addWidget(self.lbl_status)

        # Stats Row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        self.card_cats, self.lbl_stats_cats = self._make_stat_card(stats_row, "—", "Kategori Produk")
        self.card_items, self.lbl_stats_items = self._make_stat_card(stats_row, "—", "Jumlah Produk")
        self.card_stock, self.lbl_stats_stock = self._make_stat_card(stats_row, "—", "Total Unit Stok")
        cl.addLayout(stats_row)

        # Body split: table (left) + search panel (right) — using QSplitter for resizable panels
        body_splitter = QSplitter(Qt.Horizontal)
        body_splitter.setHandleWidth(5)
        body_splitter.setChildrenCollapsible(False)

        # Tabel Inventaris
        tbl_card = QGroupBox("Daftar Inventaris Gudang")
        tbl_v = QVBoxLayout(tbl_card)
        tbl_v.setContentsMargins(8, 6, 8, 8)
        tbl_v.setSpacing(6)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nama Barang", "Kategori", "Stok"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setColumnWidth(2, 160)   # initial Kategori width
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        # Matikan pengeditan ID Barang
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemClicked.connect(self.on_table_row_selected)
        tbl_v.addWidget(self.table)

        # Tombol CRUD di bawah tabel
        crud_row = QHBoxLayout()
        crud_row.setSpacing(8)
        btn_add = QPushButton("➕ Tambah")
        btn_add.clicked.connect(self.action_crud_add)
        btn_edit = QPushButton("✏ Ubah")
        btn_edit.setObjectName("btn_secondary")
        btn_edit.clicked.connect(self.action_crud_edit)
        btn_del = QPushButton("🗑 Hapus")
        btn_del.setStyleSheet("background-color:#ef4444; color:white; border-radius:6px; padding:7px 12px;")
        btn_del.clicked.connect(self.action_crud_delete)
        crud_row.addWidget(btn_add)
        crud_row.addWidget(btn_edit)
        crud_row.addWidget(btn_del)
        crud_row.addStretch()
        tbl_v.addLayout(crud_row)

        body_splitter.addWidget(tbl_card)

        # Panel Pencarian dan Analisis
        search_card = QGroupBox("Pencarian & Analisis Performa")
        search_card.setMinimumWidth(280)
        search_card.setMaximumWidth(520)
        sv = QVBoxLayout(search_card)
        sv.setSpacing(4)
        sv.setContentsMargins(10, 8, 10, 10)

        lbl_id = QLabel("Masukkan ID Barang:")
        sv.addWidget(lbl_id)
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Contoh: 1025")
        self.input_id.returnPressed.connect(self.on_search)
        sv.addWidget(self.input_id)

        sv.addSpacing(6)
        lbl_metode = QLabel("Metode Pencarian:")
        sv.addWidget(lbl_metode)
        self.radio_both = QRadioButton("Kedua Algoritma")
        self.radio_seq  = QRadioButton("Sequential Search")
        self.radio_bin  = QRadioButton("Binary Search")
        self.radio_both.setChecked(True)
        self._rg = QButtonGroup()
        for r in (self.radio_both, self.radio_seq, self.radio_bin):
            self._rg.addButton(r)
            sv.addWidget(r)

        sv.addSpacing(6)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_search = QPushButton("⚡ Cari")
        self.btn_search.clicked.connect(self.on_search)
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setObjectName("btn_secondary")
        self.btn_refresh.clicked.connect(lambda: (self.refresh_table(), self.result_table.setRowCount(0), self.trace_area.clear(), self.trace_area.setVisible(False)))
        btn_row.addWidget(self.btn_search)
        btn_row.addWidget(self.btn_refresh)
        sv.addLayout(btn_row)

        sv.addSpacing(6)
        sv.addWidget(QLabel("Hasil Perbandingan Metrik:"))
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Algoritma", "Waktu Eksekusi", "Perbandingan", "Detail Hasil"])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setRowCount(0)
        self.result_table.setMinimumHeight(90)
        self.result_table.setMaximumHeight(160)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        sv.addWidget(self.result_table)

        self.trace_area = QTextEdit()
        self.trace_area.setReadOnly(True)
        self.trace_area.setPlaceholderText("Trace langkah pencarian akan muncul di sini...")
        self.trace_area.setVisible(False)
        sv.addWidget(self.trace_area)

        sv.addStretch(1)

        # Tombol "Tampilkan Grafik" — disembunyikan hingga pencarian selesai
        self.btn_show_chart = QPushButton("📊 Tampilkan Grafik Perbandingan")
        self.btn_show_chart.setVisible(False)
        self.btn_show_chart.clicked.connect(self.show_chart)
        sv.addWidget(self.btn_show_chart)

        body_splitter.addWidget(search_card)

        # Atur rasio ukuran awal 65% tabel : 35% pencarian
        body_splitter.setSizes([650, 350])

        cl.addWidget(body_splitter, stretch=1)

        root.addWidget(content)

        # Flag untuk mode step-by-step
        self.step_mode_enabled = False

        # Inisialisasi tabel dan statistik
        self.refresh_table()
        self.update_inventory_stats()

    # Builder stat card
    def _make_stat_card(self, parent_layout, value, label_text, warn=False):
        card = QFrame()
        card.setObjectName("stats_card")
        v = QVBoxLayout(card)
        lbl_val = QLabel(value)
        lbl_val.setObjectName("stats_value")
        if warn:
            lbl_val.setStyleSheet("color:#ea580c; font-size:20px; font-weight:bold;")
        lbl_lbl = QLabel(label_text)
        lbl_lbl.setObjectName("stats_label")
        v.addWidget(lbl_val)
        v.addWidget(lbl_lbl)
        parent_layout.addWidget(card)
        return card, lbl_val

    # Update statistik inventaris
    def update_inventory_stats(self):
        if not self.data:
            for lbl in (self.lbl_stats_cats, self.lbl_stats_items,
                        self.lbl_stats_stock):
                lbl.setText("0")
            return
        cats = set()
        total_stok = 0
        for item in self.data:
            cats.add(item.get("kategori", ""))
            s = int(item.get("stok", 0))
            total_stok += s
        self.lbl_stats_cats.setText(f"{len(cats)}")
        self.lbl_stats_items.setText(f"{len(self.data)}")
        self.lbl_stats_stock.setText(f"{total_stok:,}")

    def refresh_table(self):
        self.table.setRowCount(len(self.data))
        for r, item in enumerate(self.data):
            id_item = QTableWidgetItem(str(item["id"]))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(r, 0, id_item)
            self.table.setItem(r, 1, QTableWidgetItem(item["nama"]))
            self.table.setItem(r, 2, QTableWidgetItem(item.get("kategori", "")))
            self.table.setItem(r, 3, QTableWidgetItem(str(item.get("stok", 0))))

    def apply_sorting(self):
        sort_by = self.cb_sort_by.currentText()
        order   = self.cb_sort_order.currentText()
        rev = (order == "Descending")
        if sort_by == "ID Barang":
            self.data.sort(key=lambda x: int(x["id"]), reverse=rev)
        else:
            self.data.sort(key=lambda x: str(x["nama"]).lower(), reverse=rev)
        self.refresh_table()
        self.lbl_status.setText(f"✓ Data diurutkan berdasarkan {sort_by} ({order}).")
        self.lbl_status.setStyleSheet("color: #16a34a; font-weight: 500; font-size: 12px; margin-top: -5px; margin-bottom: 5px;")

    def on_table_row_selected(self, item):
        row = item.row()
        cell = self.table.item(row, 0)
        if cell:
            self.input_id.setText(cell.text())

    # Aksi Sidebar
    def action_reset_data(self):
        self.load_data()
        self.apply_sorting()
        self.update_inventory_stats()
        self.lbl_status.setText("✓ Data gudang berhasil dimuat ulang dari gudang.json.")
        self.lbl_status.setStyleSheet("color: #16a34a; font-weight: 500; font-size: 12px; margin-top: -5px; margin-bottom: 5px;")

    def action_toggle_step_mode(self):
        self.step_mode_enabled = not self.step_mode_enabled
        status = "AKTIF" if self.step_mode_enabled else "NONAKTIF"
        self.lbl_status.setText(f"🎮 Mode Step by Step: {status}")
        self.lbl_status.setStyleSheet("color: #0b5ed7; font-weight: 500; font-size: 12px; margin-top: -5px; margin-bottom: 5px;")

    # CRUD Operations
    def action_crud_add(self):
        # compute next available numeric ID
        try:
            existing_ids = [int(x["id"]) for x in self.data_original if str(x.get("id","")).strip() != ""]
            next_id = max(existing_ids) + 1 if existing_ids else 1000
        except Exception:
            next_id = 1000
        dlg = CRUDDialog(self, next_id=next_id)
        if dlg.exec_():
            new = dlg.get_data()
            if new:
                if any(x["id"] == new["id"] for x in self.data_original):
                    QMessageBox.warning(self, "ID Duplikat",
                                        f"Barang dengan ID {new['id']} sudah ada!")
                    return
                self.data_original.append(new)
                self.data_original.sort(key=lambda x: int(x["id"]))
                self.data = list(self.data_original)
                self.apply_sorting()
                self.update_inventory_stats()
                if self.save_data_to_json():
                    QMessageBox.information(self, "Sukses", "Barang baru berhasil ditambahkan!")

    def action_crud_edit(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Baris", "Pilih barang di tabel terlebih dahulu.")
            return
        cell_text = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
        try:
            item_id = int(cell_text)
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Format Salah", f"ID pada baris yang dipilih tidak valid: {cell_text}\nHarap perbaiki menjadi angka sebelum mengubah.")
            return
        orig = next((x for x in self.data_original if x["id"] == item_id), None)
        if not orig:
            return
        dlg = CRUDDialog(self, item_data=orig)
        if dlg.exec_():
            upd = dlg.get_data()
            if upd:
                orig["nama"] = upd["nama"]
                orig["kategori"] = upd["kategori"]
                orig["stok"] = upd["stok"]
                self.data = list(self.data_original)
                self.apply_sorting()
                self.update_inventory_stats()
                if self.save_data_to_json():
                    QMessageBox.information(self, "Sukses", "Data barang berhasil diubah!")

    def action_crud_delete(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Baris", "Pilih barang di tabel terlebih dahulu.")
            return
        cell_text = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
        try:
            item_id = int(cell_text)
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Format Salah", f"ID pada baris yang dipilih tidak valid: {cell_text}\nHarap perbaiki menjadi angka sebelum menghapus.")
            return
        item_name = self.table.item(row, 1).text()
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Hapus barang '{item_name}' (ID: {item_id})?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.data_original = [x for x in self.data_original if x["id"] != item_id]
            self.data = list(self.data_original)
            self.apply_sorting()
            self.update_inventory_stats()
            if self.save_data_to_json():
                QMessageBox.information(self, "Sukses", "Barang berhasil dihapus!")

    # Fitur Pencarian
    def on_search(self):
        text = self.input_id.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Kosong", "Masukkan ID barang terlebih dahulu.")
            self.input_id.setFocus()
            return
        try:
            target = int(text)
        except ValueError:
            QMessageBox.warning(self, "Format Salah", "ID harus berupa angka.")
            self.input_id.setFocus()
            return

        # Pilihan algoritma
        pilihan = "Kedua Algoritma"
        if self.radio_seq.isChecked():
            pilihan = "Sequential Search"
        elif self.radio_bin.isChecked():
            pilihan = "Binary Search"

        # Bersihkan hasil yang disimpan
        self._last_seq_result = None
        self._last_bin_result = None

        found_item = None
        self.result_table.setRowCount(0)
        self.trace_area.clear()

        row_idx = 0

        # Fungsi helper untuk menyisipkan item read-only
        def add_result_item(row, col, text, is_red=False):
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            if is_red:
                item.setForeground(Qt.red)
            self.result_table.setItem(row, col, item)

        if pilihan in ("Kedua Algoritma", "Sequential Search"):
            t0 = time.perf_counter()
            res, steps, logs = sequential_search(self.data, target)
            dur = time.perf_counter() - t0
            self._last_seq_result = {"waktu": dur, "langkah": steps, "ditemukan": res is not None}
            
            self.result_table.insertRow(row_idx)
            add_result_item(row_idx, 0, "Sequential Search")
            add_result_item(row_idx, 1, f"{dur*1_000_000:.2f} µs ({dur:.6f} s)")
            add_result_item(row_idx, 2, f"{steps} kali")
            
            if res:
                add_result_item(row_idx, 3, f"{res['nama']} (ID: {res['id']})")
                found_item = res
            else:
                add_result_item(row_idx, 3, "Tidak ditemukan di dalam database", is_red=True)
                
            if self.step_mode_enabled:
                self.trace_area.append(f"<b>🎮 Trace (Sequential Search):</b><br>" + "<br>".join(logs) + "<br>")
            row_idx += 1

        if pilihan in ("Kedua Algoritma", "Binary Search"):
        # Binary Search memerlukan data terurut berdasarkan ID ascending.
            # Kami mengurutkan salinan data agar pencarian selalu sukses tanpa merusak urutan visual tabel.
            data_sorted = sorted(self.data, key=lambda x: int(x["id"]))
            t0 = time.perf_counter()
            res, steps, logs = binary_search(data_sorted, target)
            dur = time.perf_counter() - t0
            self._last_bin_result = {"waktu": dur, "langkah": steps, "ditemukan": res is not None}
            
            self.result_table.insertRow(row_idx)
            add_result_item(row_idx, 0, "Binary Search")
            add_result_item(row_idx, 1, f"{dur*1_000_000:.2f} µs ({dur:.6f} s)")
            add_result_item(row_idx, 2, f"{steps} kali")
            
            if res:
                add_result_item(row_idx, 3, f"{res['nama']} (ID: {res['id']})")
                found_item = res
            else:
                add_result_item(row_idx, 3, "Tidak ditemukan di dalam database", is_red=True)
                
            if self.step_mode_enabled:
                self.trace_area.append(f"<b>🎮 Trace (Binary Search):</b><br>" + "<br>".join(logs) + "<br>")
            row_idx += 1

        self.trace_area.setVisible(self.step_mode_enabled)

        if found_item:
            self._highlight_table_row(found_item["id"])

        # Tampilkan tombol grafik hanya ketika ada setidaknya satu hasil
        has_results = (self._last_seq_result is not None or self._last_bin_result is not None)
        self.btn_show_chart.setVisible(has_results)

        # Pop-up otomatis: tampilkan detail barang jika ditemukan
        if found_item:
            dlg = ProductDetailDialog(self, item_data=found_item, algoritma=pilihan)
            dlg.exec_()


    def _highlight_table_row(self, item_id):
        for r in range(self.table.rowCount()):
            cell = self.table.item(r, 0)
            if cell and cell.text() == str(item_id):
                self.table.selectRow(r)
                self.table.scrollToItem(cell)
                break

    # Tampilkan Grafik Perbandingan
    def show_chart(self):
        try:
            import matplotlib
            matplotlib.use("Qt5Agg")
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
        except ImportError:
            QMessageBox.warning(
                self, "Matplotlib Tidak Tersedia",
                "Library matplotlib diperlukan untuk menampilkan grafik.\n"
                "Instal dengan: pip install matplotlib"
            )
            return

        seq = self._last_seq_result
        bin_ = self._last_bin_result

        labels = []
        seq_langkah = seq_waktu_us = bin_langkah = bin_waktu_us = None

        if seq:
            seq_langkah = seq["langkah"]
            seq_waktu_us = seq["waktu"] * 1_000_000

        if bin_:
            bin_langkah = bin_["langkah"]
            bin_waktu_us = bin_["waktu"] * 1_000_000

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle("Perbandingan Algoritma Pencarian", fontsize=14, fontweight="bold", color="#1e293b")
        fig.patch.set_facecolor("#f4f5f7")

        PINK  = "#fb7185"
        BLUE  = "#60a5fa"
        GRAY  = "#e2e8f0"

        # --- Jumlah Perbandingan (iterasi) ---
        ax1 = axes[0]
        ax1.set_facecolor("#ffffff")
        ax1.set_title("Jumlah Perbandingan (Iterasi)", fontsize=11, color="#334155", pad=10)

        bar_vals_l = []
        bar_colors_l = []
        bar_labels_l = []
        if seq:
            bar_vals_l.append(seq_langkah)
            bar_colors_l.append(PINK)
            bar_labels_l.append("Sequential")
        if bin_:
            bar_vals_l.append(bin_langkah)
            bar_colors_l.append(BLUE)
            bar_labels_l.append("Binary")

        bars1 = ax1.bar(bar_labels_l, bar_vals_l, color=bar_colors_l,
                        width=0.4, edgecolor="white", linewidth=1.5)
        for bar, val in zip(bars1, bar_vals_l):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                     f"{val}", ha="center", va="bottom", fontsize=11,
                     fontweight="bold", color="#1e293b")
        ax1.set_ylabel("Jumlah Perbandingan", color="#475569", fontsize=9)
        ax1.set_ylim(0, max(bar_vals_l) * 1.35 if bar_vals_l else 5)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.tick_params(colors="#475569")

        # --- Waktu Eksekusi ---
        ax2 = axes[1]
        ax2.set_facecolor("#ffffff")
        ax2.set_title("Waktu Eksekusi (µs)", fontsize=11, color="#334155", pad=10)

        bar_vals_t = []
        bar_colors_t = []
        bar_labels_t = []
        if seq:
            bar_vals_t.append(seq_waktu_us)
            bar_colors_t.append(PINK)
            bar_labels_t.append("Sequential")
        if bin_:
            bar_vals_t.append(bin_waktu_us)
            bar_colors_t.append(BLUE)
            bar_labels_t.append("Binary")

        bars2 = ax2.bar(bar_labels_t, bar_vals_t, color=bar_colors_t,
                        width=0.4, edgecolor="white", linewidth=1.5)
        for bar, val in zip(bars2, bar_vals_t):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(bar_vals_t) * 0.01,
                     f"{val:.2f}", ha="center", va="bottom", fontsize=10,
                     fontweight="bold", color="#1e293b")
        ax2.set_ylabel("Waktu (µs)", color="#475569", fontsize=9)
        ax2.set_ylim(0, max(bar_vals_t) * 1.35 if bar_vals_t else 5)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.tick_params(colors="#475569")

        # Legenda
        patches = []
        if seq:
            patches.append(mpatches.Patch(color=PINK, label="Sequential Search"))
        if bin_:
            patches.append(mpatches.Patch(color=BLUE, label="Binary Search"))
        if patches:
            fig.legend(handles=patches, loc="lower center", ncol=2, frameon=False,
                       fontsize=10, labelcolor="#334155")

        plt.tight_layout(rect=[0, 0.06, 1, 1])
        plt.show()

    # Format hasil pencarian
    def _format_hasil(self, nama_alg, waktu, langkah, hasil):
        if nama_alg.startswith("Sequential"):
            bg, border, tc = "#fdf2f8", "#fbcfe8", "#db2777"
        else:
            bg, border, tc = "#f0f9ff", "#bae6fd", "#0284c7"
        text_c = "#334155"

        if hasil:
            body = (
                f"Waktu eksekusi: <b style='color:#0f172a;'>{waktu:.6f}</b> detik "
                f"({waktu*1_000_000:.2f} µs)<br>"
                f"Jumlah perbandingan: <b style='color:#0f172a;'>{langkah}</b> kali<br>"
                f"Hasil: <b style='color:#0f172a;'>{hasil['nama']}</b> — "
                f"ID: {hasil['id']} — Kategori: {hasil.get('kategori','')} — "
                f"Stok: {hasil.get('stok',0)}"
            )
        else:
            body = (
                f"Waktu eksekusi: <b style='color:#0f172a;'>{waktu:.6f}</b> detik<br>"
                f"Jumlah perbandingan: <b style='color:#0f172a;'>{langkah}</b> kali<br>"
                f"Hasil: <b style='color:#ef4444;'>Tidak ditemukan di dalam database</b>"
            )

        return (
            f"<div style='background-color:{bg}; border:1.5px solid {border}; "
            f"padding:12px; border-radius:8px; color:{text_c}; "
            f"font-family:\"Poppins\",\"Arial\",sans-serif; font-size:13px;'>"
            f"<b style='color:{tc}; font-size:14px;'>{nama_alg}</b><br>{body}</div>"
        )

    def _format_step_logs(self, nama_alg, logs):
        log_text = "<br>".join(logs)
        return (
            f"<div style='background:#fafafa; border:1px dashed #cbd5e1; "
            f"padding:10px; border-radius:6px; font-family:Consolas,monospace; "
            f"font-size:11px; color:#475569;'>"
            f"<b style='color:#0f172a;'>🎮 Trace ({nama_alg}):</b><br>{log_text}</div>"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())
