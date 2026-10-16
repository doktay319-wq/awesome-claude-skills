"""Boşluk doldurma (invuloefeningen) verisi. Cevaplar: boşluk başına bir giriş, alternatifler '|' ile ayrılır."""
import json, os

R = "/home/user/awesome-claude-skills/zouff-mission3"
fills = []


def F(page, ex, instr, instr_nl, text, answers, hint="", guess=False):
    fills.append(dict(page=page, ex=ex, instr=instr, instr_nl=instr_nl, text=text, answers=answers, hint=hint, guess=guess))


# ---- p29 6a
i, n = "Marquez ce qui va ensemble. Plusieurs solutions sont possibles !", "Duid aan wat samengaat. Er zijn meerdere oplossingen mogelijk!"
for t, a, h in [
    ("J'aime écouter ___.", "la radio|des amies", "un jour. / la radio. / des amies."),
    ("J'aime téléphoner ___.", "avec un GSM|à une amie", "avec un GSM. / de la musique. / à une amie."),
    ("J'aime danser ___.", "avec un ami", "une chanson. / au basket. / avec un ami."),
    ("J'aime chanter ___.", "des chansons", "au padel. / des chansons. / la radio."),
    ("J'aime regarder ___.", "la télé|un film", "la télé. / un film. / une semaine."),
    ("J'aime jouer ___.", "au basket|de la musique", "au basket. / avec un ami. / de la musique."),
]:
    F(29, "6a", i, n, t, [a], "Kies uit: " + h)

# ---- p31 11c
i, n = "Écrivez l'article défini : le, la, l' ou les.", "Schrijf het bepaald lidwoord: le, la, l' of les."
for w, a in [("GSM", "le"), ("musique", "la"), ("portable", "le"), ("weekends", "les"), ("télé", "la"),
             ("ami", "l'"), ("cinéma", "le"), ("semaines", "les"), ("chanson", "la"), ("film", "le")]:
    F(31, "11c", i, n, f"___ {w}", [a])

# ---- p32 13a / 13b
i, n = "Regardez bien l'article. Complétez avec au, à la, à l', aux.", "Kijk goed naar het lidwoord. Vul aan met au, à la, à l', aux."
for h, t, a in [("l'école", "Les élèves sont ___ école.", "à l'"), ("le voisin", "Nous téléphonons ___ voisin de Lina.", "au"),
                ("la page", "Les exercices sont ___ page 11.", "à la"), ("les amies", "Éléonore téléphone ___ amies de Rhim.", "aux"),
                ("le tableau", "Le texte est ___ tableau.", "au")]:
    F(32, "13a", i, n, t, [a], h)
for t, a in [("Timothy et Finn jouent ___ ordinateur.", "à l'"), ("Najib téléphone ___ voisins.", "aux"),
             ("Je regarde les films ___ télé.", "à la"), ("Vous téléphonez ___ profs de 5A et 5B ?", "aux"),
             ("Anaïs regarde un film ___ cinéma.", "au")]:
    F(32, "13b", "Continuez.", "Ga verder.", t, [a])

# ---- p33 15 + 16c
i, n = "Combinez ce qui va ensemble. Écrivez la bonne forme d'aimer.", "Verbind wat bij elkaar hoort. Schrijf de juiste vorm van aimer."
for t, a in [("Clara Cornette ___.", "aime"), ("Tu ___.", "aimes"), ("Astérix ___.", "aime"), ("J'___.", "aime"),
             ("Vous ___.", "aimez"), ("Les amis de Nour ___.", "aiment"), ("Papa et moi, nous ___.", "aimons"),
             ("Belle et Sébastien ___.", "aiment")]:
    F(33, "15", i, n, t, [a], "aimer")
i, n = "Marquez le sujet. Complétez avec une forme d'aimer.", "Duid het onderwerp aan. Vul de juiste vorm van aimer aan."
for t, a in [("Ariane et Marcel, vous ___ les sports ?", "aimez"), ("Oui, nous ___ le basket et le tennis.", "aimons"),
             ("Olivier, tu ___ Chloé ?", "aimes"), ("Non, moi, j'___ Suki.", "aime"),
             ("Les élèves de 5A ___ la prof ?", "aiment"), ("Oui, et la prof ___ les élèves.", "aime"),
             ("Le voisin ___ chanter ?", "aime"), ("Oui, les voisins ___ la musique.", "aiment")]:
    F(33, "16c", i, n, t, [a], "aimer")

# ---- p34 17a / 17b
i, n = "Conjuguez les verbes.", "Vervoeg de werkwoorden."
subj = [("Je", "e"), ("Tu", "es"), ("Il", "e"), ("Elle", "e"), ("Nous", "ons"), ("Vous", "ez"), ("Ils", "ent"), ("Elles", "ent")]
for verb, stem, rest in [("danser", "dans", "avec un ami"), ("chanter", "chant", "une chanson"),
                         ("écouter", "écout", "la radio"), ("jouer", "jou", "à l'ordinateur")]:
    for s, e in subj:
        if s == "Je" and stem[0] in "aeiouéh":
            t = f"J'___ {rest}."
        else:
            t = f"{s} ___ {rest}."
        F(34, "17a", i, n, t, [stem + e], verb)
i, n = "Marquez le sujet. Complétez avec la bonne forme du verbe.", "Duid het onderwerp aan. Vul aan met de juiste werkwoordsvorm."
for v, t, a in [
    ("aimer", "Tu ___ Chloé ?", "aimes"), ("aimer", "Non, j'___ Suki.", "aime"),
    ("écouter", "Zoé ___ la radio ?", "écoute"), ("écouter", "Oui ! Et Tim et Muriel ___ la radio aussi.", "écoutent"),
    ("regarder", "Mo et Sam ___ la télé ?", "regardent"), ("regarder", "Oui, ils ___ un film.", "regardent"),
    ("danser", "Tu ___ avec Ismaël ?", "danses"), ("danser", "Oui, et Sandrine ___ avec Samir.", "danse"),
    ("téléphoner", "Vous ___ à qui ?", "téléphonez"), ("téléphoner", "Je ___ à un ami.", "téléphone"),
    ("chanter", "Vous ___ une chanson ?", "chantez"), ("chanter", "Oui, nous ___ une chanson de Zaz.", "chantons"),
]:
    F(34, "17b", i, n, t, [a], v)

# ---- p35 Détour
i, n = "Complétez les dialogues avec des substantifs de cette Mission.", "Vul de dialogen aan met zelfstandige naamwoorden van deze Mission."
for t, a in [("Tu écoutes de la musique ? — Oui, une ___ de Stromae.", "chanson"),
             ("Aline téléphone à une voisine ? — Non, à une ___.", "amie"),
             ("Tu aimes le weekend ? — Oui, samedi et ___ sont super !", "dimanche"),
             ("C'est quoi, « mercredi » ? — Mercredi est un jour de la ___.", "semaine")]:
    F(35, "1a", i, n, t, [a])
i, n = "Complétez avec des verbes à la bonne forme.", "Met werkwoorden in de juiste vorm."
F(35, "1b", i, n, "Tu fais quoi, mardi ? — Mardi, je ___ au tennis. Et toi ?", ["joue"], "jouer")
F(35, "1b", i, n, "Tu ___ avec qui ? — Avec Rachid. Il ___ danser avec moi.", ["danses", "aime"], "danser / aimer", True)
F(35, "1b", i, n, "Vous ___ la télé ? — Oui, nous ___ un film de 007.", ["regardez", "regardons"], "regarder")
F(35, "1b", i, n, "Les élèves ___ de la musique ? — Oui, et ils ___ des chansons aussi.", ["écoutent", "chantent"], "écouter / chanter", True)
i, n = "Complétez avec le, la, l' ou les.", "Met le, la, l' of les."
F(35, "1c", i, n, "Tu aimes ___ musique ? — Oui, j'aime ___ chansons de Zaz.", ["la", "les"])
F(35, "1c", i, n, "Tu écoutes ___ radio ? — Non, je regarde ___ télé.", ["la", "la"])
F(35, "1c", i, n, "Tu as ___ ordinateur de la prof ? — Non, j'ai ___ portable de Jules.", ["l'", "le"])
i, n = "Complétez avec au, à la, à l' ou aux.", "Met au, à la, à l' of aux."
F(35, "1d", i, n, "Tu téléphones à qui ? — Je téléphone ___ amies de la classe.", ["aux"])
F(35, "1d", i, n, "Vos amis regardent un film ? — Oui, ils sont ___ cinéma.", ["au"])
F(35, "1d", i, n, "Les élèves sont ___ école du lundi ___ vendredi.", ["à l'", "au"])

# ---- p41
i, n = "Complétez les phrases avec la bonne forme d'être.", "Met de juiste vorm van être."
for h, t, a in [("Mauro et Basil", "Ils ___ de Bruxelles.", "sont"), ("", "Vous ___ des amis ?", "êtes"),
                ("Arianne", "Elle ___ la prof de 5A.", "est"), ("", "Je ___ d'Ostende.", "suis")]:
    F(41, "4a", i, n, t, [a], h)
i, n = "Complétez avec le bon pronom personnel.", "Met het juiste persoonlijk voornaamwoord."
for h, t, a in [("Félix et moi", "___ sommes de Charleroi.", "Nous"), ("Julie et Noura", "___ sont des élèves.", "Elles"),
                ("Georges", "___ est l'ami de Noura.", "Il"), ("", "___ es qui ?", "Tu")]:
    F(41, "4b", i, n, t, [a], h)
i, n = "Écrivez les phrases au singulier ou au pluriel.", "Schrijf de zinnen in het enkelvoud of het meervoud."
for h, t, a in [("→ singulier", "Ce sont des voisins de l'école.", "C'est un voisin de l'école"),
                ("→ singulier", "Voici les amies de Marise.", "Voici l'amie de Marise"),
                ("→ pluriel", "Il y a un cinéma ?", "Il y a des cinémas"),
                ("→ pluriel", "C'est la feuille de Levi.", "Ce sont les feuilles de Levi"),
                ("→ pluriel", "C'est une chanson de Rahim.", "Ce sont des chansons de Rahim")]:
    F(41, "5a", i, n, t + " → ___", [a], h)
i, n = "Complétez les phrases (Ce sont / Il y a / Voici).", "Vul de zinnen aan."
for t, a in [("Het zijn boeken.", "Ce sont des livres"), ("Er zijn oefeningen.", "Il y a des exercices"), ("Hier zijn balpennen.", "Voici des stylos")]:
    F(41, "5b", i, n, t + " → ___", [a])

# ---- p42
i, n = "Traduisez. Choisissez les bons mots.", "Vertaal. Kies de juiste woorden."
F(42, "6", i, n, "Het zijn liedjes van radio. → ___", ["Ce sont des chansons de radio"], "c'est · ce sont · de · des · la · le · un · une · chanson(s) · radio(s)")
F(42, "6", i, n, "Het is een pagina met oefeningen. → ___", ["C'est une page avec des exercices"], "avec · C'est · Ce sont · des · un · une · exercice(s) · page(s)")
i, n = "Regardez le calendrier. Complétez avec le nom du jour et la bonne forme du verbe.", "Kijk naar de kalender. Vul de naam van de dag en de juiste werkwoordsvorm aan."
cal = "MA radio · DI dansen · WO bal · DO computer · VR microfoon · ZA telefoon · ZO film"
for h, t, a in [("zingen", "___, nous ___ des chansons.", ["vendredi", "chantons"]),
                ("houden van", "___, Tessa ___ jouer au football.", ["mercredi", "aime"]),
                ("dansen", "___, les élèves ___ à l'école.", ["mardi", "dansent"]),
                ("spelen", "___, Max ___ à l'ordinateur.", ["jeudi", "joue"]),
                ("telefoneren", "___, vous ___ à des amis.", ["samedi", "téléphonez"]),
                ("luisteren naar", "___, tu ___ la radio ?", ["lundi", "écoutes"]),
                ("kijken naar", "___, je ___ un film au cinéma.", ["dimanche", "regarde"])]:
    F(42, "7", i, n, t, a, f"{h} — {cal}")
i, n = "Complétez avec le, la, l' ou les.", "Vul aan."
for t, a in [("Voici ___ radio de Caro.", "la"), ("J'aime ___ portable de Marc.", "le"), ("C'est ___ ordinateur de Bilal.", "l'"),
             ("Voici ___ cinéma.", "le"), ("Prenez ___ exercices 2 et 3.", "les"), ("C'est ___ semaine d'Yves.", "la")]:
    F(42, "8a", i, n, t, [a])
i, n = "Complétez avec à la, à l', au ou aux.", "Vul aan."
for t, a in [("Je téléphone ___ amis d'Annick.", "aux"), ("Nous écoutons les chansons ___ radio.", "à la"),
             ("Vous aimez regarder des films ___ cinéma.", "au"), ("Les élèves sont ___ école ?", "à l'"),
             ("Les exercices sont ___ tableau.", "au"), ("Le texte est ___ page 4.", "à la")]:
    F(42, "8b", i, n, t, [a])

for k, f in enumerate(fills, 1):
    f["id"] = f"x{k:03d}"
    assert f["text"].count("___") == len(f["answers"]), f["text"]
os.makedirs(R, exist_ok=True)
json.dump(fills, open(f"{R}/exercises_fill.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(fills), "invuloefeningen")
