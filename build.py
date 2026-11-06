#!/usr/bin/env python3
"""Bangun 3 situs agency (website / chatbot / gabungan) dari template index.html."""
import os, html as htmlmod

BASE = os.path.expanduser("~/workspace/ai-agency-site/index.html")
OUT = os.path.expanduser("~/workspace/agency-sites")
WA = "https://wa.me/628811722942"

with open(BASE, encoding="utf-8") as f:
    base = f.read()

def cut(h, start, end):
    i = h.index(start); j = h.index(end, i)
    return h[:i], h[j:]

def tiers_js(tiers):
    items = []
    for t in tiers:
        feats = ",".join("'" + f.replace("'", "\\'") + "'" for f in t["feats"])
        hot = ",hot:true" if t.get("hot") else ""
        items.append(
            "{code:'%s',name:'%s',tag:'%s',price:'%s',per:'%s'%s,feats:[%s],cta:'%s'}" % (
                t["code"], t["name"], t["tag"], t["price"], t["per"], hot, feats, t["cta"]))
    return """<script>
const PKG=[%s];
(function(){
 const grid=document.getElementById('tierGrid');
 grid.innerHTML=PKG.map(p=>'<article class="tier'+(p.hot?' hot':'')+'">'
  +(p.hot?'<span class="flag">Paling dipilih</span>':'')
  +'<h3>'+p.name+'</h3><p class="tagline">'+p.tag+'</p>'
  +'<div class="harga">'+p.price+' <span>'+p.per+'</span></div>'
  +'<ul>'+p.feats.map(f=>'<li>'+f+'</li>').join('')+'</ul>'
  +'<a class="btn '+(p.hot?'':'ghost')+'" href="%s?text='+encodeURIComponent('Halo, saya tertarik paket '+p.code+' ('+p.name+').')+'" target="_blank" rel="noopener">'+p.cta+'</a>'
  +'</article>').join('');
})();
</script>""" % (",".join(items), WA)

def faq_html(items):
    rows = "".join(
        '<details><summary>%s</summary><div class="ans"><div><p>%s</p></div></div></details>' % (q, a)
        for q, a in items)
    return ('<section id="faq"><div class="wrap">\n  <span class="kicker">Tanya jawab</span>\n'
            '  <h2 class="sec">Sering ditanyakan.</h2>\n  <div class="faq">\n    %s\n  </div>\n</div></section>' % rows)

def steps_html(steps):
    rows = "".join('<div class="step"><h3>%s</h3><p>%s</p></div>' % s for s in steps)
    return ('<section id="cara"><div class="wrap">\n  <span class="kicker">Cara kerja</span>\n'
            '  <h2 class="sec">Dari cerita Anda<br>ke website live.</h2>\n  <div class="steps">\n    %s\n  </div>\n</div></section>' % rows)

SVC_WEB = '''<article class="svc a">
      <div><span class="num">01</span><h3>Website</h3><p>Halaman bisnis Anda di internet — dirancang untuk meyakinkan pengunjung dalam hitungan detik, bukan sekadar ada.</p>
      <ul><li>Desain custom, mobile-responsive</li><li>SEO dasar agar mudah ditemukan Google</li><li>Tombol WhatsApp &amp; Google Maps</li><li>Revisi sampai Anda puas</li></ul></div>
      <div class="price">Mulai dari <b>Rp2,5 jt</b> · sekali bayar</div>
    </article>'''
SVC_BOT = '''<article class="svc b">
      <div><span class="num">01</span><h3>Chatbot</h3><p>Asisten otomatis untuk bisnis Anda: menyapa pelanggan, menjawab harga dan FAQ, lalu mengantar mereka ke booking — siang dan malam.</p>
      <ul><li>Menjawab harga, FAQ, dan booking otomatis</li><li>Di website dan WhatsApp</li><li>Handoff ke admin saat butuh manusia</li><li>Hanya menjawab dari data bisnis Anda — tidak mengarang</li></ul></div>
      <div class="price">Mulai dari <b>Rp3,9 jt</b> + Rp199 rb/bln</div>
    </article>'''

POPUP_CSS = """
/* cross-sell popup */
.xsell{position:fixed;inset:0;z-index:200;display:none;align-items:center;justify-content:center;background:rgba(8,13,26,.55);backdrop-filter:blur(6px);padding:20px}
.xsell.show{display:flex}
.xsell-card{background:#fff;border-radius:24px;max-width:440px;width:100%;padding:34px 30px;position:relative;box-shadow:0 30px 70px rgba(0,0,0,.3);animation:pop .45s cubic-bezier(.16,1,.3,1)}
@keyframes pop{from{opacity:0;transform:translateY(24px) scale(.97)}to{opacity:1;transform:none}}
.xsell-card h3{font-family:"Space Grotesk",sans-serif;font-size:1.35rem;margin-bottom:10px;line-height:1.3}
.xsell-card p{color:var(--mut);font-size:.92rem;line-height:1.65;margin-bottom:20px}
.xsell-card .row{display:flex;flex-direction:column;gap:10px}
.xsell-card .row .btn{justify-content:center}
.xsell-close{position:absolute;top:10px;right:16px;background:none;border:0;font-size:1.4rem;cursor:pointer;color:var(--mut)}
"""

POPUP_JS = """<script>
(function(){
 var KEY='xsell_seen_v1', shown=false;
 try{ var t=+localStorage.getItem(KEY)||0; if(Date.now()-t<7*864e5) return; }catch(e){}
 function close(){ document.getElementById('xsell').classList.remove('show'); }
 function show(){ if(shown) return; shown=true;
  document.getElementById('xsell').classList.add('show');
  try{ localStorage.setItem(KEY, String(Date.now())); }catch(e){} }
 document.getElementById('xsellClose').onclick=close;
 document.getElementById('xsellLater').onclick=close;
 document.getElementById('xsell').addEventListener('click',function(e){ if(e.target===this) close(); });
 setTimeout(show, 30000);
 document.addEventListener('mouseout',function(e){ if(!e.relatedTarget && e.clientY<=0) show(); });
})();
</script>"""

def popup_html(title, desc, buttons):
    btns = "".join(
        '\n   <a class="btn%s" href="%s" target="_blank" rel="noopener">%s</a>' % (
            "" if primary else " ghost", url, label)
        for label, url, primary in buttons)
    return ('''<div class="xsell" id="xsell" role="dialog" aria-label="Penawaran">
 <div class="xsell-card">
  <button class="xsell-close" id="xsellClose" aria-label="Tutup">\u00d7</button>
  <h3>%s</h3>
  <p>%s</p>
  <div class="row">%s
   <button class="btn ghost" id="xsellLater">Nanti saja</button>
  </div>
 </div>
</div>''' % (title, desc, btns))

def layanan_section(cards_html, h2):
    return ('<section id="layanan"><div class="wrap">\n  <span class="kicker">Layanan kami</span>\n'
            '  <h2 class="sec">%s</h2>\n  <div class="duo">\n    %s\n  </div>\n</div></section>' % (h2, cards_html))

def paket_section(h2, lead, tiers, note):
    return ('<section id="paket"><div class="wrap">\n  <span class="kicker">Paket</span>\n'
            '  <h2 class="sec">%s</h2>\n  <p class="lead">%s</p>\n'
            '  <div class="tier-grid" id="tierGrid"></div>\n  <p class="pkg-note">%s</p>\n</div></section>'
            % (h2, lead, note))

W_TIERS = [
    dict(code="W1", name="Website Basic", tag="Satu halaman yang meyakinkan.", price="Rp2,5 jt", per="sekali bayar",
         feats=["1 halaman (hero, tentang, layanan, kontak)", "Desain template premium", "SEO dasar + tombol WhatsApp", "2x revisi"], cta="Pilih W1"),
    dict(code="W2", name="Website Standard", tag="Untuk bisnis yang mulai serius online.", price="Rp4,9 jt", per="sekali bayar", hot=True,
         feats=["5 halaman, semi-custom", "SEO dasar + Google Maps", "Tombol WhatsApp & formulir kontak", "3x revisi"], cta="Pilih W2"),
    dict(code="W3", name="Website Premium", tag="Hadir penuh dengan konten.", price="Rp7,5 jt", per="sekali bayar",
         feats=["8 halaman + blog", "Desain custom penuh", "SEO + struktur konten", "5x revisi"], cta="Pilih W3"),
]
B_TIERS = [
    dict(code="B1", name="Chatbot Dasar", tag="Menyapa dan menjawab otomatis.", price="Rp3,9 jt", per="+ Rp199 rb/bln",
         feats=["Menjawab FAQ & daftar harga", "Alur booking + handoff admin", "1 nomor WhatsApp", "2x revisi alur"], cta="Pilih B1"),
    dict(code="B2", name="Chatbot Lengkap", tag="Paket utama chatbot.", price="Rp6,9 jt", per="+ Rp349 rb/bln", hot=True,
         feats=["Semua isi Chatbot Dasar", "Jawaban AI dari data bisnis Anda", "Laporan chat bulanan", "3x revisi alur"], cta="Pilih B2"),
    dict(code="B3", name="Chatbot Multi-cabang", tag="Untuk bisnis yang ramai.", price="Rp11 jt", per="+ Rp599 rb/bln",
         feats=["Semua isi Chatbot Lengkap", "Multi-cabang & multi-admin", "Integrasi sistem / kalender", "Prioritas support"], cta="Pilih B3"),
]
C_TIERS = [
    dict(code="C1", name="Gabungan Basic", tag="Website + chatbot dasar.", price="Rp8,9 jt", per="+ Rp299 rb/bln",
         feats=["Website 5 halaman", "Chatbot: cabang, harga, FAQ, booking", "Handoff ke WhatsApp admin", "2x revisi"], cta="Pilih C1"),
    dict(code="C2", name="Gabungan Standard", tag="Paket utama kami.", price="Rp12 jt", per="+ Rp499 rb/bln", hot=True,
         feats=["Website 8 halaman custom", "Chatbot lengkap + laporan bulanan", "Pembaruan konten berkala", "3x revisi"], cta="Pilih C2"),
    dict(code="C3", name="Gabungan Premium", tag="Untuk bisnis multi-cabang.", price="Rp18 jt", per="+ Rp899 rb/bln",
         feats=["Website 10 halaman + landing promo", "Chatbot multi-cabang", "Laporan lengkap + prioritas support", "5x revisi"], cta="Pilih C3"),
]

VARIANTS = {
    "website": dict(
        title="Jasa Pembuatan Website untuk UMKM Indonesia — AI Digital Agency",
        meta="Jasa pembuatan website untuk klinik, kuliner, jasa, dan UMKM Indonesia. Mulai Rp2,5 jt sekali bayar — desain custom, SEO dasar, tombol WhatsApp.",
        hero_h1='Website yang <span class="it">bekerja,</span><br>bukan sekadar dipajang.',
        hero_sub="Kami membangun website untuk klinik, kuliner, jasa, dan UMKM Indonesia — dirancang menangkap pengunjung dan mengubahnya jadi pelanggan.",
        hero_meta="<b>3 paket · mulai Rp2,5 jt · sekali bayar.</b>",
        layanan_h2="Satu produk:<br>website yang menjual.",
        cards=SVC_WEB,
        paket_h2="Pilih tier yang<br>pas untuk bisnis Anda.",
        paket_lead="Tiga tier website, dari satu halaman sampai custom penuh. Naik tier kapan saja.",
        tiers=W_TIERS,
        paket_note="Pembayaran via QRIS / transfer, sekali bayar di awal pengerjaan. <b>Harga dapat berubah; konfirmasi saat konsultasi.</b>",
        steps=[
            ("Ceritakan bisnis Anda", "Konsultasi gratis via Telegram. Ceritakan layanan, harga, dan cara pelanggan menghubungi Anda sekarang."),
            ("Kami bangun", "Website dibangun dari data bisnis Anda — teks dan harga yang Anda konfirmasi, bukan karangan."),
            ("Anda review", "Lihat preview-nya, minta revisi sampai pas. Tidak launch sebelum Anda bilang ya."),
            ("Launch", "Website live dan mulai bekerja — menangkap pengunjung dan mengantar mereka menghubungi Anda."),
        ],
        faq=[
            ("Berapa lama pengerjaannya?", "Umumnya 7–14 hari tergantung tier. Estimasi pasti kami sampaikan setelah konsultasi awal."),
            ("Apakah saya dapat revisi?", "Ya — setiap paket termasuk jatah revisi (2x, 3x, atau 5x sesuai tier)."),
            ("Bagaimana pembayarannya?", "Via QRIS / transfer, sekali bayar di awal pengerjaan."),
            ("Apakah website-nya SEO-friendly?", "Ya — SEO dasar termasuk: struktur heading, meta, kecepatan, dan Google Maps."),
            ("Bisa tambah halaman nanti?", "Bisa — naik tier atau tambah halaman custom kapan saja."),
        ],
        footer="Website untuk UMKM Indonesia.",
        closing_h2="Ceritakan bisnis Anda — konsultasi gratis.",
        closing_p="Tidak ada kewajiban. Ceritakan saja bisnis Anda, kami tunjukkan seperti apa website-nya sebelum Anda memutuskan.",
    ),
    "chatbot": dict(
        title="Jasa Pembuatan Chatbot WhatsApp & Website — AI Digital Agency",
        meta="Jasa pembuatan chatbot untuk bisnis Indonesia: menjawab harga, FAQ, dan booking otomatis 24/7. Mulai Rp3,9 jt + Rp199 rb/bln.",
        hero_h1='Chatbot yang <span class="it">menjawab,</span><br>siang dan malam.',
        hero_sub="Chatbot WhatsApp dan website untuk bisnis Indonesia — menjawab harga, FAQ, dan mengantar pelanggan ke booking, 24 jam tanpa henti.",
        hero_meta="<b>3 paket · mulai Rp3,9 jt + Rp199 rb/bln.</b>",
        layanan_h2="Satu produk:<br>asisten otomatis bisnis Anda.",
        cards=SVC_BOT,
        paket_h2="Pilih tier yang<br>pas untuk bisnis Anda.",
        paket_lead="Tiga tier chatbot, dari alur dasar sampai multi-cabang. Naik tier kapan saja.",
        tiers=B_TIERS,
        paket_note="Retainer bulanan untuk platform chatbot, maintenance, dan pembaruan konten. <b>Biaya pesan WhatsApp (per-pesan, dari Meta) ditagih sesuai pemakaian.</b> Pembayaran via QRIS / transfer. Harga dapat berubah; konfirmasi saat konsultasi.",
        steps=[
            ("Ceritakan bisnis Anda", "Konsultasi gratis via Telegram. Ceritakan layanan, harga, FAQ, dan alur booking Anda sekarang."),
            ("Kami bangun", "Chatbot dibangun dari data bisnis Anda — hanya menjawab dari yang Anda konfirmasi, tidak mengarang."),
            ("Anda review", "Uji alur percakapannya, minta revisi sampai pas. Tidak launch sebelum Anda bilang ya."),
            ("Launch & melayani", "Chatbot live 24/7 — menjawab, mengantar booking, dan menyerahkan ke admin Anda saat dibutuhkan."),
        ],
        faq=[
            ("Apakah chatbot bisa mengarang harga?", "Tidak — chatbot hanya menjawab dari data bisnis yang Anda konfirmasi. Yang tidak ada di datanya, diserahkan ke admin."),
            ("Apakah butuh WhatsApp Business API?", "Untuk chatbot di WhatsApp, ya — kami bantu setup-nya. Biaya pesan WhatsApp (per-pesan, dari Meta) ditagih sesuai pemakaian."),
            ("Berapa lama pengerjaannya?", "Umumnya 7–14 hari tergantung tier. Estimasi pasti setelah konsultasi awal."),
            ("Bagaimana pembayarannya?", "Via QRIS / transfer. Biaya build di awal, retainer bulanan setelah chatbot live."),
            ("Bisa ubah jawaban chatbot nanti?", "Bisa — pembaruan konten (harga baru, FAQ baru) termasuk dalam retainer."),
        ],
        footer="Chatbot untuk UMKM Indonesia.",
        closing_h2="Ceritakan bisnis Anda — konsultasi gratis.",
        closing_p="Tidak ada kewajiban. Ceritakan saja bisnis Anda, kami tunjukkan seperti apa chatbot-nya sebelum Anda memutuskan.",
    ),
    "gabungan": dict(
        title="Website + Chatbot untuk UMKM Indonesia — AI Digital Agency",
        meta="Paket gabungan website + chatbot untuk klinik, kuliner, jasa, dan UMKM Indonesia. Website menangkap pengunjung, chatbot menutup booking. Mulai Rp8,9 jt.",
        hero_h1='Website yang <span class="it">bekerja,</span><br>bukan sekadar dipajang.',
        hero_sub="Website + chatbot untuk klinik, kuliner, jasa, dan UMKM Indonesia. Website menangkap pengunjung, chatbot menjawab harga dan menutup booking — 24 jam, tanpa henti.",
        hero_meta="<b>3 paket gabungan · mulai Rp8,9 jt + Rp299 rb/bln.</b>",
        layanan_h2="Satu paket lengkap:<br>website + chatbot.",
        cards=SVC_WEB + "\n" + SVC_BOT.replace('Mulai dari <b>Rp3,9 jt</b> + Rp199 rb/bln', 'Termasuk dalam paket gabungan'),
        paket_h2="Pilih tier yang<br>pas untuk bisnis Anda.",
        paket_lead="Tiga tier gabungan website + chatbot. Mulai dari yang paling sesuai — naik tier kapan saja.",
        tiers=C_TIERS,
        paket_note="Paket Gabungan termasuk retainer bulanan untuk platform chatbot, maintenance, dan pembaruan konten. <b>Biaya pesan WhatsApp (per-pesan, dari Meta) ditagih sesuai pemakaian</b> — supaya kami tidak menombok saat chat Anda ramai. Pembayaran via QRIS / transfer. Harga dapat berubah; konfirmasi saat konsultasi.",
        steps=[
            ("Ceritakan bisnis Anda", "Konsultasi gratis via Telegram. Ceritakan layanan, harga, cabang, dan cara pelanggan menghubungi Anda sekarang."),
            ("Kami bangun", "Website dan chatbot dibangun dari data bisnis Anda — harga dan FAQ yang Anda konfirmasi, bukan karangan."),
            ("Anda review", "Lihat preview-nya, minta revisi sampai pas. Tidak launch sebelum Anda bilang ya."),
            ("Launch & melayani", "Website live, chatbot melayani pengunjung 24/7 — menjawab, mengantar booking, dan menyerahkan ke admin Anda."),
        ],
        faq=[
            ("Berapa lama pengerjaannya?", "Umumnya 14–21 hari tergantung tier. Estimasi pasti kami sampaikan setelah konsultasi awal."),
            ("Apakah chatbot bisa halusinasi / mengarang harga?", "Tidak — chatbot hanya menjawab dari data bisnis yang Anda konfirmasi. Yang tidak ada di datanya, diserahkan ke admin."),
            ("Apakah saya butuh WhatsApp Business API?", "Untuk chatbot yang melayani di WhatsApp, ya — kami bantu setup-nya. Biaya pesan WhatsApp (per-pesan, dari Meta) ditagih sesuai pemakaian."),
            ("Bagaimana pembayarannya?", "Via QRIS / transfer. Biaya build di awal pengerjaan; retainer bulanan setelah website live."),
            ("Apakah saya bisa revisi setelah launch?", "Ya. Setiap paket termasuk jatah revisi, plus pembaruan konten berkala dalam retainer."),
        ],
        footer="Website & chatbot untuk UMKM Indonesia.",
        closing_h2="Ceritakan bisnis Anda — konsultasi gratis.",
        closing_p="Tidak ada kewajiban. Ceritakan saja bisnis Anda, kami tunjukkan seperti apa website dan chatbot-nya sebelum Anda memutuskan.",
    ),
}

POPUPS = {    "website": popup_html(
        "Website + chatbot = pelanggan terlayani 24/7",
        "Website Anda sudah bagus. Tambah chatbot: menjawab harga, FAQ, dan mengantar pengunjung ke booking — siang dan malam, tanpa admin.",
        [("Lihat Paket Gabungan", "https://jasa-website-chatbot-di.pages.dev", True)]),
    "chatbot": popup_html(
        "Chatbot paling kuat di atas website sendiri",
        "Belum punya website? Atau mau sekalian paket lengkap — website yang dilayani chatbot 24/7?",
        [("Lihat Paket Gabungan", "https://jasa-website-chatbot-di.pages.dev", True),
         ("Lihat Jasa Website", "https://jasa-website-di.pages.dev", False)]),
    "gabungan": None,
}

# Perbaikan layout desktop: bubble chat menutupi teks mockup di tengah kata.
# Beri ruang kosong di bawah isi mockup, bubble duduk di ruang itu.
LAYOUT_FIX_CSS = """
/* fix hero kanan: bubble tidak lagi menutupi teks */
.mock-body{padding-bottom:132px}
.chat-bubble{right:18px;bottom:22px}
"""

# Perbaikan anti-slop (stop-slop / avoid-ai-writing): hilangkan pola
# "bukan sekadar X" dan em dash — tulis ulang langsung.
DESLOP = [
    ('Website yang <span class="it">bekerja,</span><br>bukan sekadar dipajang.',
     'Website yang <span class="it">mendatangkan</span><br>pelanggan baru.'),
    ('<p>Halaman bisnis Anda di internet — dirancang untuk meyakinkan pengunjung dalam hitungan detik, bukan sekadar ada.</p>',
     '<p>Halaman bisnis Anda di internet. Pengunjung paham dan menghubungi Anda dalam hitungan detik.</p>'),
    ('Mulai Rp2,5 jt sekali bayar — desain custom, SEO dasar, tombol WhatsApp.',
     'Mulai Rp2,5 jt sekali bayar. Desain custom, SEO dasar, tombol WhatsApp.'),
    ('dan UMKM Indonesia — dirancang menangkap pengunjung dan mengubahnya jadi pelanggan.',
     'dan UMKM Indonesia. Setiap halaman dirancang menangkap pengunjung dan mengubahnya jadi pelanggan.'),
    ('chatbot menjawab harga dan menutup booking — 24 jam, tanpa henti.',
     'chatbot menjawab harga dan menutup booking, 24 jam tanpa henti.'),
    ('Website + chatbot demo untuk klinik gigi — chatbot menjawab harga dan booking langsung, tanpa menunggu admin.',
     'Website + chatbot demo untuk klinik gigi. Chatbot menjawab harga dan booking langsung, tanpa menunggu admin.'),
    ('dengan cerita “Cemas → Ditemani → Tenang” — perjalanan pasien dari takut sampai senyum',
     'dengan cerita “Cemas → Ditemani → Tenang”: perjalanan pasien dari takut sampai senyum'),
    ('Chatbot yang menjawab harga, FAQ, dan booking — lalu handoff ke WhatsApp admin dengan pesan yang sudah terisi',
     'Chatbot yang menjawab harga, FAQ, dan booking, lalu handoff ke WhatsApp admin dengan pesan yang sudah terisi'),
    ('Mau booking di cabang mana?” — menjawab harga langsung, lalu mengantar ke booking.',
     'Mau booking di cabang mana?” Chatbot menjawab harga langsung, lalu mengantar ke booking.'),
    ('<b>UMKM lainnya</b> — semua yang butuh pelanggan baru dari internet.',
     '<b>UMKM lainnya</b>. Semua yang butuh pelanggan baru dari internet.'),
    ('Website dibangun dari data bisnis Anda — teks dan harga yang Anda konfirmasi, bukan karangan.',
     'Website dibangun dari data bisnis Anda. Teks dan harga yang Anda konfirmasi, bukan karangan.'),
    ('Website live dan mulai bekerja — menangkap pengunjung dan mengantar mereka menghubungi Anda.',
     'Website live dan mulai bekerja. Menangkap pengunjung dan mengantar mereka menghubungi Anda.'),
    ('Chatbot dibangun dari data bisnis Anda — hanya menjawab dari yang Anda konfirmasi, tidak mengarang.',
     'Chatbot dibangun dari data bisnis Anda. Hanya menjawab dari yang Anda konfirmasi, tidak mengarang.'),
    ('Chatbot live 24/7 — menjawab, mengantar booking, dan menyerahkan ke admin Anda saat dibutuhkan.',
     'Chatbot live 24/7. Menjawab, mengantar booking, dan menyerahkan ke admin Anda saat dibutuhkan.'),
    ('Website dan chatbot dibangun dari data bisnis Anda — harga dan FAQ yang Anda konfirmasi, bukan karangan.',
     'Website dan chatbot dibangun dari data bisnis Anda. Harga dan FAQ yang Anda konfirmasi, bukan karangan.'),
    ('Website live, chatbot melayani pengunjung 24/7 — menjawab, mengantar booking, dan menyerahkan ke admin Anda.',
     'Website live, chatbot melayani pengunjung 24/7. Menjawab, mengantar booking, dan menyerahkan ke admin Anda.'),
    ('Ya — setiap paket termasuk jatah revisi (2x, 3x, atau 5x sesuai tier).',
     'Ya. Setiap paket termasuk jatah revisi (2x, 3x, atau 5x sesuai tier).'),
    ('Ya — SEO dasar termasuk: struktur heading, meta, kecepatan, dan Google Maps.',
     'Ya. SEO dasar termasuk struktur heading, meta, kecepatan, dan Google Maps.'),
    ('Bisa — naik tier atau tambah halaman custom kapan saja.',
     'Bisa. Naik tier atau tambah halaman custom kapan saja.'),
    ('Tidak — chatbot hanya menjawab dari data bisnis yang Anda konfirmasi',
     'Tidak. Chatbot hanya menjawab dari data bisnis yang Anda konfirmasi'),
    ('Untuk chatbot di WhatsApp, ya — kami bantu setup-nya.',
     'Untuk chatbot di WhatsApp, ya. Kami bantu setup-nya.'),
    ('Bisa — pembaruan konten (harga baru, FAQ baru) termasuk dalam retainer.',
     'Bisa. Pembaruan konten (harga baru, FAQ baru) termasuk dalam retainer.'),
    ('Ceritakan Bisnis Anda — Konsultasi Gratis',
     'Konsultasi Gratis: Ceritakan Bisnis Anda'),
    ('<h2>Ceritakan bisnis Anda — konsultasi gratis.</h2>',
     '<h2>Ceritakan bisnis Anda. Konsultasi gratis.</h2>'),
    ('https://t.me/HermesMuseChat_bot', 'https://wa.me/628811722942'),
    ('Telegram — @HermesMuseChat_bot', 'Hubungi Kami'),
    ('Chat via Telegram', 'Chat via WhatsApp'),
    ('via Telegram', 'via WhatsApp'),
    ('mengantar pengunjung ke booking — siang dan malam, tanpa admin.',
     'mengantar pengunjung ke booking. Siang dan malam, tanpa admin.'),
    ('Chatbot WhatsApp dan website untuk bisnis Indonesia — menjawab harga, FAQ, dan mengantar pelanggan',
     'Chatbot WhatsApp dan website untuk bisnis Indonesia. Menjawab harga, FAQ, dan mengantar pelanggan'),
    ('ditagih sesuai pemakaian</b> — supaya kami tidak menombok saat chat Anda ramai.',
     'ditagih sesuai pemakaian</b>, supaya kami tidak menombok saat chat Anda ramai.'),
    ('Untuk chatbot yang melayani di WhatsApp, ya — kami bantu setup-nya.',
     'Untuk chatbot yang melayani di WhatsApp, ya. Kami bantu setup-nya.'),
    (' — AI Digital Agency</title>', ' · AI Digital Agency</title>'),
    ('<h3>NK Health — Klinik Gigi Jakarta Barat</h3>', '<h3>NK Health: Klinik Gigi Jakarta Barat</h3>'),
    ('lalu mengantar mereka ke booking — siang dan malam.</p>',
     'lalu mengantar mereka ke booking. Siang dan malam.</p>'),
    ('Hanya menjawab dari data bisnis Anda — tidak mengarang',
     'Hanya menjawab dari data bisnis Anda, tidak mengarang'),
    ('Atau mau sekalian paket lengkap — website yang dilayani chatbot 24/7?',
     'Atau mau sekalian paket lengkap: website yang dilayani chatbot 24/7?'),
    ('Mulai dari yang paling sesuai — naik tier kapan saja.',
     'Mulai dari yang paling sesuai. Naik tier kapan saja.'),
]

for name, v in VARIANTS.items():
    h = base
    # head
    h = h.replace(
        "<title>AI Digital Agency — Website & Chatbot untuk UMKM Indonesia</title>",
        "<title>%s</title>" % htmlmod.escape(v["title"]))
    h = h.replace(
        '<meta name="description" content="AI Digital Agency membangun website dan chatbot untuk klinik, kuliner, jasa, dan UMKM Indonesia. Website yang bekerja: menangkap pengunjung, menjawab harga, dan menutup booking.">',
        '<meta name="description" content="%s">' % htmlmod.escape(v["meta"]))
    # hero
    h = h.replace(
        '<h1 class="hero-entrance">Website yang <span class="it">bekerja,</span><br>bukan sekadar dipajang.</h1>',
        '<h1 class="hero-entrance">%s</h1>' % v["hero_h1"])
    h = h.replace(
        '<p class="sub hero-entrance d1">Kami membangun website dan chatbot untuk klinik, kuliner, jasa, dan UMKM Indonesia. Website menangkap pengunjung, chatbot menjawab harga dan menutup booking — 24 jam, tanpa henti.</p>',
        '<p class="sub hero-entrance d1">%s</p>' % v["hero_sub"])
    h = h.replace(
        '<p class="hero-meta hero-entrance d3"><b>2 produk · 6 paket · mulai Rp2,5 jt.</b></p>',
        '<p class="hero-meta hero-entrance d3">%s</p>' % v["hero_meta"])
    # sections
    pre, h = cut(h, '<section id="layanan">', '<section id="paket">')
    h = pre + layanan_section(v["cards"], v["layanan_h2"]) + "\n\n" + h
    pre, h = cut(h, '<section id="paket">', '<section id="portofolio">')
    h = pre + paket_section(v["paket_h2"], v["paket_lead"], v["tiers"], v["paket_note"]) + "\n\n" + h
    pre, h = cut(h, '<section id="cara">', '<section id="faq">')
    h = pre + steps_html(v["steps"]) + "\n\n" + h
    pre, h = cut(h, '<section id="faq">', '<section style="padding-top:0">')
    h = pre + faq_html(v["faq"]) + "\n\n" + h
    # closing
    h = h.replace(
        "<h2>Ceritakan bisnis Anda — konsultasi gratis.</h2>",
        "<h2>%s</h2>" % v["closing_h2"])
    h = h.replace(
        "<p>Tidak ada kewajiban. Ceritakan saja bisnis Anda, kami tunjukkan seperti apa website dan chatbot-nya sebelum Anda memutuskan.</p>",
        "<p>%s</p>" % v["closing_p"])
    # footer
    h = h.replace(
        "<b>AI Digital Agency</b><br>Website &amp; chatbot untuk UMKM Indonesia.",
        "<b>AI Digital Agency</b><br>%s" % v["footer"])
    # script
    pre, h = cut(h, "<script>", "</script>")
    h = pre + tiers_js(v["tiers"]) + h[len("</script>"):]
    # cross-sell popup (kecuali situs gabungan — sudah tier tertinggi)
    pop = POPUPS[name]
    if pop:
        h = h.replace("</style>", POPUP_CSS + "\n</style>", 1)
        h = h.replace("</body>", pop + "\n" + POPUP_JS + "\n</body>", 1)
        assert 'id="xsell"' in h and "xsell_seen_v1" in h, name
    # anti-slop copy
    for old, new in DESLOP:
        h = h.replace(old, new)
    assert "bukan sekadar" not in h, name
    # layout fix desktop (semua varian)
    h = h.replace("</style>", LAYOUT_FIX_CSS + "\n</style>", 1)
    # sanity: no leftover toggle
    assert "showPkg" not in h, name
    assert '<div class="toggle"' not in h, name
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(h)
    print(name, len(h), "bytes OK")
