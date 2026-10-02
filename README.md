# Salzberg Weekly Plan

An 800×480 family plan for the reTerminal E1002 (6-color E Ink Spectra 6), shown through SenseCraft HMI.

**Display URL:** https://doogree122.github.io/salzbergplan/

The page reads the family Google Sheet, **Salzberg Weekly Family Plan**, every time the display refreshes. To change what's shown, just edit the Sheet.

## How it reads the Sheet

- **Tab:** the first tab that has a `Child` header row. Put the current week's tab first, leftmost.
- **Days:** the day columns (`Monday` … `Friday`). Hidden columns and hidden rows are skipped.
- **Kids:** each kid's rows are the ones under their name in column A. The `Item` text (To school, Home + time, Afterschool) picks the little picture.
- **Drivers:** the cell **color** is matched to the sheet's **Legend** row. If a cell's color isn't in the legend, the page looks for a name in the text instead (for example, "Navit"). A black cell means "not applicable". The "Needs to be figured out" color, or a `?` in the text, makes the row yellow. `NO SCHOOL` shows white text on black.
- **Family dinner** and the **Ori/Navit Night Activity** row appear in the green dinner bar.
- **Pictures:** the activity picture comes from keywords: soccer, music, guitar, dance, boxing, math, tutoring, drama/rehearsal, CLUE, swim, basketball. The dinner picture also comes from keywords: schnitzel, grill, sushi, salmon/fish, pizza, pasta, tacos, burger, Sukkot, Shabbat/holiday. Anything else gets a star or a plate.
- **Family photo:** the right side shows a photo from the shared Google Photos album "Salz Fam Photos", a different one every 15 minutes (whenever GitHub runs the render job). The GitHub job crops it to the panel (favoring the top, where faces usually are) and dithers it to the six display colors. If the album can't be read, a placeholder shows instead. The album link is `ALBUM` in `photo.py`. Note that plan.png is public, so the current photo is visible to anyone with the display link.
- **FYI:** type `FYI` in any cell of the sheet. Notes to its right and in the rows below it, up to the first blank row, show in a box over the bottom of the photo. Notes on the FYI row always show. In the rows below, a note under a day column shows only on that day. Up to six fit.
- **Timing:** the page uses Eastern time. From 7 pm on it shows tomorrow, and on weekends it shows the next school day.

Settings are at the top of the script in `index.html`: `PEOPLE` (the badge color for each driver), `HELPERS` (other grown-ups who get a white badge), `KID_COLORS`, `TAB`, and `ROLLOVER_HOUR`.

The Sheet must stay shared as **Anyone with the link → Viewer**.

## SenseCraft HMI

Add a **Web** element that fills the 800×480 canvas, set its URL to the display URL, choose a refresh interval, and push it to the device.

`week.html` is the older Tue–Fri grid. It isn't connected to the Sheet.
