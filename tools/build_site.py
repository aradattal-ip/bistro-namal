#!/usr/bin/env python3
"""Generates the static pages of the ביסטרו נמל demo site (header/footer shared)."""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent

ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "fish": '<path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.47-3.44 6-7 6s-7.56-2.53-8.5-6Z"/><path d="M18 12v.5"/><path d="M16 17.93a9.77 9.77 0 0 1 0-11.86"/><path d="M7 10.67C7 8 5.58 5.97 2.73 5.5c-1 1.5-1 5 .23 6.5-1.24 1.5-1.24 5-.23 6.5C5.58 18.03 7 16 7 13.33"/>',
    "waves": '<path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>',
    "anchor": '<circle cx="12" cy="5" r="3"/><line x1="12" y1="22" x2="12" y2="8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "menu": '<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/>',
    "arrow": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
    "map": '<polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/>',
}


def icon(name, size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg viewBox="0 0 24 24"{s} fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


BRAND_MARK = '''<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
  <circle cx="20" cy="20" r="19" fill="#c0623b"/>
  <circle cx="20" cy="12.5" r="2.6" fill="none" stroke="#fff" stroke-width="2"/>
  <path d="M20 15v15M14.5 19h11M11 24.5a9 9 0 0 0 18 0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
</svg>'''

WAVES = '''<svg class="hero-waves" viewBox="0 0 1440 88" preserveAspectRatio="none" aria-hidden="true" focusable="false">
  <path d="M0 40 C 180 10, 360 70, 540 40 S 900 10, 1080 40 S 1320 70, 1440 40 V90 H0 Z" fill="#ece0c9"/>
  <path d="M0 58 C 200 30, 400 86, 600 58 S 1000 30, 1200 58 S 1380 80, 1440 60 V90 H0 Z" fill="#f6efe2"/>
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
      <label class="nav-toggle-label" for="nav-toggle" aria-hidden="true">{icon("menu", 28)}</label>
      <nav class="main-nav" aria-label="ניווט ראשי">
        <ul>
{items}
        </ul>
      </nav>
      <a class="btn btn-primary btn-sm header-cta" href="{tel(MAIN_PHONE)}">{icon("phone")}הזמנת מקום</a>
    </div>
  </header>'''


def footer():
    links = "\n".join(f'            <li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h2>ביסטרו נמל</h2>
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


def page(filename, title, description, body, extra_head=""):
    html = f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#12283b">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&amp;family=Frank+Ruhl+Libre:wght@500;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">{extra_head}
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


def page_hero(eyebrow, title, lead):
    return f'''    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
      {WAVES}
    </section>'''


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

# ---------------------------------------------------------------- index

HERO_ART = '''<svg class="hero-art" viewBox="0 0 400 320" aria-hidden="true" focusable="false">
  <circle cx="250" cy="150" r="92" fill="#c0623b" opacity="0.9"/>
  <circle cx="250" cy="150" r="118" fill="none" stroke="#f0a985" stroke-opacity="0.35" stroke-width="2"/>
  <g fill="none" stroke="#f6efe2" stroke-width="3" stroke-linecap="round">
    <path d="M40 232 C 70 222, 100 242, 130 232 S 190 222, 220 232 S 280 242, 310 232 S 360 222, 380 230" stroke-opacity="0.9"/>
    <path d="M20 262 C 55 252, 90 272, 125 262 S 195 252, 230 262 S 300 272, 335 262 S 375 254, 395 260" stroke-opacity="0.55"/>
    <path d="M60 290 C 95 280, 130 300, 165 290 S 235 280, 270 290 S 330 298, 360 290" stroke-opacity="0.3"/>
  </g>
  <g>
    <rect x="70" y="112" width="26" height="104" fill="#f6efe2"/>
    <rect x="70" y="138" width="26" height="14" fill="#c0623b"/>
    <rect x="70" y="174" width="26" height="14" fill="#c0623b"/>
    <path d="M64 112 h38 l-7 -16 h-24 z" fill="#f6efe2"/>
    <rect x="76" y="80" width="14" height="16" fill="#f0a985"/>
    <path d="M70 80 l13 -14 l13 14 z" fill="#f6efe2"/>
    <rect x="58" y="214" width="50" height="10" rx="2" fill="#f6efe2"/>
  </g>
  <g>
    <path d="M196 214 h112 l-14 22 h-84 z" fill="#f6efe2"/>
    <path d="M252 210 V 128" stroke="#f6efe2" stroke-width="4"/>
    <path d="M256 132 l42 70 h-42 z" fill="#f6efe2" opacity="0.95"/>
    <path d="M248 140 l-34 62 h34 z" fill="#f0a985"/>
  </g>
</svg>'''

DISH_ART = {
    "fish": '<svg viewBox="0 0 120 80" aria-hidden="true" focusable="false"><ellipse cx="60" cy="44" rx="54" ry="30" fill="#fff" stroke="#e2d6bf" stroke-width="2"/><path d="M28 44c8-12 22-18 36-18 12 0 20 8 24 18-4 10-12 18-24 18-14 0-28-6-36-18z" fill="#2b5d7c"/><path d="M28 44l-12-10v20z" fill="#2b5d7c"/><circle cx="78" cy="40" r="2.5" fill="#fff"/><path d="M92 30c4 2 6 6 6 10" stroke="#5f6f3a" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="96" cy="54" r="5" fill="#f0c94a"/></svg>',
    "pasta": '<svg viewBox="0 0 120 80" aria-hidden="true" focusable="false"><ellipse cx="60" cy="44" rx="54" ry="30" fill="#fff" stroke="#e2d6bf" stroke-width="2"/><g fill="none" stroke="#e7b75a" stroke-width="3" stroke-linecap="round"><path d="M36 46c8-14 22-14 30 0s22 14 26 0"/><path d="M34 40c10-12 24-12 32 2s20 12 24-2"/><path d="M40 52c8-10 20-10 28 0s18 8 22-2"/></g><circle cx="52" cy="38" r="4" fill="#c0623b"/><circle cx="72" cy="50" r="4" fill="#c0623b"/><path d="M80 34c3-3 8-3 10 0" stroke="#5f6f3a" stroke-width="3" fill="none" stroke-linecap="round"/></svg>',
    "salad": '<svg viewBox="0 0 120 80" aria-hidden="true" focusable="false"><ellipse cx="60" cy="44" rx="54" ry="30" fill="#fff" stroke="#e2d6bf" stroke-width="2"/><ellipse cx="46" cy="40" rx="12" ry="7" fill="#7d9445" transform="rotate(-20 46 40)"/><ellipse cx="70" cy="36" rx="12" ry="7" fill="#5f6f3a" transform="rotate(25 70 36)"/><ellipse cx="62" cy="52" rx="12" ry="6" fill="#8fa858"/><circle cx="40" cy="54" r="6" fill="#c0623b"/><circle cx="82" cy="50" r="6" fill="#c0623b"/><rect x="54" y="40" width="9" height="9" rx="2" fill="#f6efe2" stroke="#e2d6bf"/></svg>',
}

def qa_card(q, a):
    return f'''          <article class="card qa">
            <h3><span class="qa-label">שאלה:</span> {q}</h3>
            <p><span class="qa-label">תשובה:</span> {a}</p>
          </article>'''


FAQ_TEASER = qa_card(*FAQ[0][2][0]) + "\n" + qa_card(*FAQ[1][2][0])

about = f'''    <section class="hero">
      <div class="container hero-inner">
        <div>
          <span class="eyebrow">מטבח ים תיכוני על קו המים</span>
          <h1>ביסטרו נמל</h1>
          <p class="hero-lead">דגים טריים מהדייגים של הבוקר, ירקות מהשוק ויין טוב, עם הרגליים כמעט במים. שלוש מסעדות בנמל תל אביב, בנמל חיפה ובמרינה הרצליה.</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="menu.html">לתפריט המלא{icon("arrow")}</a>
            <a class="btn btn-ghost" href="branches.html">הסניפים שלנו</a>
          </div>
        </div>
        {HERO_ART}
      </div>
      {WAVES}
    </section>

    <section class="section" id="about" aria-labelledby="about-title">
      <div class="container about">
        <div class="about-text">
          <span class="eyebrow">אודות</span>
          <h2 id="about-title">ביסטרו קטן שהתחיל ברציף</h2>
          <p>ביסטרו נמל נפתח בשנת 2014 בהאנגר ישן בנמל תל אביב, עם שישה שולחנות ותפריט שנכתב כל בוקר על לוח לפי מה שהדייגים הביאו. היום יש לנו שלוש מסעדות לאורך החוף, והרעיון נשאר אותו רעיון. אוכל פשוט, טרי ומדויק, שירות חם ונינוח ונוף פתוח לים.</p>
          <p>השף והבעלים, יואב לוי, מבשל מטבח ים תיכוני עם השפעות מהמטבח הצפון אפריקאי והאיטלקי. הלחם נאפה אצלנו בטאבון, הפסטה נעשית במקום, ואת רשימת היין אנחנו בונים עם יקבים קטנים מהגליל ומהגולן.</p>
          <p>אנחנו מסעדה רגועה ומזמינה. אפשר לקפוץ לצהריים קלים מול הים, לחגוג ערב עם חברים או לסגור את המרפסת לאירוע.</p>
        </div>
        <aside class="facts" aria-labelledby="facts-title">
          <h3 id="facts-title">בקצרה</h3>
          <ul>
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
        </aside>
      </div>
    </section>

    <section class="section section-alt" aria-labelledby="why-title">
      <div class="container">
        <div class="section-head">
          <h2 id="why-title">למה אצלנו</h2>
          <p>שלושה דברים שלא מתפשרים עליהם</p>
        </div>
        <div class="grid grid-3">
          <article class="card feature">
            <span class="icon-badge">{icon("fish")}</span>
            <h3>דג טרי בכל בוקר</h3>
            <p>אנחנו קונים ישירות מהדייגים בנמל, והתפריט משתנה לפי מה שעלה ברשת.</p>
          </article>
          <article class="card feature">
            <span class="icon-badge">{icon("sun")}</span>
            <h3>מרפסת מול הים</h3>
            <p>בכל אחת מהמסעדות יש ישיבה בחוץ מול המים, עם חימום בחורף וצל בקיץ.</p>
          </article>
          <article class="card feature">
            <span class="icon-badge">{icon("truck")}</span>
            <h3>משלוחים ואיסוף עצמי</h3>
            <p>רוב התפריט מגיע גם הביתה, מנמל תל אביב וממרינה הרצליה.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="dishes-title">
      <div class="container">
        <div class="section-head">
          <h2 id="dishes-title">המנות שאהובות עלינו</h2>
          <p>טעימה קטנה מהתפריט</p>
        </div>
        <div class="grid grid-3">
          <article class="card dish">
            <div class="dish-art">{DISH_ART["fish"]}</div>
            <h3>דניס שלם על הגריל</h3>
            <p>דניס שלם מהדייגים, לימון שרוף ושמן זית, עם תפוחי אדמה צלויים.</p>
          </article>
          <article class="card dish">
            <div class="dish-art">{DISH_ART["pasta"]}</div>
            <h3>לינגוויני פירות ים</h3>
            <p>שרימפס, קלמרי ומולים עם עגבניות שרי, שום ויין לבן.</p>
          </article>
          <article class="card dish">
            <div class="dish-art">{DISH_ART["salad"]}</div>
            <h3>סלט הנמל</h3>
            <p>עלים, עגבניות שרי, צנונית ופטה בשמן זית לימוני.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-alt" aria-labelledby="faq-teaser-title">
      <div class="container">
        <div class="section-head">
          <h2 id="faq-teaser-title">לפני שמגיעים</h2>
          <p>השאלות שהכי הרבה שואלים אותנו</p>
        </div>
        <div class="grid grid-2">
{FAQ_TEASER}
        </div>
        <p style="margin-top: var(--s5)"><a class="btn btn-outline" href="faq.html">לכל השאלות והתשובות{icon("arrow")}</a></p>
      </div>
    </section>

    <section class="section-tight" aria-label="הזמנת מקום">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>שומרים לכם שולחן מול הים</h2>
            <p>מוקד ההזמנות פתוח בכל יום, מ־10 בבוקר ועד 10 בלילה</p>
          </div>
          <a class="btn btn-outline" href="{tel(MAIN_PHONE)}">{icon("phone")}<span class="ltr nums">{MAIN_PHONE}</span></a>
        </div>
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
     about,
     extra_head='\n  <script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>")

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
          <ul class="menu-list" role="list">
{chr(10).join(lis)}
          </ul>
        </section>''')

menu_body = f'''{page_hero("התפריט", "התפריט שלנו", "מטבח ים תיכוני שמשתנה מעט לפי העונה ולפי מה שהדייגים מביאים. אותו תפריט בכל שלוש המסעדות, וגם במשלוח.")}
    <nav class="menu-nav" aria-label="קטגוריות בתפריט">
      <div class="container">
        <div class="chips">
{chips}
        </div>
      </div>
    </nav>
    <div class="section">
      <div class="container">
{chr(10).join(sections)}
        <div class="legend" aria-label="מקרא">
          <span><span class="tag tag-vegan">טבעוני</span> ללא מוצרים מן החי</span>
          <span><span class="tag tag-veg">צמחוני</span> ללא בשר ודגים</span>
          <span><span class="tag tag-gf">ללא גלוטן</span> המטבח אינו סטרילי מגלוטן</span>
        </div>
        <p class="menu-note">המחירים בשקלים וכוללים מע״מ. אם יש לכם אלרגיה או רגישות למזון, ספרו לנו כשאתם מזמינים.</p>
      </div>
    </div>
'''
page("menu.html", "התפריט | ביסטרו נמל",
     "התפריט המלא של ביסטרו נמל עם מחירים, פתיחים, דגים ופירות ים, עיקריות, פסטות, קינוחים ושתייה.",
     menu_body)

# ---------------------------------------------------------------- branches

cards = []
for b in BRANCHES:
    hours = '<span class="sep"> · </span>'.join(
        f'<span class="day"><span>{d}</span><span class="t">{t}</span></span>'
        for d, t in b["hours"])
    facts_line = (
        f'<span class="b-top"><span class="b-name">{b["name"]}</span>{icon("anchor")}</span><span class="sep">, </span>'
        f'<span class="row">{icon("pin")}<span class="v" data-k="כתובת">{b["address"]}</span></span><span class="sep">, </span>'
        f'<span class="row">{icon("map")}<span class="v" data-k="עיר">{b["city"]}</span></span><span class="sep">, </span>'
        f'<span class="row">{icon("phone")}<span class="v" data-k="טלפון"><a href="{tel(b["phone"])}"><span class="ltr nums">{b["phone"]}</span></a></span></span><span class="sep">, </span>'
        f'<span class="row">{icon("utensils")}<span class="v"><span class="k">כשרות</span> {b["kosher"]}</span></span><span class="sep">, </span>'
        f'<span class="row">{icon("clock")}<span class="v"><span class="k">שעות פתיחה</span> <span class="hours">{hours}</span></span></span>'
    )
    cards.append(f'''          <article class="card branch-card">
            <p class="branch-facts">{facts_line}</p>
            <p class="branch-note">{b["note"]}</p>
            <div class="branch-actions">
              <a class="btn btn-primary btn-sm" href="{tel(b["phone"])}">{icon("phone")}התקשרו להזמנה</a>
            </div>
          </article>''')

COAST = '''<svg viewBox="0 0 300 380" aria-hidden="true" focusable="false">
  <rect x="1" y="1" width="298" height="378" rx="16" fill="#dce7ee" stroke="#e2d6bf" stroke-width="2"/>
  <path d="M290 1 H170 C 160 60, 150 110, 140 160 C 128 220, 112 290, 96 379 H283 a 16 16 0 0 0 16 -16 V17 a 16 16 0 0 0 -16 -16 Z" fill="#ece0c9"/>
  <path d="M170 1 C 160 60, 150 110, 140 160 C 128 220, 112 290, 96 379" fill="none" stroke="#2b5d7c" stroke-width="3"/>
  <g font-family="Assistant, sans-serif" font-size="17" font-weight="700" fill="#12283b" text-anchor="end">
    <circle cx="162" cy="62" r="9" fill="#c0623b" stroke="#fff" stroke-width="2"/><text x="180" y="68">חיפה</text>
    <circle cx="136" cy="190" r="9" fill="#c0623b" stroke="#fff" stroke-width="2"/><text x="154" y="196">הרצליה</text>
    <circle cx="124" cy="252" r="9" fill="#c0623b" stroke="#fff" stroke-width="2"/><text x="142" y="258">תל אביב</text>
  </g>
  <g fill="none" stroke="#2b5d7c" stroke-opacity="0.35" stroke-width="2" stroke-linecap="round">
    <path d="M30 120 q10 -6 20 0 t20 0"/><path d="M50 260 q10 -6 20 0 t20 0"/><path d="M20 330 q10 -6 20 0 t20 0"/>
  </g>
</svg>'''

branches_body = f'''{page_hero("הסניפים", "שלושה נמלים, מטבח אחד", "בכל המסעדות אותו תפריט, אותו צוות מטבח ואותה מרפסת מול הים. בחרו את הנמל הקרוב אליכם.")}
    <section class="section" aria-label="רשימת הסניפים">
      <div class="container">
        <div class="grid grid-3">
{chr(10).join(cards)}
        </div>
        <div class="branch-map">
          {COAST}
          <div>
            <h2>מוקד הזמנות אחד לכל המסעדות</h2>
            <p class="muted-lead">אפשר להזמין שולחן, משלוח או איסוף עצמי מכל המסעדות בטלפון אחד. המוקד זמין בכל יום בין 10:00 ל־22:00.</p>
            <p><a class="btn btn-outline" href="{tel(MAIN_PHONE)}">{icon("phone")}<span class="ltr nums">{MAIN_PHONE}</span></a></p>
          </div>
        </div>
      </div>
    </section>
'''
page("branches.html", "הסניפים | ביסטרו נמל",
     "הסניפים של ביסטרו נמל בנמל תל אביב, בנמל חיפה ובמרינה הרצליה, עם כתובות, טלפונים ושעות פתיחה.",
     branches_body)

# ---------------------------------------------------------------- faq

groups = []
for ic, title, qas in FAQ:
    items = "\n".join(f'''          <article class="card qa">
            <h3><span class="qa-label">שאלה:</span> {q}</h3>
            <p><span class="qa-label">תשובה:</span> {a}</p>
          </article>''' for q, a in qas)
    groups.append(f'''        <section class="faq-group" aria-label="{title}">
          <h2>{icon(ic)}{title}</h2>
          <div class="qa-list">
{items}
          </div>
        </section>''')

faq_body = f'''{page_hero("שאלות נפוצות", "שאלות ותשובות", "כל מה שכדאי לדעת לפני שמגיעים, מזמינים משלוח או מתכננים אירוע.")}
    <div class="section">
      <div class="container">
{chr(10).join(groups)}
      </div>
    </div>
'''
page("faq.html", "שאלות נפוצות | ביסטרו נמל",
     "שאלות נפוצות על ביסטרו נמל. הזמנת מקום, ביטולים, משלוחים, כשרות, חניה, נגישות ואמצעי תשלום.",
     faq_body)

# ---------------------------------------------------------------- contact

branch_phones = "\n".join(
    f'            <p>{b["short"]} <a href="{tel(b["phone"])}"><span class="ltr nums">{b["phone"]}</span></a></p>'
    for b in BRANCHES)
zones = "\n".join(f'''          <div class="card zone">
            <h3>{t}</h3>
            <ul>
{chr(10).join(f"              <li>{a}</li>" for a in areas)}
            </ul>
          </div>''' for t, areas in DELIVERY)
dfacts = "\n".join(f'          <li><span class="k">{k}:</span> <span>{v}</span></li>' for k, v in DELIVERY_FACTS)
facts = "\n".join(f'          <li><span class="k">{k}:</span> <span>{v}</span></li>' for k, v in FACTS)

DELIVERY_QA = "\n".join(qa_card(q, a) for q, a in FAQ[1][2])
contact_body = f'''{page_hero("צור קשר", "צור קשר ומשלוחים", "הזמנת מקום, משלוח הביתה או סתם שאלה. אנחנו זמינים בטלפון ובדוא״ל.")}
    <section class="section" aria-labelledby="reach-title">
      <div class="container">
        <h2 id="reach-title" class="visually-hidden">דרכי התקשרות</h2>
        <div class="contact-grid">
          <div class="card contact-card">
            <span class="icon-badge">{icon("phone")}</span>
            <h2>מוקד הזמנות</h2>
            <p><a class="big" href="{tel(MAIN_PHONE)}"><span class="ltr">{MAIN_PHONE}</span></a></p>
            <p class="muted">בכל יום בין 10:00 ל־22:00, לשולחן, למשלוח ולאיסוף עצמי</p>
          </div>
          <div class="card contact-card">
            <span class="icon-badge">{icon("anchor")}</span>
            <h2>טלפון ישיר למסעדות</h2>
{branch_phones}
          </div>
          <div class="card contact-card">
            <span class="icon-badge">{icon("mail")}</span>
            <h2>דוא״ל</h2>
            <p><a href="mailto:hello@bistro-namal.example"><span class="ltr">hello@bistro-namal.example</span></a></p>
            <p class="muted">לאירועים, לשיתופי פעולה ולמשוב. עונים תוך יום עסקים.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="delivery" aria-labelledby="delivery-title">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">משלוחים</span>
          <h2 id="delivery-title">משלוחים ואיסוף עצמי</h2>
          <p>רוב התפריט מגיע גם הביתה. מזמינים בטלפון במוקד ההזמנות.</p>
        </div>
        <div class="delivery-zones">
{zones}
        </div>
        <ul class="info-list" style="margin-top: var(--s6)">
{dfacts}
        </ul>
        <h3 class="sub-head">שאלות על משלוחים</h3>
        <div class="grid grid-3">
{DELIVERY_QA}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="info-title">
      <div class="container">
        <div class="section-head">
          <h2 id="info-title">מידע שימושי</h2>
          <p>פרטים שכדאי לדעת לפני שמגיעים</p>
        </div>
        <ul class="info-list">
{facts}
        </ul>
      </div>
    </section>
'''
page("contact.html", "צור קשר ומשלוחים | ביסטרו נמל",
     "יצירת קשר עם ביסטרו נמל. מוקד הזמנות, טלפונים של המסעדות, אזורי משלוח, דמי משלוח ומידע שימושי.",
     contact_body)

(OUT / "favicon.svg").write_text(BRAND_MARK.replace('class="brand-mark" ', 'xmlns="http://www.w3.org/2000/svg" '), encoding="utf-8")
print("built", sorted(p.name for p in OUT.iterdir()))
