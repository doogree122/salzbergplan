# Salzberg Weekly Plan

An 800×480 family schedule graphic for a 6-color E Ink Spectra 6 display (black, white, red, yellow, green, blue only).

- `index.html` — **Today view**: big header for today (or the next school day), each kid's drop-off / pickup / after-school with driver badges, dinner, and tiles for the other days.
- `week.html` — **Week grid**: Tue–Fri for all kids in one table, today's column highlighted.

## Updating the schedule

Edit the block marked `EDIT THIS BLOCK` near the bottom of each file (`DAYS`, `ROWS`, `DINNER`, `DRIVERS`, and `SHORT` in `index.html`). It mirrors the family Google Sheet.

Driver colors: Ori = blue, Navit = red, Sapir = green, Arielle = yellow, Robkins = black. Cells containing `?` or `NEEDS` are highlighted yellow; `NO SCHOOL` shows inverted.

## Hosting

Turn on GitHub Pages (Settings → Pages → Deploy from branch → `main` / root) and point the display at the Pages URL. The page scales to fit any window; on the panel it renders at native 800×480.
