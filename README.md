# Salzberg Weekly Plan

An 800×480 family plan for the reTerminal E1002 (6-color E Ink Spectra 6), shown through SenseCraft HMI.

**Display URL:** https://doogree122.github.io/salzbergplan/

The page reads the family Google Sheet, **Salzberg Weekly Family Plan**, every time the display refreshes. To change what's shown, just edit the Sheet.

## How it reads the Sheet

- **Tab:** the first tab that has a `Child` header row. Put the current week's tab first, leftmost.
- **Days:** the day columns (`Monday` … `Friday`). Hidden columns and hidden rows are skipped.
- **Kids:** the kids are stacked top to bottom (Kol, Meitav, Havi; change `KID_ORDER` at the top of the script). In each kid's card the morning drive (To school) comes first, then Back home, then everything else. Each kid's rows are the ones under their name in column A. Rows that are blank (or `—`, or black) for the day are left off that kid's card; a kid with nothing that day shows "Nothing planned". The `Item` text (To school, Home + time, Afterschool) picks the little picture. Only To school and Back home rows show their label; other rows (Afterschool, assignments…) show just the picture and the text.
- **Drivers:** the cell **color** is matched to the sheet's **Legend** row. If a cell's color isn't in the legend, the page looks for a name in the text instead (for example, "Navit"). Any cell that says "carpool" gets a CP circle. A black cell means "not applicable". The "Needs to be figured out" color, or a `?` in the text, makes the row yellow. `NO SCHOOL` shows white text on black.
- **Family dinner** and the **Ori/Navit Night Activity** row appear in the green dinner bar, as just the dinner and the activity (no titles).
- **Pictures:** the activity picture comes from keywords: drums, soccer, music, guitar, dance, boxing, math, tutoring, drama/rehearsal, CLUE, swim, basketball. The dinner picture also comes from keywords: schnitzel, grill, sushi, salmon/fish, pizza, pasta, tacos, burger, Sukkot, Shabbat/holiday. Anything else gets a star or a plate.
- **Family photo:** the right side shows a photo from the shared Google Photos album "Salz Fam Photos", a different one every 15 minutes (whenever GitHub runs the render job). The GitHub job finds the faces in it with OpenCV and crops around them (if it finds none, it keeps more of the top) and dithers it to the six display colors. If the album can't be read, a placeholder shows instead. To check the crops, run the workflow by hand with "preview" ticked: it publishes crops-preview.png on the display branch, showing every photo with its faces (red) and crop (green) until the next run. The album link is `ALBUM` in `photo.py`. Note that plan.png is public, so the current photo is visible to anyone with the display link.
- **FYI:** the FYI section in the sheet is not shown on the display (its rows are just skipped).
- **Shabbat screen:** on Friday from 4 pm and all of Saturday, the whole display is a family photo with "שבת שלום" and the candle-lighting and Shabbat-ends times for Atlanta from hebcal.com. `SHABBAT_MODE` and `SHABBAT_START_HOUR` are at the top of the script in index.html. Add `?shabbat=1` to the page address to see it any day, or run the workflow with "shabbat_preview" ticked.
- **Refreshing:** each run of the GitHub job waits until the next quarter hour and starts the next one, so the display and photo update every 15 minutes. To stop it, disable the "Render display image" workflow under Actions.
- **Weather:** the picture next to the day (sun, partly cloudy, cloud, fog, rain, storm or snow) and the high/low come from the free Open-Meteo forecast for Atlanta, for the day being shown. If it can't be reached, the plain sun shows.
- **Timing:** the page uses Eastern time. From 7 pm on it shows tomorrow, and on weekends it shows the next school day.

Settings are at the top of the script in `index.html`: `PEOPLE` (the badge color for each driver), `HELPERS` (other grown-ups who get a white badge), `KID_COLORS`, `TAB`, and `ROLLOVER_HOUR`.

The Sheet must stay shared as **Anyone with the link → Viewer**.

## SenseCraft HMI

Add a **Web** element that fills the 800×480 canvas, set its URL to the display URL, choose a refresh interval, and push it to the device.

`week.html` is the older Tue–Fri grid. It isn't connected to the Sheet.
