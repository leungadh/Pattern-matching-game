/*
 * Pattern Match — host-run memory game.
 * Plain JavaScript, no libraries, no build step. Works from file:// on Windows and macOS.
 *
 * Flow: flip 2 tiles -> match? pair glows, then fades away revealing that part of the
 * hidden answer image underneath the board -> miss? tiles flip back. The host ends the
 * round with "Correct!" (someone guessed the picture) or "Reveal answer" (nobody did).
 */
(function () {
  "use strict";

  const DEFAULTS = {
    title: "Pattern Match", gridSize: 6, icons: [], pairs: [], answers: [],
    flipBackDelayMs: 1200, clearDelayMs: 700, sound: true, music: false, volume: 0.8
  };
  // Every piece of text the engine writes on screen. An edition can override any of
  // them in config.js under `strings` (e.g. Chinese), so the engine stays language-free.
  const STRINGS = {
    boardCleared: "Board cleared!",
    boardClearedSub: "What's the picture? Host: press C or R",
    correct: "Correct! It's {title}",
    correctSub: "Solved with {pairs} of {total} pairs found in {turns} turns",
    reveal: "It was: {title}",
    revealSub: "Press N for a new game",
    peek: "Answer: {title}",
    tileEntry: "Tile {n}…",
    confirm: "Press again to confirm",
    soundOn: "Sound on", soundOff: "Sound off",
    musicOn: "Music on", musicOff: "Music off"
  };
  const cfg = Object.assign({}, DEFAULTS, window.GAME_CONFIG || {});
  const str = Object.assign({}, STRINGS, cfg.strings || {});
  const tr = (key, vars) => str[key].replace(/\{(\w+)\}/g, (_, k) => (vars && k in vars ? vars[k] : ""));
  const $ = (id) => document.getElementById(id);

  const el = {
    title: $("title"), pairs: $("pairs"), totalPairs: $("totalPairs"), turns: $("turns"),
    tileEntry: $("tileEntry"), board: $("board"), answerLayer: $("answerLayer"),
    grid: $("grid"), banner: $("banner"), peek: $("peek"), soundLabel: $("soundLabel"),
    musicLabel: $("musicLabel")
  };

  const state = {
    tiles: [],          // { el, key, index, open, matched }
    open: [],           // currently face-up, unmatched tiles (max 2)
    missTimer: null,
    pairs: 0, totalPairs: 0, turns: 0, streak: 0,
    answer: null, lastAnswer: -1,
    over: false,
    gameId: 0
  };

  // ---------- helpers ----------
  function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function normaliseAnswer(a) {
    if (typeof a === "string") {
      const base = a.split("/").pop().replace(/\.[^.]+$/, "").replace(/[-_]+/g, " ");
      return { image: a, title: base.charAt(0).toUpperCase() + base.slice(1) };
    }
    return a;
  }

  function pickAnswer() {
    const list = cfg.answers.map(normaliseAnswer);
    if (!list.length) return null;
    let i = Math.floor(Math.random() * list.length);
    if (list.length > 1 && i === state.lastAnswer) i = (i + 1) % list.length;
    state.lastAnswer = i;
    return list[i];
  }

  function showError(msg) {
    el.grid.innerHTML = "";
    const d = document.createElement("div");
    d.className = "error";
    d.innerHTML = msg;
    el.grid.appendChild(d);
  }

  function updateStats() {
    el.pairs.textContent = state.pairs;
    el.totalPairs.textContent = state.totalPairs;
    el.turns.textContent = state.turns;
  }

  // ---------- sound (see sound.js — all synthesised, no audio files) ----------
  const snd = window.Sound || { play() {}, stopDrumroll() {}, setSfx() {}, setMusic() {},
                                setIntensity() {}, pauseMusic() {}, resumeMusic() {}, setVolume() {} };
  snd.setVolume(cfg.volume);
  snd.setSfx(cfg.sound);
  snd.setMusic(cfg.music);
  const play = (name, opts) => snd.play(name, opts);

  // ---------- game setup ----------
  function newGame(firstLoad) {
    clearTimeout(state.missTimer);
    const n = cfg.gridSize;
    const total = n * n;
    // An odd board (5x5, 7x7) leaves the centre cell empty so the rest pair up.
    const blank = total % 2 === 1 ? (total - 1) / 2 : -1;
    const playable = blank >= 0 ? total - 1 : total;
    const textMode = Array.isArray(cfg.pairs) && cfg.pairs.length > 0;
    document.documentElement.style.setProperty("--n", n);
    el.title.textContent = cfg.title;
    document.title = cfg.title;

    Object.assign(state, { tiles: [], open: [], missTimer: null, pairs: 0, turns: 0, streak: 0, over: false });
    state.gameId++;
    state.totalPairs = playable / 2;
    el.banner.hidden = true;
    el.board.classList.remove("done");
    hidePeek();
    updateStats();
    snd.stopDrumroll();
    snd.setIntensity(0);
    snd.resumeMusic();
    if (firstLoad !== true) play("shuffle");

    const have = textMode ? cfg.pairs.length : cfg.icons.length;
    if (have < state.totalPairs) {
      return showError(`Not enough ${textMode ? "pairs" : "icons"} in config.js: ` +
                       `a ${n}×${n} board needs ${state.totalPairs}, found ${have}.`);
    }

    state.answer = pickAnswer();
    if (!state.answer) return showError("No answer images listed in config.js (answers: [...]).");
    el.answerLayer.style.backgroundImage = `url("${encodeURI(state.answer.image)}")`;
    const probe = new Image();
    probe.onerror = () => showError(`Could not load answer image:<br><b>${state.answer.image}</b><br>Check the file name in config.js.`);
    probe.src = state.answer.image;

    // Build the deck. Picture mode: two identical icons per pair.
    // Text mode: each pair is two DIFFERENT texts that belong together; the match
    // is decided by the pair they came from, not by what they say.
    let deck;
    if (textMode) {
      const chosen = shuffle(cfg.pairs.slice()).slice(0, state.totalPairs);
      deck = chosen.flatMap((p, k) => [{ key: "p" + k, text: String(p[0]) },
                                       { key: "p" + k, text: String(p[1]) }]);
    } else {
      const chosen = shuffle(cfg.icons.slice()).slice(0, state.totalPairs);
      deck = chosen.flatMap((src) => [{ key: src, src }, { key: src, src }]);
    }
    shuffle(deck);

    el.grid.innerHTML = "";
    let num = 0;
    for (let cell = 0; cell < total; cell++) {
      if (cell === blank) {
        const d = document.createElement("div");
        d.className = "tile-blank";
        d.setAttribute("aria-hidden", "true");
        el.grid.appendChild(d);
        continue;
      }
      const card = deck[num];
      num++;
      const b = document.createElement("button");
      b.className = "tile";
      b.type = "button";
      b.setAttribute("aria-label", `Tile ${num}`);
      b.innerHTML =
        `<span class="tile-inner">` +
          `<span class="face front">${num}</span>` +
          `<span class="face back"></span>` +
        `</span>`;
      const back = b.querySelector(".back");
      if (card.text !== undefined) fillText(back, card.text);
      else {
        const img = document.createElement("img");
        img.alt = ""; img.draggable = false; img.src = card.src;
        back.appendChild(img);
      }
      const tile = { el: b, key: card.key, index: num - 1, open: false, matched: false };
      b.addEventListener("click", () => flip(tile));
      el.grid.appendChild(b);
      state.tiles.push(tile);
    }
  }

  // Lay a short phrase out as big as it fits on a card. Chinese has no spaces, so
  // a 4-character phrase is split 2 + 2 (e.g. 加我 / 力量) rather than squeezed on one
  // line; text with spaces wraps normally. Size is a fraction of the cell (--fs).
  function fillText(back, text) {
    back.classList.add("text");
    const span = document.createElement("span");
    span.className = "txt";
    const chars = Array.from(text.trim());
    let perLine, lines;
    if (/\s/.test(text)) {
      perLine = Math.max(4, Math.ceil(Math.sqrt(chars.length * 2)));
      lines = Math.ceil(chars.length / perLine);
      span.textContent = text;
    } else {
      perLine = chars.length <= 3 ? chars.length : chars.length === 4 ? 2 : Math.ceil(Math.sqrt(chars.length));
      lines = Math.ceil(chars.length / perLine);
      for (let i = 0; i < chars.length; i += perLine) {
        if (i) span.appendChild(document.createElement("br"));
        span.appendChild(document.createTextNode(chars.slice(i, i + perLine).join("")));
      }
    }
    const fs = Math.min(0.36, 0.8 / perLine, 0.7 / (lines * 1.15));
    back.style.setProperty("--fs", fs.toFixed(3));
    back.appendChild(span);
  }

  // ---------- core rules ----------
  function closeMissed() {
    clearTimeout(state.missTimer);
    state.missTimer = null;
    state.open.forEach((t) => { t.open = false; t.el.classList.remove("open", "miss"); });
    state.open = [];
  }

  function flip(tile) {
    if (state.over || tile.matched || tile.open) return;
    if (state.open.length === 2) closeMissed();   // clicking during a miss skips the wait

    tile.open = true;
    tile.el.classList.add("open");
    state.open.push(tile);
    play("flip");

    if (state.open.length < 2) return;

    state.turns++;
    const [a, b] = state.open;
    if (a.key === b.key) {
      a.matched = b.matched = true;
      a.open = b.open = false;
      a.el.classList.add("matched");
      b.el.classList.add("matched");
      state.open = [];
      state.pairs++;
      state.streak++;
      play("match", { streak: state.streak });
      snd.setIntensity(state.pairs / state.totalPairs);   // music speeds up as the picture appears
      const id = state.gameId;
      setTimeout(() => {
        if (id !== state.gameId) return;
        a.el.classList.add("cleared"); b.el.classList.add("cleared");
        play("clear");
      }, cfg.clearDelayMs);
      if (state.pairs === Math.floor(state.totalPairs / 2) && state.pairs < state.totalPairs) {
        setTimeout(() => { if (id === state.gameId && !state.over) play("halfway"); }, cfg.clearDelayMs + 250);
      }
      if (state.pairs === state.totalPairs) {
        setTimeout(() => {
          if (id !== state.gameId || state.over) return;
          showBanner(tr("boardCleared"), tr("boardClearedSub"));
          play("boardCleared");
        }, cfg.clearDelayMs + 600);
      }
    } else {
      a.el.classList.add("miss");
      b.el.classList.add("miss");
      state.streak = 0;
      play("miss");
      state.missTimer = setTimeout(closeMissed, cfg.flipBackDelayMs);
    }
    updateStats();
  }

  function flipByNumber(num) {
    const t = state.tiles[num - 1];
    if (t) flip(t);
  }

  // ---------- end of round ----------
  function showBanner(main, sub) {
    el.banner.innerHTML = `${main}${sub ? `<small>${sub}</small>` : ""}`;
    el.banner.hidden = false;
  }

  function uncoverAll() {
    closeMissed();
    state.over = true;
    el.board.classList.add("done");
    const rest = shuffle(state.tiles.filter((t) => !t.el.classList.contains("cleared")));
    rest.forEach((t, i) => setTimeout(() => {
      t.el.classList.add("matched", "cleared");
    }, i * 45));
    return rest.length * 45 + 500;
  }

  function endRound(correct) {
    if (state.over) return;
    const wait = uncoverAll();
    hidePeek();
    const title = state.answer ? state.answer.title : "";
    const id = state.gameId;
    setTimeout(() => {
      if (id !== state.gameId) return;
      snd.pauseMusic();
      if (correct) {
        showBanner(tr("correct", { title }),
                   tr("correctSub", { pairs: state.pairs, total: state.totalPairs, turns: state.turns }));
        play("fanfare");
        confetti();
      } else {
        showBanner(tr("reveal", { title }), tr("revealSub"));
        play("sadTrombone");
      }
    }, wait);
  }

  function confetti() {
    const colours = ["#ffd54f", "#e53935", "#43a047", "#1e88e5", "#ec407a", "#ffffff"];
    for (let i = 0; i < 90; i++) {
      const c = document.createElement("div");
      c.className = "confetti";
      c.style.left = Math.random() * 100 + "vw";
      c.style.background = colours[i % colours.length];
      c.style.animationDuration = 2 + Math.random() * 2.5 + "s";
      c.style.animationDelay = Math.random() * 0.6 + "s";
      document.body.appendChild(c);
      setTimeout(() => c.remove(), 5500);
    }
  }

  // ---------- host tools ----------
  let peekTimer = null;
  function togglePeek() {
    if (!el.peek.hidden) return hidePeek();
    el.peek.textContent = state.answer ? tr("peek", { title: state.answer.title }) : "";
    el.peek.hidden = false;
    peekTimer = setTimeout(hidePeek, 3000);
  }
  function hidePeek() { clearTimeout(peekTimer); el.peek.hidden = true; }

  function updateSoundLabels() {
    el.soundLabel.textContent = snd.sfx ? tr("soundOn") : tr("soundOff");
    if (el.musicLabel) el.musicLabel.textContent = snd.music ? tr("musicOn") : tr("musicOff");
  }
  function toggleSound() { snd.setSfx(!snd.sfx); updateSoundLabels(); }
  function toggleMusic() {
    snd.setMusic(!snd.music);
    if (snd.music && state.over) snd.pauseMusic();   // stay quiet until the next round starts
    updateSoundLabels();
  }

  function toggleFullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  }

  // Destructive actions need a second press within 2.5 s, so a stray key can't spoil a round.
  const armed = {};
  function confirmThen(action, fn) {
    const btn = document.querySelector(`[data-action="${action}"]`);
    // "New game" only needs confirming while a round is in progress
    if (action === "new" && (state.turns === 0 || state.over)) return fn();
    if (armed[action]) {
      clearTimeout(armed[action].timer);
      btn.classList.remove("armed");
      btn.innerHTML = armed[action].html;
      delete armed[action];
      return fn();
    }
    armed[action] = { html: btn.innerHTML, timer: setTimeout(() => {
      btn.classList.remove("armed");
      btn.innerHTML = armed[action].html;
      delete armed[action];
      if (action !== "new") snd.stopDrumroll();
    }, 2500) };
    if (action !== "new") play("drumroll");   // game-show suspense while the host confirms
    btn.classList.add("armed");
    btn.innerHTML = btn.innerHTML.replace(/<\/kbd>.*$/, "</kbd> " + tr("confirm"));
  }

  const actions = {
    new: () => confirmThen("new", () => newGame()),
    correct: () => { if (!state.over) confirmThen("correct", () => endRound(true)); },
    reveal: () => { if (!state.over) confirmThen("reveal", () => endRound(false)); },
    peek: togglePeek,
    sound: toggleSound,
    music: toggleMusic,
    fullscreen: toggleFullscreen
  };

  document.querySelectorAll("[data-action]").forEach((b) => {
    b.addEventListener("click", () => { actions[b.dataset.action](); b.blur(); });
  });

  // ---------- keyboard: host can type tile numbers the audience calls out ----------
  let entry = "", entryTimer = null;
  function commitEntry() {
    clearTimeout(entryTimer);
    const num = parseInt(entry, 10);
    entry = "";
    el.tileEntry.hidden = true;
    if (num >= 1 && num <= state.tiles.length) flipByNumber(num);
  }

  document.addEventListener("keydown", (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key.toLowerCase();

    if (/^[0-9]$/.test(k)) {
      entry += k;
      play("tick");
      el.tileEntry.textContent = tr("tileEntry", { n: entry });
      el.tileEntry.hidden = false;
      clearTimeout(entryTimer);
      // commit straight away when no further digit could make a valid tile number
      if (parseInt(entry, 10) * 10 > state.tiles.length || entry.length >= String(state.tiles.length).length) commitEntry();
      else entryTimer = setTimeout(commitEntry, 1200);
      return;
    }
    if (k === "enter" && entry) { e.preventDefault(); return commitEntry(); }
    if (k === "escape") { entry = ""; el.tileEntry.hidden = true; hidePeek(); return; }

    const map = { n: "new", c: "correct", r: "reveal", p: "peek", m: "sound", b: "music", f: "fullscreen" };
    if (map[k]) { e.preventDefault(); actions[map[k]](); }
  });

  updateSoundLabels();
  newGame(true);

  // exposed for automated testing only
  window.__game = { state, flipByNumber, newGame, endRound };
})();
