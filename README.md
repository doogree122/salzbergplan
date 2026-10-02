# Salzberg Weekly Plan

An 800×480 family schedule for the reTerminal E1002 (6-color E Ink Spectra 6) via SenseCraft HMI.

**Display URL:** https://doogree122.github.io/salzbergplan/

- `index.html`: the **Today view**. It shows today, or tomorrow after 7 pm, or the next school day on weekends. Days are figured in Eastern time.
- `schedule.csv`: the schedule data. Use it as a starter for the Google Sheet, and as a backup if the Sheet can't be reached.
- `week.html`: the older Tue–Fri grid. Its data is still built into the file.

## Weekly updates

Edit the Google Sheet. The display picks up the changes at its next refresh. Google can take about 5 minutes to republish the CSV.

### Sheet format (first tab, same layout as `schedule.csv`)

| Kid | Item | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Meitav | Drop-off | Ori | Sapir | … | … |
| Dinner | | Schnitzel Night | Grill | … | … |
| Driver | Ori | blue | | | |

- **Day columns:** any of Mon–Sun, in any order. You can add a `Mon` column.
- **Kid rows:** group each kid's rows together. The label in the `Item` column can be anything. A kid's row labelled `After…` feeds the small day tiles, which show the first word of each activity.
- **`Dinner` row:** one dinner per day.
- **`Driver` rows:** a name, then a color in the next column: blue, red, green, yellow or black. Any cell that mentions that name gets a colored badge. Use `white` for helpers who should get a plain badge but stay out of the legend.
- **Highlighting:** `?` or `NEEDS` highlights a cell yellow. `NO SCHOOL` shows white text on black. Use `—` or leave a cell blank for nothing.

## One-time setup

1. **Google Sheet:** import `schedule.csv` (File → Import). Then go to File → Share → Publish to web, choose the tab and **Comma-separated values (.csv)**, click Publish, and copy the link.
2. **Connect it:** paste the link into `SHEET_CSV` near the bottom of `index.html`. You can also add it to the display URL instead: `…/salzbergplan/?sheet=<link>`.
3. **SenseCraft HMI:** add a **Web** element that fills the 800×480 page and set its URL to the display URL. Set the device's refresh interval and push the page to the reTerminal.

If the Sheet can't be loaded, the page falls back to `schedule.csv` and shows **SHEET OFFLINE** in the footer.
