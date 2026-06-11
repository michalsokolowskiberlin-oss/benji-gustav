# 🐾 Benji & Gustav — ein Tamagotchi zum Verschenken

Zwei Pixel-Hunde, die sich jeden Tag auf Besuch freuen: füttern, Ball spielen,
streicheln, Häufchen wegmachen — und wer jeden Tag vorbeischaut, schaltet
Überraschungen frei.

## Was drin steckt

| Datei | Zweck |
|---|---|
| `index.html` | Die komplette App (Spiel, Grafik, Logik) — eine einzige Datei |
| `manifest.webmanifest` | Macht daraus eine "echte" App fürs Handy (Name, Icon) |
| `sw.js` | Service Worker — App funktioniert auch offline |
| `icons/` | App-Icons (mit `tools/gen_icons.py` erzeugt) |

## Features

- **Beide Hunde haben eigene Bedürfnisse**: Futter 🦴, Freude ❤️, Energie ⚡ —
  sie verfallen in Echtzeit, auch wenn die App geschlossen ist (max. 3 Tage
  werden simuliert).
- **Aktionen**: Füttern, Ball spielen (Apportieren!), Putzen, Licht aus
  (Schlafen), Streicheln (Hund antippen), Medizin (wenn krank).
- **Nachts schlafen sie von selbst** (23–7 Uhr) und tanken Energie — niemand
  stirbt über Nacht. Bewusst gnädig: Vernachlässigung macht sie nur quengelig
  oder krank, Medizin heilt.
- **Welpen wachsen**: Nach 5 Tagen guter Pflege werden aus den Welpen große
  Hunde (mit kleiner Feier 🎉).
- **Tages-Streak 🔥**: Jeden Tag öffnen = Serie. Belohnungen: Tag 3 Halstücher 🧣,
  Tag 7 Schleifen 🎀, Tag 14 Sonnenbrillen 🕶️, Tag 30 Kronen 👑.
- **💌-Nachricht**: Einmal am Tag wartet eine kleine Überraschungsnachricht.
- **Sanfte Hintergrundmusik 🎵**: ruhiger Ambient-Teppich im Tempo langsamer
  Atmung (~6 Atemzüge/Min), direkt im Browser erzeugt (keine Audiodatei).
  Per 🎵-Knopf an/aus; wird automatisch leiser, wenn das Licht aus ist.

## Selbst ausprobieren

Doppelklick auf `index.html` reicht (Spielstand wird im Browser gespeichert).
Oder mit Server (nötig für App-Icon/Offline-Test):

```bash
# im Projektordner ausführen:
python3 -m http.server 4173
# dann http://localhost:4173 öffnen
```

## Aufs Handy der Beschenkten 🎁

Die App muss einmal kostenlos ins Netz (HTTPS), damit sie wie eine echte App
installierbar ist. Zwei einfache Wege:

### Weg A: GitHub Pages (kostenlos, dauerhaft)

1. Auf [github.com](https://github.com) ein Repository anlegen (z. B.
   `benji-gustav`, public).
2. Diese Dateien hochladen (`index.html`, `manifest.webmanifest`, `sw.js`,
   Ordner `icons/`) — geht auch per Drag & Drop im Browser ("uploading an
   existing file").
3. Im Repo: **Settings → Pages → Branch: main → Save.**
4. Nach ~1 Minute ist die App erreichbar unter
   `https://DEINNAME.github.io/benji-gustav/`

### Weg B: Netlify Drop (noch schneller)

1. [app.netlify.com/drop](https://app.netlify.com/drop) öffnen (kostenloses
   Konto nötig).
2. Den ganzen Projektordner ins Browserfenster ziehen — fertig, du bekommst
   sofort eine URL.

### Dann auf ihrem Handy

1. Link in **Safari** (iPhone) bzw. **Chrome** (Android) öffnen.
2. iPhone: **Teilen-Knopf → "Zum Home-Bildschirm"**.
   Android: **Menü ⋮ → "App installieren"**.
3. Fertig — eigenes Icon, läuft im Vollbild, funktioniert offline. 🐶🐶

> **Wichtig:** Der Spielstand lebt im Browser des Geräts. Einmal auf ihrem
> Handy eingerichtet, bleibt alles erhalten — solange die App nicht gelöscht
> wird.

## Personalisieren ✏️

Alles Wichtige steht ganz oben im `<script>`-Block von `index.html`:

- **`NOTES`** — die täglichen 💌-Nachrichten. Eigene Sätze eintragen!
- **`SPECIAL_DATES`** — Geburtstag/Jahrestag, z. B.
  `{ m: 3, d: 14, text: "Alles Gute zum Geburtstag! 🎂" }`
- **`PAL`** — Fellfarben: `b`/`d` = Benji, `g`/`G` = Gustav
  (falls die echten Benji & Gustav andere Farben haben 😉).

Nach Änderungen die Dateien einfach neu hochladen.
