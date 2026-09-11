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
    title: "Pattern Match", gridSize: 6, icons: [], answers: [],
    flipBackDelayMs: 1200, clearDelayMs: 700, sound: true, music: false, volume: 0.8
  };
  const cfg = Object.assign({}, DEFAULTS, window.GAME_CONFIG || {});
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
    document.documentElement.style.setProperty("--n", n);
    el.title.textContent = cfg.title;
    document.title = cfg.title;

    Object.assign(state, { tiles: [], open: [], missTimer: null, pairs: 0, turns: 0, streak: 0, over: false });
    state.gameId++;
    state.totalPairs = total / 2;
    el.banner.hidden = true;
    hidePeek();
    updateStats();
    snd.stopDrumroll();
    snd.setIntensity(0);
    snd.resumeMusic();
    if (firstLoad !== true) play("shuffle");

    if (total % 2 !== 0) return showError(`gridSize ${n} gives ${total} tiles — it must be an even number.`);
    if (cfg.icons.length < state.totalPairs) {
      return showError(`Not enough icons in config.js: need ${state.totalPairs}, found ${cfg.icons.length}.`);
    }

    state.answer = pickAnswer();
    if (!state.answer) return showError("No answer images listed in config.js (answers: [...]).");
    el.answerLayer.style.backgroundImage = `url("${encodeURI(state.answer.image)}")`;
    const probe = new Image();
    probe.onerror = () => showError(`Could not load answer image:<br><b>${state.answer.image}</b><br>Check the file name in config.js.`);
    probe.src = state.answer.image;

    // choose icons for this game, duplicate into pairs, shuffle positions
    const chosen = shuffle(cfg.icons.slice()).slice(0, state.totalPairs);
    const deck = shuffle(chosen.flatMap((src) => [src, src]));

    el.grid.innerHTML = "";
    deck.forEach((src, i) => {
      const b = document.createElement("button");
      b.className = "tile";
      b.type = "button";
      b.setAttribute("aria-label", `Tile ${i + 1}`);
      b.innerHTML =
        `<span class="tile-inner">` +
          `<span class="face front">${i + 1}</span>` +
          `<span class="face back"><img alt="" draggable="false"></span>` +
        `</span>`;
      b.querySelector("img").src = src;
      const tile = { el: b, key: src, index: i, open: false, matched: false };
      b.addEventListener("click", () => flip(tile));
      el.grid.appendChild(b);
      state.tiles.push(tile);
    });
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
          showBanner("Board cleared!", "What's the picture? Host: press C or R");
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
        showBanner(`Correct! It's ${title}`, `Solved with ${state.pairs} of ${state.totalPairs} pairs found in ${state.turns} turns`);
        play("fanfare");
        confetti();
      } else {
        showBanner(`It was: ${title}`, "Press N for a new game");
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
    el.peek.textContent = state.answer ? `Answer: ${state.answer.title}` : "";
    el.peek.hidden = false;
    peekTimer = setTimeout(hidePeek, 3000);
  }
  function hidePeek() { clearTimeout(peekTimer); el.peek.hidden = true; }

  function updateSoundLabels() {
    el.soundLabel.textContent = snd.sfx ? "Sound on" : "Sound off";
    if (el.musicLabel) el.musicLabel.textContent = snd.music ? "Music on" : "Music off";
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
    btn.innerHTML = btn.innerHTML.replace(/<\/kbd>.*$/, "</kbd> Press again to confirm");
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
      el.tileEntry.textContent = `Tile ${entry}…`;
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
