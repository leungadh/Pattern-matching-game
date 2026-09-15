/*
 * Sound engine for Pattern Match.
 * Every sound is synthesised by the browser (Web Audio API), so there are no audio files
 * to ship and nothing to install. Works from file:// in Edge, Chrome, Firefox and Safari.
 *
 *   Sound.play("flip" | "match" | "miss" | "clear" | "halfway" | "boardCleared" |
 *              "shuffle" | "drumroll" | "fanfare" | "sadTrombone" | "tick", opts)
 *   Sound.stopDrumroll()
 *   Sound.setSfx(bool) / Sound.setMusic(bool) / Sound.setIntensity(0..1)
 */
(function () {
  "use strict";

  let ctx = null, master, sfxBus, musicBus, noiseBuf;
  let sfxOn = true, musicOn = false, volume = 0.8;

  function init() {
    if (ctx) return ctx;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -14; comp.ratio.value = 4;
    master = ctx.createGain(); master.gain.value = volume;
    sfxBus = ctx.createGain(); sfxBus.gain.value = 1;
    musicBus = ctx.createGain(); musicBus.gain.value = 0.35;
    sfxBus.connect(master); musicBus.connect(master); master.connect(comp); comp.connect(ctx.destination);

    // 2 seconds of white noise, reused for clicks, drums and cymbals
    noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const d = noiseBuf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    return ctx;
  }

  // Browsers only allow audio after a click or key press, so unlock on the first one.
  let unlocked = false;
  function unlock() {
    if (!init()) return;
    if (ctx.state === "suspended") ctx.resume();
    if (!unlocked && musicOn) Music.start();
    unlocked = true;
  }
  ["pointerdown", "keydown"].forEach((ev) => window.addEventListener(ev, unlock, { capture: true }));

  // ---------- building blocks ----------
  const midi = (n) => 440 * Math.pow(2, (n - 69) / 12);

  function env(g, t, peak, attack, decay) {
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(peak, t + attack);
    g.gain.exponentialRampToValueAtTime(0.0001, t + attack + decay);
  }

  function osc({ freq, type = "sine", t = 0, peak = 0.2, attack = 0.005, decay = 0.3,
                 slideTo = null, bus = sfxBus, filter = null, vibrato = 0 }) {
    const start = ctx.currentTime + t;
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = type;
    o.frequency.setValueAtTime(freq, start);
    if (slideTo) o.frequency.exponentialRampToValueAtTime(slideTo, start + attack + decay);
    if (vibrato) {
      const lfo = ctx.createOscillator(), lg = ctx.createGain();
      lfo.frequency.value = 6; lg.gain.value = vibrato;
      lfo.connect(lg).connect(o.frequency);
      lfo.start(start); lfo.stop(start + attack + decay + 0.05);
    }
    env(g, start, peak, attack, decay);
    let node = o;
    if (filter) {
      const f = ctx.createBiquadFilter();
      f.type = filter.type || "lowpass"; f.frequency.value = filter.freq; f.Q.value = filter.q || 1;
      node.connect(f); node = f;
    }
    node.connect(g).connect(bus);
    o.start(start); o.stop(start + attack + decay + 0.05);
    return o;
  }

  function noise({ t = 0, peak = 0.2, attack = 0.002, decay = 0.1, type = "bandpass",
                   freq = 2000, q = 1, bus = sfxBus }) {
    const start = ctx.currentTime + t;
    const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
    s.buffer = noiseBuf;
    s.loop = true;
    f.type = type; f.frequency.value = freq; f.Q.value = q;
    env(g, start, peak, attack, decay);
    s.connect(f).connect(g).connect(bus);
    s.start(start, Math.random()); s.stop(start + attack + decay + 0.05);
    return s;
  }

  // a soft bell: fundamental + a slightly detuned overtone
  function bell(note, t, peak = 0.16, decay = 0.6) {
    osc({ freq: midi(note), type: "sine", t, peak, decay });
    osc({ freq: midi(note) * 2.01, type: "sine", t, peak: peak * 0.35, decay: decay * 0.6 });
    osc({ freq: midi(note), type: "triangle", t, peak: peak * 0.3, decay: 0.12 });
  }

  // C-major pentatonic, used so rising combos always sound pleasant
  const PENTA = [0, 2, 4, 7, 9];
  const pent = (step, base = 72) => base + 12 * Math.floor(step / 5) + PENTA[((step % 5) + 5) % 5];

  // ---------- sound effects ----------
  let drumroll = null;

  const SFX = {
    // card flip: a short papery swish plus a tiny wooden click
    flip() {
      noise({ peak: 0.7, decay: 0.07, freq: 3200, q: 0.8 });
      osc({ freq: 1400, type: "triangle", peak: 0.14, decay: 0.03, slideTo: 700 });
    },

    // matched pair: a two-note chime that climbs higher with every match in a row
    match({ streak = 1 } = {}) {
      const s = Math.min(streak - 1, 9);
      bell(pent(s * 2), 0, 0.18);
      bell(pent(s * 2 + 2), 0.09, 0.18, 0.8);
      if (streak >= 3) bell(pent(s * 2 + 4), 0.18, 0.14, 0.9);   // combo sparkle
      if (streak >= 5) noise({ t: 0.18, peak: 0.08, decay: 0.5, type: "highpass", freq: 7000 });
    },

    // wrong pair: a gentle "uh-oh"
    miss() {
      osc({ freq: midi(62), type: "square", peak: 0.08, decay: 0.14, filter: { freq: 1200 } });
      osc({ freq: midi(58), type: "square", t: 0.15, peak: 0.08, decay: 0.28, slideTo: midi(55), filter: { freq: 900 } });
    },

    // matched tiles fade away: a quick glittery run
    clear() {
      [0, 2, 4, 5, 7].forEach((st, i) => osc({ freq: midi(pent(st, 84)), type: "sine", t: i * 0.035, peak: 0.05, decay: 0.18 }));
    },

    // halfway through the board
    halfway() {
      [67, 72, 76, 79].forEach((n, i) => bell(n, i * 0.1, 0.13, 0.5));
    },

    // every pair found — the picture is fully visible
    boardCleared() {
      [60, 64, 67, 72, 76, 79, 84].forEach((n, i) => bell(n, i * 0.07, 0.12, 0.7));
    },

    // new game: cards being shuffled, then a ready chime
    shuffle() {
      for (let i = 0; i < 12; i++) {
        noise({ t: i * 0.045 * (1 - i * 0.03), peak: 0.18, decay: 0.03, freq: 2500 + Math.random() * 1500, q: 1.2 });
      }
      bell(79, 0.55, 0.12, 0.5); bell(84, 0.62, 0.12, 0.7);
    },

    // host pressed C or R once: game-show snare roll until confirmed
    drumroll() {
      if (drumroll) return;
      const nodes = [];
      const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
      const lfo = ctx.createOscillator(), lg = ctx.createGain();
      s.buffer = noiseBuf; s.loop = true;
      f.type = "bandpass"; f.frequency.value = 1800; f.Q.value = 0.7;
      g.gain.value = 0;
      g.gain.setTargetAtTime(0.18, ctx.currentTime, 0.6);          // roll gets louder
      lfo.frequency.value = 18; lg.gain.value = 0.09;               // the "rrrr" of the sticks
      lfo.connect(lg).connect(g.gain);
      s.connect(f).connect(g).connect(sfxBus);
      s.start(); lfo.start();
      nodes.push(s, lfo);
      drumroll = { nodes, g };
    },

    // someone guessed right
    fanfare() {
      stopDrumroll();
      noise({ peak: 0.3, decay: 1.6, type: "highpass", freq: 5000 });              // cymbal crash
      osc({ freq: 55, type: "sine", peak: 0.5, decay: 0.35, slideTo: 40 });        // kick
      const line = [[67, 0], [67, 0.12], [67, 0.24], [72, 0.4], [76, 0.62], [79, 0.84]];
      line.forEach(([n, t]) => {
        osc({ freq: midi(n), type: "sawtooth", t, peak: 0.07, decay: 0.2, filter: { freq: 2500 } });
        osc({ freq: midi(n - 12), type: "square", t, peak: 0.05, decay: 0.2, filter: { freq: 1500 } });
      });
      [72, 76, 79, 84].forEach((n) => osc({ freq: midi(n), type: "sawtooth", t: 1.05, peak: 0.05, attack: 0.02, decay: 1.2, filter: { freq: 3000 }, vibrato: 4 }));
      osc({ freq: midi(48), type: "triangle", t: 1.05, peak: 0.2, decay: 1.2 });
    },

    // nobody guessed: "wah wah wah wahhh"
    sadTrombone() {
      stopDrumroll();
      [[63, 0, 0.35], [62, 0.45, 0.35], [61, 0.9, 0.35], [60, 1.35, 1.2]].forEach(([n, t, d], i) => {
        osc({ freq: midi(n - 12), type: "sawtooth", t, peak: 0.22, attack: 0.04, decay: d,
              filter: { freq: 900, q: 3 }, vibrato: i === 3 ? 7 : 0, slideTo: i === 3 ? midi(n - 13) : null });
      });
    },

    // little tick for typed tile numbers
    tick() {
      osc({ freq: 1800, type: "square", peak: 0.03, decay: 0.02, filter: { freq: 3000 } });
    }
  };

  function stopDrumroll() {
    if (!drumroll) return;
    const { nodes, g } = drumroll;
    g.gain.cancelScheduledValues(ctx.currentTime);
    g.gain.setTargetAtTime(0, ctx.currentTime, 0.03);
    nodes.forEach((n) => { try { n.stop(ctx.currentTime + 0.2); } catch (e) {} });
    drumroll = null;
  }

  // ---------- background music: a light, looping game-show groove ----------
  const Music = (function () {
    // C - Am - F - G, one bar each
    const CHORDS = [[48, 60, 64, 67], [45, 57, 60, 64], [41, 57, 60, 65], [43, 55, 59, 62]];
    let timer = null, nextTime = 0, step = 0, intensity = 0;

    function schedule() {
      const bpm = 100 + intensity * 30;          // speeds up as more pairs are found
      const eighth = 60 / bpm / 2;
      while (nextTime < ctx.currentTime + 0.15) {
        const t = nextTime - ctx.currentTime;
        const bar = Math.floor(step / 8) % 4, beat = step % 8;
        const [bass, ...tones] = CHORDS[bar];
        const opt = { bus: musicBus };
        if (beat === 0 || beat === 4) osc({ ...opt, freq: midi(bass), type: "triangle", t, peak: 0.3, decay: 0.35 });
        if (beat === 6) osc({ ...opt, freq: midi(bass + 7), type: "triangle", t, peak: 0.2, decay: 0.2 });
        const arp = [0, 1, 2, 1, 0, 2, 1, 2][beat];
        osc({ ...opt, freq: midi(tones[arp] + 12), type: "square", t, peak: 0.035, decay: 0.12, filter: { freq: 2200 } });
        if (beat % 2 === 1) noise({ ...opt, t, peak: 0.05, decay: 0.03, type: "highpass", freq: 8000 });
        if (beat === 2 || beat === 6) noise({ ...opt, t, peak: 0.08 + intensity * 0.05, decay: 0.08, freq: 1800, q: 0.8 });
        nextTime += eighth;
        step++;
      }
    }

    return {
      start() {
        if (!ctx || timer) return;
        nextTime = ctx.currentTime + 0.05;
        timer = setInterval(schedule, 25);
      },
      stop() { clearInterval(timer); timer = null; },
      setIntensity(x) { intensity = Math.max(0, Math.min(1, x)); },
      get playing() { return !!timer; }
    };
  })();

  // ---------- public API ----------
  window.Sound = {
    play(name, opts) {
      if (!sfxOn || !init() || !SFX[name]) return;
      if (ctx.state === "suspended") ctx.resume();
      try { SFX[name](opts); } catch (e) { /* sound must never break the game */ }
    },
    stopDrumroll() { if (ctx) stopDrumroll(); },
    setSfx(on) { sfxOn = !!on; if (!sfxOn && ctx) stopDrumroll(); },
    setMusic(on) {
      musicOn = !!on;
      if (!musicOn) return Music.stop();
      if (ctx) { if (ctx.state === "suspended") ctx.resume(); Music.start(); }
      // otherwise it starts on the first click/key press (browsers block audio before that)
    },
    setIntensity(x) { Music.setIntensity(x); },
    pauseMusic() { Music.stop(); },
    resumeMusic() { if (musicOn && ctx) Music.start(); },
    setVolume(v) { volume = Math.max(0, Math.min(1, v)); if (master) master.gain.value = volume; },
    get sfx() { return sfxOn; },
    get music() { return musicOn; },
    get musicPlaying() { return Music.playing; }
  };
})();
