#!/usr/bin/env python3
"""Génère le site statique Grizzly Dépannage. Lancer : python3 build.py"""
import json, math, html, datetime, pathlib, hashlib

ROOT = pathlib.Path(__file__).parent
DOMAIN = "https://grizzlydepannage.com/"
NAME = "Grizzly Dépannage"
TEL, TEL_E164, TEL_HREF = "06 07 94 57 98", "+33607945798", "tel:+33607945798"
EMAIL = "grizzlydepannage@gmail.com"
STREET, CP, CITY = "38 rue Pierre Brossolette", "91130", "Ris-Orangis"
LAT0, LON0 = 48.6536, 2.4137
VHU_PR = "PR 9100012D"  # agrément du centre VHU partenaire
LABEL_IMG = "assets/img/labels/ministere-transition-ecologique.webp"
TODAY = datetime.date.today().isoformat()
def ver(p): return hashlib.md5((ROOT / p).read_bytes()).hexdigest()[:8]
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Inter:wght@400;500;600;700&display=swap"

# ---------------------------------------------------------------- icônes (tracé Lucide)
I = {
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
 "down": '<path d="m6 9 6 6 6-6"/>',
 "sms": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-10 5L2 7"/>',
 "tag": '<path d="M12 2H2v10l9.29 9.29a1 1 0 0 0 1.41 0l8.59-8.59a1 1 0 0 0 0-1.41Z"/><circle cx="7" cy="7" r="1.5"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 "truck": '<path d="M10 17h4V5H2v12h3"/><path d="M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L19 9h-5v8h1"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
 "recycle": '<path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/><path d="m14 16-3 3 3 3"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096"/>',
 "cone": '<path d="M9.3 6.2a4.55 4.55 0 0 0 5.4 0"/><path d="M7.9 10.7c.9.8 2.4 1.3 4.1 1.3s3.2-.5 4.1-1.3"/><path d="M13.9 3.5a1.93 1.93 0 0 0-3.8-.1l-3 10c-.1.2-.1.4-.1.6 0 1.7 2.2 3 5 3s5-1.3 5-3c0-.2 0-.4-.1-.5Z"/><path d="m7.5 12.2-4.7 2.7c-.5.3-.8.7-.8 1.1s.3.8.8 1.1l7.6 4.5c.9.5 2.1.5 3 0l7.6-4.5c.7-.3 1-.7 1-1.1s-.3-.8-.8-1.1l-4.7-2.8"/>',
 "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
 "battery": '<rect width="16" height="10" x="2" y="7" rx="2"/><path d="M22 11v2M6 11v2M10 11v2"/>',
 "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
 "parking": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>',
}
def ic(n, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

esc = html.escape

# ---------------------------------------------------------------- métiers
SERVICES = [
 dict(slug="enlevement-epave", img="epaves-vue-dessus", name="Enlèvement d’épave", icon="recycle",
  short="Enlèvement gratuit de votre véhicule hors d’usage, remis à notre centre VHU agréé partenaire pour destruction.",
  kpis=[("recycle", "Enlèvement gratuit", "Véhicule complet avec ses papiers"), ("shield", "Centre VHU agréé partenaire", "Agrément " + VHU_PR), ("doc", "Certificat de destruction", "Remis par le centre agréé")], trust=True,
  title="Enlèvement d’épave gratuit à Ris-Orangis | Grizzly Dépannage",
  desc="Épaviste à Ris-Orangis et 25 km autour : enlèvement d’épave gratuit, remise à un centre VHU agréé partenaire (PR 9100012D), certificat de destruction. 06 07 94 57 98.",
  h1=["Enlèvement d’épave gratuit", "à <span class=y>Ris-Orangis</span>"],
  lead="Une voiture hors d’usage dort dans votre garage, votre cour ou sur la rue ? Grizzly Dépannage l’enlève gratuitement et la remet à son partenaire, centre VHU agréé par la préfecture (PR 9100012D), qui la dépollue, la recycle et établit le certificat de destruction.",
  items=["Carte grise barrée avec la mention « Vendu le … pour destruction », datée et signée", "Certificat de situation administrative (non-gage) de moins de 15 jours", "Pièce d’identité du titulaire de la carte grise"],
  items_title="Les documents à préparer",
  items2_title="Les véhicules concernés",
  items2=["Voitures, utilitaires, motos et scooters", "Véhicules accidentés, brûlés ou non roulants", "Véhicules immobilisés depuis longtemps", "En garage, box, cour privée ou sur la voie publique"],
  note="L’enlèvement est gratuit pour un véhicule complet, moteur et pièces principales en place, avec ses papiers. Véhicule désossé ou carte grise perdue : appelez, on regarde votre cas avant de se déplacer.",
  faq=[("L’enlèvement d’épave est-il vraiment gratuit ?", "Oui, pour un véhicule complet, accessible au camion et accompagné de ses papiers. Aucun frais de déplacement. Si le véhicule est incomplet, on vous le dit au téléphone avant de venir."),
       ("Quels documents fournir pour faire enlever une épave ?", "La carte grise barrée avec la mention « Vendu le … pour destruction », datée et signée, un certificat de non-gage de moins de 15 jours et la pièce d’identité du titulaire."),
       ("J’ai perdu la carte grise, que faire ?", "Appelez-nous avec le numéro d’immatriculation. Selon la situation, une déclaration de perte peut suffire. On vous explique la démarche avant de se déplacer."),
       ("Qui délivre le certificat de destruction ?", "Notre partenaire, le centre VHU agréé PR 9100012D, qui reçoit le véhicule. Ce certificat prouve la destruction et vous permet de résilier votre assurance."),
       ("Êtes-vous épaviste agréé ?", "Grizzly Dépannage assure l’enlèvement et le transport. Le traitement du véhicule est réalisé par notre partenaire, centre VHU agréé par la préfecture sous le numéro PR 9100012D, dans le cadre de la filière réglementée par le Ministère de la Transition écologique.")]),
 dict(slug="depannage-automobile", img="arrimage-roue", name="Dépannage automobile", icon="wrench",
  short="Batterie à plat, crevaison, panne sèche, clés enfermées : on vous remet en route sur place quand c’est possible.",
  title="Dépannage automobile à Ris-Orangis 24h/24 | Grizzly Dépannage",
  desc="Dépannage automobile à Ris-Orangis et 25 km autour : batterie, crevaison, panne sèche, clés enfermées. Prix annoncé avant le départ, 24h/24 et 7j/7. 06 07 94 57 98.",
  h1=["Dépannage automobile", "à <span class=y>Ris-Orangis</span>"],
  lead="Batterie à plat, crevaison, voiture qui refuse de démarrer : Grizzly Dépannage se déplace avec le matériel pour vous remettre en route sur place. Si la panne demande un garage, le même camion embarque votre véhicule.",
  items=["Batterie déchargée : démarrage assisté au booster et contrôle de la charge", "Crevaison : pose de votre roue de secours", "Panne sèche : apport de carburant pour rejoindre la station", "Clés enfermées dans le véhicule", "Voiture qui ne démarre plus : premier diagnostic sur place", "Véhicule bloqué en stationnement"],
  items_title="Les pannes réglées sur place",
  note="Pas de réparation possible au bord de la route ? On charge le véhicule sur le plateau et on le dépose au garage de votre choix, sans rappeler un second dépanneur.",
  faq=[("Combien coûte un dépannage automobile à Ris-Orangis ?", "Le prix dépend de la distance, de l’heure et de la panne. Grizzly Dépannage vous l’annonce au téléphone avant de partir. Vous acceptez ou non, sans engagement."),
       ("Pouvez-vous réparer ma voiture sur place ?", "Oui pour les pannes courantes : batterie, roue, carburant, clés enfermées. Pour une panne mécanique lourde, on remorque votre véhicule vers le garage de votre choix."),
       ("Intervenez-vous la nuit et le week-end ?", "Oui. Le téléphone répond 24h/24 et 7j/7, jours fériés compris, et la dépanneuse part à toute heure.")]),
 dict(slug="remorquage", img="chargement-plateau", name="Remorquage", icon="truck",
  short="Voiture accidentée ou non roulante chargée sur plateau et déposée au garage, chez vous ou en concession.",
  title="Remorquage voiture à Ris-Orangis 24h/24 | Grizzly Dépannage",
  desc="Remorquage de voiture, utilitaire et moto à Ris-Orangis et dans un rayon de 25 km. Plateau, destination au choix, tarif annoncé avant le départ. 06 07 94 57 98.",
  h1=["Remorquage de véhicule", "à <span class=y>Ris-Orangis</span>"],
  lead="Voiture accidentée, en panne ou non roulante : on la charge sur plateau et on la dépose où vous voulez, au garage, chez vous ou en concession. Vous connaissez le tarif avant que le camion ne parte.",
  items=["Voitures accidentées ou non roulantes", "Pannes mécaniques : moteur, embrayage, boîte de vitesses", "Utilitaires, 4x4 et motos", "Voitures basses et véhicules de collection", "Sortie de parking souterrain, selon la hauteur d’accès", "Destination au choix : garage, domicile, concession"],
  items_title="Ce qu’on remorque",
  note="Vous avez une assistance avec votre assurance ? Appelez-la d’abord : certains contrats imposent leur propre dépanneur. Sinon, on vous remet une facture détaillée à transmettre à votre assureur.",
  faq=[("Combien coûte un remorquage autour de Ris-Orangis ?", "Le tarif dépend de la distance jusqu’à la destination, du type de véhicule et de l’heure. On vous le donne au téléphone avant de partir, pas au moment de payer."),
       ("Où déposez-vous le véhicule ?", "À l’adresse de votre choix : votre garage, votre domicile, une concession. Au-delà de la zone des 25 km, on vous fait un prix sur demande."),
       ("Remorquez-vous les motos et les utilitaires ?", "Oui : voitures, utilitaires, 4x4 et motos. Précisez le modèle au téléphone pour qu’on vienne avec le bon équipement.")]),
 dict(slug="assistance-routiere", img="plateau-en-ville", name="Assistance routière", icon="cone",
  short="Panne ou accident sur la route, en zone commerciale ou en parking : mise en sécurité, dépannage ou remorquage.",
  title="Assistance routière autour de Ris-Orangis 24h/24 | Grizzly Dépannage",
  desc="Assistance routière à Ris-Orangis, Évry-Courcouronnes, Grigny et 25 km autour : panne, accident sans blessé, parking. 24h/24. 06 07 94 57 98.",
  h1=["Assistance routière", "autour de <span class=y>Ris-Orangis</span>"],
  lead="Panne sur une départementale, en ville, dans une zone commerciale ou un parking : on arrive avec gyrophares et balisage, on sécurise, puis on dépanne sur place ou on remorque.",
  items=["Allumez les feux de détresse", "Enfilez le gilet jaune avant de sortir du véhicule", "Posez le triangle à 30 m au moins, si vous pouvez le faire sans danger", "Faites sortir les passagers côté trottoir ou derrière la glissière", "Appelez le 06 07 94 57 98 et donnez un repère précis"],
  items_title="Les bons réflexes en attendant la dépanneuse",
  items2_title="Où on intervient",
  items2=["Routes départementales et nationales hors voies réglementées", "Rues et parkings en ville", "Parkings de centres commerciaux et zones d’activité", "Parkings souterrains, selon la hauteur d’accès"],
  note="Sur l’autoroute A6 et les voies rapides soumises à agrément, la loi réserve l’intervention aux dépanneurs agréés : utilisez la borne d’appel orange ou le 112. Une fois votre véhicule sorti de l’axe, on prend le relais jusqu’au garage.",
  faq=[("Intervenez-vous sur l’autoroute A6 ?", "Non. Sur autoroute, seul le dépanneur agréé pour le secteur a le droit d’intervenir : appelez depuis une borne orange ou le 112. Une fois le véhicule déposé hors de l’autoroute, on peut le transporter jusqu’à votre garage."),
       ("Que faire en cas d’accident ?", "S’il y a un blessé, appelez d’abord le 15 ou le 112. Sans blessé, mettez-vous en sécurité, remplissez le constat, puis appelez-nous pour dégager et remorquer le véhicule."),
       ("En combien de temps arrivez-vous ?", "Ça dépend de l’endroit et de l’heure. Au téléphone, on vous donne une heure d’arrivée précise, pas une promesse générale.")]),
 dict(slug="transport-vehicule", img="transport-plateau", name="Transport de véhicule", icon="car",
  short="Véhicule sans plaque, sans contrôle technique ou non roulant, transporté d’une adresse à l’autre.",
  title="Transport de véhicule sur plateau depuis Ris-Orangis | Grizzly Dépannage",
  desc="Transport de voiture sur plateau depuis Ris-Orangis : achat entre particuliers, véhicule sans contrôle technique, sortie de box. 06 07 94 57 98.",
  h1=["Transport de véhicule", "depuis <span class=y>Ris-Orangis</span>"],
  lead="Vous achetez une voiture qui ne roule pas, un véhicule sans contrôle technique ou sans assurance, ou vous devez vider un box : on le transporte sur plateau d’une adresse à l’autre.",
  items=["Achat ou vente entre particuliers", "Véhicule sans contrôle technique ou sans assurance", "Déménagement d’un véhicule non roulant", "Sortie de box ou de garage fermé depuis longtemps", "Transfert vers un carrossier, un garage ou une concession", "Voiture de collection ou de projet"],
  items_title="Les cas les plus fréquents",
  note="Pour un prix précis, donnez-nous l’adresse de départ, l’adresse d’arrivée et le modèle du véhicule. On vous rappelle avec un tarif ferme.",
  faq=[("Faites-vous des transports longue distance ?", "Notre zone principale couvre 25 km autour de Ris-Orangis. Pour une destination plus lointaine, on vous fait un prix sur demande."),
       ("Dois-je être présent au chargement ?", "Une personne doit remettre les clés et les papiers au départ, et une autre réceptionner le véhicule à l’arrivée. Ça peut être vous ou quelqu’un que vous désignez."),
       ("Comment obtenir un prix ?", "Appelez le 06 07 94 57 98 ou remplissez le formulaire avec les deux adresses et le modèle. On vous rappelle avec un tarif ferme.")]),
 dict(slug="sortie-fourriere", img="parc-vehicules-aerien", name="Sortie de fourrière", icon="key",
  short="Récupération en fourrière d’un véhicule qui ne peut pas repartir par la route, livré chez vous ou au garage.",
  title="Sortie de fourrière à Ris-Orangis | Grizzly Dépannage",
  desc="Voiture en fourrière qui ne peut pas rouler ? Grizzly Dépannage la récupère avec la mainlevée et la livre chez vous ou au garage. 06 07 94 57 98.",
  h1=["Sortie de fourrière", "et transport du véhicule"],
  lead="Votre voiture est en fourrière et ne peut pas repartir par la route : assurance expirée, contrôle technique dépassé, panne ou dégâts. Une fois la mainlevée obtenue, Grizzly Dépannage va la chercher et la livre chez vous ou au garage.",
  items=["Vous obtenez la mainlevée (autorisation de sortie) et vous réglez les frais de fourrière", "On se présente à la fourrière avec les documents", "On charge le véhicule et on le livre à l’adresse convenue"],
  items_title="Comment ça se passe",
  note="Les frais de fourrière se règlent à la fourrière et ne sont pas inclus dans notre tarif. Notre prix couvre le déplacement et le transport du véhicule.",
  faq=[("Quels documents pour sortir une voiture de fourrière ?", "En général : la mainlevée, la carte grise, une pièce d’identité et le permis. La fourrière vous confirme la liste exacte selon votre situation."),
       ("Les frais de fourrière sont-ils compris dans votre prix ?", "Non. Vous réglez la fourrière directement. Notre tarif couvre le déplacement et le transport du véhicule jusqu’à l’adresse convenue."),
       ("Pourquoi passer par un dépanneur pour sortir de fourrière ?", "Quand le véhicule ne peut pas rouler, légalement ou mécaniquement : pas d’assurance, contrôle technique dépassé, panne, dégâts. On le transporte sur plateau.")]),
]
SVC = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- communes (lat, lon, CP, page dédiée, axes routiers)
TOWNS_RAW = [
 ("Évry-Courcouronnes", 48.6290, 2.4400, "91000", True, "la N7, l’A6 et la N104"),
 ("Grigny", 48.6547, 2.3930, "91350", True, "l’A6"),
 ("Viry-Châtillon", 48.6710, 2.3750, "91170", True, "l’A6 et la N7"),
 ("Juvisy-sur-Orge", 48.6897, 2.3770, "91260", True, "la N7"),
 ("Draveil", 48.6850, 2.4100, "91210", True, ""),
 ("Soisy-sur-Seine", 48.6500, 2.4520, "91450", True, ""),
 ("Corbeil-Essonnes", 48.6139, 2.4820, "91100", True, "la N7 et la N104"),
 ("Bondoufle", 48.6130, 2.3790, "91070", True, "la N104"),
 ("Fleury-Mérogis", 48.6360, 2.3630, "91700", True, "la N104"),
 ("Savigny-sur-Orge", 48.6770, 2.3490, "91600", True, "l’A6"),
 ("Athis-Mons", 48.7090, 2.3890, "91200", True, "la N7"),
 ("Brétigny-sur-Orge", 48.6110, 2.3060, "91220", True, ""),
 ("Sainte-Geneviève-des-Bois", 48.6450, 2.3190, "91700", True, ""),
 ("Lisses", 48.6030, 2.4230, "91090", True, "la N104"),
 ("Saint-Germain-lès-Corbeil", 48.6210, 2.4880, "91250", True, ""),
 ("Vigneux-sur-Seine", 48.7020, 2.4170, "91270", True, ""),
 ("Montgeron", 48.7040, 2.4600, "91230", True, "la N6"),
 ("Mennecy", 48.5660, 2.4370, "91540", True, ""),
 ("Morsang-sur-Orge", 48.6630, 2.3510, "91390", True, ""),
 ("Saint-Michel-sur-Orge", 48.6340, 2.3120, "91240", True, ""),
 ("Étiolles", 48.6330, 2.4800, "91450", False, ""),
 ("Villabé", 48.5890, 2.4510, "91100", False, ""),
 ("Tigery", 48.6420, 2.5070, "91250", False, ""),
 ("Saint-Pierre-du-Perray", 48.6120, 2.4950, "91280", False, ""),
 ("Le Coudray-Montceaux", 48.5640, 2.4990, "91830", False, ""),
 ("Brunoy", 48.6980, 2.5040, "91800", False, ""),
 ("Yerres", 48.7170, 2.4930, "91330", False, ""),
 ("Longjumeau", 48.6940, 2.2960, "91160", False, ""),
 ("Orly", 48.7430, 2.3930, "94310", False, ""),
 ("Villeneuve-Saint-Georges", 48.7320, 2.4490, "94190", False, ""),
 ("Massy", 48.7309, 2.2713, "91300", False, ""),
 ("Arpajon", 48.5900, 2.2470, "91290", False, ""),
 ("Lieusaint", 48.6330, 2.5500, "77127", False, ""),
 ("Combs-la-Ville", 48.6640, 2.5640, "77380", False, ""),
 ("Savigny-le-Temple", 48.5840, 2.5830, "77176", False, ""),
 ("Melun", 48.5390, 2.6600, "77000", False, ""),
]
import unicodedata
def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return "".join(c if c.isalnum() else "-" for c in s).strip("-").replace("--", "-")
def xy(lat, lon):
    return ((lon - LON0) * math.cos(math.radians(LAT0)) * 111.32, (lat - LAT0) * 110.57)
DIRS = ["au nord", "au nord-est", "à l’est", "au sud-est", "au sud", "au sud-ouest", "à l’ouest", "au nord-ouest"]
LABELS = {"Évry-Courcouronnes", "Grigny", "Viry-Châtillon", "Juvisy-sur-Orge", "Corbeil-Essonnes", "Draveil", "Brétigny-sur-Orge", "Montgeron", "Mennecy", "Athis-Mons", "Sainte-Geneviève-des-Bois", "Massy", "Melun", "Orly"}
TOWNS = []
for n, la, lo, cp, page, axes in TOWNS_RAW:
    x, y = xy(la, lo); km = round(math.hypot(x, y), 1)
    if km > 25.5: continue
    b = (math.degrees(math.atan2(x, y)) + 360) % 360
    TOWNS.append(dict(n=n, cp=cp, slug=slugify(n), x=round(x, 2), y=round(y, 2), km=km, dir=DIRS[int((b + 22.5) // 45) % 8],
                      page=page, axes=axes, url=f"depannage-{slugify(n)}.html" if page else "", major=n in LABELS))
TOWNS.sort(key=lambda t: t["km"])
def town_json(focus=None):
    arr = [dict(n=CITY, cp=CP, slug="ris-orangis", x=0, y=0, km=0, hq=True)]
    for t in TOWNS:
        arr.append({k: t[k] for k in ("n", "cp", "slug", "x", "y", "km", "url")} | {"major": t["major"]})
    return json.dumps(arr, ensure_ascii=False)
def kmf(v): return str(v).replace(".", ",")

# ---------------------------------------------------------------- blocs communs
def head(title, desc, path, ld=(), og_title=None):
    url = DOMAIN + ("" if path == "index.html" else path)
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0A0A0B">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, dépannage et remorquage à Ris-Orangis 24h/24">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="FR-91">
<meta name="geo.placename" content="{CITY}">
<meta name="geo.position" content="{LAT0};{LON0}">
<meta name="ICBM" content="{LAT0}, {LON0}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/style.css?v={ver("assets/css/style.css")}">
{lds}
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<div class="progress" aria-hidden="true"></div>
'''

def vhu_badge(href="enlevement-epave.html#agrement"):
    return f'''<a class="vhu" href="{href}" aria-label="En partenariat avec le centre VHU agréé, agrément {VHU_PR}"><span class="vhu-ico">{ic("shield")}</span><span class="vhu-txt"><small><span class="lg">En partenariat avec le</span><span class="sm">Partenaire</span></small><b>Centre VHU agréé</b><em class="num">{VHU_PR}</em></span></a>'''

def trust_cards():
    return f'''<div class="trust">
 <div class="tcard tcard-vhu rv" style="--i:0"><span class="tico">{ic("shield")}</span><p class="tk">En partenariat avec le</p><b>Centre VHU agréé</b><span class="pr num">{VHU_PR}</span><p>Votre véhicule part chez notre partenaire, centre de traitement des véhicules hors d’usage agréé par la préfecture.</p></div>
 <div class="tcard tcard-label rv" style="--i:1"><img src="{LABEL_IMG}" width="520" height="365" alt="Ministère de la Transition écologique" loading="lazy"><b>Filière réglementée par l’État</b><p>Dépollution, recyclage des matériaux et traçabilité, selon les règles du Ministère de la Transition écologique.</p></div>
 <div class="tcard rv" style="--i:2"><span class="tico">{ic("doc")}</span><b>Certificat de destruction</b><p>Établi par le centre agréé et enregistré au système d’immatriculation. Il vous libère du véhicule et de son assurance.</p></div>
 <div class="tcard rv" style="--i:3"><span class="tico">{ic("recycle")}</span><b>0 € pour vous</b><p>Enlèvement gratuit d’un véhicule complet avec ses papiers, sans frais de déplacement.</p></div>
</div>'''

def header(active=""):
    dd = "".join(f'<a href="{s["slug"]}.html"><span class="ico">{ic(s["icon"])}</span><span><b>{s["name"]}</b><span>{esc(s["short"][:62].rsplit(" ",1)[0])}…</span></span></a>' for s in SERVICES)
    cur = lambda k: ' aria-current="page"' if active == k else ""
    tiles = [(s["slug"] + ".html", s["icon"], s["name"], s["slug"]) for s in SERVICES[1:]] + [("zone-intervention.html", "pin", "Zone d’intervention", "zone")]
    msvc = "".join(f'<a class="mt" href="{h}" style="--i:{i+1}"{cur(k)}><span class="ico">{ic(n)}</span><b>{t}</b></a>' for i, (h, n, t, k) in enumerate(tiles))
    return f'''<header class="hdr">
 <div class="wrap">
  <a class="brand" href="./" aria-label="{NAME}, accueil"><img src="assets/img/brand.webp" width="48" height="52" alt=""><span><b>GRIZZLY</b><small>Dépannage</small></span></a>
  {vhu_badge()}
  <nav class="nav" aria-label="Navigation principale">
   <div class="dd"><button type="button" aria-expanded="false" aria-haspopup="true">Services {ic("down")}</button><div class="dd-panel">{dd}</div></div>
   <a href="zone-intervention.html"{cur("zone")}>Zone d’intervention</a>
   <a href="./#faq">Questions</a>
   <a href="./#contact">Devis</a>
  </nav>
  <div class="hdr-cta">
   <span class="live"><i></i>Disponible 24h/24</span>
   <a class="btn btn-y btn-call" href="{TEL_HREF}">{ic("phone")}<span class="num">{TEL}</span></a>
  </div>
  <button class="burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
 </div>
</header>
<nav class="mnav" id="mnav" aria-label="Menu mobile">
 <div class="mnav-in">
  <a class="mnav-top" href="enlevement-epave.html"{cur(SERVICES[0]["slug"])}><span class="ico">{ic("recycle")}</span><span class="t"><small>Notre priorité</small><b>Enlèvement d’épave gratuit</b><em>à Ris-Orangis et 25 km autour</em></span>{ic("arrow")}</a>
  <p class="mnav-k">Services</p>
  <div class="mnav-svc">{msvc}</div>
  <p class="mnav-k">Infos</p>
  <div class="mnav-links">
   <a href="./" style="--i:7">Accueil {ic("arrow")}</a>
   <a href="./#faq" style="--i:8">Questions fréquentes {ic("arrow")}</a>
   <a href="./#contact" style="--i:9">Demander un devis {ic("arrow")}</a>
  </div>
 </div>
 <div class="mnav-foot">
  <span class="live"><i></i>Disponible 24h/24 et 7j/7</span>
  <div class="mnav-cta"><a class="btn btn-y btn-call" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span><span class="num">{TEL}</span></a><a class="btn btn-ghost" href="sms:{TEL_E164}" aria-label="Envoyer un SMS">{ic("sms")}<span>SMS</span></a></div>
 </div>
</nav>
'''

def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    towns = "".join(f'<li><a href="{t["url"]}">Dépannage {t["n"]}</a></li>' for t in TOWNS if t["page"] and t["km"] < 9)
    return f'''<section class="cta-band" aria-label="Appel">
 <div class="wrap">
  <h2 class="h-l rv">Une panne ? Un seul numéro.</h2>
  <a class="btn btn-dark btn-lg btn-call rv" style="--i:1" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span><span class="bigtel num">{TEL}</span></a>
 </div>
</section>
<footer class="ftr">
 <div class="wrap">
  <div class="ftr-grid">
   <div>
    <a class="brand" href="./"><img src="assets/img/brand.webp" width="48" height="52" alt="" loading="lazy"><span><b>GRIZZLY</b><small>Dépannage</small></span></a>
    <p>Enlèvement d’épave gratuit, dépannage et remorquage à Ris-Orangis et dans un rayon de 25 km. 24h/24 et 7j/7.</p>
    <ul class="meta">
     <li>{ic("phone")}<a class="num" href="{TEL_HREF}">{TEL}</a></li>
     <li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li>{ic("pin")}<span>{STREET}, <span class=num>{CP} {CITY}</span></span></li>
    </ul>
   </div>
   <div><h4>Services</h4><ul>{svc}</ul></div>
   <div><h4>Villes</h4><ul>{towns}<li><a href="zone-intervention.html">Toutes les communes →</a></li></ul></div>
   <div><h4>Infos</h4><ul><li><a href="./#faq">Questions fréquentes</a></li><li><a href="./#contact">Demande de devis</a></li><li><a href="mentions-legales.html">Mentions légales</a></li><li><a href="mentions-legales.html#confidentialite">Confidentialité</a></li></ul></div>
  </div>
  <div class="ftr-labels">
   <img class="lbl" src="{LABEL_IMG}" width="520" height="365" alt="Ministère de la Transition écologique" loading="lazy">
   {vhu_badge()}
   <p>Enlèvement d’épave en partenariat avec un centre VHU agréé ({VHU_PR}). Filière des véhicules hors d’usage réglementée par le Ministère de la Transition écologique.</p>
  </div>
  <div class="ftr-bot"><span>© {datetime.date.today().year} {NAME}</span><span>Ris-Orangis · Essonne (91)</span></div>
 </div>
</footer>
<div class="callbar"><a class="c1" href="{TEL_HREF}">{ic("phone")}<span class="num">{TEL}</span></a><a class="c2" href="sms:{TEL_E164}" aria-label="Envoyer un SMS">{ic("sms")}SMS</a></div>
<script src="assets/js/main.js?v={ver("assets/js/main.js")}" defer></script>
</body>
</html>
'''

def faq_html(faq):
    return "".join(f'<details class="qa rv" style="--i:{i}"><summary>{esc(q)}<i aria-hidden="true"></i></summary><div class="a"><p>{esc(a)}</p></div></details>' for i, (q, a) in enumerate(faq))
def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u} for i, (n, u) in enumerate(items)]}

BIZ_ID = DOMAIN + "#entreprise"
def business_ld():
    return {
     "@context": "https://schema.org", "@type": ["AutomotiveBusiness", "EmergencyService"], "@id": BIZ_ID,
     "name": NAME, "url": DOMAIN, "telephone": TEL_E164, "email": EMAIL,
     "image": DOMAIN + "og-image.jpg", "logo": DOMAIN + "favicon-512.png",
     "description": "Épaviste et dépanneur à Ris-Orangis (91) : enlèvement d’épave gratuit en partenariat avec un centre VHU agréé (PR 9100012D), dépannage automobile, remorquage, assistance routière, transport de véhicule et sortie de fourrière, 24h/24 et 7j/7 dans un rayon de 25 km.",
     "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "postalCode": CP, "addressRegion": "Île-de-France", "addressCountry": "FR"},
     "geo": {"@type": "GeoCoordinates", "latitude": LAT0, "longitude": LON0},
     "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}],
     "areaServed": [{"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": LAT0, "longitude": LON0}, "geoRadius": "25000"}] + [{"@type": "City", "name": CITY}] + [{"@type": "City", "name": t["n"]} for t in TOWNS],
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Prestations de dépannage", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["short"], "url": DOMAIN + s["slug"] + ".html"}} for s in SERVICES]},
     "knowsAbout": ["dépannage automobile", "remorquage", "enlèvement d’épave", "centre VHU", "sortie de fourrière", "transport de véhicule sur plateau"],
    }

def form_html():
    opts = "".join(f"<option>{s['name']}</option>" for s in SERVICES)
    return f'''<form class="form rv rv-r" id="quoteForm" action="https://formsubmit.co/ajax/{EMAIL}" method="post" novalidate>
 <h3 class="h-m">Demande de devis</h3>
 <p class="sub">Épave, transport, fourrière : décrivez la situation, on vous rappelle avec un prix. Pour une panne en cours, appelez directement.</p>
 <input type="hidden" name="_subject" value="Nouvelle demande de devis · site Grizzly Dépannage">
 <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
 <div class="fg">
  <div class="field"><label for="nom">Nom <em>*</em></label><input id="nom" name="nom" type="text" autocomplete="name" required><span class="err" aria-live="polite"></span></div>
  <div class="field"><label for="tel">Téléphone <em>*</em></label><input id="tel" name="telephone" type="tel" autocomplete="tel" inputmode="tel" required><span class="err" aria-live="polite"></span></div>
  <div class="field"><label for="ville">Ville</label><input id="ville" name="ville" type="text" autocomplete="address-level2" placeholder="Ex. Grigny"></div>
  <div class="field"><label for="type">Prestation</label><select id="type" name="prestation">{opts}</select></div>
  <div class="field full"><label for="msg">Votre situation</label><textarea id="msg" name="message" placeholder="Modèle du véhicule, adresse de départ et d’arrivée, état du véhicule…"></textarea></div>
 </div>
 <button class="btn btn-y btn-lg" type="submit">Recevoir mon prix {ic("arrow")}</button>
 <p class="legal">Vos coordonnées servent uniquement à vous rappeler. <a href="mentions-legales.html#confidentialite">Confidentialité</a></p>
 <div class="done" role="status">{ic("check")}<h3 class="h-m">Demande envoyée</h3><p class="lead" style="margin-inline:auto">On vous rappelle rapidement. C’est urgent ? Appelez le <a class="num" href="{TEL_HREF}">{TEL}</a>.</p></div>
</form>'''

def radar_block(focus=""):
    return f'''<div class="radar rv rv-s" data-focus="{focus}"><div class="sweep" aria-hidden="true"></div></div>
<script type="application/json" id="towns-data">{town_json()}</script>'''

def towns_bands(link_all=True):
    bands = [("Moins de 5 km", 0, 5), ("5 à 10 km", 5, 10), ("10 à 15 km", 10, 15), ("15 à 25 km", 15, 26)]
    out = [f'<div class="band"><h3>Base<i></i></h3><ul class="towns"><li><a href="./" data-slug="ris-orangis">Ris-Orangis (91130)</a></li></ul></div>']
    for lab, a, b in bands:
        li = "".join((f'<li><a href="{t["url"]}" data-slug="{t["slug"]}">{t["n"]}</a></li>' if t["page"] else f'<li><span data-slug="{t["slug"]}">{t["n"]}</span></li>') for t in TOWNS if a <= t["km"] < b)
        if li: out.append(f'<div class="band"><h3>{lab}<i></i></h3><ul class="towns">{li}</ul></div>')
    return '<div class="bands">' + "".join(out) + "</div>"

# ---------------------------------------------------------------- accueil
HOME_FAQ = [
 ("L’enlèvement d’épave est-il gratuit ?", "Oui, pour un véhicule complet, accessible au camion et accompagné de ses papiers. Le véhicule part chez notre partenaire, centre VHU agréé PR 9100012D, qui établit le certificat de destruction."),
 ("Votre centre VHU est-il agréé ?", "Oui. Grizzly Dépannage enlève et transporte le véhicule, puis le remet à son partenaire, centre VHU agréé par la préfecture sous le numéro PR 9100012D. Le centre dépollue, recycle et délivre le certificat de destruction."),
 ("Combien coûte un dépannage ou un remorquage ?", "Le prix dépend de la distance, de l’heure et de la situation. Grizzly Dépannage vous annonce le tarif au téléphone avant que la dépanneuse ne parte. Vous décidez ensuite, sans engagement."),
 ("Intervenez-vous la nuit, le week-end et les jours fériés ?", "Oui. Le téléphone répond 24h/24 et 7j/7, jours fériés compris, et la dépanneuse part à toute heure."),
 ("Dans quelles villes intervenez-vous ?", "À Ris-Orangis et dans un rayon de 25 km : Évry-Courcouronnes, Grigny, Viry-Châtillon, Juvisy-sur-Orge, Draveil, Corbeil-Essonnes, Savigny-sur-Orge, Athis-Mons, Sainte-Geneviève-des-Bois, Brétigny-sur-Orge, Montgeron, Mennecy et les communes voisines."),
 ("Intervenez-vous sur l’autoroute A6 ?", "Non. Sur autoroute, seul le dépanneur agréé du secteur peut intervenir : appelez depuis une borne orange ou le 112. Une fois le véhicule sorti de l’autoroute, on le transporte jusqu’à votre garage."),
 ("Mon assurance peut-elle prendre en charge le dépannage ?", "Souvent, oui. Si votre contrat inclut une assistance, appelez-la d’abord car certains contrats imposent leur dépanneur. Sinon, on vous remet une facture détaillée à transmettre à votre assureur."),
]
GALLERY = [("Chargement sur plateau", "Véhicule non roulant hissé au treuil", "chargement-plateau"),
           ("Épaves vues du ciel", "Direction le centre VHU agréé", "epaves-vue-aerienne"),
           ("Arrimage", "Chaque roue sanglée avant de rouler", "arrimage-roue"),
           ("Casse automobile", "La dernière étape d’un véhicule hors d’usage", "casse-auto-aerienne"),
           ("Transport de véhicule", "D’une adresse à l’autre, sur plateau", "transport-plateau"),
           ("Remorquage en ville", "Rues étroites et stationnement serré", "plateau-en-ville")]

def home():
    ld = [business_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": DOMAIN, "inLanguage": "fr-FR", "publisher": {"@id": BIZ_ID}}, faq_ld(HOME_FAQ)]
    mq = " ".join(f"<span>{t}</span>" for t in [CITY] + [x["n"] for x in TOWNS if x["km"] < 16])
    svc = "".join(f'''<a class="svc rv" style="--i:{i}" href="{s["slug"]}.html">
  <img class="bgimg" src="assets/img/photos/{s["img"]}-sm.webp" alt="" loading="lazy" width="900" height="600">
  <span class="ico">{ic(s["icon"])}</span><span class="go">{ic("arrow")}</span>
  <h3 class="h-m">{s["name"]}</h3><p>{esc(s["short"])}</p></a>''' for i, s in enumerate(SERVICES))
    def photo(i, g):
        own = f"assets/img/galerie/{i+1:02d}.webp"
        if (ROOT / own).exists():
            return f'<img src="{own}" alt="{esc(g[0])} par {NAME}" loading="lazy" width="920" height="1150">'
        return f'<span class="tag">Illustration</span><img src="assets/img/photos/{g[2]}-sm.webp" alt="{esc(g[0])} : {esc(g[1])}" loading="lazy" width="900" height="600">'
    shots = "".join(f'''<figure class="shot">
  {photo(i, g)}
  <figcaption><div><b>{g[0]}</b><span>{g[1]}</span></div><span class="idx">{i+1:02d}</span></figcaption></figure>''' for i, g in enumerate(GALLERY))
    ring = "ÉPAVE GRATUITE · DÉPANNAGE 24H/24 · RIS-ORANGIS · 25 KM · "
    return head("Enlèvement d’épave gratuit et dépannage à Ris-Orangis | Grizzly Dépannage",
                "Épaviste et dépanneur à Ris-Orangis (91) : enlèvement d’épave gratuit avec un centre VHU agréé partenaire, certificat de destruction, dépannage et remorquage 24h/24 dans un rayon de 25 km. 06 07 94 57 98.",
                "index.html", ld, og_title="Grizzly Dépannage · Enlèvement d’épave gratuit et dépannage à Ris-Orangis") + header() + f'''
<main id="main">
<section class="hero">
 <canvas class="road" aria-hidden="true"></canvas><div class="grain" aria-hidden="true"></div>
 <div class="wrap hero-grid">
  <div>
   <p class="eyebrow fade">Épaviste 24h/24 · Essonne (91)</p>
   <h1 class="h-xl"><span class="ln"><span>Enlèvement</span></span><span class="ln"><span style="--d:1">d’épave <span class="y">gratuit</span></span></span><span class="ln ln-city"><span style="--d:2"><span class="plate">{ic("pin")}à Ris-Orangis</span></span></span></h1>
   <p class="lead fade" style="--d:1">Voiture hors d’usage, accidentée ou immobilisée : on l’enlève gratuitement et on la remet à notre partenaire, centre VHU agréé, qui établit le certificat de destruction. Une panne ? Même numéro, 24h/24 : <a class="num" href="{TEL_HREF}" style="color:var(--txt);font-weight:600">{TEL}</a>.</p>
   <div class="hero-ctas fade" style="--d:2">
    <a class="btn btn-y btn-lg btn-call" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span>Faire enlever mon épave</a>
    <a class="btn btn-ghost btn-lg" href="enlevement-epave.html">Documents à préparer</a>
   </div>
   <ul class="chips fade" style="--d:3">
    <li>{ic("recycle")}Épave enlevée gratuitement</li><li>{ic("shield")}Centre VHU agréé partenaire</li><li>{ic("doc")}Certificat de destruction</li><li>{ic("clock")}Dépannage 24h/24</li>
   </ul>
  </div>
  <div class="emblem fade" style="--d:1" aria-hidden="true">
   <div class="beacon"></div>
   <svg class="txt" viewBox="0 0 400 400"><defs><path id="circ" d="M200,200 m-176,0 a176,176 0 1,1 352,0 a176,176 0 1,1 -352,0"/></defs><text><textPath href="#circ" textLength="1100" lengthAdjust="spacing">{ring}</textPath></text></svg>
   <div class="badge"><img src="assets/img/emblem-3d.webp" width="894" height="964" alt="" fetchpriority="high"></div>
  </div>
 </div>
</section>
<div class="hero-foot"><div class="tape" aria-label="Communes desservies"><div class="marquee">{mq} {mq}</div></div></div>

<section class="photoband" aria-labelledby="t-epave">
 <img class="pb-img" src="assets/img/photos/epaves-vue-aerienne.webp" alt="Vue aérienne d’épaves de voitures en attente de destruction" loading="lazy" width="2000" height="1123">
 <div class="wrap">
  <p class="eyebrow rv">Épaviste à Ris-Orangis</p>
  <h2 class="h-xl rv" id="t-epave">Votre épave part <br><span class="y">gratuitement.</span></h2>
  <p class="lead rv" style="color:#d6d6d6">Véhicule complet avec ses papiers : on l’enlève sans frais et on le remet à notre centre VHU agréé partenaire ({VHU_PR}), qui établit le certificat de destruction.</p>
  <div class="hero-ctas rv"><a class="btn btn-y btn-lg btn-call" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span>Faire enlever mon épave</a><a class="btn btn-ghost btn-lg" href="enlevement-epave.html">Documents à préparer</a></div>
 </div>
 <span class="credit">Photo d’illustration</span>
</section>
<section class="sec" aria-labelledby="t-trust">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow rv">Filière agréée</p><h2 class="h-l rv" id="t-trust">Votre épave, <span class="y">traitée dans les règles.</span></h2><p class="lead rv">La loi impose de confier un véhicule hors d’usage à un centre VHU agréé. Grizzly Dépannage l’enlève chez vous et le remet à son partenaire agréé : vous n’avez rien d’autre à gérer.</p></div></div>
  {trust_cards()}
 </div>
</section>

<section class="sec on-paper" aria-labelledby="t-steps">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow rv">En panne ?</p><h2 class="h-l rv" id="t-steps">Trois étapes, <br>pas de surprise.</h2></div></div>
  <ol class="steps" style="list-style:none;padding:0;margin:0">
   <li class="step rv" style="--i:0"><span class="n">1</span><h3 class="h-s">Vous appelez</h3><p>Au <a class="num" href="{TEL_HREF}"><b>{TEL}</b></a>. Donnez l’adresse, le véhicule et ce qui se passe.</p></li>
   <li class="step rv" style="--i:2"><span class="n">2</span><h3 class="h-s">Prix et heure d’arrivée</h3><p>On vous annonce le tarif et l’heure d’arrivée avant de partir. Vous décidez.</p></li>
   <li class="step rv" style="--i:4"><span class="n">3</span><h3 class="h-s">On s’occupe du véhicule</h3><p>Dépannage sur place quand c’est possible, sinon remorquage vers le garage ou l’adresse de votre choix.</p></li>
  </ol>
 </div>
</section>

<section class="sec" id="services" aria-labelledby="t-svc">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow rv">Nos services</p><h2 class="h-l rv" id="t-svc">Six métiers, <span class="y">un seul numéro.</span></h2><p class="lead rv">De l’épave qui encombre votre cour à la batterie à plat, Grizzly Dépannage gère toute la chaîne avec son propre camion plateau.</p></div></div>
  <div class="svc-grid">{svc}</div>
 </div>
</section>

<div class="divider" aria-hidden="true"></div>
<section class="sec on-paper" aria-labelledby="t-why">
 <div class="wrap why">
  <div>
   <p class="eyebrow rv">Pourquoi Grizzly</p>
   <h2 class="h-l rv" id="t-why">Un dépanneur local, <br>joignable pour de vrai.</h2>
   <ul class="checks">
    <li class="rv" style="--i:1">{ic("user")}<div><b>Vous parlez au dépanneur</b><span>Au bout du fil, celui qui se déplace. Pas de plateforme, pas d’intermédiaire.</span></div></li>
    <li class="rv" style="--i:2">{ic("tag")}<div><b>Prix annoncé avant le départ</b><span>Le montant est donné au téléphone. Pas de supplément découvert au moment de payer.</span></div></li>
    <li class="rv" style="--i:3">{ic("truck")}<div><b>Camion plateau</b><span>Votre véhicule voyage entièrement chargé sur le plateau, sans traîner au sol.</span></div></li>
    <li class="rv" style="--i:4">{ic("doc")}<div><b>Facture détaillée</b><span>Un document clair à transmettre à votre assurance ou à votre garage.</span></div></li>
   </ul>
  </div>
  <div class="facts">
   <div class="fact rv rv-s" style="--i:1"><b>0<em> €</em></b><span>Pour l’enlèvement d’une épave complète avec ses papiers</span></div>
   <div class="fact rv rv-s" style="--i:2"><b>24<em>/</em>7</b><span>Téléphone ouvert jour et nuit, jours fériés compris</span></div>
   <div class="fact rv rv-s" style="--i:3"><b>25<em> km</em></b><span>Rayon d’intervention autour de Ris-Orangis</span></div>
   <div class="fact rv rv-s" style="--i:4"><b>1<em> n°</em></b><span>Un numéro direct : <a class="num" href="{TEL_HREF}"><b style="font:inherit;display:inline">{TEL}</b></a></span></div>
  </div>
 </div>
</section>

<section class="gal" id="galerie" aria-labelledby="t-gal">
 <div class="gal-pin">
  <div class="wrap gal-head"><div><p class="eyebrow">Galerie</p><h2 class="h-l" id="t-gal">Le métier <span class="y">en images.</span></h2></div><p class="gal-count" aria-hidden="true"><b>01</b> / {len(GALLERY):02d}</p></div>
  <div class="gal-track">{shots}</div>
  <div class="wrap"><div class="gal-bar" aria-hidden="true"><i></i></div></div>
 </div>
</section>

<section class="sec" id="zone" style="background:var(--ink-2)" aria-labelledby="t-zone">
 <div class="wrap zone">
  {radar_block()}
  <div>
   <p class="eyebrow rv">Zone d’intervention</p>
   <h2 class="h-l rv" id="t-zone">Ris-Orangis <span class="y">et 25 km</span> autour.</h2>
   <p class="lead rv">Touchez un point de la carte pour voir sa distance depuis notre base. Votre commune n’apparaît pas ? Appelez, on vous dit tout de suite si on peut venir.</p>
   {towns_bands()}
  </div>
 </div>
</section>

<section class="sec on-paper" id="faq" aria-labelledby="t-faq">
 <div class="wrap faq">
  <div><p class="eyebrow rv">Questions fréquentes</p><h2 class="h-l rv" id="t-faq">Ce qu’on nous demande au téléphone.</h2><p class="lead rv">Une autre question ? Appelez le <a class="num" href="{TEL_HREF}" style="color:var(--ink);font-weight:700">{TEL}</a>.</p></div>
  <div class="faq-list">{faq_html(HOME_FAQ)}</div>
 </div>
</section>

<section class="sec" id="contact" aria-labelledby="t-contact">
 <div class="wrap contact">
  <div class="rv rv-l">
   <p class="eyebrow">Contact</p>
   <h2 class="h-l" id="t-contact">Urgent ? <br>Le téléphone d’abord.</h2>
   <div class="callcard" style="margin-top:32px">
    <p class="eyebrow">Urgence 24h/24 · 7j/7</p>
    <a class="tel num" href="{TEL_HREF}">{TEL}</a>
    <p>Le dépanneur vous répond et vous annonce le prix avant de partir.</p>
    <a class="btn btn-dark btn-lg btn-call" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span>Appeler maintenant</a>
   </div>
   <ul class="meta">
    <li>{ic("sms")}<span>Par SMS : <a class="num" href="sms:{TEL_E164}">{TEL}</a></span></li>
    <li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li>{ic("pin")}<span>{STREET}, <span class=num>{CP} {CITY}</span></span></li>
    <li>{ic("clock")}<span>24h/24, 7j/7, jours fériés compris</span></li>
   </ul>
  </div>
  {form_html()}
 </div>
</section>
</main>
''' + footer()

# ---------------------------------------------------------------- pages métier
def others(exclude):
    return "".join(f'<a class="other rv" style="--i:{i}" href="{s["slug"]}.html"><span class="ico">{ic(s["icon"])}</span><b>{s["name"]}</b></a>' for i, s in enumerate(x for x in SERVICES if x["slug"] != exclude))

def service_page(s):
    path = s["slug"] + ".html"
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "url": DOMAIN + path,
           "provider": {"@id": BIZ_ID, "@type": "AutomotiveBusiness", "name": NAME, "telephone": TEL_E164},
           "areaServed": [{"@type": "City", "name": CITY}] + [{"@type": "City", "name": t["n"]} for t in TOWNS if t["page"]],
           "hoursAvailable": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}},
          crumbs_ld([("Accueil", ""), (s["name"], path)]), faq_ld(s["faq"])]
    lis = lambda arr, cls="": f'<ul class="list-check {cls}">' + "".join(f'<li class="rv" style="--i:{i}">{ic("check")}<span>{esc(x)}</span></li>' for i, x in enumerate(arr)) + "</ul>"
    second = ""
    if s.get("items2"):
        second = f'<div><h2 class="h-m rv" style="margin-bottom:24px">{s["items2_title"]}</h2>{lis(s["items2"])}</div>'
    towns = "".join(f'<li><a href="{t["url"]}">{s["name"]} à {t["n"]}</a></li>' for t in TOWNS if t["page"])
    kp = s.get("kpis") or [("tag", "Prix annoncé avant le départ", "Au téléphone, sans engagement"), ("clock", "24h/24 et 7j/7", "Nuits, week-ends et jours fériés"), ("pin", "Ris-Orangis et 25 km", "Essonne, nord 77 et sud 94")]
    kpis = "".join(f'<div class="kpi rv rv-r" style="--i:{i+1}">{ic(k)}<div><b>{b}</b><span>{sp}</span></div></div>' for i, (k, b, sp) in enumerate(kp))
    trust = ""
    if s.get("trust"):
        trust = f'''<section class="sec" id="agrement" aria-labelledby="t-trust">
 <div class="wrap">
  <div class="sec-head"><div><p class="eyebrow rv">Filière agréée</p><h2 class="h-l rv" id="t-trust">Un centre agréé, <span class="y">un certificat officiel.</span></h2></div></div>
  {trust_cards()}
 </div>
</section>
'''
    return head(s["title"], s["desc"], path, ld) + header(s["slug"]) + f'''
<main id="main">
<section class="phero has-img">
 <img class="phero-img" src="assets/img/photos/{s["img"]}.webp" alt="" width="2000" height="1333" fetchpriority="high">
 <canvas class="road" aria-hidden="true"></canvas><div class="grain" aria-hidden="true"></div>
 <div class="wrap">
  <ol class="crumbs"><li><a href="./">Accueil</a></li><li><a href="./#services">Services</a></li><li aria-current="page">{s["name"]}</li></ol>
  <div class="phero-grid">
   <div>
    <p class="eyebrow rv">{s["name"]} · 24h/24 7j/7</p>
    <h1 class="h-xl rv" style="font-size:clamp(2.3rem,6vw,4.8rem)">{s["h1"][0]}<br>{s["h1"][1]}</h1>
    <p class="lead rv">{esc(s["lead"])}</p>
    <div class="hero-ctas rv"><a class="btn btn-y btn-lg btn-call" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span>Appeler le <span class="num">{TEL}</span></a><a class="btn btn-ghost btn-lg" href="./#contact">Demander un devis</a></div>
   </div>
   <div class="kpis">{kpis}</div>
  </div>
 </div>
</section>
{trust}<section class="sec on-paper">
 <div class="wrap split">
  <div><h2 class="h-m rv" style="margin-bottom:24px">{s["items_title"]}</h2>{lis(s["items"])}</div>
  {second or f'<div class="prose rv"><h2 class="h-m" style="margin-bottom:24px;color:var(--ink)">Comment ça se passe</h2><p><strong>1. Vous appelez le {TEL}.</strong> Vous donnez l’adresse, le véhicule et la situation.</p><p><strong>2. On vous annonce le prix et l’heure d’arrivée.</strong> Vous acceptez ou non, sans engagement.</p><p><strong>3. On intervient.</strong> Sur place quand c’est possible, sinon on charge le véhicule sur le plateau.</p></div>'}
 </div>
 <div class="wrap"><p class="note rv">{esc(s["note"])}</p></div>
</section>
<section class="sec" aria-labelledby="t-faq">
 <div class="wrap faq">
  <div><p class="eyebrow rv">Questions fréquentes</p><h2 class="h-l rv" id="t-faq">{s["name"]} : vos questions.</h2></div>
  <div class="faq-list on-paper" style="background:none">{faq_html(s["faq"])}</div>
 </div>
</section>
<section class="sec" style="background:var(--ink-2);padding-top:clamp(60px,8vw,100px)">
 <div class="wrap">
  <h2 class="h-m rv" style="margin-bottom:22px">{s["name"]} dans votre commune</h2>
  <ul class="towns rv">{towns}</ul>
  <h2 class="h-m rv" style="margin:64px 0 22px">Nos autres services</h2>
  <div class="others">{others(s["slug"])}</div>
 </div>
</section>
</main>
''' + footer()

# ---------------------------------------------------------------- pages ville
def town_page(t):
    path = t["url"]
    near = sorted((x for x in TOWNS if x is not t), key=lambda x: math.hypot(x["x"] - t["x"], x["y"] - t["y"]))[:6]
    axes = f" On connaît bien les accès par {t['axes']}." if t["axes"] else ""
    faq = [(f"Intervenez-vous à {t['n']} la nuit et le week-end ?", f"Oui. {t['n']} se trouve à {kmf(t['km'])} km de notre base de Ris-Orangis. Le téléphone répond 24h/24 et 7j/7, jours fériés compris."),
           (f"Combien coûte un dépannage à {t['n']} ?", f"Le prix dépend de l’heure, de la panne et de la destination du véhicule. On vous l’annonce au téléphone avant de partir pour {t['n']}, sans engagement."),
           (f"Enlevez-vous les épaves à {t['n']} ?", f"Oui. L’enlèvement d’épave est gratuit à {t['n']} pour un véhicule complet avec ses papiers. Il part chez notre partenaire, centre VHU agréé {VHU_PR}, qui établit le certificat de destruction.")]
    faq = [faq[2], faq[0], faq[1]]
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": f"Dépannage et remorquage à {t['n']}", "serviceType": "Dépannage automobile et remorquage",
           "url": DOMAIN + path, "provider": {"@id": BIZ_ID, "@type": "AutomotiveBusiness", "name": NAME, "telephone": TEL_E164},
           "areaServed": {"@type": "City", "name": t["n"], "address": {"@type": "PostalAddress", "postalCode": t["cp"], "addressLocality": t["n"], "addressCountry": "FR"}}},
          crumbs_ld([("Accueil", ""), ("Zone d’intervention", "zone-intervention.html"), (f"Dépannage {t['n']}", path)]), faq_ld(faq)]
    svc = "".join(f'<a class="other rv" style="--i:{i}" href="{s["slug"]}.html"><span class="ico">{ic(s["icon"])}</span><b>{s["name"]} à {t["n"]}</b></a>' for i, s in enumerate(SERVICES))
    nl = "".join((f'<li><a href="{x["url"]}">{x["n"]}</a></li>' if x["page"] else f'<li><span>{x["n"]}</span></li>') for x in near)
    return head(f"Épaviste et dépanneur {t['n']} ({t['cp']}) | Grizzly Dépannage",
                f"Enlèvement d’épave gratuit et dépannage à {t['n']} ({t['cp']}), à {kmf(t['km'])} km de Ris-Orangis. Centre VHU agréé partenaire, certificat de destruction. 24h/24. {TEL}.",
                path, ld) + header("zone") + f'''
<main id="main">
<section class="phero">
 <canvas class="road" aria-hidden="true"></canvas><div class="grain" aria-hidden="true"></div>
 <div class="wrap">
  <ol class="crumbs"><li><a href="./">Accueil</a></li><li><a href="zone-intervention.html">Zone d’intervention</a></li><li aria-current="page">{t["n"]}</li></ol>
  <div class="phero-grid">
   <div>
    <p class="eyebrow rv">Épaviste et dépanneur · {t["n"]} ({t["cp"]})</p>
    <h1 class="h-xl rv" style="font-size:clamp(2.2rem,5.6vw,4.6rem)">Enlèvement d’épave et dépannage <br>à <span class="y">{t["n"]}</span></h1>
    <p class="lead rv">{t["n"]} se trouve à {kmf(t["km"])} km {t["dir"]} de notre base de Ris-Orangis.{axes} Épave à faire enlever gratuitement, panne ou accident : appelez, on vous donne le prix et l’heure d’arrivée avant de partir.</p>
    <div class="hero-ctas rv"><a class="btn btn-y btn-lg btn-call" href="{TEL_HREF}"><span class="ring">{ic("phone")}</span>Appeler le <span class="num">{TEL}</span></a><a class="btn btn-ghost btn-lg" href="./#contact">Demander un devis</a></div>
   </div>
   <div class="kpis">
    <div class="kpi rv rv-r" style="--i:1">{ic("pin")}<div><b>{kmf(t["km"])} km de Ris-Orangis</b><span>Distance à vol d’oiseau depuis notre base</span></div></div>
    <div class="kpi rv rv-r" style="--i:2">{ic("clock")}<div><b>24h/24 et 7j/7</b><span>Nuits, week-ends et jours fériés</span></div></div>
    <div class="kpi rv rv-r" style="--i:3">{ic("shield")}<div><b>Épave gratuite, centre VHU agréé</b><span>Partenaire agréé {VHU_PR}</span></div></div>
   </div>
  </div>
 </div>
</section>
<section class="sec" style="background:var(--ink-2)">
 <div class="wrap zone">
  {radar_block(t["slug"])}
  <div>
   <h2 class="h-l rv">Nos services à <span class="y">{t["n"]}</span></h2>
   <div class="others" style="margin-top:28px;grid-template-columns:1fr">{svc}</div>
   <h3 class="h-s rv" style="margin:40px 0 14px">Communes voisines</h3>
   <ul class="towns rv">{nl}</ul>
  </div>
 </div>
</section>
<section class="sec on-paper" aria-labelledby="t-faq">
 <div class="wrap faq">
  <div><p class="eyebrow rv">Questions fréquentes</p><h2 class="h-l rv" id="t-faq">Dépannage à {t["n"]}</h2></div>
  <div class="faq-list">{faq_html(faq)}</div>
 </div>
</section>
</main>
''' + footer()

def zone_page():
    path = "zone-intervention.html"
    ld = [business_ld(), crumbs_ld([("Accueil", ""), ("Zone d’intervention", path)])]
    return head("Zone d’intervention : Ris-Orangis et 25 km | Grizzly Dépannage",
                f"Grizzly Dépannage intervient à Ris-Orangis et dans {len(TOWNS)} communes à moins de 25 km : Évry, Grigny, Viry-Châtillon, Corbeil-Essonnes… 24h/24. {TEL}.",
                path, ld) + header("zone") + f'''
<main id="main">
<section class="phero">
 <canvas class="road" aria-hidden="true"></canvas><div class="grain" aria-hidden="true"></div>
 <div class="wrap">
  <ol class="crumbs"><li><a href="./">Accueil</a></li><li aria-current="page">Zone d’intervention</li></ol>
  <p class="eyebrow rv">Zone d’intervention</p>
  <h1 class="h-xl rv" style="font-size:clamp(2.3rem,6vw,4.8rem)">Ris-Orangis <span class="y">et 25 km</span> autour</h1>
  <p class="lead rv">Notre base est à Ris-Orangis, au cœur de l’Essonne. De là, la dépanneuse couvre {len(TOWNS)} communes du 91, du nord de la Seine-et-Marne et du sud du Val-de-Marne.</p>
 </div>
</section>
<section class="sec" style="background:var(--ink-2)">
 <div class="wrap zone">{radar_block()}<div>{towns_bands()}</div></div>
</section>
</main>
''' + footer()

def legal_page():
    T = '<span class="todo">à compléter</span>'
    return head("Mentions légales et confidentialité | Grizzly Dépannage", "Mentions légales et politique de confidentialité du site Grizzly Dépannage, Ris-Orangis.", "mentions-legales.html") + header() + f'''
<main id="main" class="legal-page">
<section class="phero"><div class="wrap"><ol class="crumbs"><li><a href="./">Accueil</a></li><li aria-current="page">Mentions légales</li></ol><h1 class="h-l">Mentions légales</h1></div></section>
<section class="sec"><div class="wrap prose">
<h2>Éditeur du site</h2>
<p>{NAME}<br>{STREET}, {CP} {CITY}<br>Téléphone : {TEL} · Courriel : {EMAIL}<br>Forme juridique : {T}<br>SIRET : {T}<br>Numéro de TVA : {T}<br>Directeur de la publication : {T}</p>
<h2>Assurance professionnelle</h2>
<p>Assureur et numéro de contrat : {T}</p>
<h2>Hébergement</h2>
<p>GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, logos et visuels de ce site appartiennent à {NAME}. Toute reproduction sans autorisation est interdite.</p>
<h2 id="confidentialite">Confidentialité</h2>
<p>Le formulaire de devis collecte votre nom, votre téléphone, votre ville et votre message. Ces données servent uniquement à vous rappeler et à établir un devis. Elles transitent par le service FormSubmit et arrivent dans la boîte mail de {NAME}. Elles ne sont ni vendues ni cédées, et sont supprimées au plus tard trois ans après le dernier contact.</p>
<p>Vous pouvez demander l’accès, la rectification ou la suppression de vos données à {EMAIL}. Vous pouvez aussi saisir la CNIL (cnil.fr).</p>
<p>Ce site n’utilise pas de cookie de suivi publicitaire.</p>
</div></section>
</main>
''' + footer()

def page_404():
    return head("Page introuvable | Grizzly Dépannage", "Cette page n’existe pas.", "404.html") + header() + f'''
<main id="main"><section class="phero" style="min-height:80svh;display:flex;align-items:center"><canvas class="road" aria-hidden="true"></canvas>
<div class="wrap"><p class="eyebrow">Erreur 404</p><h1 class="h-xl">Mauvaise sortie.</h1><p class="lead">Cette page n’existe pas. Votre véhicule, lui, on peut aller le chercher.</p>
<div class="hero-ctas"><a class="btn btn-y btn-lg" href="{TEL_HREF}">{ic("phone")}{TEL}</a><a class="btn btn-ghost btn-lg" href="./">Retour à l’accueil</a></div></div></section></main>''' + footer()

# ---------------------------------------------------------------- fichiers annexes
def llms():
    svc = "\n".join(f"- [{s['name']}]({DOMAIN}{s['slug']}.html) : {s['short']}" for s in SERVICES)
    towns = ", ".join(f"{t['n']} ({t['cp']}, {kmf(t['km'])} km)" for t in TOWNS)
    faq = "\n".join(f"- **{q}** {a}" for q, a in HOME_FAQ)
    return f"""# {NAME} : dépanneur à Ris-Orangis (91)

> {NAME} est un épaviste et dépanneur basé à Ris-Orangis (91130, Essonne). Il intervient 24h/24 et 7j/7 dans un rayon de 25 km : enlèvement d’épave gratuit en partenariat avec un centre VHU agréé ({VHU_PR}), dépannage sur place, remorquage sur plateau, assistance routière, transport de véhicule et sortie de fourrière. Le prix est annoncé au téléphone avant le départ. Téléphone : {TEL}.

## Coordonnées
- Nom : {NAME}
- Adresse : {STREET}, {CP} {CITY}, France
- Téléphone : {TEL} ({TEL_E164})
- Courriel : {EMAIL}
- Site : {DOMAIN}
- Horaires : 24h/24, 7j/7, jours fériés compris
- Zone : 25 km autour de Ris-Orangis (Essonne, nord de la Seine-et-Marne, sud du Val-de-Marne)

## Services
{svc}

## Ce qu’il faut savoir
- Le tarif est annoncé au téléphone avant le départ de la dépanneuse, sans engagement.
- L’enlèvement d’épave est gratuit pour un véhicule complet avec ses papiers ; le véhicule est remis au centre VHU agréé partenaire ({VHU_PR}), qui délivre le certificat de destruction. Filière réglementée par le Ministère de la Transition écologique.
- {NAME} n’intervient pas sur l’autoroute A6 : la loi y réserve le dépannage aux dépanneurs agréés (borne orange ou 112).

## Communes desservies (distance depuis Ris-Orangis)
{towns}

## Questions fréquentes
{faq}
"""

def sitemap(paths):
    urls = "".join(f"<url><loc>{DOMAIN}{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

if __name__ == "__main__":
    out = {"index.html": home(), "zone-intervention.html": zone_page(), "mentions-legales.html": legal_page(), "404.html": page_404()}
    for s in SERVICES: out[s["slug"] + ".html"] = service_page(s)
    for t in TOWNS:
        if t["page"]: out[t["url"]] = town_page(t)
    for p, c in out.items(): (ROOT / p).write_text(c, encoding="utf-8")
    paths = [("index.html", "1.0")] + [(s["slug"] + ".html", "0.9") for s in SERVICES] + [("zone-intervention.html", "0.8")] + [(t["url"], "0.7") for t in TOWNS if t["page"]] + [("mentions-legales.html", "0.2")]
    (ROOT / "sitemap.xml").write_text(sitemap(paths), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}sitemap.xml\n", encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms(), encoding="utf-8")
    print(f"{len(out)} pages, {len(TOWNS)} communes")
