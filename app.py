"""
StockStory - Inventory Dashboard
Flask Application with dummy data for all screens.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)
app.secret_key = 'stockstory-secret-key-2026'

# ───────────────────────────────────────────
# DUMMY DATA
# ───────────────────────────────────────────

CATEGORIES = ['Elektronik', 'Makanan', 'Minuman', 'Pakaian', 'Alat Tulis', 'Peralatan', 'Lainnya']

BARANG_LIST = [
    {'id': 1, 'kode': 'BRG-001', 'nama': 'Laptop ASUS VivoBook', 'kategori': 'Elektronik', 'stok': 25, 'satuan': 'Unit', 'harga': 8500000, 'lokasi': 'Gudang A', 'stok_min': 5, 'gambar': '', 'deskripsi': 'Laptop ASUS VivoBook 14 inch, RAM 8GB, SSD 512GB'},
    {'id': 2, 'kode': 'BRG-002', 'nama': 'Mouse Wireless Logitech', 'kategori': 'Elektronik', 'stok': 150, 'satuan': 'Unit', 'harga': 250000, 'lokasi': 'Gudang A', 'stok_min': 20, 'gambar': '', 'deskripsi': 'Mouse wireless Logitech M331 Silent'},
    {'id': 3, 'kode': 'BRG-003', 'nama': 'Kertas HVS A4 80gsm', 'kategori': 'Alat Tulis', 'stok': 500, 'satuan': 'Rim', 'harga': 55000, 'lokasi': 'Gudang B', 'stok_min': 50, 'gambar': '', 'deskripsi': 'Kertas HVS A4 80 gram, 500 lembar per rim'},
    {'id': 4, 'kode': 'BRG-004', 'nama': 'Tinta Printer Canon', 'kategori': 'Alat Tulis', 'stok': 80, 'satuan': 'Botol', 'harga': 95000, 'lokasi': 'Gudang B', 'stok_min': 10, 'gambar': '', 'deskripsi': 'Tinta printer Canon GI-790 Black'},
    {'id': 5, 'kode': 'BRG-005', 'nama': 'Mie Instan Goreng', 'kategori': 'Makanan', 'stok': 1200, 'satuan': 'Pcs', 'harga': 3500, 'lokasi': 'Gudang C', 'stok_min': 100, 'gambar': '', 'deskripsi': 'Mie instan goreng rasa original'},
    {'id': 6, 'kode': 'BRG-006', 'nama': 'Air Mineral 600ml', 'kategori': 'Minuman', 'stok': 2400, 'satuan': 'Botol', 'harga': 4000, 'lokasi': 'Gudang C', 'stok_min': 200, 'gambar': '', 'deskripsi': 'Air mineral kemasan botol 600ml'},
    {'id': 7, 'kode': 'BRG-007', 'nama': 'Kaos Polos Hitam', 'kategori': 'Pakaian', 'stok': 300, 'satuan': 'Pcs', 'harga': 75000, 'lokasi': 'Gudang D', 'stok_min': 30, 'gambar': '', 'deskripsi': 'Kaos polos cotton combed 30s warna hitam'},
    {'id': 8, 'kode': 'BRG-008', 'nama': 'Keyboard Mechanical', 'kategori': 'Elektronik', 'stok': 45, 'satuan': 'Unit', 'harga': 450000, 'lokasi': 'Gudang A', 'stok_min': 10, 'gambar': '', 'deskripsi': 'Keyboard mechanical RGB blue switch'},
    {'id': 9, 'kode': 'BRG-009', 'nama': 'Sapu Lantai', 'kategori': 'Peralatan', 'stok': 60, 'satuan': 'Pcs', 'harga': 35000, 'lokasi': 'Gudang E', 'stok_min': 10, 'gambar': '', 'deskripsi': 'Sapu lantai ijuk gagang kayu'},
    {'id': 10, 'kode': 'BRG-010', 'nama': 'Pulpen Pilot G2', 'kategori': 'Alat Tulis', 'stok': 3, 'satuan': 'Lusin', 'harga': 180000, 'lokasi': 'Gudang B', 'stok_min': 5, 'gambar': '', 'deskripsi': 'Pulpen gel Pilot G2 0.5mm hitam'},
]


def generate_transactions():
    """Generate dummy transaction history."""
    types = ['masuk', 'keluar']
    transactions = []
    for i in range(1, 51):
        tipe = random.choice(types)
        brg = random.choice(BARANG_LIST)
        qty = random.randint(1, 50)
        days_ago = random.randint(0, 60)
        tanggal = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        transactions.append({
            'id': i,
            'kode_transaksi': f"TRX-{str(i).zfill(4)}",
            'tipe': tipe,
            'barang_id': brg['id'],
            'barang_nama': brg['nama'],
            'barang_kode': brg['kode'],
            'kategori': brg['kategori'],
            'jumlah': qty,
            'satuan': brg['satuan'],
            'tanggal': tanggal,
            'keterangan': f"{'Penerimaan' if tipe == 'masuk' else 'Pengeluaran'} barang dari {'supplier' if tipe == 'masuk' else 'departemen'}",
            'petugas': random.choice(['Ahmad Rizky', 'Siti Nurhaliza', 'Budi Santoso', 'Dewi Lestari']),
        })
    transactions.sort(key=lambda x: x['tanggal'], reverse=True)
    return transactions


TRANSACTIONS = generate_transactions()

USER_PROFILE = {
    'nama': 'Ahmad Rizky',
    'email': 'ahmad.rizky@stockstory.id',
    'role': 'Admin Gudang',
    'perusahaan': 'PT. StockStory Indonesia',
    'telepon': '+62 812 3456 7890',
    'alamat': 'Jl. Merdeka No. 123, Jakarta Pusat',
    'bergabung': '15 Januari 2025',
    'avatar_initial': 'AR',
}

FAQ_LIST = [
    {
        'q': 'Bagaimana cara menambah barang baru?',
        'a': 'Buka menu "Data Barang" di sidebar, lalu klik tombol "+ Tambah Barang". Isi formulir yang tersedia dan klik "Simpan".',
    },
    {
        'q': 'Bagaimana cara mencatat barang masuk?',
        'a': 'Buka menu "Barang Masuk" di sidebar, lalu klik "+ Catat Barang Masuk". Pilih barang, isi jumlah, dan simpan.',
    },
    {
        'q': 'Bagaimana cara melihat laporan inventaris?',
        'a': 'Buka menu "Laporan" di sidebar. Anda dapat memfilter berdasarkan periode, kategori, dan mengunduh laporan dalam format PDF atau Excel.',
    },
    {
        'q': 'Apa itu stok minimum?',
        'a': 'Stok minimum adalah batas terendah stok barang. Jika stok di bawah batas ini, sistem akan memberikan peringatan agar Anda segera melakukan restock.',
    },
    {
        'q': 'Bagaimana cara mengedit data barang?',
        'a': 'Buka menu "Data Barang", cari barang yang ingin diedit, lalu klik ikon edit (pensil) di kolom aksi.',
    },
    {
        'q': 'Bagaimana cara mengekspor data?',
        'a': 'Pada setiap halaman tabel, terdapat tombol "Ekspor" yang memungkinkan Anda mengunduh data dalam format CSV, Excel, atau PDF.',
    },
]

# ───────────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────────

def get_kpi():
    """Calculate KPI data for dashboard."""
    total_barang = len(BARANG_LIST)
    total_stok = sum(b['stok'] for b in BARANG_LIST)
    total_nilai = sum(b['stok'] * b['harga'] for b in BARANG_LIST)
    stok_rendah = sum(1 for b in BARANG_LIST if b['stok'] <= b['stok_min'])
    masuk_bulan_ini = sum(1 for t in TRANSACTIONS if t['tipe'] == 'masuk' and t['tanggal'] >= datetime.now().strftime('%Y-%m-01'))
    keluar_bulan_ini = sum(1 for t in TRANSACTIONS if t['tipe'] == 'keluar' and t['tanggal'] >= datetime.now().strftime('%Y-%m-01'))

    return {
        'total_barang': total_barang,
        'total_stok': total_stok,
        'total_nilai': total_nilai,
        'stok_rendah': stok_rendah,
        'masuk_bulan_ini': masuk_bulan_ini,
        'keluar_bulan_ini': keluar_bulan_ini,
    }


def get_timeline():
    """Get recent activity timeline."""
    timeline = []
    for t in TRANSACTIONS[:10]:
        icon = 'arrow_downward' if t['tipe'] == 'masuk' else 'arrow_upward'
        color = 'success' if t['tipe'] == 'masuk' else 'danger'
        label = 'Barang Masuk' if t['tipe'] == 'masuk' else 'Barang Keluar'
        timeline.append({
            'icon': icon,
            'color': color,
            'label': label,
            'desc': f"{t['jumlah']} {t['satuan']} {t['barang_nama']}",
            'petugas': t['petugas'],
            'tanggal': t['tanggal'],
        })
    return timeline


def get_chart_data():
    """Generate chart data for dashboard."""
    labels = []
    masuk_data = []
    keluar_data = []
    for i in range(6, -1, -1):
        d = datetime.now() - timedelta(days=i)
        label = d.strftime('%d %b')
        labels.append(label)
        day_str = d.strftime('%Y-%m-%d')
        masuk_data.append(sum(t['jumlah'] for t in TRANSACTIONS if t['tipe'] == 'masuk' and t['tanggal'] == day_str))
        keluar_data.append(sum(t['jumlah'] for t in TRANSACTIONS if t['tipe'] == 'keluar' and t['tanggal'] == day_str))
    return {'labels': labels, 'masuk': masuk_data, 'keluar': keluar_data}


def get_kategori_data():
    """Generate per-category stock data for pie chart."""
    cat_map = {}
    for b in BARANG_LIST:
        cat_map[b['kategori']] = cat_map.get(b['kategori'], 0) + b['stok']
    return {'labels': list(cat_map.keys()), 'data': list(cat_map.values())}


def format_rupiah(value):
    """Format number as Rupiah string."""
    return f"Rp {value:,.0f}".replace(',', '.')


app.jinja_env.filters['rupiah'] = format_rupiah

# ───────────────────────────────────────────
# ROUTES
# ───────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    kpi = get_kpi()
    timeline = get_timeline()
    chart_data = get_chart_data()
    kategori_data = get_kategori_data()
    return render_template('dashboard.html',
                           kpi=kpi,
                           timeline=timeline,
                           chart_data=json.dumps(chart_data),
                           kategori_data=json.dumps(kategori_data),
                           page_title='Dashboard')


@app.route('/data-barang')
def data_barang():
    search = request.args.get('search', '').lower()
    kategori = request.args.get('kategori', '')
    filtered = BARANG_LIST
    if search:
        filtered = [b for b in filtered if search in b['nama'].lower() or search in b['kode'].lower()]
    if kategori:
        filtered = [b for b in filtered if b['kategori'] == kategori]
    return render_template('data_barang.html',
                           barang_list=filtered,
                           categories=CATEGORIES,
                           search=search,
                           kategori=kategori,
                           page_title='Data Barang')


@app.route('/tambah-barang', methods=['GET', 'POST'])
def tambah_barang():
    if request.method == 'POST':
        new_id = max(b['id'] for b in BARANG_LIST) + 1
        new_kode = f"BRG-{str(new_id).zfill(3)}"
        item = {
            'id': new_id,
            'kode': new_kode,
            'nama': request.form.get('nama', ''),
            'kategori': request.form.get('kategori', ''),
            'stok': int(request.form.get('stok', 0)),
            'satuan': request.form.get('satuan', ''),
            'harga': int(request.form.get('harga', 0)),
            'lokasi': request.form.get('lokasi', ''),
            'stok_min': int(request.form.get('stok_min', 0)),
            'gambar': '',
            'deskripsi': request.form.get('deskripsi', ''),
        }
        BARANG_LIST.append(item)
        flash('Barang berhasil ditambahkan!', 'success')
        return redirect(url_for('data_barang'))
    return render_template('tambah_barang.html',
                           categories=CATEGORIES,
                           page_title='Tambah Barang')


@app.route('/edit-barang/<int:barang_id>', methods=['GET', 'POST'])
def edit_barang(barang_id):
    barang = next((b for b in BARANG_LIST if b['id'] == barang_id), None)
    if not barang:
        flash('Barang tidak ditemukan!', 'danger')
        return redirect(url_for('data_barang'))
    if request.method == 'POST':
        barang['nama'] = request.form.get('nama', barang['nama'])
        barang['kategori'] = request.form.get('kategori', barang['kategori'])
        barang['stok'] = int(request.form.get('stok', barang['stok']))
        barang['satuan'] = request.form.get('satuan', barang['satuan'])
        barang['harga'] = int(request.form.get('harga', barang['harga']))
        barang['lokasi'] = request.form.get('lokasi', barang['lokasi'])
        barang['stok_min'] = int(request.form.get('stok_min', barang['stok_min']))
        barang['deskripsi'] = request.form.get('deskripsi', barang['deskripsi'])
        flash('Barang berhasil diperbarui!', 'success')
        return redirect(url_for('data_barang'))
    return render_template('edit_barang.html',
                           barang=barang,
                           categories=CATEGORIES,
                           page_title='Edit Barang')


@app.route('/hapus-barang/<int:barang_id>')
def hapus_barang(barang_id):
    global BARANG_LIST
    BARANG_LIST = [b for b in BARANG_LIST if b['id'] != barang_id]
    flash('Barang berhasil dihapus!', 'success')
    return redirect(url_for('data_barang'))


@app.route('/barang-masuk', methods=['GET', 'POST'])
def barang_masuk():
    if request.method == 'POST':
        barang_id = int(request.form.get('barang_id', 0))
        jumlah = int(request.form.get('jumlah', 0))
        barang = next((b for b in BARANG_LIST if b['id'] == barang_id), None)
        if barang and jumlah > 0:
            barang['stok'] += jumlah
            new_trx = {
                'id': len(TRANSACTIONS) + 1,
                'kode_transaksi': f"TRX-{str(len(TRANSACTIONS) + 1).zfill(4)}",
                'tipe': 'masuk',
                'barang_id': barang['id'],
                'barang_nama': barang['nama'],
                'barang_kode': barang['kode'],
                'kategori': barang['kategori'],
                'jumlah': jumlah,
                'satuan': barang['satuan'],
                'tanggal': datetime.now().strftime('%Y-%m-%d'),
                'keterangan': request.form.get('keterangan', ''),
                'petugas': USER_PROFILE['nama'],
            }
            TRANSACTIONS.insert(0, new_trx)
            flash(f'{jumlah} {barang["satuan"]} {barang["nama"]} berhasil ditambahkan ke stok!', 'success')
            return redirect(url_for('barang_masuk'))
        else:
            flash('Data tidak valid!', 'danger')

    masuk_list = [t for t in TRANSACTIONS if t['tipe'] == 'masuk'][:20]
    return render_template('barang_masuk.html',
                           barang_list=BARANG_LIST,
                           masuk_list=masuk_list,
                           page_title='Barang Masuk')


@app.route('/barang-keluar', methods=['GET', 'POST'])
def barang_keluar():
    if request.method == 'POST':
        barang_id = int(request.form.get('barang_id', 0))
        jumlah = int(request.form.get('jumlah', 0))
        barang = next((b for b in BARANG_LIST if b['id'] == barang_id), None)
        if barang and jumlah > 0 and barang['stok'] >= jumlah:
            barang['stok'] -= jumlah
            new_trx = {
                'id': len(TRANSACTIONS) + 1,
                'kode_transaksi': f"TRX-{str(len(TRANSACTIONS) + 1).zfill(4)}",
                'tipe': 'keluar',
                'barang_id': barang['id'],
                'barang_nama': barang['nama'],
                'barang_kode': barang['kode'],
                'kategori': barang['kategori'],
                'jumlah': jumlah,
                'satuan': barang['satuan'],
                'tanggal': datetime.now().strftime('%Y-%m-%d'),
                'keterangan': request.form.get('keterangan', ''),
                'petugas': USER_PROFILE['nama'],
            }
            TRANSACTIONS.insert(0, new_trx)
            flash(f'{jumlah} {barang["satuan"]} {barang["nama"]} berhasil dikeluarkan dari stok!', 'success')
            return redirect(url_for('barang_keluar'))
        else:
            flash('Data tidak valid atau stok tidak mencukupi!', 'danger')

    keluar_list = [t for t in TRANSACTIONS if t['tipe'] == 'keluar'][:20]
    return render_template('barang_keluar.html',
                           barang_list=BARANG_LIST,
                           keluar_list=keluar_list,
                           page_title='Barang Keluar')


@app.route('/riwayat')
def riwayat():
    tipe = request.args.get('tipe', '')
    search = request.args.get('search', '').lower()
    filtered = TRANSACTIONS
    if tipe:
        filtered = [t for t in filtered if t['tipe'] == tipe]
    if search:
        filtered = [t for t in filtered if search in t['barang_nama'].lower() or search in t['kode_transaksi'].lower()]
    return render_template('riwayat.html',
                           transactions=filtered,
                           tipe=tipe,
                           search=search,
                           page_title='Riwayat Transaksi')


@app.route('/laporan')
def laporan():
    kpi = get_kpi()
    kategori_data = get_kategori_data()

    # Per-category breakdown
    cat_breakdown = []
    for cat in CATEGORIES:
        items = [b for b in BARANG_LIST if b['kategori'] == cat]
        if items:
            cat_breakdown.append({
                'kategori': cat,
                'jumlah_item': len(items),
                'total_stok': sum(b['stok'] for b in items),
                'total_nilai': sum(b['stok'] * b['harga'] for b in items),
            })

    # Top items by stock value
    top_items = sorted(BARANG_LIST, key=lambda b: b['stok'] * b['harga'], reverse=True)[:5]

    # Low stock items
    low_stock = [b for b in BARANG_LIST if b['stok'] <= b['stok_min']]

    return render_template('laporan.html',
                           kpi=kpi,
                           kategori_data=json.dumps(kategori_data),
                           cat_breakdown=cat_breakdown,
                           top_items=top_items,
                           low_stock=low_stock,
                           page_title='Laporan Inventaris')


@app.route('/profil')
def profil():
    return render_template('profil.html',
                           user=USER_PROFILE,
                           page_title='Profil')


@app.route('/bantuan')
def bantuan():
    return render_template('bantuan.html',
                           faq_list=FAQ_LIST,
                           page_title='Bantuan')


# ───────────────────────────────────────────
# API ENDPOINTS (for AJAX)
# ───────────────────────────────────────────

@app.route('/api/barang/<int:barang_id>')
def api_barang_detail(barang_id):
    barang = next((b for b in BARANG_LIST if b['id'] == barang_id), None)
    if barang:
        return jsonify(barang)
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
