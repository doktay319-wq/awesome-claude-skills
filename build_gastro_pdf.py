from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV", boldItalic="DV-B")

BLUE = "#1a5fb4"
H1 = ParagraphStyle("h1", fontName="DV-B", fontSize=14, leading=18, spaceBefore=6, spaceAfter=6, textColor=colors.HexColor("#111111"))
H2 = ParagraphStyle("h2", fontName="DV-B", fontSize=11, leading=14, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("b", fontName="DV", fontSize=8.8, leading=12, spaceAfter=3.5)
CELL = ParagraphStyle("c", parent=BODY, fontSize=8, leading=10.5, spaceAfter=0)
NOTE = ParagraphStyle("n", parent=BODY, fontSize=8, textColor=colors.grey)


def tr(t):
    return f'<font color="{BLUE}">({t})</font>'


def esc(s):
    return s


story = []


def h1(nl, tk):
    story.append(Paragraph(f"{nl} {tr(tk)}", H1))


def h2(nl, tk):
    story.append(Paragraph(f"{nl} {tr(tk)}", H2))


def p(nl, tk):
    story.append(Paragraph(f"{nl} {tr(tk)}", BODY))


def bullets(items):
    for nl, tk in items:
        story.append(Paragraph(f"• {nl} {tr(tk)}", BODY))


def numbered(items, start=1):
    for i, (nl, tk) in enumerate(items, start):
        story.append(Paragraph(f"{i}. {nl} {tr(tk)}", BODY))


def table(header, rows, widths):
    data = [[Paragraph(f"<b>{h[0]}</b><br/>{tr(h[1])}", CELL) for h in header]]
    for r in rows:
        data.append([Paragraph(f"{nl}<br/>{tr(tk)}", CELL) for nl, tk in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6dede")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))


# ---------------------------------------------------------------- 3
h1("3. ENTERALE VOEDING", "3. ENTERAL BESLENME")
h2("3.1 Definitie", "3.1 Tanım")
p("Volwaardige speciale vloeibare voeding die de dagelijkse voedingsstoffen en vocht levert, aangepast aan de toestand van de zorgvrager.",
  "Günlük besin öğelerini ve sıvıyı sağlayan, bakım alanın durumuna uyarlanmış, tam değerli özel sıvı beslenme.")
p("Via katheter in maag of verder in het maagdarmstelsel; kan ook als bijvoeding.",
  "Kateter yoluyla mideye veya sindirim sisteminin daha ilerisine verilir; ek beslenme olarak da kullanılabilir.")
p("Wordt voorgeschreven door arts/diëtiste.", "Doktor/diyetisyen tarafından reçete edilir.")
p("Voordelen tegenover parenterale voeding: veiliger, eenvoudiger, meer fysiologisch en minder duur.",
  "Parenteral beslenmeye göre avantajları: daha güvenli, daha basit, daha fizyolojik ve daha ucuz.")

h2("3.2 Indicaties", "3.2 Endikasyonlar")
bullets([
    ("Niet of onvoldoende kunnen eten/drinken door kauw- of slikproblemen: ernstige mondslijmvliesontsteking, slokdarmaandoeningen, verlammingen, bewusteloosheid/ernstige zwakte.",
     "Çiğneme veya yutma sorunları nedeniyle hiç ya da yeterince yiyip içememek: ağır ağız mukozası iltihabı, yemek borusu hastalıkları, felçler, bilinçsizlik/ağır halsizlik."),
    ("Niet mogen eten/drinken door medische behandeling, bijvoorbeeld slokdarm-/maagaandoeningen of hoofd-halsoperaties.",
     "Tıbbi tedavi nedeniyle yiyip içmenin yasak olması, örneğin yemek borusu/mide hastalıkları veya baş-boyun ameliyatları."),
    ("Verminderde eetlust, bijvoorbeeld bij ernstige depressiviteit, anorexia nervosa, bestraling of chemotherapie.",
     "İştahın azalması, örneğin ağır depresyon, anoreksiya nervoza, radyoterapi veya kemoterapi durumunda."),
])

h2("3.3 Doorspoelen", "3.3 Kateteri yıkama")
bullets([
    ("<b>Doel:</b> verstopping en verzuring van achtergebleven voeding/medicatie voorkomen en zorgen dat de volledige dosis voeding/medicatie wordt toegediend.",
     "<b>Amaç:</b> kalan besin/ilacın tıkanmasını ve ekşimesini önlemek ve besin/ilacın tam dozunun verilmesini sağlamak."),
    ("<b>Wanneer:</b> druppelvoeding 3–4×/dag; portievoeding vóór en na iedere portie; vóór en na medicatie; vóór en na wisselen van voedingsfles; ongebruikte katheter 1×/dag.",
     "<b>Ne zaman:</b> damla beslenmede günde 3–4 kez; porsiyon beslenmede her porsiyondan önce ve sonra; ilaçtan önce ve sonra; besin şişesi değiştirilirken önce ve sonra; kullanılmayan kateter günde 1 kez."),
    ("<b>Materiaal:</b> 50 ml-spuit met handwarm, niet-bruisend drinkwater.",
     "<b>Malzeme:</b> ılık, gazsız içme suyu dolu 50 ml'lik enjektör."),
    ("<b>Hoeveelheid:</b> 20–40 ml voor volledig doorspoelen; bij meerdere spoelingen vlak na elkaar max. 2–5 ml om overvulling te voorkomen.",
     "<b>Miktar:</b> tam yıkama için 20–40 ml; art arda birden fazla yıkamada aşırı dolmayı önlemek için en fazla 2–5 ml."),
])

h2("Bij verstopping", "Tıkanma durumunda")
numbered([
    ("Gebruik water op kamertemperatuur in een halfvolle spuit en maak pompende bewegingen.",
     "Oda sıcaklığında suyu yarı dolu enjektörde kullan ve pompalama hareketleri yap."),
    ("Kneed het uitwendige deel van de katheter.", "Kateterin dışarıdaki kısmını yoğur (masaj yap)."),
    ("Gebruik <b>nooit bruisende/koolzuurhoudende drank</b> om een verstopping te verhelpen.",
     "Tıkanıklığı gidermek için <b>asla gazlı/karbondioksitli içecek</b> kullanma."),
    ("Eventueel kan volgens de cursus een opgeloste natriumbicarbonaatoplossing worden gebruikt.",
     "Gerekirse kursa göre çözülmüş sodyum bikarbonat çözeltisi kullanılabilir."),
    ("Als de verstopping niet opgelost raakt: arts contacteren; katheter kan vervangen moeten worden.",
     "Tıkanıklık çözülmezse: doktora başvur; kateterin değiştirilmesi gerekebilir."),
])

h2("3.4 Toedieningsvormen en snelheid", "3.4 Uygulama şekilleri ve hız")
table([("Vorm", "Şekil"), ("Betekenis", "Anlamı"), ("Cursuswaarden", "Kurs değerleri")], [
    [("<b>Bolus</b>", "Bolus"), ("Portie in één keer via spuit/hevel", "Porsiyonun enjektör/huni ile tek seferde verilmesi"), ("250–350 ml per portie, 4–6×/dag", "porsiyon başına 250–350 ml, günde 4–6 kez")],
    [("<b>Intermittent</b>", "Aralıklı"), ("Dripsysteem, meerdere toedieningen", "Damla sistemi, birden fazla uygulama"), ("2–6 uur per voeding", "beslenme başına 2–6 saat")],
    [("<b>Continu</b>", "Sürekli"), ("Langer durende toediening", "Daha uzun süren uygulama"), ("12–24 uur volgens voorschrift", "reçeteye göre 12–24 saat")],
], [3.8 * cm, 6.5 * cm, 6.5 * cm])
p("Ideale inloopsnelheid volgens cursus: 125 ml/u, maximum 200 ml/u. Bij een dripsysteem wordt handmatig gerekend met 20 druppels = 1 ml; tel 15 seconden en vermenigvuldig ×4. Een voedingspomp regelt ml/u.",
  "Kursa göre ideal akış hızı: 125 ml/saat, en fazla 200 ml/saat. Damla sisteminde elle hesaplanır: 20 damla = 1 ml; 15 saniye say ve ×4 ile çarp. Beslenme pompası ml/saat'i ayarlar.")

h2("3.5 Eerste enterale voeding", "3.5 İlk enteral beslenme")
bullets([
    ("Via nasogastrische katheter: in de eerste 24 uur kunnen kleine hoeveelheden water en/of medicatie worden gegeven.",
     "Nazogastrik kateter yoluyla: ilk 24 saatte az miktarda su ve/veya ilaç verilebilir."),
    ("Voedingsstoma: eerst 24 uur laten vormen; enterale voeding start na 24 uur. Te vroeg vullen kan lekkage/peritonitis veroorzaken.",
     "Beslenme stoması: önce 24 saat oluşmaya bırakılır; enteral beslenme 24 saat sonra başlar. Çok erken doldurmak sızıntıya/peritonite yol açabilir."),
    ("Start voeding volgens opklimschema: volume en concentratie stapsgewijs verhogen.",
     "Beslenmeye artırma şemasına göre başla: hacim ve konsantrasyonu adım adım artır."),
    ("Laatste voeding niet vlak voor slapen om reflux/aspiratie te beperken.",
     "Reflü/aspirasyonu azaltmak için son beslenmeyi uykudan hemen önce verme."),
])

h2("3.6 Algemene aandachtspunten", "3.6 Genel dikkat noktaları")
bullets([
    ("Controleer voorschrift: soort voeding, hoeveelheid, duur, aantal voedingen per 24 uur en timing.",
     "Reçeteyi kontrol et: besin türü, miktar, süre, 24 saatteki besleme sayısı ve zamanlama."),
    ("Water en voeding op kamertemperatuur.", "Su ve besin oda sıcaklığında olmalı."),
    ("Te warme vloeistof kan weefselbeschadiging geven; te koude voeding kan hoestprikkel en maagkrampen veroorzaken.",
     "Çok sıcak sıvı doku hasarına yol açabilir; çok soğuk besin öksürük refleksine ve mide kramplarına neden olabilir."),
    ("Werk hygiënisch; controleer vervaldatum.", "Hijyenik çalış; son kullanma tarihini kontrol et."),
    ("Trousse en Janet-spuit dagelijks vervangen volgens cursus.", "Kursa göre set (trousse) ve Janet enjektörünü her gün değiştir."),
    ("Geopende voeding: maximaal 24 uur op kamertemperatuur; in koelkast maximaal 24 uur, volgens het schema in de cursus.",
     "Açılmış besin: oda sıcaklığında en fazla 24 saat; buzdolabında en fazla 24 saat, kurstaki şemaya göre."),
    ("Observeer de zorgvrager en pas voeding/schema enkel aan in overleg met arts/diëtiste.",
     "Bakım alanı gözlemle; besini/şemayı yalnızca doktor/diyetisyenle görüşerek değiştir."),
])

# ---------------------------------------------------------------- 4
story.append(PageBreak())
h1("4. PROBLEMEN BIJ ENTERALE VOEDING", "4. ENTERAL BESLENMEDE SORUNLAR")


def problem(title_nl, title_tk, cause_nl, cause_tk, sol_nl, sol_tk):
    h2(title_nl, title_tk)
    p(f"<b>Oorzaak/signalen:</b> {cause_nl}", f"<b>Neden/belirtiler:</b> {cause_tk}")
    p(f"<b>Voorkomen/oplossing:</b> {sol_nl}", f"<b>Önleme/çözüm:</b> {sol_tk}")


problem("Verstopte katheter", "Tıkanmış kateter",
        "Niet regelmatig spoelen, te dunne katheter, visceuze voeding, medicatieresten.",
        "Düzenli yıkanmaması, çok ince kateter, kıvamlı (viskoz) besin, ilaç artıkları.",
        "Voor/na voeding en voor/tussen/na medicatie spoelen; techniek correct. Bij verstopping: pompende bewegingen, kneden, water; geen bruiswater; arts indien niet opgelost. (Vloeibare medicatie waar mogelijk.)",
        "Beslenmeden önce/sonra ve ilaçtan önce/arasında/sonra yıka; teknik doğru olsun. Tıkanmada: pompalama hareketleri, yoğurma, su; gazlı su yok; çözülmezse doktora bildir. (Mümkünse sıvı ilaç kullan.)")
problem("Diarree", "İshal",
        "Te koude voeding, te grote portie, te snelle toediening, medicatie, hygiëne, te lang gebruikt systeem, pathologie of onaangepaste voeding.",
        "Çok soğuk besin, çok büyük porsiyon, çok hızlı uygulama, ilaçlar, hijyen, çok uzun süre kullanılan sistem, hastalık veya uygun olmayan besin.",
        "Hygiënisch werken, kleinere/verdeelde porties, niet te snel; systeem om 24u vervangen. Voeding trager/continu, arts verwittigen; vezelrijke of lactosearme voeding na overleg.",
        "Hijyenik çalış, daha küçük/bölünmüş porsiyonlar, çok hızlı olmasın; sistemi 24 saatte bir değiştir. Beslenmeyi yavaşlat/sürekli yap, doktora haber ver; görüşme sonrası lifli veya laktozsuz besin.")
problem("Nausea/braken", "Bulantı/kusma",
        "Te grote portie, te snelle voeding, medicatie, vertraagde maaglediging, obstructie, verkeerde katheterligging of onaangepaste voeding.",
        "Çok büyük porsiyon, çok hızlı besleme, ilaçlar, gecikmiş mide boşalması, tıkanıklık, kateterin yanlış yerleşimi veya uygun olmayan besin.",
        "Kleinere porties; beginsnelheid 25–50 ml/u; observeren. Bij braken voeding stoppen maar wel doorspoelen; trager zetten en arts verwittigen.",
        "Daha küçük porsiyonlar; başlangıç hızı 25–50 ml/saat; gözlemle. Kusmada beslenmeyi durdur ama kateteri yine de yıka; hızı yavaşlat ve doktora haber ver.")
problem("Aspiratie", "Aspirasyon",
        "Verplaatste/verkeerd geplaatste katheter, verkeerde houding, reflux of onvoldoende maaglediging.",
        "Yer değiştirmiş/yanlış yerleştirilmiş kateter, yanlış pozisyon, reflü veya yetersiz mide boşalması.",
        "Juist afmeten en controleren, goed fixeren, halfzittende houding, residu bepalen, nauwkeurig observeren. Bij aspiratie: houding aanpassen, voeding onmiddellijk stoppen, arts verwittigen.",
        "Doğru ölç ve kontrol et, iyi sabitle, yarı oturur pozisyon, rezidüyü belirle, dikkatle gözlemle. Aspirasyonda: pozisyonu ayarla, beslenmeyi hemen durdur, doktora haber ver.")
problem("Maagretentie", "Mide retansiyonu (mide içeriğinin birikmesi)",
        "Verminderde maag-/darmmotiliteit, te grote portie of te snelle toediening.",
        "Azalmış mide/bağırsak hareketliliği, çok büyük porsiyon veya çok hızlı uygulama.",
        "Voor elke toediening residu bepalen; kleinere porties; niet te snel; bij voorkeur pomp. Bij >100–150 ml residu 4 uur na voeding: voeding trager/stop, arts, aangepast schema; eventueel postpylore katheter volgens arts.",
        "Her uygulamadan önce rezidüyü belirle; daha küçük porsiyonlar; çok hızlı olmasın; tercihen pompa. Beslenmeden 4 saat sonra >100–150 ml rezidüde: beslenmeyi yavaşlat/durdur, doktora bildir, uyarlanmış şema; gerekirse doktora göre postpilorik kateter.")
problem("Gewichtsverandering", "Kilo değişimi",
        "Te weinig/te veel voeding, pathologie, braken/diarree, onaangepaste voeding.",
        "Çok az/çok fazla besin, hastalık, kusma/ishal, uygun olmayan besin.",
        "Gewicht opvolgen, juiste berekening/toediening, welzijn bevragen; overleg arts/diëtiste en voeding aanpassen.",
        "Kiloyu takip et, doğru hesaplama/uygulama, iyilik halini sor; doktor/diyetisyenle görüş ve besini ayarla.")
problem("Obstipatie", "Kabızlık",
        "Te weinig vocht/vezels, medicatie, pathologie, weinig drinken/beweging.",
        "Az sıvı/lif, ilaçlar, hastalık, az içme/hareket.",
        "Voldoende vocht, vezels, beweging; in overleg met arts laxativa en extra vocht/vezels.",
        "Yeterli sıvı, lif, hareket; doktorla görüşerek laksatif ve ek sıvı/lif.")
problem("Uitdroging", "Dehidrasyon (susuzluk)",
        "Te weinig vocht, koorts, diarree, braken, warme omgeving of groot verlies.",
        "Az sıvı, ateş, ishal, kusma, sıcak ortam veya büyük sıvı kaybı.",
        "Voldoende vocht en vochtbalans controleren; extra vocht alleen volgens overleg/voorschrift.",
        "Yeterli sıvı ve sıvı dengesini kontrol et; ek sıvıyı yalnızca görüşme/reçeteye göre ver.")
problem("Huidirritatie", "Cilt tahrişi",
        "Druk, slechte/te strakke fixatie, pleisterallergie, infectie, wild vlees.",
        "Baskı, kötü/çok sıkı sabitleme, flaster alerjisi, enfeksiyon, granülasyon dokusu (yabani et).",
        "Dagelijks controleren/verzorgen; niet te strak fixeren; NGS afwisselend neusgat; splitkompres bij PEG/PEG-J. Reinigen, anders fixeren, arts bij problemen.",
        "Her gün kontrol et/bakım yap; çok sıkı sabitleme; NGS (nazogastrik sonda) dönüşümlü burun deliğinde; PEG/PEG-J'de yarık kompres. Temizle, farklı sabitle, sorun varsa doktora başvur.")
problem("Katheter niet juiste plaats", "Kateter doğru yerde değil",
        "Hoesten, trekken, slechte fixatie, ballon defect; katheter verschoven/uitgevallen.",
        "Öksürme, çekilme, kötü sabitleme, balon arızası; kateter kaymış/düşmüş.",
        "Goed fixeren en markeren. Plaats controleren met geschikte middelen; waterproef alleen om luchtweg uit te sluiten, niet om juiste maagpositie te bewijzen. PEG zo snel mogelijk opnieuw plaatsen om sluiten fistel te voorkomen.",
        "İyi sabitle ve işaretle. Yerini uygun yöntemlerle kontrol et; su testi yalnızca hava yolunda olmadığını dışlamak içindir, midede doğru konumu kanıtlamak için değil. Fistülün kapanmasını önlemek için PEG'i mümkün olan en kısa sürede yeniden yerleştir.")
problem("Losgekomen voedingskatheter", "Ayrılmış beslenme kateteri",
        "Connectie verbroken, vettige/verkeerde connector, defect aanzetstuk of onvoldoende aansluiting.",
        "Bağlantının kopması, yağlı/yanlış konnektör, arızalı bağlantı ucu veya yetersiz bağlantı.",
        "Connector reinigen, juiste materialen gebruiken, zorgvuldig aansluiten; verlies aan voeding registreren.",
        "Konnektörü temizle, doğru malzemeleri kullan, dikkatlice bağla; kaybolan besini kaydet.")
problem("Lekkage fistel", "Fistül sızıntısı",
        "Fixatieplaat verkeerd, te grote fistel, ballon onvoldoende gevuld.",
        "Fiksasyon plakası yanlış, fistül çok geniş, balon yeterince doldurulmamış.",
        "Fixatiedisk op juiste plaats, 2 mm tussen huid en plaat, ballon correct vullen, huid droog houden; arts indien nodig.",
        "Fiksasyon diskini doğru yere yerleştir, cilt ile plaka arasında 2 mm, balonu doğru doldur, cildi kuru tut; gerekirse doktora başvur.")
problem("PEG kan niet meer draaien", "PEG artık dönmüyor",
        "Maagmucosa vastgegroeid of katheter kleeft aan wand.",
        "Mide mukozası yapışmış veya kateter duvara yapışmış.",
        "PEG vanaf gevormde stoma minstens 1×/24u 180–360° draaien; <b>PEG-J nooit draaien</b>. Als draaien niet lukt: onmiddellijk arts.",
        "PEG'i oluşmuş stomadan itibaren en az günde 1 kez 180–360° çevir; <b>PEG-J'yi asla çevirme</b>. Çevrilemezse: hemen doktora haber ver.")
p("Tijdens de eerste 10 dagen blijft de sonde ter plaatse om de fistel te laten vormen. Het afsluitplaatje blijft strak tegen de huid volgens de postoperatieve stappenlijst. Eerste 10 dagen niet draaien en niet douchen/baden volgens de cursus. Dagelijks observeren op roodheid, drukletsel, verweking en irritatie.",
  "İlk 10 gün boyunca fistülün oluşması için sonda yerinde kalır. Kapatma plakası, ameliyat sonrası adım listesine göre cilde sıkıca temas eder. Kursa göre ilk 10 gün çevirme ve duş/banyo yapma. Her gün kızarıklık, basınç yarası, yumuşama (maserasyon) ve tahriş yönünden gözlemle.")

# ---------------------------------------------------------------- 5
story.append(PageBreak())
h1("5. VOEDINGSSTOMA: VERZORGING EN KATHETERWISSEL", "5. BESLENME STOMASI: BAKIM VE KATETER DEĞİŞİMİ")
p("<b>Eerste 10 dagen / zolang vochtafscheiding: steriele verzorging.</b>",
  "İlk 10 gün / sıvı akıntısı olduğu sürece: steril bakım.")
h2("Na fistelvorming (>10 dagen)", "Fistül oluştuktan sonra (>10 gün)")
numbered([
    ("Handhygiëne en materiaal voorbereiden.", "El hijyeni yap ve malzemeyi hazırla."),
    ("Bed op goede werkhoogte; abdomen vrijmaken.", "Yatağı uygun çalışma yüksekliğine getir; karnı aç."),
    ("Handschoenen aantrekken.", "Eldiven giy."),
    ("Plaats extern fixatieplaatje markeren.", "Dış fiksasyon plakasının yerini işaretle."),
    ("Fixatieplaatje losmaken en splitkompres verwijderen indien aanwezig.", "Fiksasyon plakasını gevşet ve varsa yarık kompresi çıkar."),
    ("Huid van binnen naar buiten reinigen.", "Cildi içten dışa doğru temizle."),
    ("Fixatieplaatje reinigen.", "Fiksasyon plakasını temizle."),
    ("Huid en plaatje drogen.", "Cildi ve plakayı kurula."),
    ("PEG/gastrostomie ballonkatheter volgens de cursus voorzichtig 3–4 cm dompelen en 180–360° draaien. <b>PEG-J niet draaien.</b>",
     "PEG/gastrostomi balonlu kateterini kursa göre dikkatlice 3–4 cm içeri it ve 180–360° çevir. <b>PEG-J'yi çevirme.</b>"),
    ("Zo nodig katheter reinigen; splitkompres bij vochtige huid.", "Gerekirse kateteri temizle; cilt nemliyse yarık kompres kullan."),
    ("Fixatieplaatje op gemarkeerde plaats sluiten.", "Fiksasyon plakasını işaretlenen yerde kapat."),
    ("Katheter met 20 ml lauw water spoelen.", "Kateteri 20 ml ılık suyla yıka."),
    ("Handschoenen uit, handhygiëne, opruimen en rapporteren.", "Eldivenleri çıkar, el hijyeni, toparla ve raporla."),
])

h2("Gastrostomie ballonkatheter vervangen", "Gastrostomi balonlu kateterin değiştirilmesi")
numbered([
    ("Controleer balloninhoud, Charrière en vorige inbrengdiepte.", "Balon hacmini, Charrière (çap) ve önceki yerleştirme derinliğini kontrol et."),
    ("Verzamel juiste nieuwe katheter, extern fixatieplaatje, afsluitdop, spuiten, steriel water, water, kompressen, glijmiddel enz.",
     "Doğru yeni kateteri, dış fiksasyon plakasını, kapatma kapağını, enjektörleri, steril suyu, suyu, kompresleri, kayganlaştırıcıyı vb. topla."),
    ("Comfortabele houding; handhygiëne en handschoenen.", "Rahat pozisyon; el hijyeni ve eldiven."),
    ("Stoma en katheter reinigen.", "Stomayı ve kateteri temizle."),
    ("Bestaande ballon met spuit ledigen.", "Mevcut balonu enjektörle boşalt."),
    ("Katheter verwijderen en huid naast de stoma ondersteunen; diepte observeren.", "Kateteri çıkar ve stomanın yanındaki cildi destekle; derinliği gözlemle."),
    ("Stoma indien nodig opnieuw reinigen; handhygiëne.", "Gerekirse stomayı tekrar temizle; el hijyeni."),
    ("Nieuwe katheter uit verpakking nemen.", "Yeni kateteri ambalajından çıkar."),
    ("Ballon controleren met water; ballon moet mooi rond en volledig rond de katheter zijn. Water weer terugtrekken.",
     "Balonu suyla kontrol et; balon düzgün yuvarlak olmalı ve kateteri tamamen çevrelemeli. Suyu tekrar çek."),
    ("Tip met glijmiddel bevochtigen.", "Ucu kayganlaştırıcıyla nemlendir."),
    ("Nieuwe katheter inbrengen tot vorige diepte + 2 cm, minstens 7 cm.", "Yeni kateteri önceki derinlik + 2 cm, en az 7 cm olacak şekilde yerleştir."),
    ("Fixatieballon vullen met juiste hoeveelheid water.", "Fiksasyon balonunu doğru miktarda suyla doldur."),
    ("Katheter terugtrekken tot weerstand.", "Direnç hissedene kadar kateteri geri çek."),
    ("Extern fixatieplaatje op ongeveer 2 mm van huid plaatsen.", "Dış fiksasyon plakasını cilde yaklaşık 2 mm mesafede yerleştir."),
    ("Afsluitdop plaatsen, overtollig glijmiddel verwijderen en katheter spoelen.", "Kapatma kapağını tak, fazla kayganlaştırıcıyı temizle ve kateteri yıka."),
    ("Rapporteer gebruikte katheter, Charrière en balloninhoud.", "Kullanılan kateteri, Charrière (çap) ve balon hacmini raporla."),
])

h2("Verwijderen PEG/ballonkatheter", "PEG/balonlu kateterin çıkarılması")
p("<b>Accidenteel:</b> binnen de eerste 10 dagen is dit urgent; arts moet onmiddellijk handelen. Na 10 dagen zo snel mogelijk een vervangkatheter in de fistel plaatsen omdat de stoma al na 4–6 uur kan sluiten. Volgens de cursus kan een Foley als tijdelijke oplossing worden gebruikt wanneer geen gastrostomie-ballonkatheter beschikbaar is.",
  "<b>Kazara:</b> ilk 10 gün içinde bu acildir; doktor hemen müdahale etmelidir. 10 günden sonra, stoma 4–6 saat içinde kapanabileceği için mümkün olan en kısa sürede fistüle yedek kateter yerleştirilmelidir. Kursa göre gastrostomi balonlu kateter yoksa geçici çözüm olarak Foley kullanılabilir.")
p("<b>Geplande verwijdering</b> van een endoscopisch geplaatste katheter gebeurt door de arts; bij een ballonkatheter wordt de katheter verwijderd en het stomagaatje dichtgekleefd met Steristrips. Lekkage opvolgen en rapporteren.",
  "<b>Planlı çıkarma:</b> endoskopik olarak yerleştirilmiş kateter doktor tarafından çıkarılır; balonlu kateterde kateter çıkarılır ve stoma deliği Steristrip ile kapatılır. Sızıntıyı izle ve raporla.")

# ---------------------------------------------------------------- 6
story.append(PageBreak())
h1("6. MEDICATIE VIA DE GASTRO-ENTERALE KATHETER", "6. GASTRO-ENTERAL KATETER YOLUYLA İLAÇ VERİLMESİ")
p("Medicatie via de katheter is verantwoord wanneer de zorgvrager door slikproblemen en/of de katheter niet goed oraal kan innemen. Oraal innemen zo lang mogelijk behouden.",
  "Bakım alan kişi yutma sorunları nedeniyle ilacı ağızdan iyi alamıyorsa ve/veya kateter varsa, ilacın kateter yoluyla verilmesi uygundur. Ağızdan alımı mümkün olduğunca uzun süre koru.")
p("<b>Niet alle medicatie mag worden geplet.</b> Controleer arts/apotheker en de cursuswebsite pletmedicatie.be. Indien mogelijk kan de arts een andere vorm voorschrijven, zoals siroop, poeder, drank of zetpil.",
  "<b>Tüm ilaçlar ezilemez.</b> Doktoru/eczacıyı ve kurs web sitesi pletmedicatie.be'yi kontrol et. Mümkünse doktor şurup, toz, içecek veya fitil gibi başka bir form yazabilir.")
p("Medicatie pletten = het geneesmiddel van vorm veranderen zodat het in water opgelost en via de enterale katheter toegediend kan worden. Het moet zo fijn mogelijk worden gemalen.",
  "İlaç ezme = ilacın şeklini değiştirerek suda çözünmesini ve enteral kateter yoluyla verilebilmesini sağlamak. Mümkün olduğunca ince öğütülmelidir.")
p("Niet pletten bij gereguleerde afgifte, bijvoorbeeld Retard, Contin of SR: pletten kan de vertraagde afgifte verbreken en een overdosis veroorzaken. Maagsapresistente/enteric-coated medicatie (E.C./MSR) niet pletten omdat de bescherming tegen maagzuur/maagwand verloren gaat; de cursus vermeldt als uitzondering dat dit bij toediening via een jejunumkatheter wel kan.",
  "Kontrollü salınımlı ilaçlar (ör. Retard, Contin veya SR) ezilmez: ezmek gecikmeli salınımı bozup aşırı doza neden olabilir. Mide asidine dirençli/enterik kaplı ilaçlar (E.C./MSR) ezilmez, çünkü mide asidine/mide duvarına karşı koruma kaybolur; kurs, jejunum kateteri yoluyla verilirken bunun istisna olarak yapılabileceğini belirtir.")

h2("6.1 Stappenplan medicatie", "6.1 İlaç verme adım planı")
numbered([
    ("Controleer voorschrift, identiteit en juiste toedieningswijze.", "Reçeteyi, kimliği ve doğru uygulama yolunu kontrol et."),
    ("Bereid medicatie vlak vóór toediening voor.", "İlacı uygulamadan hemen önce hazırla."),
    ("Plet de tablet met pletmateriaal of open de capsule wanneer dit mag.", "Tableti ezme aracıyla ez veya izin veriliyorsa kapsülü aç."),
    ("Voeg 10–15 ml water toe en meng gelijkmatig.", "10–15 ml su ekle ve homojen karıştır."),
    ("Trek het mengsel op in een 50 ml-spuit met kathetertip en etiketteer.", "Karışımı kateter uçlu 50 ml'lik enjektöre çek ve etiketle."),
    ("Stop zo nodig de sondevoeding.", "Gerekirse sonda beslenmesini durdur."),
    ("Controleer de ligging van de katheter.", "Kateterin yerleşimini kontrol et."),
    ("Spoel de katheter met 30 ml water.", "Kateteri 30 ml suyla yıka."),
    ("Dien het geneesmiddel toe.", "İlacı ver."),
    ("Spoel indien meerdere geneesmiddelen worden gegeven tussen elk geneesmiddel met 10 ml water.", "Birden fazla ilaç veriliyorsa her ilaç arasında 10 ml suyla yıka."),
    ("Spoel na het laatste geneesmiddel met 30 ml water.", "Son ilaçtan sonra 30 ml suyla yıka."),
    ("Controleer of alle medicatieresten zijn doorgespoeld.", "Tüm ilaç artıklarının yıkandığını kontrol et."),
    ("Start sondevoeding opnieuw indien nodig; anders katheter afsluiten met dop/klem.", "Gerekirse sonda beslenmesini yeniden başlat; aksi halde kateteri kapak/klemp ile kapat."),
    ("Handschoenen uit, handhygiëne, opruimen.", "Eldivenleri çıkar, el hijyeni, toparla."),
    ("Rapporteer dat medicatie werd toegediend.", "İlacın verildiğini raporla."),
])

h2("6.2 Complicaties medicatie", "6.2 İlaç komplikasyonları")
bullets([
    ("<b>Obstructie katheter:</b> geplette medicatie kan klonteren → fijn pletten/vloeibare vorm.",
     "<b>Kateter tıkanması:</b> ezilmiş ilaç topaklanabilir → ince ez/sıvı form kullan."),
    ("<b>Steenvorming:</b> voeding + medicatie; vloeistoffen/medicatie met pH &lt;4 kunnen voeding minder vloeibaar maken → medicatie niet mengen met voeding.",
     "<b>Taşlaşma (topaklaşma):</b> besin + ilaç; pH &lt;4 olan sıvılar/ilaçlar besini daha az akışkan yapabilir → ilacı besinle karıştırma."),
    ("<b>Chemische wijziging:</b> sommige medicatie, o.a. vitaminen, kan minder werkzaam worden door contact met voeding → gescheiden toedienen.",
     "<b>Kimyasal değişim:</b> bazı ilaçlar, ör. vitaminler, besinle temas edince daha az etkili olabilir → ayrı ver."),
    ("<b>Overdosering:</b> vooral bij gereguleerde afgifte wanneer coating wordt vernietigd.",
     "<b>Aşırı doz:</b> özellikle kontrollü salınımlı ilaçlarda kaplama bozulduğunda."),
    ("<b>Onderdosering:</b> medicatieresten blijven in potje/spuit achter; enteric coating wordt vernietigd; continue voeding kan opname van nuchtere medicatie verminderen; sommige vetoplosbare stoffen kunnen door PVC worden geabsorbeerd → direct met water doorspoelen.",
     "<b>Eksik doz:</b> ilaç artıkları kapta/enjektörde kalır; enterik kaplama bozulur; sürekli beslenme aç karnına alınması gereken ilaçların emilimini azaltabilir; bazı yağda çözünen maddeler PVC tarafından emilebilir → hemen suyla yıka."),
    ("<b>Voeding:</b> medicatie kan de samenstelling van enterale voeding beïnvloeden → voeding en medicatie gescheiden houden.",
     "<b>Besin:</b> ilaç enteral besinin bileşimini etkileyebilir → besin ve ilacı ayrı tut."),
])

h2("Belangrijke aandachtspunten", "Önemli dikkat noktaları")
bullets([
    ("Controleer dosis, tijdstip, toedieningswijze, toedieningsduur en juiste zorgvrager.", "Dozu, zamanı, uygulama şeklini, uygulama süresini ve doğru bakım alanı kontrol et."),
    ("Niet alle medicatie mag geplet worden.", "Tüm ilaçlar ezilemez."),
    ("Bij pletten van antibiotica, hormo… [tekst onleesbaar op de foto]",
     "Antibiyotik, hormon vb. ezilirken… [fotoğrafta metin okunaksız]"),
    ("Controleer altijd de positionering van de katheter.", "Kateterin konumunu her zaman kontrol et."),
    ("Controleer of alle medicatieresten in de spuit zitten.", "Tüm ilaç artıklarının enjektörde olduğunu kontrol et."),
    ("Was en droog medicatiebekers en pletmateriaal grondig na gebruik.", "Kullandıktan sonra ilaç kaplarını ve ezme malzemesini iyice yıka ve kurula."),
])

# ---------------------------------------------------------------- 7 / 8
story.append(PageBreak())
h1("7. ALLES IN ÉÉN: KATHETER → BEHANDELING", "7. HEPSİ BİR ARADA: KATETER → TEDAVİ")
table([("Situatie", "Durum"), ("Katheter", "Kateter"), ("Wat doe je ermee?", "Onunla ne yaparsın?")], [
    [("Nuchtere maagkatherisatie / maagvocht onderzoeken", "Aç karnına mide kateterizasyonu / mide sıvısını inceleme"),
     ("<b>Levin 14 Ch (basis)</b>", "Levin 14 Ch (temel)"),
     ("Inbrengen, positie controleren, maagvocht aspireren; staal indien voorgeschreven.", "Yerleştir, konumu kontrol et, mide sıvısını aspire et; reçete edilmişse numune al.")],
    [("Actieve maagaspiratie", "Aktif mide aspirasyonu"), ("<b>Sump</b>", "Sump"),
     ("Aspireren met Janet/Gomco; dubbel lumen beschermt maagwand.", "Janet/Gomco ile aspire et; çift lümen mide duvarını korur.")],
    [("Passieve maagdrainage", "Pasif mide drenajı"), ("<b>Levin 16 Ch</b>", "Levin 16 Ch"),
     ("Collector lager dan maag; drainage door zwaartekracht/communicerende vaten.", "Toplama torbası midenin altında; yerçekimi/iletişimli kaplar prensibiyle drenaj.")],
    [("Maagspoeling", "Mide yıkama"), ("<b>Faucher</b>", "Faucher"),
     ("Orogastrisch; groot lumen; maaginhoud verwijderen en volgens protocol spoelen.", "Orogastrik; geniş lümen; mide içeriğini boşalt ve protokole göre yıka.")],
    [("Enterale voeding, kortdurend", "Enteral beslenme, kısa süreli"), ("<b>Levin 12 Ch / microkatheter</b>", "Levin 12 Ch / mikrokateter"),
     ("Voeding volgens schema: bolus, intermittent of continu; ligging vóór voeding controleren.", "Şemaya göre besleme: bolus, aralıklı veya sürekli; beslenmeden önce yerleşimi kontrol et.")],
    [("Enterale voeding, langdurig in maag", "Enteral beslenme, mideye uzun süreli"), ("<b>PEG/PRG / ballonkatheter</b>", "PEG/PRG / balonlu kateter"),
     ("Voeding via voedingsstoma; dagelijkse verzorging na fistelvorming.", "Beslenme stoması yoluyla besleme; fistül oluştuktan sonra günlük bakım.")],
    [("Enterale voeding voorbij pylorus", "Pilorun ötesine enteral beslenme"), ("<b>PEG-J of PEJ</b>", "PEG-J veya PEJ"),
     ("Voeding rechtstreeks in jejunum; PEG-J nooit draaien.", "Besin doğrudan jejunuma verilir; PEG-J asla çevrilmez.")],
    [("Medicatie via gastro-enterale weg", "Gastro-enteral yolla ilaç"), ("Geschikte maag-/voedingskatheter", "Uygun mide/beslenme kateteri"),
     ("Eerst controleren of geneesmiddel geplet mag worden; voeding stoppen indien nodig; spoelen vóór/tussen/na.", "Önce ilacın ezilip ezilemeyeceğini kontrol et; gerekirse beslenmeyi durdur; önce/arasında/sonra yıka.")],
], [5.2 * cm, 4.4 * cm, 7.4 * cm])

h1("8. 10-STAPPENPLAN: VASTE VOLGORDE", "8. 10 ADIMLI PLAN: SABİT SIRA")
p("De cursus gebruikt bij de verpleegtechnische handelingen steeds deze vaste structuur:",
  "Kurs, hemşirelik tekniği uygulamalarında her zaman şu sabit yapıyı kullanır:")
numbered([
    ("Gegevensverzameling", "Veri toplama"),
    ("Materiaalverzameling", "Malzeme toplama"),
    ("Handhygiëne", "El hijyeni"),
    ("Voorbereiding zorgvrager en kamer", "Bakım alanın ve odanın hazırlanması"),
    ("Uitvoering", "Uygulama"),
    ("Nazorg bij de zorgvrager", "Bakım alanın son bakımı"),
    ("Nazorg van de kamer", "Odanın son düzenlenmesi"),
    ("Opruimen gebruikt materiaal", "Kullanılan malzemenin toplanması"),
    ("Handhygiëne", "El hijyeni"),
    ("Evalueren en rapporteren", "Değerlendirme ve raporlama"),
])
h2("De 7 concrete stappenplannen in de cursus", "Kurstaki 7 somut adım planı")
numbered([
    ("Maagkatherisatie", "Mide kateterizasyonu"),
    ("Verwijderen van de maagkatheter", "Mide kateterinin çıkarılması"),
    ("Postoperatief verzorgen PEG – PEG-J – PEJ", "PEG – PEG-J – PEJ'in ameliyat sonrası bakımı"),
    ("Verzorgen PEG na 10 dagen plaatsing", "Yerleştirmeden 10 gün sonra PEG bakımı"),
    ("Verwijderen en vervangen gastrostomie ballonkatheter", "Gastrostomi balonlu kateterin çıkarılması ve değiştirilmesi"),
    ("Voorbereiden en toedienen enterale voeding", "Enteral beslenmenin hazırlanması ve uygulanması"),
    ("Toedienen van medicatie via de gastro-enterale weg", "Gastro-enteral yolla ilaç verilmesi"),
])

# ---------------------------------------------------------------- 9
story.append(PageBreak())
h1("9. SNELLE EXAMENCHECKLIST", "9. HIZLI SINAV KONTROL LİSTESİ")
p("Als je weinig tijd hebt, ken zeker deze koppelingen en cijfers uit de cursus:",
  "Az vaktin varsa, kurstan en azından şu eşleşmeleri ve rakamları bil:")
bullets([
    ("<b>Levin:</b> 12 Ch voeding; 14 Ch basis; 16 Ch drainage; 18–20 Ch maagspoeling.", "<b>Levin:</b> 12 Ch beslenme; 14 Ch temel; 16 Ch drenaj; 18–20 Ch mide yıkama."),
    ("<b>Sump:</b> actieve maagaspiratie.", "<b>Sump:</b> aktif mide aspirasyonu."),
    ("<b>Faucher:</b> maagspoeling, orogastrisch, groot lumen.", "<b>Faucher:</b> mide yıkama, orogastrik, geniş lümen."),
    ("<b>PEG/PRG:</b> rechtstreeks in maag.", "<b>PEG/PRG:</b> doğrudan mideye."),
    ("<b>PEG-J:</b> PEG + verlengkatheter naar jejunum; nooit draaien.", "<b>PEG-J:</b> PEG + jejunuma uzatma kateteri; asla çevirme."),
    ("<b>PEJ:</b> rechtstreeks in jejunum.", "<b>PEJ:</b> doğrudan jejunuma."),
    ("<b>pH:</b> maagvocht typisch pH 1–2; pH &gt;5 of twijfel in stappenplan → RX.", "<b>pH:</b> mide sıvısı tipik olarak pH 1–2; pH &gt;5 veya şüphe varsa adım planında → röntgen (RX)."),
    ("<b>Doorspoelen:</b> meestal 20–40 ml; bij veel opeenvolgende spoelingen 2–5 ml.", "<b>Yıkama:</b> çoğunlukla 20–40 ml; çok sayıda art arda yıkamada 2–5 ml."),
    ("<b>Enterale voeding:</b> bolus 250–350 ml, intermittent 2–6 u, continu 12–24 u.", "<b>Enteral beslenme:</b> bolus 250–350 ml, aralıklı 2–6 saat, sürekli 12–24 saat."),
    ("<b>Inloopsnelheid:</b> ideaal 125 ml/u, maximum 200 ml/u; begin bij nausea 25–50 ml/u.", "<b>Akış hızı:</b> ideal 125 ml/saat, en fazla 200 ml/saat; bulantıda 25–50 ml/saat ile başla."),
    ("<b>Maagresidu:</b> 100–150 ml na 4 u wordt in de cursus als probleemgrens genoemd.", "<b>Mide rezidüsü:</b> 4 saat sonra 100–150 ml, kursta sorun sınırı olarak belirtilir."),
    ("<b>Voedingsstoma:</b> eerste voeding na 24 u; eerste 10 dagen steriele verzorging/niet draaien.", "<b>Beslenme stoması:</b> ilk besleme 24 saat sonra; ilk 10 gün steril bakım/çevirme yok."),
    ("<b>Na fistelvorming:</b> dagelijkse verzorging; PEG/ballonkatheter 180–360° draaien volgens cursus; PEG-J nooit draaien.", "<b>Fistül oluştuktan sonra:</b> günlük bakım; kursa göre PEG/balonlu kateter 180–360° çevrilir; PEG-J asla çevrilmez."),
    ("<b>Ballon:</b> volwassenen 5–10 ml steriel water volgens cursus, maar altijd katheter/verpakking volgen.", "<b>Balon:</b> kursa göre yetişkinlerde 5–10 ml steril su, ama her zaman kateterin/ambalajın talimatına uy."),
    ("<b>PEG valt uit:</b> eerste 10 dagen urgent; na 10 dagen zo snel mogelijk vervangen omdat fistel kan sluiten.", "<b>PEG düşerse:</b> ilk 10 gün acil; 10 günden sonra fistül kapanabileceği için en kısa sürede değiştir."),
    ("<b>Medicatie:</b> nooit automatisch pletten; Retard/Contin/SR en E.C./MSR zijn belangrijke waarschuwingen.", "<b>İlaç:</b> asla otomatik ezme; Retard/Contin/SR ve E.C./MSR önemli uyarılardır."),
    ("<b>Bij aspiratie:</b> voeding onmiddellijk stoppen, houding aanpassen, arts verwittigen en nodige maatregelen nemen.", "<b>Aspirasyonda:</b> beslenmeyi hemen durdur, pozisyonu ayarla, doktora haber ver ve gerekli önlemleri al."),
    ("<b>Bij braken:</b> voeding stoppen, maar katheter volgens cursus wel doorspoelen.", "<b>Kusmada:</b> beslenmeyi durdur, ama kursa göre kateteri yine de yıka."),
])
h2("Bron", "Kaynak")
p("Samengesteld uit de aangeleverde cursus <i>Gastro Ent (1).pdf</i>, M3/OLOD3 – Gastro-enterologie, laatste aanpassing juni 2026. De cursus vermeldt o.a. bronnen van PIVH, Thomas More, UZ Gent, LUMC, Radboudumc, Nutricia en andere onderwijs-/zorgbronnen.",
  "Verilen kurs dosyası <i>Gastro Ent (1).pdf</i>, M3/OLOD3 – Gastro-enteroloji'den derlenmiştir, son güncelleme Haziran 2026. Kurs; PIVH, Thomas More, UZ Gent, LUMC, Radboudumc, Nutricia ve diğer eğitim/bakım kaynaklarını belirtir.")
p("<b>Deze PDF is een studiesamenvatting, geen vervanging van de officiële checklists of lokale verpleegkundige protocollen.</b>",
  "<b>Bu PDF bir çalışma özetidir; resmî kontrol listelerinin veya yerel hemşirelik protokollerinin yerini almaz.</b>")


def footer(canvas, doc):
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(colors.grey)
    canvas.drawString(1.8 * cm, 1 * cm, "Gastro-enterologie – studiesamenvatting (NL + TR)")
    canvas.drawRightString(A4[0] - 1.8 * cm, 1 * cm, f"Pagina {doc.page}")


doc = SimpleDocTemplate("/home/user/awesome-claude-skills/Gastro-enterologie_NL-TR.pdf", pagesize=A4,
                        leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.7 * cm,
                        title="Gastro-enterologie – studiesamenvatting (NL + TR)")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("ok")
