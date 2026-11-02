      <a href="#roll">Kits</a>
      <a href="#map">Map</a>
      <a href="#files">Files</a>
      <a href="#reading">Preview</a>
      <a href="media.html">Stills</a>
      <a href="midi/arrangement.mid">Arrangement</a>
    </nav>
  </header>
  <main>
    <section class="stage">
      <div>
        <p class="kicker">Four kits · two variations · 32-bar arrangements</p>
        <h1 id="title">Glass Harbor</h1>
        <p id="identity"></p>
        <p class="meta" id="facts"></p>
        <p id="rhythm"></p>
        <p class="note" id="limits"></p>
        <p class="note" id="departures"></p>
        <p>__DIRECTION__</p>
      </div>
      <div id="roll">
        <figure class="hero">
          <img src="art/hero.jpg" width="1280" height="720" alt="Illustration of five horizontal lanes on a midnight field. Long pale bars are the pad, a bright lane is the lead, and short ticks are drums. Not a photograph of a studio or of performers.">
          <figcaption class="note">Illustration of lanes. Not a photograph of a session or of performers.</figcaption>
        </figure>
        <div class="rail" id="rail" role="tablist" aria-label="Kits"></div>
        <div class="switch">
          <button type="button" id="var-a" aria-pressed="true">Variation A</button>
          <button type="button" id="var-b" aria-pressed="false">Variation B</button>
          <button type="button" id="view-kit" aria-pressed="true">8-bar kit</button>
          <button type="button" id="view-arr" aria-pressed="false">32-bar arrangement</button>
        </div>
        <div class="phrases" id="phrases"></div>
        <div class="transport">
          <button type="button" id="play">Play lanes</button>
          <span id="transport-label">Space plays. J and K change kit.</span>
        </div>
        <div class="roll-wrap">
          <div class="label-col" id="label-col"></div>
          <div class="scroller" id="scroller">
            <div class="ruler" id="ruler"></div>
            <div id="lanes"></div>
          </div>
        </div>
        <p class="legend">
          <span><i class="swatch" style="background:#c9deef"></i>pad</span>
          <span><i class="swatch" style="background:#f2f6ff"></i>lead</span>
          <span><i class="swatch" style="background:#7ea2c4"></i>keys</span>
          <span><i class="swatch" style="background:#1c3148"></i>bass</span>
          <span><i class="swatch" style="background:#5c7c99"></i>drums</span>
        </p>
        <p class="note" id="status">Reading the MIDI.</p>
      </div>
    </section>
    <p>__RANGE__</p>
    <h2 id="map">Kit map</h2>
    <ul class="map">__KIT_ITEMS__</ul>
    <p>__REF_NOTE__ Variation A of each role has its own attack pattern. The four kits are not transpositions of one phrase.</p>
    <div class="flow" aria-label="File contract">
      <span>Score</span><span>MIDI</span><span>Reopened validation</span><span>MP3</span><span>Film</span><span>Stills</span><span>Drafts</span><span>Catalog</span>
    </div>
    <p class="note"><a href="articles/medium-draft-Cursor.md">Article draft</a> · <a href="articles/medium-paste-Cursor.txt">plain text</a></p>
    <h2>Article draft</h2>
    <p>DRAFT. __ARTICLE_TITLE__</p>
    <p>__TAG_LINE__</p>
    <p>__WARNING__</p>
    <h2 id="files">Files</h2>
    <p class="meta">Validation __RESULT__. Core __CORE__. Reference __REFS__. <a href="midi/validation-Cursor.json">validation report</a> · <a href="catalog/catalog-Cursor.json">catalog</a> · <a href="score/canonical-score-Cursor.json">canonical score</a></p>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Part</th><th>Role</th><th>Var</th><th>Count</th><th>BPM</th><th>Bars</th><th>Notes</th></tr></thead>
        <tbody>__PART_ROWS__</tbody>
      </table>
    </div>
    <h2>Arrangements</h2>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Kit</th><th>BPM</th><th>Bars</th><th>What the file contains</th></tr></thead>
        <tbody>__ARR_ROWS__</tbody>
      </table>
    </div>
    <section id="reading">
      <p class="kicker">Recorded reading</p>
      <p>__PREVIEW_STATEMENT__ The encoded MP3 is __PREVIEW_SECONDS__ seconds. __PREVIEW_LINE__. The film is __FILM_SECONDS__ seconds and shows __ON_PICTURE__.</p>
      <audio controls preload="metadata" src="preview/preview.mp3"></audio>
      <p><a href="preview/preview.mp3">preview/preview.mp3</a> · <a href="preview/preview-manifest-Cursor.txt">preview manifest</a></p>
      <video controls preload="metadata" poster="film/poster.jpg" width="1280" height="720">
        <source src="film/preview.mp4" type="video/mp4">
        <track kind="captions" src="film/preview.vtt" srclang="en" label="English" default>
      </video>
      <p><a href="film/preview.mp4">film/preview.mp4</a> · <a href="film/preview.vtt">film/preview.vtt</a> · <a href="media.html">stills</a></p>
    </section>
    <p>__PROGRAM__</p>
    <p>__AUDITION__</p>
    <p>__PUBLICATION__</p>
  </main>
  <script id="pack" type="application/json">__DATA__</script>
  <script>
    const pack = JSON.parse(document.getElementById("pack").textContent);
    const rail = document.getElementById("rail");
    const phrases = document.getElementById("phrases");
    const scroller = document.getElementById("scroller");
    const ruler = document.getElementById("ruler");
    const lanes = document.getElementById("lanes");
    const labelCol = document.getElementById("label-col");
    const status = document.getElementById("status");
    let kitId = "k01";
    let variation = "a";
    let view = "kit";
    let laneNotes = {};
    let audio = null;
    let playing = false;
    let followId = 0;
    let rollWidth = 1120;

    function kit() {
      return pack.kits.find((item) => item.id === kitId);
    }
    function pitchName(pitch) {
      return kit().spell[pitch % 12] + String(Math.floor(pitch / 12) - 1);
    }
    function readVlq(viewBytes, offset) {
      let value = 0;
      let byte = 0;
      do {
        byte = viewBytes.getUint8(offset);
        offset += 1;
        value = (value << 7) | (byte & 0x7f);
      } while (byte & 0x80);
      return [value, offset];
    }
    function parseMidi(buffer) {
      const viewBytes = new DataView(buffer);
      const head = String.fromCharCode(viewBytes.getUint8(0), viewBytes.getUint8(1), viewBytes.getUint8(2), viewBytes.getUint8(3));
      if (head !== "MThd" || viewBytes.getUint16(12) !== 960) throw new Error("unexpected MIDI header");
      const tracks = viewBytes.getUint16(10);
      let offset = 14;
      const parsed = [];
      for (let trackIndex = 0; trackIndex < tracks; trackIndex += 1) {
        const mark = String.fromCharCode(viewBytes.getUint8(offset), viewBytes.getUint8(offset + 1), viewBytes.getUint8(offset + 2), viewBytes.getUint8(offset + 3));
        if (mark !== "MTrk") throw new Error("missing track");
        const length = viewBytes.getUint32(offset + 4);
        offset += 8;
        const end = offset + length;
        let tick = 0;
        let running = 0;
        let name = "";
        const open = new Map();
        const notes = [];
        while (offset < end) {
          let delta;
          [delta, offset] = readVlq(viewBytes, offset);
          tick += delta;
          let byte = viewBytes.getUint8(offset);
          if (byte >= 0x80) {
            running = byte;
            offset += 1;
          }
          if (running === 0xff) {
            const metaType = viewBytes.getUint8(offset);
            offset += 1;
            let metaLen;
            [metaLen, offset] = readVlq(viewBytes, offset);
            if (metaType === 0x03) {
              name = "";
              for (let index = 0; index < metaLen; index += 1) name += String.fromCharCode(viewBytes.getUint8(offset + index));
            }
            offset += metaLen;
            continue;
          }
          const kind = running & 0xf0;
          const data1 = byte < 0x80 ? byte : viewBytes.getUint8(offset);
          if (byte >= 0x80) offset += 1;
          let data2 = 0;
          if (kind !== 0xc0 && kind !== 0xd0) {
            data2 = viewBytes.getUint8(offset);
            offset += 1;
          }
          const key = (running & 0x0f) + ":" + data1;
          if (kind === 0x90 && data2 > 0) open.set(key, { tick: tick, velocity: data2 });
          else if (kind === 0x80 || (kind === 0x90 && data2 === 0)) {
            const started = open.get(key);
            if (started) {
              notes.push({ pitch: data1, start: started.tick, duration: tick - started.tick, velocity: started.velocity });
              open.delete(key);
            }
          }
        }
        notes.sort((a, b) => a.start - b.start || a.pitch - b.pitch);
        parsed.push({ name: name, notes: notes });
      }
      return parsed;
    }
    function partPath(role) {
      const found = pack.parts.find((part) => part.kit_id === kitId && part.role === role && part.variation === variation);
      if (!found) throw new Error("missing " + role);
      return found.path;
    }
    function arrangementPath() {
      const found = pack.arrangements.find((item) => item.kit_id === kitId);
      if (!found) throw new Error("missing arrangement");
      return found.path;
    }
    function renderCopy() {
      const item = kit();
      document.getElementById("title").textContent = item.title;
      document.getElementById("identity").textContent = item.identity;
      const bars = view === "arrangement" ? item.arrangement_bars : item.bars;
      document.getElementById("facts").textContent = item.id + " · " + item.bpm + " BPM · " + bars + " bars on screen · " + item.collection + " · tonic " + item.tonic;
      document.getElementById("rhythm").textContent = item.harmonic_rhythm;
      document.getElementById("limits").textContent = item.limitations;
      document.getElementById("departures").textContent = item.departures.length ? item.departures.join(" ") : "No pitched note in this kit is flagged as a departure.";
      const mode = view === "