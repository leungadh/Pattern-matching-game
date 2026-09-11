# Pattern Match

A host-run memory game for a big screen. 36 numbered tiles hide 18 pairs of pictures.
Every matched pair disappears and uncovers part of a hidden answer image under the board.
The audience shouts out what they think the picture is, and the host decides if they're right.

<p align="center">
  <img src="icons/Hero.png" width="600"
       alt="Pattern Match mid-game: 7 of 18 pairs found, with cleared tiles revealing part of a birthday-cake picture under the numbered board">
</p>

## Run it (Windows or Mac)

1. Copy the whole `Pattern-matching-game` folder to the PC (USB stick, OneDrive, zip file — any way works).
2. Double-click `index.html`. It opens in Edge or Chrome. You don't need to install anything, and it works offline.
3. Press **F** for full screen.

## How to play

- The audience calls out two tile numbers. The host clicks them or types them (for example `1` `2` for tile 12; for tiles 1–3, press Enter).
- **Match:** the pair glows gold, then fades away and shows that part of the answer image.
- **No match:** the tiles flash red and flip back.
- Anyone can guess the picture at any time. The host presses **C** if the guess is right and **R** to show the answer if nobody gets it.

## Host keys

| Key | Action |
|---|---|
| `1`–`36` | Flip that tile |
| **C** ×2 | Correct! Shows the whole picture with confetti |
| **R** ×2 | Shows the answer (nobody guessed it) |
| **N** | New game (press twice if a round is in progress) |
| **P** | Host peek. Shows the answer name for 3 seconds. The audience can see it too, so look away from the projector or blank it first. |
| **M** | Sound effects on/off |
| **B** | Background music on/off (speeds up as more of the picture appears) |
| **F** | Full screen |
| Esc | Cancels a half-typed tile number |

C, R and N (during a round) need a second press within 2.5 seconds, so a stray key press can't spoil a round.

## Sounds

All sounds are made by the browser, so there are no audio files to copy.

- **Flip:** a card swish.
- **Match:** a chime that climbs higher with every match in a row. Three or more in a row adds a sparkle.
- **Miss:** a gentle "uh-oh". It also resets the streak.
- **Milestones:** a jingle when half the pairs are found, and a flourish when the board is cleared.
- **Pressing C or R once:** a drum roll while you confirm. Then a fanfare with a cymbal crash for a correct guess, or a "wah-wah-wahhh" if nobody got it.
- **New game:** a card-shuffle sound.

The volume and the on/off defaults are in `config.js` (`sound`, `music`, `volume`).

## Add your own pictures

**New answer image:** put it in `answers/` (a square JPG or PNG works best), then add one line in `config.js`:

```js
answers: [
  { image: "answers/lighthouse.svg",  title: "Lighthouse" },
  { image: "answers/my-photo.jpg",    title: "Victoria Harbour" }   // ← new
]
```

**New or extra tile icons:** put them in `icons/` and add their paths to `icons: [...]`.
If there are more than 18 icons, each game picks 18 at random.

To change the board size, set `gridSize` (4 = 16 tiles, 6 = 36 tiles, 8 = 64 tiles). You need at least (gridSize²)/2 icons.

## Files

```
index.html          page layout
style.css           look and animations
game.js             game rules (plain JavaScript, no libraries)
sound.js            sound effects and background music (generated, no audio files)
config.js           ← the only file you normally edit
icons/              18 tile pictures (SVG)
answers/            hidden answer pictures
tools/make_icons.py re-generates the built-in icons (optional, needs Python)
tools/make_answers.py re-generates the built-in answer pictures (optional, needs Python)
```

File names are case-sensitive on the web, so `Lighthouse.JPG` and `lighthouse.jpg` are different files. Keep names lowercase with no spaces to be safe.
