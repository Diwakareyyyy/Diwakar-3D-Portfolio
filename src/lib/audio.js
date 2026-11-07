// Portfolio Audio Engine — Initial Walking Character Intro Footsteps ONLY
// =========================================================================================
// Strict Audio Policy:
//   1. Footsteps Sound ONLY: Synchronized with the walking character on the Homepage intro
//      using `public/audio/boot_step_left.wav` and `public/audio/boot_step_right.wav`.
//   2. Footsteps play ONLY while the walking intro is active.
//   3. Footsteps STOP completely as soon as the walking video finishes, the intro settles,
//      or the user navigates away from the Homepage.
//   4. Background music, ambient music, whoosh effects, click SFX, and transition sounds
//      are COMPLETELY REMOVED / DISABLED. No other audio anywhere on the site.
// =========================================================================================

export const AUDIO_PATHS = {
  // Intro walking boot-footstep sound effects (synchronized to hero walk cycle)
  stepL: 'public/audio/boot_step_left.wav',
  stepR: 'public/audio/boot_step_right.wav',
};

// Synchronized left/right foot-contact phases across the hero walk cycle
const HERO_STEP_PHASES = [
  { phase: 0.020, foot: 'L' },
  { phase: 0.087, foot: 'R' },
  { phase: 0.213, foot: 'L' },
  { phase: 0.340, foot: 'R' },
  { phase: 0.500, foot: 'L' },
  { phase: 0.637, foot: 'R' },
  { phase: 0.760, foot: 'L' },
  { phase: 0.880, foot: 'R' },
];

export class CinematicAudio {
  constructor() {
    this.ctx = null;
    this.masterGain = null;
    this.sfxGain = null;

    this.buffers = { stepL: null, stepR: null };
    this.buffersReady = false;
    this.loadingPromise = null;

    // User-controllable state
    this.unlocked = false;
    this.muted = false;
    this.sfxEnabled = true;
    this.volume = 0.75; // 0..1

    // Intro walking state: footsteps play ONLY during intro walk
    this.introWalkDone = false;
    this.introStepsPlayed = 0;
    this.targetIntroSteps = 8;
    this.lastClipPhase = -1;
    this.lastStepAtMs = 0;
    this.lastSeqTime = 0;
    this.heroOnScreen = true;
    this.currentSection = 'stage';

    this._bindUnlockEvents();
    this._bindUI();
    this._bindVisibility();

    // Attempt early context initialization in case browser permits autoplay
    this._tryAutoUnlock();
  }

  _ensureContext() {
    if (this.ctx) return this.ctx;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return null;

    const ctx = new AudioCtx();
    this.ctx = ctx;

    // Master -> Destination
    this.masterGain = ctx.createGain();
    this.masterGain.gain.value = this.muted ? 0 : this.volume;
    this.masterGain.connect(ctx.destination);

    // SFX chain: Footsteps -> SFX Gain -> Master
    this.sfxGain = ctx.createGain();
    this.sfxGain.gain.value = this.sfxEnabled ? 1.0 : 0.0;
    this.sfxGain.connect(this.masterGain);

    return ctx;
  }

  async _loadBuffers() {
    if (this.loadingPromise) return this.loadingPromise;
    const ctx = this._ensureContext();
    if (!ctx) return;

    const loadOne = async (key, url) => {
      try {
        const res = await fetch(url);
        if (!res.ok) return false;
        const arr = await res.arrayBuffer();
        this.buffers[key] = await ctx.decodeAudioData(arr);
        return true;
      } catch (e) {
        console.warn(`[audio] Could not load ${url}:`, e.message);
        return false;
      }
    };

    this.loadingPromise = Promise.all([
      loadOne('stepL', AUDIO_PATHS.stepL),
      loadOne('stepR', AUDIO_PATHS.stepR),
    ]).then(() => {
      this.buffersReady = true;
    });
    return this.loadingPromise;
  }

  async _tryAutoUnlock() {
    try {
      const ctx = this._ensureContext();
      if (!ctx) return;
      this._loadBuffers();
      if (ctx.state === 'running') {
        this.unlocked = true;
        this._updateUI();
      }
    } catch {
      // Autoplay blocked until gesture; handled by _bindUnlockEvents
    }
  }

  _bindUnlockEvents() {
    const unlock = async () => {
      if (this.unlocked) return;
      const ctx = this._ensureContext();
      if (!ctx) return;

      try {
        if (ctx.state === 'suspended') {
          await ctx.resume();
        }
      } catch {
        // Ignore non-gesture rejection
      }

      if (ctx.state === 'running') {
        this.unlocked = true;

        if (this.heroOnScreen && this.introStepsPlayed === 0 && this.lastSeqTime >= 5.2) {
          this.introWalkDone = false;
          this.targetIntroSteps = 4;
        } else if (!this.heroOnScreen) {
          this.introWalkDone = true;
        }

        this._updateUI();
        await this._loadBuffers();
      }
    };

    const events = ['pointerdown', 'click', 'keydown', 'touchstart'];
    events.forEach((ev) => {
      window.addEventListener(ev, unlock, { passive: true });
    });
  }

  /**
   * Concludes the intro walking audio. No further sounds will play anywhere.
   */
  _finishIntroWalk() {
    if (this.introWalkDone) return;
    this.introWalkDone = true;
    this._updateUI();
  }

  /**
   * Plays a single synchronized acoustic boot footstep ('L' or 'R').
   * STRICT: Never plays after introWalkDone is true.
   */
  playBootStep(foot = 'L', intensity = 1.0) {
    if (this.introWalkDone) return;
    if (!this.unlocked || this.muted || !this.sfxEnabled || !this.ctx) return;
    const ctx = this.ctx;
    if (ctx.state !== 'running') return;

    const now = ctx.currentTime;
    const panVal = foot === 'L' ? -0.12 : 0.12;

    const panner = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
    const stepGain = ctx.createGain();
    stepGain.gain.value = Math.min(1.0, 0.85 * intensity);

    if (panner) {
      panner.pan.value = panVal;
      stepGain.connect(panner);
      panner.connect(this.sfxGain);
    } else {
      stepGain.connect(this.sfxGain);
    }

    const buf = foot === 'L' ? this.buffers.stepL : this.buffers.stepR;
    if (buf) {
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.playbackRate.value = (foot === 'L' ? 0.99 : 1.01) + (Math.random() - 0.5) * 0.015;
      src.connect(stepGain);
      src.start(now);
    }
  }

  /**
   * Called each frame from main.js.
   * Plays synchronized boot footsteps during the intro walk ONLY.
   * Immediately stops when the walk finishes or when the intro settles.
   */
  syncIntroWalk(seqTimeSec, heroClip, heroOnScreen, settledTimeSec = 6.25) {
    this.lastSeqTime = seqTimeSec;
    this.heroOnScreen = heroOnScreen !== false;

    // If intro walk is already complete, do nothing (no sounds whatsoever)
    if (this.introWalkDone) {
      return;
    }

    // Stop footsteps immediately if user scrolled past Intro
    if (heroOnScreen === false) {
      this._finishIntroWalk();
      return;
    }

    // Stop footsteps once the intro timeline settles
    if (seqTimeSec >= settledTimeSec) {
      this._finishIntroWalk();
      return;
    }

    const el = heroClip?.el;
    if (!el || el.paused || !heroClip.duration) return;

    // Stop footsteps if video has finished playing
    if (el.currentTime >= (heroClip.duration || 10.0) * 0.95) {
      this._finishIntroWalk();
      return;
    }

    const dur = heroClip.duration || 10.0;
    const phase = (el.currentTime % dur) / dur;

    if (!this.unlocked) {
      this.lastClipPhase = phase;
      return;
    }

    const prev = this.lastClipPhase;
    this.lastClipPhase = phase;

    // Play initial boot step when walking starts
    const nowMs = performance.now();
    if (this.introStepsPlayed === 0 && nowMs - this.lastStepAtMs > 460) {
      this.lastStepAtMs = nowMs;
      this.introStepsPlayed = 1;
      this.playBootStep('L', 0.95);
      return;
    }

    if (prev < 0 || nowMs - this.lastStepAtMs < 460) return;

    for (const st of HERO_STEP_PHASES) {
      const crossed =
        (prev <= st.phase && phase >= st.phase && phase - prev < 0.25) ||
        (prev > 0.90 && phase < 0.10 && (st.phase >= prev || st.phase <= phase));
      if (crossed) {
        this.lastStepAtMs = nowMs;
        this.introStepsPlayed += 1;
        const foot = this.introStepsPlayed % 2 === 1 ? 'L' : 'R';
        const isLast = this.introStepsPlayed >= this.targetIntroSteps;
        this.playBootStep(foot, isLast ? 0.82 : 0.96);

        if (isLast) {
          this._finishIntroWalk();
        }
        break;
      }
    }
  }

  /**
   * Called when the active section changes.
   * Completely silent: immediately stops footsteps if user navigates away from Intro.
   */
  onSectionChange(sectionId) {
    if (!sectionId || sectionId === this.currentSection) return;
    this.currentSection = sectionId;

    if (sectionId !== 'stage' && sectionId !== 'home' && !this.introWalkDone) {
      this._finishIntroWalk();
    }
  }

  setMuted(muted) {
    this.muted = Boolean(muted);
    if (this.ctx && this.masterGain) {
      const now = this.ctx.currentTime;
      this.masterGain.gain.cancelScheduledValues(now);
      this.masterGain.gain.setTargetAtTime(this.muted ? 0.0 : this.volume, now, 0.05);
    }
    this._updateUI();
  }

  toggleMute() {
    this.setMuted(!this.muted);
  }

  setSfxEnabled(enabled) {
    this.sfxEnabled = Boolean(enabled);
    if (this.ctx && this.sfxGain) {
      const now = this.ctx.currentTime;
      this.sfxGain.gain.cancelScheduledValues(now);
      this.sfxGain.gain.setTargetAtTime(this.sfxEnabled ? 1.0 : 0.0, now, 0.05);
    }
    this._updateUI();
  }

  setVolume(val) {
    this.volume = Math.max(0, Math.min(1, Number(val)));
    if (this.volume > 0 && this.muted) {
      this.muted = false;
    }
    if (this.ctx && this.masterGain) {
      const now = this.ctx.currentTime;
      this.masterGain.gain.cancelScheduledValues(now);
      this.masterGain.gain.setTargetAtTime(this.muted ? 0.0 : this.volume, now, 0.05);
    }
    this._updateUI();
  }

  _bindVisibility() {
    document.addEventListener('visibilitychange', () => {
      if (!this.ctx || !this.unlocked) return;
      if (document.visibilityState === 'hidden') {
        this.ctx.suspend().catch(() => {});
      } else {
        this.ctx.resume().catch(() => {});
      }
    });
  }

  _bindUI() {
    const rootEl = document.getElementById('audioCtrl');
    const muteBtn = document.getElementById('audioMuteBtn');
    const panelBtn = document.getElementById('audioPanelBtn');
    const panel = document.getElementById('audioPanel');
    const sfxBtn = document.getElementById('audioSfxToggle');
    const volSlider = document.getElementById('audioVolSlider');

    if (!rootEl) return;

    muteBtn?.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleMute();
    });

    panelBtn?.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = rootEl.classList.toggle('is-open');
      panelBtn.setAttribute('aria-expanded', String(isOpen));
      if (panel) panel.hidden = !isOpen;
    });

    sfxBtn?.addEventListener('click', (e) => {
      e.stopPropagation();
      this.setSfxEnabled(!this.sfxEnabled);
      // STRICT: No preview click sound. Only synchronized intro walking footsteps are permitted.
    });

    volSlider?.addEventListener('input', (e) => {
      this.setVolume(parseFloat(e.target.value) / 100);
    });

    document.addEventListener('click', (e) => {
      if (rootEl.classList.contains('is-open') && !rootEl.contains(e.target)) {
        rootEl.classList.remove('is-open');
        panelBtn?.setAttribute('aria-expanded', 'false');
        if (panel) panel.hidden = true;
      }
    });

    this._updateUI();
  }

  _updateUI() {
    const rootEl = document.getElementById('audioCtrl');
    const muteBtn = document.getElementById('audioMuteBtn');
    const muteLabel = document.getElementById('audioMuteLabel');
    const sfxBtn = document.getElementById('audioSfxToggle');
    const volSlider = document.getElementById('audioVolSlider');
    const volVal = document.getElementById('audioVolVal');

    if (!rootEl) return;

    const activeSound = !this.muted && this.volume > 0 && this.sfxEnabled && !this.introWalkDone;
    rootEl.classList.toggle('is-muted', this.muted || !this.sfxEnabled);
    rootEl.classList.toggle('is-playing', Boolean(this.unlocked && activeSound));

    if (muteBtn) {
      muteBtn.setAttribute('aria-pressed', String(this.muted));
      muteBtn.setAttribute('title', this.muted ? 'Unmute footsteps audio' : 'Mute footsteps audio');
    }
    if (muteLabel) {
      muteLabel.textContent = this.muted ? 'MUTED' : 'SOUND';
    }
    if (sfxBtn) {
      sfxBtn.classList.toggle('is-on', this.sfxEnabled && !this.muted);
      sfxBtn.setAttribute('aria-pressed', String(this.sfxEnabled));
      const stateSpan = sfxBtn.querySelector('.audio-toggle__state');
      if (stateSpan) stateSpan.textContent = this.sfxEnabled ? 'ON' : 'OFF';
    }
    const pct = Math.round((this.muted ? 0 : this.volume) * 100);
    if (volSlider && document.activeElement !== volSlider) {
      volSlider.value = String(pct);
    }
    if (volVal) {
      volVal.textContent = `${pct}%`;
    }
  }
}
