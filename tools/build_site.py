#!/usr/bin/env python3
"""Generates the static pages of the ביסטרו נמל demo site.

Edit the data below and run `python3 tools/build_site.py`. Never hand-edit the HTML.
The site is read by Vocaly's website auto-discovery, so keep the text rules in README.md.
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent

# Photos: free Unsplash photos, served from the Unsplash CDN.
PHOTOS = {
    "hero": "photo-1586153464906-c4c3833ebe1e",       # terrace over the sea
    "about_main": "photo-1601065700897-d9fa1c093f3e", # bright dining room
    "about_small": "photo-1772352214475-12f9a75618d8",# table by the water
    "dish_fish": "photo-1644784643137-b9073dd262f6",
    "dish_pasta": "photo-1539586345401-51d5bfba7ac0",
    "dish_salad": "photo-1606735584785-1848fdcaea57",
    "cta": "photo-1672636401225-ec3d4025a4af",        # wine and dishes on a table
    "menu_hero": "photo-1606850780554-b55ea4dd0b70",  # seafood board
    "branches_hero": "photo-1643800244690-bf7c6d749b9b",
    "faq_hero": "photo-1664547654523-24e8a9121988",   # beach terrace
    "contact_hero": "photo-1699568290058-de7b14d26f37", # marina at sunset
    "g_focaccia": "photo-1619452357216-e88ca8119eeb",
    "g_pasta": "photo-1672636402078-4b957a572e4e",
    "g_salad": "photo-1599021419847-d8a7a6aba5b4",
    "g_tart": "photo-1519915028121-7d3463d20b13",
    "b_tlv": "photo-1636405189493-181ecf851006",
    "b_haifa": "photo-1684923087005-4469d0503b52",
    "b_herzliya": "photo-1584632252106-cf92568799c8",
}


def photo(key, w=1200, h=None):
    size = f"&w={w}" + (f"&h={h}" if h else "")
    return f"https://images.unsplash.com/{PHOTOS[key]}?auto=format&fit=crop&q=72{size}"


def img(key, alt, w=900, h=None, cls="", eager=False):
    c = f' class="{cls}"' if cls else ""
    loading = "eager" if eager else "lazy"
    return f'<img{c} src="{photo(key, w, h)}" alt="{alt}" loading="{loading}" decoding="async">'


ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "menu": '<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/>',
    "arrow": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
    "map": '<polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/>',
    "anchor": '<circle cx="12" cy="5" r="3"/><line x1="12" y1="22" x2="12" y2="8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/>',
}


def icon(name, size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg viewBox="0 0 24 24"{s} fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


BRAND_MARK = '''<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
  <circle cx="20" cy="20" r="18.5" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="20" cy="12.5" r="2.4" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <path d="M20 15v15M15 19h10M11.5 24.5a8.5 8.5 0 0 0 17 0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
</svg>'''

NAV = [
    ("index.html", "בית"),
    ("menu.html", "תפריט"),
    ("branches.html", "סניפים"),
    ("faq.html", "שאלות נפוצות"),
    ("contact.html", "צור קשר ומשלוחים"),
]

MAIN_PHONE = "03-7770100"


def tel(num):
    return "tel:" + num.replace("-", "")


def header(active):
    items = "\n".join(
        f'          <li><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>'
        for href, label in NAV)
    return f'''<a class="skip-link" href="#main">דילוג לתוכן הראשי</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="ביסטרו נמל, לדף הבית">
        {BRAND_MARK}
        <span class="brand-name">ביסטרו נמל</span>
      </a>
      <input class="nav-toggle" type="checkbox" id="nav-toggle" aria-label="פתיחה וסגירה של הניווט">
      <label class="nav-toggle-label" for="nav-toggle" aria-hidden="true">{icon("menu", 26)}</label>
      <nav class="main-nav" aria-label="ניווט ראשי">
        <ul>
{items}
        </ul>
      </nav>
      <a class="btn btn-light btn-sm header-cta" href="{tel(MAIN_PHONE)}">הזמנת מקום</a>
    </div>
  </header>'''


def footer():
    links = "\n".join(f'            <li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="index.html">{BRAND_MARK}<span class="brand-name">ביסטרו נמל</span></a>
          <p>מטבח ים תיכוני על קו המים. דגים טריים, ירקות מהשוק ויין טוב, בשלושה נמלים לאורך החוף.</p>
        </div>
        <div>
          <h2>ניווט</h2>
          <ul>
{links}
          </ul>
        </div>
        <div>
          <h2>דברו איתנו</h2>
          <ul>
            <li>מוקד הזמנות <a href="{tel(MAIN_PHONE)}"><span class="ltr nums">{MAIN_PHONE}</span></a></li>
            <li>דוא״ל <a href="mailto:hello@bistro-namal.example"><span class="ltr">hello@bistro-namal.example</span></a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2026 ביסטרו נמל. כל הזכויות שמורות.</p>
        <p>אתר הדגמה. המסעדה והפרטים באתר בדיוניים.</p>
      </div>
    </div>
  </footer>'''


def page(filename, title, description, body, extra_head="", preload=None):
    pre = f'\n  <link rel="preload" as="image" href="{preload}">' if preload else ""
    html = f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#0f1d28">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&amp;family=Frank+Ruhl+Libre:wght@400;500;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">{pre}{extra_head}
</head>
<body>
  {header(filename)}
  <main id="main">
{body}
  </main>
  {footer()}
</body>
</html>
'''
    (OUT / filename).write_text(html, encoding="utf-8")


def page_hero(key, eyebrow, title, lead):
    return f'''    <section class="page-hero" style="--bg: url('{photo(key, 1800)}')">
      <div class="container">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>'''


def qa_item(q, a):
    return f'''          <article class="qa">
            <h3><span class="qa-label">שאלה:</span> {q}</h3>
            <p><span class="qa-label">תשובה:</span> {a}</p>
          </article>'''


# ---------------------------------------------------------------- data

BRANCHES = [
    {
        "name": "סניף נמל תל אביב",
        "short": "נמל תל אביב",
        "address": "האנגר 12 בנמל תל אביב",
        "city": "תל אביב",
        "phone": "03-7770101",
        "kosher": "המסעדה אינה כשרה",
        "hours": [("ראשון עד חמישי", "12:00–23:30"), ("שישי", "11:00–00:00"), ("שבת", "11:00–23:30")],
        "note": "מרפסת מול הים, חדר אירועים פרטי עד 60 סועדים",
        "street": "האנגר 12, נמל תל אביב",
    },
    {
        "name": "סניף נמל חיפה",
        "short": "נמל חיפה",
        "address": "דרך העצמאות 54 במתחם הנמל",
        "city": "חיפה",
        "phone": "04-7770202",
        "kosher": "המסעדה אינה כשרה",
        "hours": [("ראשון עד חמישי", "12:00–23:00"), ("שישי", "12:00–17:00"), ("שבת", "19:00–23:00")],
        "note": "ישיבה פנימית וחיצונית, נוף לרציף הדייגים",
        "street": "דרך העצמאות 54, חיפה",
    },
    {
        "name": "סניף מרינה הרצליה",
        "short": "מרינה הרצליה",
        "address": "רציף 3 במרינה הרצליה",
        "city": "הרצליה",
        "phone": "09-7770303",
        "kosher": "המסעדה אינה כשרה",
        "hours": [("ראשון עד שבת", "12:00–23:00")],
        "note": "מרפסת על המזח, ידידותי לכלבים בישיבה בחוץ",
        "street": "רציף 3, מרינה הרצליה",
    },
]

MENU = [
    ("starters", "פתיחים", "לחלוק במרכז השולחן", [
        ("פוקאצ׳ת הבית", 32, "מהטאבון, עם שמן זית כתית, מלח ים ושום קונפי", ["vegan"]),
        ("מטבוחה ופלפלים קלויים", 28, "עגבניות מבושלות לאט, פלפלים חריפים קלויים ולחם חם", ["vegan"]),
        ("סביצ׳ה דג ים", 62, "דג ים טרי, ליים, צ׳ילי ירוק, בצל סגול וכוסברה", ["gf"]),
        ("קלמרי פריך", 56, "טבעות קלמרי בציפוי קל, איולי לימון ועשבי תיבול", []),
        ("קרפצ׳יו סלק", 42, "סלק אפוי, טחינה, אגוזי מלך קלויים ושמן זית", ["vegan", "gf"]),
        ("חציל על האש", 38, "חציל שרוף, יוגורט עזים, סילאן ושקדים קלויים", ["veg", "gf"]),
    ]),
    ("salads", "סלטים", "ירקות מהשוק של הבוקר", [
        ("סלט הנמל", 54, "עלים, עגבניות שרי, מלפפון, צנונית, פטה ושמן זית לימוני", ["veg", "gf"]),
        ("טבולה ירוקה", 46, "בורגול, פטרוזיליה, נענע, עגבנייה ולימון", ["vegan"]),
        ("סלט עגבניות ובצל סגול", 44, "עגבניות עונה, בצל סגול, סומק ושמן זית", ["vegan", "gf"]),
        ("סלט קינואה ופטה", 52, "קינואה, עדשים שחורות, פטה, רימון ועשבים", ["veg", "gf"]),
    ]),
    ("seafood", "דגים ופירות ים", "הדגים מגיעים מהדייגים בכל בוקר", [
        ("דניס שלם על הגריל", 118, "דניס שלם, לימון שרוף, שמן זית ותפוחי אדמה צלויים", ["gf"]),
        ("פילה לברק בחמאת לימון", 112, "פילה לברק צרוב, חמאת לימון וצלפים, ירקות ירוקים", ["gf"]),
        ("שרימפס בחמאה ושום", 98, "שרימפס במחבת, חמאה, שום, צ׳ילי ויין לבן, עם לחם", []),
        ("מולים ביין לבן", 88, "מולים טריים, יין לבן, שמנת ועשבים", [], True),
        ("פירות ים במחבת", 136, "שרימפס, קלמרי ומולים בחמאת עגבניות ושום", []),
        ("פיש אנד צ׳יפס", 84, "פילה דג לבן בבלילת בירה, צ׳יפס ורוטב טרטר", []),
    ]),
    ("mains", "עיקריות", "מהגריל ומהתנור", [
        ("סטייק אנטריקוט", 158, "300 גרם אנטריקוט מיושן, חמאת עשבים ותפוחי אדמה", ["gf"]),
        ("חזה עוף על הגריל", 84, "חזה עוף במרינדת לימון ושום, פירה ושעועית ירוקה", ["gf"]),
        ("קבב טלה על האש", 92, "קבב טלה, טחינה, סלט עגבניות ופיתה מהטאבון", []),
        ("המבורגר ביסטרו", 78, "קציצת בקר 250 גרם, איולי, חסה ועגבנייה, עם צ׳יפס", []),
        ("ריזוטו פטריות", 74, "אורז ארבוריו, פטריות יער, פרמזן ושמן כמהין", ["veg", "gf"]),
    ]),
    ("pasta", "פסטות", "פסטה טרייה מהמטבח שלנו", [
        ("לינגוויני פירות ים", 96, "שרימפס, קלמרי ומולים, עגבניות שרי, שום ויין לבן", []),
        ("ניוקי ברוטב עגבניות", 68, "ניוקי תפוחי אדמה, רוטב עגבניות, בזיליקום ופרמזן", ["veg"]),
        ("טליאטלה שמנת ופטריות", 72, "פטריות, שמנת, טימין ופרמזן", ["veg"]),
        ("רביולי בטטה", 74, "רביולי במילוי בטטה, חמאת מרווה ואגוזי לוז", ["veg"]),
    ]),
    ("desserts", "קינוחים", "סיום מתוק", [
        ("מלבי מי ורדים", 34, "מלבי, סירופ מי ורדים, פיסטוקים וקוקוס", ["veg", "gf"]),
        ("טארט לימון", 42, "בצק פריך, קרם לימון ומרנג שרוף", ["veg"]),
        ("פונדנט שוקולד", 46, "פונדנט חם עם כדור גלידת וניל", ["veg"]),
        ("סורבה פירות", 36, "שלושה כדורי סורבה עונתיים", ["vegan", "gf"]),
    ]),
    ("drinks", "שתייה ויין", "משקאות קלים, קפה, בירה ויין", [
        ("לימונדה נענע", 18, "לימונים סחוטים, נענע וקרח", ["vegan", "gf"]),
        ("מים מינרליים", 14, "בקבוק 750 מ״ל, מוגזים או רגילים", ["vegan", "gf"]),
        ("קולה או קולה זירו", 14, "בקבוק זכוכית 330 מ״ל", ["vegan", "gf"]),
        ("אספרסו", 12, "כפול, מפולי קפה שנקלים במיוחד עבורנו", ["vegan", "gf"]),
        ("בירה מהחבית", 32, "חצי ליטר, בירה ישראלית מתחלפת", ["vegan"]),
        ("כוס יין לבן של הבית", 38, "סוביניון בלאן מהגליל", ["vegan", "gf"]),
        ("בקבוק יין אדום של הבית", 160, "קברנה סוביניון מהגולן", ["vegan", "gf"]),
    ]),
]

TAGS = {
    "vegan": ("tag-vegan", "טבעוני"),
    "gf": ("tag-gf", "ללא גלוטן"),
    "veg": ("tag-veg", "צמחוני"),
}

FAQ = [
    ("calendar", "הזמנות וביטולים", [
        ("האם צריך להזמין מקום מראש?",
         f"מומלץ מאוד, בעיקר בחמישי עד שבת בערב. אפשר להזמין במוקד ההזמנות במספר {MAIN_PHONE} או ישירות מול כל אחד מהסניפים. "
         "שולחן שהוזמן נשמר 15 דקות משעת ההזמנה."),
        ("מה מדיניות הביטול?",
         "אפשר לבטל או לשנות הזמנה ללא עלות עד 4 שעות לפני מועד ההגעה. בהזמנות של 10 סועדים ומעלה יש לבטל עד 24 שעות מראש."),
        ("אתם מארחים אירועים וקבוצות?",
         "כן. בנמל תל אביב יש חדר אירועים פרטי עד 60 סועדים, ובשאר המסעדות אפשר לסגור את המרפסת לקבוצות של עד 30 סועדים. "
         "לתיאום אירוע פנו למוקד ההזמנות."),
    ]),
    ("truck", "משלוחים ואיסוף עצמי", [
        ("האם יש משלוחים?",
         "כן. אנחנו שולחים מנמל תל אביב וממרינה הרצליה, בימים ראשון עד חמישי בין 12:00 ל־22:00. "
         "מזמינים בטלפון במוקד ההזמנות. מינימום הזמנה למשלוח 120 שקלים ודמי המשלוח 15 שקלים."),
        ("כמה זמן לוקח משלוח?",
         "בדרך כלל בין 40 ל־60 דקות, תלוי באזור ובעומס. בזמן ההזמנה נמסור לכם זמן משוער."),
        ("אפשר להזמין לאיסוף עצמי?",
         "כן, מכל שלוש המסעדות. מזמינים בטלפון ואוספים מהדלפק בכניסה, בדרך כלל תוך 25 דקות."),
    ]),
    ("leaf", "אוכל ותזונה", [
        ("האם המסעדה כשרה?",
         "לא. ביסטרו נמל אינה כשרה ופתוחה גם בשבת, והתפריט כולל פירות ים."),
        ("יש מנות טבעוניות או ללא גלוטן?",
         "כן. בתפריט מסומנות מנות טבעוניות, צמחוניות וללא גלוטן, ורבות מהמנות אפשר להתאים לפי בקשה. "
         "חשוב לדעת שהמטבח אינו סטרילי מגלוטן."),
        ("יש תפריט ילדים?",
         "כן. ארוחת ילדים כוללת שניצלונים, פסטה או דג קטן עם תוספת ושתייה קלה, במחיר 48 שקלים."),
    ]),
    ("pin", "הגעה ונגישות", [
        ("איפה חונים?",
         "בנמל תל אביב יש חניון בתשלום צמוד למסעדה. בחיפה חונים בחניון מתחם הנמל, ובהרצליה בחניון המרינה. בכל המקומות אפשר להגיע גם באופניים."),
        ("האם המסעדות נגישות?",
         "כן. כל שלוש המסעדות נגישות לכיסאות גלגלים, כולל שירותי נכים ושולחנות בגובה מותאם."),
        ("אפשר להגיע עם כלב?",
         "כן, כלבים מוזמנים בישיבה בחוץ בכל המסעדות. נשמח להביא קערת מים."),
    ]),
    ("card", "תשלום ומתנות", [
        ("אילו אמצעי תשלום אתם מקבלים?",
         "כרטיסי אשראי, מזומן וארנקים דיגיטליים בטלפון. אין אפשרות לתשלום בצ׳ק."),
        ("יש כרטיסי מתנה?",
         "כן. אפשר לרכוש כרטיס מתנה בכל סכום במסעדות או בטלפון במוקד ההזמנות, והוא תקף לשנה מיום הרכישה בכל המסעדות."),
    ]),
]

FACTS = [
    ("חניה", "חניון נמל תל אביב צמוד למסעדה, חניון מתחם הנמל בחיפה וחניון המרינה בהרצליה"),
    ("נגישות", "כל המסעדות נגישות לכיסאות גלגלים, כולל שירותי נכים"),
    ("אמצעי תשלום", "כרטיסי אשראי, מזומן וארנקים דיגיטליים"),
    ("הזמנת מקום", f"במוקד ההזמנות {MAIN_PHONE}, ראשון עד שבת בין 10:00 ל־22:00"),
    ("אירועים וקבוצות", "חדר אירועים פרטי עד 60 סועדים בנמל תל אביב, מרפסות לקבוצות עד 30 סועדים"),
    ("ישיבה בחוץ", "מרפסת מול הים בכל המסעדות, עם חימום בחורף"),
    ("כלבים", "מוזמנים בישיבה בחוץ"),
    ("תפריט ילדים", "ארוחת ילדים במחיר 48 שקלים"),
    ("כרטיסי מתנה", "בכל סכום, תקפים לשנה בכל המסעדות"),
]

DELIVERY = [
    ("משלוחים מנמל תל אביב", ["תל אביב–יפו (צפון ומרכז העיר)", "רמת גן", "גבעתיים"]),
    ("משלוחים ממרינה הרצליה", ["הרצליה", "רעננה", "כפר סבא"]),
]

DELIVERY_FACTS = [
    ("ימים ושעות משלוח", "ראשון עד חמישי, 12:00 עד 22:00"),
    ("מינימום הזמנה למשלוח", "120 שקלים"),
    ("דמי משלוח", "15 שקלים"),
    ("זמן משלוח משוער", "40 עד 60 דקות"),
    ("איסוף עצמי", "מכל שלוש המסעדות, בדרך כלל תוך 25 דקות"),
    ("משלוחים מחיפה", "המסעדה בחיפה אינה מבצעת משלוחים, רק איסוף עצמי"),
]


BRANCH_PHOTOS = {"נמל תל אביב": "b_tlv", "נמל חיפה": "b_haifa", "מרינה הרצליה": "b_herzliya"}

# ---------------------------------------------------------------- index

FAQ_TEASER = qa_item(*FAQ[0][2][0]) + "\n" + qa_item(*FAQ[1][2][0])

home = f'''    <section class="hero" style="--bg: url('{photo("hero", 2000)}')">
      <div class="container hero-inner">
        <span class="eyebrow">מטבח ים תיכוני על קו המים</span>
        <h1>ביסטרו נמל</h1>
        <p class="hero-lead">דגים טריים מהדייגים של הבוקר, ירקות מהשוק ויין טוב, עם הרגליים כמעט במים. שלוש מסעדות בנמל תל אביב, בנמל חיפה ובמרינה הרצליה.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="menu.html">לתפריט המלא{icon("arrow")}</a>
          <a class="btn btn-ghost" href="branches.html">הסניפים שלנו</a>
        </div>
        <ul class="hero-points" aria-label="בקיצור">
          <li>דגים טריים בכל בוקר</li>
          <li>מרפסת מול הים</li>
          <li>משלוחים ואיסוף עצמי</li>
        </ul>
      </div>
    </section>

    <section class="section" id="about" aria-labelledby="about-title">
      <div class="container about">
        <div class="about-text">
          <span class="eyebrow">אודות</span>
          <h2 id="about-title">ביסטרו קטן שהתחיל ברציף</h2>
          <p class="intro">ביסטרו נמל נפתח בשנת 2014 בהאנגר ישן בנמל תל אביב, עם שישה שולחנות ותפריט שנכתב כל בוקר על לוח לפי מה שהדייגים הביאו.</p>
          <p>היום יש לנו שלוש מסעדות לאורך החוף, והרעיון נשאר אותו רעיון. אוכל פשוט, טרי ומדויק, שירות חם ונינוח ונוף פתוח לים.</p>
          <p>השף והבעלים, יואב לוי, מבשל מטבח ים תיכוני עם השפעות מהמטבח הצפון אפריקאי והאיטלקי. הלחם נאפה אצלנו בטאבון, הפסטה נעשית במקום, ואת רשימת היין אנחנו בונים עם יקבים קטנים מהגליל ומהגולן.</p>
          <p class="signature">יואב לוי, שף ובעלים</p>
        </div>
        <div class="about-photos">
          {img("about_main", "חדר האוכל המואר של ביסטרו נמל", 900, 1100, "ph-main")}
          {img("about_small", "שולחן ערוך מול הים", 600, 600, "ph-small")}
        </div>
      </div>
    </section>

    <section class="facts-band" aria-labelledby="facts-title">
      <div class="container">
        <div class="facts-head">
          <span class="eyebrow">בקצרה</span>
          <h2 id="facts-title">מה כדאי לדעת</h2>
        </div>
        <ul class="facts">
          <li><span class="fact-label">שם העסק:</span> ביסטרו נמל</li>
          <li><span class="fact-label">תיאור:</span> מסעדת דגים ומטבח ים תיכוני עם שלוש מסעדות על קו המים, בנמל תל אביב, בנמל חיפה ובמרינה הרצליה</li>
          <li><span class="fact-label">סוג מטבח:</span> ים תיכוני, דגים ופירות ים</li>
          <li><span class="fact-label">טווח מחירים:</span> מנות עיקריות בין 68 ל־158 שקלים</li>
          <li><span class="fact-label">משלוחים:</span> מנמל תל אביב וממרינה הרצליה, מינימום הזמנה 120 שקלים</li>
          <li><span class="fact-label">נגישות:</span> כל המסעדות נגישות לכיסאות גלגלים</li>
          <li><span class="fact-label">חניה:</span> חניון צמוד או סמוך בכל אחד מהנמלים</li>
          <li><span class="fact-label">אמצעי תשלום:</span> כרטיסי אשראי, מזומן וארנקים דיגיטליים</li>
          <li><span class="fact-label">מוקד הזמנות:</span> <a href="{tel(MAIN_PHONE)}"><span class="ltr nums">{MAIN_PHONE}</span></a></li>
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="dishes-title">
      <div class="container">
        <div class="section-head section-head-split">
          <div>
            <span class="eyebrow">מהמטבח</span>
            <h2 id="dishes-title">המנות שאהובות עלינו</h2>
          </div>
          <a class="link-arrow" href="menu.html">לכל התפריט{icon("arrow")}</a>
        </div>
        <div class="dishes">
          <article class="dish">
            <div class="dish-photo">{img("dish_fish", "דג שלם צלוי על הגריל", 700, 860)}</div>
            <h3>דניס שלם על הגריל</h3>
            <p>דניס שלם מהדייגים, לימון שרוף ושמן זית, עם תפוחי אדמה צלויים.</p>
          </article>
          <article class="dish">
            <div class="dish-photo">{img("dish_pasta", "לינגוויני עם פירות ים", 700, 860)}</div>
            <h3>לינגוויני פירות ים</h3>
            <p>שרימפס, קלמרי ומולים עם עגבניות שרי, שום ויין לבן.</p>
          </article>
          <article class="dish">
            <div class="dish-photo">{img("dish_salad", "סלט ירקות עם גבינת פטה", 700, 860)}</div>
            <h3>סלט הנמל</h3>
            <p>עלים, עגבניות שרי, צנונית ופטה בשמן זית לימוני.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="faq-teaser-title">
      <div class="container narrow">
        <div class="section-head">
          <span class="eyebrow">לפני שמגיעים</span>
          <h2 id="faq-teaser-title">השאלות שהכי הרבה שואלים אותנו</h2>
        </div>
        <div class="qa-list">
{FAQ_TEASER}
        </div>
        <a class="link-arrow" href="faq.html">לכל השאלות והתשובות{icon("arrow")}</a>
      </div>
    </section>

    <section class="cta-band" style="--bg: url('{photo("cta", 1800)}')" aria-label="הזמנת מקום">
      <div class="container">
        <span class="eyebrow">הזמנת מקום</span>
        <h2>שומרים לכם שולחן מול הים</h2>
        <p>מוקד ההזמנות פתוח בכל יום, מ־10 בבוקר ועד 10 בלילה</p>
        <a class="btn btn-primary" href="{tel(MAIN_PHONE)}">{icon("phone")}<span class="ltr nums">{MAIN_PHONE}</span></a>
      </div>
    </section>
'''

jsonld = {
    "@context": "https://schema.org",
    "@type": "Restaurant",
    "name": "ביסטרו נמל",
    "description": "מסעדת דגים ומטבח ים תיכוני עם שלוש מסעדות על קו המים",
    "servesCuisine": ["ים תיכוני", "דגים ופירות ים"],
    "telephone": "+972-3-7770100",
    "email": "hello@bistro-namal.example",
    "priceRange": "₪₪",
    "acceptsReservations": True,
    "department": [
        {"@type": "Restaurant", "name": b["name"], "telephone": b["phone"],
         "address": {"@type": "PostalAddress", "streetAddress": b["street"], "addressLocality": b["city"], "addressCountry": "IL"}}
        for b in BRANCHES
    ],
}
page("index.html", "ביסטרו נמל | מטבח ים תיכוני על קו המים",
     "ביסטרו נמל, מסעדת דגים ומטבח ים תיכוני בנמל תל אביב, בנמל חיפה ובמרינה הרצליה.",
     home,
     extra_head='\n  <script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>",
     preload=photo("hero", 2000))

# ---------------------------------------------------------------- menu

chips = "\n".join(f'          <a class="chip" href="#{cid}">{title}</a>' for cid, title, _, _ in MENU)
sections = []
for cid, title, sub, items in MENU:
    lis = []
    for it in items:
        name, price, desc, tags = it[:4]
        out = len(it) > 4 and it[4]
        tag_html = "".join(f'<span class="tag {TAGS[t][0]}">{TAGS[t][1]}</span>' for t in tags)
        if out:
            tag_html = '<span class="tag tag-out">לא זמין כרגע</span>' + tag_html
        lis.append(f'''          <li class="menu-item{" is-out" if out else ""}">
            <div class="item-head"><h3 class="item-name">{name}</h3><span class="item-dots" aria-hidden="true"></span><span class="item-price" dir="ltr">{price} ₪</span></div>
            <p class="item-desc">{desc}{tag_html}</p>
          </li>''')
    sections.append(f'''        <section class="menu-section" id="{cid}" aria-labelledby="{cid}-title">
          <div class="menu-section-head"><h2 id="{cid}-title">{title}</h2><p>{sub}</p></div>
          <ul class="menu-list">
{chr(10).join(lis)}
          </ul>
        </section>''')

gallery = "".join(
    f'<figure class="g-item">{img(k, alt, 600, 600)}</figure>'
    for k, alt in [("g_focaccia", "פוקאצ׳ה מהטאבון"), ("g_pasta", "פסטה עם פירות ים"),
                   ("g_salad", "סלט עם עגבניות"), ("g_tart", "טארט לימון")])

menu_body = f'''{page_hero("menu_hero", "התפריט", "התפריט שלנו", "מטבח ים תיכוני שמשתנה מעט לפי העונה ולפי מה שהדייגים מביאים. אותו תפריט בכל שלוש המסעדות, וגם במשלוח.")}
    <nav class="menu-nav" aria-label="קטגוריות בתפריט">
      <div class="container">
        <div class="chips">
{chips}
        </div>
      </div>
    </nav>
    <div class="section">
      <div class="container">
        <div class="menu-sheet">
{chr(10).join(sections)}
          <div class="legend" aria-label="מקרא">
            <span><span class="tag tag-vegan">טבעוני</span> ללא מוצרים מן החי</span>
            <span><span class="tag tag-veg">צמחוני</span> ללא בשר ודגים</span>
            <span><span class="tag tag-gf">ללא גלוטן</span> המטבח אינו סטרילי מגלוטן</span>
          </div>
          <p class="menu-note">המחירים בשקלים וכוללים מע״מ. אם יש לכם אלרגיה או רגישות למזון, ספרו לנו כשאתם מזמינים.</p>
        </div>
        <div class="gallery" aria-hidden="true">{gallery}</div>
      </div>
    </div>
'''
page("menu.html", "התפריט | ביסטרו נמל",
     "התפריט המלא של ביסטרו נמל עם מחירים, פתיחים, דגים ופירות ים, עיקריות, פסטות, קינוחים ושתייה.",
     menu_body, preload=photo("menu_hero", 1800))

# ---------------------------------------------------------------- branches

cards = []
for b in BRANCHES:
    hours = '<span class="sep"> · </span>'.join(
        f'<span class="day"><span>{d}</span><span class="t">{t}</span></span>'
        for d, t in b["hours"])
    facts_line = (
        f'<span class="b-name">{b["name"]}</span><span class="sep">, </span>'
        f'<span class="row">{icon("pin")}<span class="v" data-k="כתובת">{b["address"]}</span></span><span class="sep">, </span>'
        f'<span class="row">{icon("map")}<span class="v" data-k="עיר">{b["city"]}</span></span><span class="sep">, </span>'
        f'<span class="row">{icon("phone")}<span class="v" data-k="טלפון"><a href="{tel(b["phone"])}"><span class="ltr nums">{b["phone"]}</span></a></span></span><span class="sep">, </span>'
        f'<span class="row">{icon("utensils")}<span class="v"><span class="k">כשרות</span> {b["kosher"]}</span></span><span class="sep">, </span>'
        f'<span class="row">{icon("clock")}<span class="v"><span class="k">שעות פתיחה</span> <span class="hours">{hours}</span></span></span>'
    )
    cards.append(f'''          <article class="branch-card">
            <div class="branch-photo">{img(BRANCH_PHOTOS[b["short"]], b["short"], 800, 520)}<span class="branch-city">{b["city"]}</span></div>
            <p class="branch-facts">{facts_line}</p>
            <p class="branch-note">{b["note"]}</p>
            <div class="branch-actions">
              <a class="btn btn-dark btn-sm" href="{tel(b["phone"])}">{icon("phone")}התקשרו להזמנה</a>
            </div>
          </article>''')

branches_body = f'''{page_hero("branches_hero", "הסניפים", "שלושה נמלים, מטבח אחד", "בכל המסעדות אותו תפריט, אותו צוות מטבח ואותה מרפסת מול הים. בחרו את הנמל הקרוב אליכם.")}
    <section class="section" aria-label="רשימת הסניפים">
      <div class="container">
        <div class="branches">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
    <section class="section section-paper" aria-labelledby="center-title">
      <div class="container center-block">
        <span class="eyebrow">מוקד הזמנות</span>
        <h2 id="center-title">טלפון אחד לכל המסעדות</h2>
        <p>אפשר להזמין שולחן, משלוח או איסוף עצמי מכל המסעדות בטלפון אחד. המוקד פתוח בכל יום, מ־10 בבוקר ועד 10 בלילה.</p>
        <a class="btn btn-primary" href="{tel(MAIN_PHONE)}">{icon("phone")}<span class="ltr nums">{MAIN_PHONE}</span></a>
      </div>
    </section>
'''
page("branches.html", "הסניפים | ביסטרו נמל",
     "הסניפים של ביסטרו נמל בנמל תל אביב, בנמל חיפה ובמרינה הרצליה, עם כתובות, טלפונים ושעות פתיחה.",
     branches_body, preload=photo("branches_hero", 1800))

# ---------------------------------------------------------------- faq

toc = "\n".join(f'            <li><a href="#faq-{i}">{icon(ic)}{title}</a></li>' for i, (ic, title, _) in enumerate(FAQ))
groups = []
for i, (ic, title, qas) in enumerate(FAQ):
    items = "\n".join(qa_item(q, a) for q, a in qas)
    groups.append(f'''          <section class="faq-group" id="faq-{i}" aria-labelledby="faq-{i}-title">
            <h2 id="faq-{i}-title">{title}</h2>
            <div class="qa-list">
{items}
            </div>
          </section>''')

faq_body = f'''{page_hero("faq_hero", "שאלות נפוצות", "שאלות ותשובות", "כל מה שכדאי לדעת לפני שמגיעים, מזמינים משלוח או מתכננים אירוע.")}
    <div class="section">
      <div class="container faq-layout">
        <aside class="faq-toc" aria-label="נושאים">
          <ul>
{toc}
          </ul>
        </aside>
        <div class="faq-main">
{chr(10).join(groups)}
        </div>
      </div>
    </div>
'''
page("faq.html", "שאלות נפוצות | ביסטרו נמל",
     "שאלות נפוצות על ביסטרו נמל. הזמנת מקום, ביטולים, משלוחים, כשרות, חניה, נגישות ואמצעי תשלום.",
     faq_body, preload=photo("faq_hero", 1800))

# ---------------------------------------------------------------- contact

branch_phones = "\n".join(
    f'            <li><span>{b["short"]}</span><a href="{tel(b["phone"])}"><span class="ltr nums">{b["phone"]}</span></a></li>'
    for b in BRANCHES)
zones = "\n".join(f'''          <div class="zone">
            <h3>{t}</h3>
            <ul>
{chr(10).join(f"              <li>{a}</li>" for a in areas)}
            </ul>
          </div>''' for t, areas in DELIVERY)
dfacts = "\n".join(f'          <li><span class="k">{k}:</span> <span>{v}</span></li>' for k, v in DELIVERY_FACTS)
facts = "\n".join(f'          <li><span class="k">{k}:</span> <span>{v}</span></li>' for k, v in FACTS)
delivery_qa = "\n".join(qa_item(q, a) for q, a in FAQ[1][2])

contact_body = f'''{page_hero("contact_hero", "צור קשר", "צור קשר ומשלוחים", "הזמנת מקום, משלוח הביתה או סתם שאלה. אנחנו זמינים בטלפון ובדוא״ל.")}
    <section class="section" aria-labelledby="reach-title">
      <div class="container">
        <h2 id="reach-title" class="visually-hidden">דרכי התקשרות</h2>
        <div class="contact-grid">
          <div class="contact-card contact-main">
            <span class="eyebrow">מוקד הזמנות</span>
            <p><a class="big" href="{tel(MAIN_PHONE)}"><span class="ltr">{MAIN_PHONE}</span></a></p>
            <p class="muted">פתוח בכל יום, מ־10 בבוקר ועד 10 בלילה. לשולחן, למשלוח ולאיסוף עצמי.</p>
          </div>
          <div class="contact-card">
            <span class="eyebrow">טלפון ישיר למסעדות</span>
            <ul class="phone-list">
{branch_phones}
            </ul>
          </div>
          <div class="contact-card">
            <span class="eyebrow">דוא״ל</span>
            <p><a class="mail" href="mailto:hello@bistro-namal.example"><span class="ltr">hello@bistro-namal.example</span></a></p>
            <p class="muted">לאירועים, לשיתופי פעולה ולמשוב. עונים תוך יום עסקים.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-paper" id="delivery" aria-labelledby="delivery-title">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">משלוחים</span>
          <h2 id="delivery-title">משלוחים ואיסוף עצמי</h2>
          <p>רוב התפריט מגיע גם הביתה. מזמינים בטלפון במוקד ההזמנות.</p>
        </div>
        <div class="delivery-grid">
          <div class="delivery-zones">
{zones}
          </div>
          <ul class="info-list">
{dfacts}
          </ul>
        </div>
        <h3 class="sub-head">שאלות על משלוחים</h3>
        <div class="qa-list qa-grid">
{delivery_qa}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="info-title">
      <div class="container narrow">
        <div class="section-head">
          <span class="eyebrow">מידע שימושי</span>
          <h2 id="info-title">פרטים שכדאי לדעת לפני שמגיעים</h2>
        </div>
        <ul class="info-list">
{facts}
        </ul>
      </div>
    </section>
'''
page("contact.html", "צור קשר ומשלוחים | ביסטרו נמל",
     "יצירת קשר עם ביסטרו נמל. מוקד הזמנות, טלפונים של המסעדות, אזורי משלוח, דמי משלוח ומידע שימושי.",
     contact_body, preload=photo("contact_hero", 1800))

(OUT / "favicon.svg").write_text(
    BRAND_MARK.replace('class="brand-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace("currentColor", "#b4643f"),
    encoding="utf-8")
print("built", sorted(p.name for p in OUT.iterdir()))
