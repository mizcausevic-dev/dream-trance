arrangement" ? "arrangement A" : "variation " + variation.toUpperCase();
      document.getElementById("transport-label").textContent = item.title + " " + mode + " · Space plays · J and K change kit";
      for (const button of rail.querySelectorAll("button")) button.setAttribute("aria-pressed", button.dataset.id === kitId ? "true" : "false");
      document.getElementById("var-a").setAttribute("aria-pressed", view === "kit" && variation === "a" ? "true" : "false");
      document.getElementById("var-b").setAttribute("aria-pressed", view === "kit" && variation === "b" ? "true" : "false");
      document.getElementById("view-kit").setAttribute("aria-pressed", view === "kit" ? "true" : "false");
      document.getElementById("view-arr").setAttribute("aria-pressed", view === "arrangement" ? "true" : "false");
      phrases.innerHTML = "";
      const phraseList = view === "arrangement" ? item.arrangement_phrases : item.phrases;
      phraseList.forEach((phrase) => {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = phrase.name;
        button.addEventListener("click", () => {
          const x = (phrase.start_bar / bars) * rollWidth;
          scroller.scrollTo({ left: Math.max(0, x - 12), behavior: "smooth" });
        });
        phrases.appendChild(button);
      });
    }
    function drawLane(host, notes, role, bars) {
      host.querySelectorAll(".block").forEach((node) => node.remove());
      const container = bars * 4 * 960;
      if (!notes.length) {
        const empty = document.createElement("div");
        empty.className = "block";
        empty.textContent = "";
        return;
      }
      const low = Math.min(...notes.map((note) => note.pitch));
      const high = Math.max(...notes.map((note) => note.pitch));
      const span = Math.max(1, high - low);
      notes.forEach((note) => {
        const block = document.createElement("div");
        block.className = "block " + role;
        block.title = pitchName(note.pitch) + " · velocity " + note.velocity;
        const y = 16 + (1 - (note.pitch - low) / span) * 46;
        block.style.left = (note.start / container) * rollWidth + "px";
        block.style.width = Math.max(3, (note.duration / container) * rollWidth - 1) + "px";
        block.style.top = y + "px";
        block.style.height = (6 + (note.velocity / 127) * 14) + "px";
        host.appendChild(block);
      });
    }
    function draw() {
      const item = kit();
      const bars = view === "arrangement" ? item.arrangement_bars : item.bars;
      rollWidth = Math.max(960, bars * 150);
      ruler.style.width = rollWidth + "px";
      ruler.innerHTML = "";
      let bar = 0;
      item.changes.forEach((name, index) => {
        const span = item.change_bars[index];
        if (view === "arrangement") {
          for (let copy = 0; copy < item.arrangement_bars; copy += item.bars) {
            const mark = document.createElement("div");
            mark.className = "change";
            mark.textContent = name;
            mark.style.left = ((copy + bar) / bars) * rollWidth + "px";
            mark.style.width = (span / bars) * rollWidth + "px";
            ruler.appendChild(mark);
          }
        } else {
          const mark = document.createElement("div");
          mark.className = "change";
          mark.textContent = name;
          mark.style.left = (bar / item.bars) * rollWidth + "px";
          mark.style.width = (span / item.bars) * rollWidth + "px";
          ruler.appendChild(mark);
        }
        bar += span;
      });
      lanes.innerHTML = "";
      labelCol.innerHTML = "";
      const gap = document.createElement("div");
      gap.className = "ruler-gap";
      labelCol.appendChild(gap);
      let total = 0;
      pack.roles.forEach((role) => {
        const label = document.createElement("div");
        label.className = "lane-label";
        label.textContent = role.label;
        labelCol.appendChild(label);
        const notesHost = document.createElement("div");
        notesHost.className = "lane-notes";
        notesHost.style.width = rollWidth + "px";
        const notes = laneNotes[role.id] || [];
        total += notes.length;
        drawLane(notesHost, notes, role.id, bars);
        lanes.appendChild(notesHost);
      });
      const source = view === "arrangement" ? "arrangement file" : "part files";
      status.textContent = total + " notes across " + pack.roles.length + " lanes, read from the " + source + ".";
    }
    async function loadKit() {
      stopPlayback();
      renderCopy();
      status.textContent = "Reading the MIDI.";
      laneNotes = {};
      try {
        if (view === "kit") {
          for (const role of pack.roles) {
            const response = await fetch(partPath(role.id));
            if (!response.ok) throw new Error(role.id + " request failed");
            const tracks = parseMidi(await response.arrayBuffer());
            laneNotes[role.id] = tracks[0].notes;
          }
        } else {
          const response = await fetch(arrangementPath());
          if (!response.ok) throw new Error("arrangement request failed");
          const tracks = parseMidi(await response.arrayBuffer());
          const byName = {};
          tracks.forEach((track) => { byName[track.name] = track.notes; });
          pack.roles.forEach((role) => {
            laneNotes[role.id] = byName[role.label] || [];
          });
        }
        draw();
      } catch (error) {
        laneNotes = {};
        lanes.innerHTML = "";
        status.textContent = "The MIDI did not load. " + error.message;
      }
    }
    function freq(pitch) {
      return 440 * Math.pow(2, (pitch - 69) / 12);
    }
    function scheduleTone(ctx, note, origin, secondsOf, type, amount, attack) {
      const when = origin + secondsOf(note.start);
      const duration = Math.max(0.05, secondsOf(note.duration));
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = type;
      osc.frequency.value = freq(note.pitch);
      const level = amount * (note.velocity / 110);
      gain.gain.setValueAtTime(0.0001, when);
      gain.gain.exponentialRampToValueAtTime(Math.max(0.0002, level), when + Math.min(attack, duration * 0.4));
      gain.gain.exponentialRampToValueAtTime(0.0001, when + duration);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(when);
      osc.stop(when + duration + 0.02);
    }
    function scheduleNoise(ctx, note, origin, secondsOf, amount, decay) {
      const when = origin + secondsOf(note.start);
      const duration = Math.max(0.03, Math.min(0.4, secondsOf(note.duration)));
      const count = Math.max(1, Math.floor(ctx.sampleRate * duration));
      const buffer = ctx.createBuffer(1, count, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      let state = note.pitch * 17 + note.start;
      for (let index = 0; index < count; index += 1) {
        state = (1103515245 * state + 12345) & 0x7fffffff;
        const noise = state / 0x7fffffff * 2 - 1;
        data[index] = noise * Math.exp(-decay * index / ctx.sampleRate);
      }
      const source = ctx.createBufferSource();
      source.buffer = buffer;
      const gain = ctx.createGain();
      gain.gain.value = amount * (note.velocity / 110);
      source.connect(gain);
      gain.connect(ctx.destination);
      source.start(when);
    }
    function schedule(ctx, note, origin, secondsOf, role) {
      if (role === "drums") {
        if (note.pitch === 36) scheduleTone(ctx, note, origin, secondsOf, "sine", 0.12, 0.005);
        else scheduleNoise(ctx, note, origin, secondsOf, 0.05, note.pitch === 46 ? 8 : 30);
        return;
      }
      if (role === "bass") scheduleTone(ctx, note, origin, secondsOf, "sine", 0.09, 0.01);
      else if (role === "keys") scheduleTone(ctx, note, origin, secondsOf, "triangle", 0.04, 0.012);
      else if (role === "lead") scheduleTone(ctx, note, origin, secondsOf, "triangle", 0.05, 0.016);
      else if (role === "pad") scheduleTone(ctx, note, origin, secondsOf, "sine", 0.02, 0.12);
    }
    function stopPlayback() {
      playing = false;
      cancelAnimationFrame(followId);
      if (audio) audio.close();
      audio = null;
      document.getElementById("play").textContent = "Play lanes";
    }
    function playLanes() {
      const notes = pack.roles.flatMap((role) => (laneNotes[role.id] || []).map((note) => ({ note: note, role: role.id })));
      if (!notes.length) return;
      stopPlayback();
      const ctx = new AudioContext();
      audio = ctx;
      playing = true;
      document.getElementById("play").textContent = "Stop";
      const item = kit();
      const secondsOf = (tick) => tick / 960 * item.tempo_us / 1000000;
      const origin = ctx.currentTime + 0.05;
      notes.forEach((itemNote) => schedule(ctx, itemNote.note, origin, secondsOf, itemNote.role));
      const bars = view === "arrangement" ? item.arrangement_bars : item.bars;
      const container = bars * 4 * item.tempo_us / 1000000;
      const follow = () => {
        if (!playing || !audio) return;
        if (audio.currentTime - origin < container) followId = requestAnimationFrame(follow);
        else stopPlayback();
      };
      follow();
    }
    function stepKit(direction) {
      const index = pack.kits.findIndex((item) => item.id === kitId);
      kitId = pack.kits[(index + direction + pack.kits.length) % pack.kits.length].id;
      loadKit();
    }
    pack.kits.forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.id = item.id;
      button.textContent = item.id + " " + item.title;
      button.addEventListener("click", () => { kitId = item.id; loadKit(); });
      rail.appendChild(button);
    });
    document.getElementById("var-a").addEventListener("click", () => { variation = "a"; if (view === "arrangement") view = "kit"; loadKit(); });
    documen