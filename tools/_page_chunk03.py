t.getElementById("var-b").addEventListener("click", () => { variation = "b"; if (view === "arrangement") view = "kit"; loadKit(); });
    document.getElementById("view-kit").addEventListener("click", () => { view = "kit"; loadKit(); });
    document.getElementById("view-arr").addEventListener("click", () => { view = "arrangement"; loadKit(); });
    document.getElementById("play").addEventListener("click", () => { if (playing) stopPlayback(); else playLanes(); });
    window.addEventListener("keydown", (event) => {
      const tag = document.activeElement && document.activeElement.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (event.target && event.target.closest && event.target.closest("video, audio")) return;
      if (event.code === "Space") {
        event.preventDefault();
        if (playing) stopPlayback(); else playLanes();
      } else if (event.key === "j" || event.key === "J") stepKit(-1);
      else if (event.key === "k" || event.key === "K") stepKit(1);
    });
    loadKit();
  </script>
</body>
</html>
"""
