# Pattern Match — Roadmap

Improvement ideas, in rough priority order. The current game is documented in
[README.md](README.md), and the architecture in [DESIGN.md](DESIGN.md).

Status key: ☐ not started · ◐ in progress · ☑ done

## Recommended next: 1 + 2
Together these turn the game from a puzzle into a proper game-show round.

---

## Biggest wins for a host-run game

### 1. Separate host window ☐
**Problem:** the host peek (**P**) shows the answer on the projector as well.
**Idea:** open a second window on the laptop, with the projector as an extended display. The host window
shows the answer, a map of where each icon sits, and all the controls. The projector shows only the board.
**Notes:** `window.open()` returns a direct reference to the second window, so this works both from
`file://` and on Netlify with no server.

### 2. Teams and scoring ☐
- 2–4 named teams take turns. A team keeps its turn while it keeps matching.
- Points for each pair, plus a **guess bonus** that shrinks as more of the picture is uncovered.
- A live "guess now for X points" counter on screen, so people are pushed to guess early.
- A scoreboard strip, and a winner banner after the final round.

### 3. Drop in your own photo ☐
Drag any picture onto the board to use it as the answer for that round, with no need to edit `config.js`.
Good for events: a team photo, the venue, a product shot. Nothing is uploaded; the picture stays in the browser.

## Polish

### 4. Hint key ☐
The host uncovers one random extra tile when the room is stuck. Optionally, it costs points once
teams exist.

### 5. Board size and difficulty from the screen ☐
Choose a quick 4×4 (8 pairs) or the full 6×6 (18 pairs) without editing the config.
An 8×8 board would need more icons.

### 6. Survive an accidental refresh ☐
Save the round (tile layout, cleared pairs, answer, scores) in the browser so pressing F5 on stage
doesn't lose the game.

## Now that it's online (Netlify)

### 7. Hide the answers from snoopers ☐
Anyone can currently open `config.js` or the `answers/` folder in their browser.
Scramble the answer file names and encode the titles to stop casual peeking.
This isn't real security; it just keeps honest players honest.

### 8. Themed packs ☐
Swap in a whole set of tile icons and answers per event, for example
`packs/network-security/` (firewall, padlock, router, data centre) as an icebreaker for training sessions.
Choose the pack from the screen or with `?pack=` in the address.

---

## Done
- ☑ Core game: 6×6 board, answer image revealed under cleared tiles, host controls
- ☑ 18 original SVG tile icons
- ☑ 12 answer pictures
- ☑ Generated sound effects and optional background music
- ☑ Git repository, GitHub and Netlify hosting
