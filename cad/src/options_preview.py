"""Shaded preview of the concept options picture, media/options.png (WLS-OPT-001), from the D3 models.

Run from the repo root:  python cad/src/options_preview.py
Each panel is components(option) from cad/src/model.py with the context left out and everything below
z = -400 mm cut away (the borehole is shortened for display), shaded with .kit/concept.py, with the kit's
1.75 m scale figure on the same ground. It is a stand-in so the repo carries an options picture between
publishes: the kit 1.9 picture is a Blender Cycles render made with `python .kit/options.py` (or --export and
--compose on the studio machine), which overwrites this file. The picture says so in its subtitle.
Repo-specific helper; nothing here is in .kit/.
"""
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
import concept  # noqa: E402
import model as M  # noqa: E402

INK, MUTED, ACCENT, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"
Z_CUT = -400.0


def panel(key, path):
    keep = M.bx(-3000, 3000, -3000, 3000, Z_CUT, 4000)
    parts = []
    for p in M.components(key):
        if p["kind"] == "context":
            continue
        s = p["shape"]
        bb = s.bounding_box()
        if bb.min.Z < Z_CUT:
            s = s & keep
            if s is None or s.volume < 1e-3:
                continue
        parts.append(concept.Part(p["name"], s, p["color"], None))
    parts = concept.with_scale_figure(parts, gap=300.0)
    v = M.OPTION_VIEWS.get(key, {})
    concept._render(parts, path, elev=v.get("el", 18), azim=v.get("az", -40), size=(5, 5), dpi=160)
    return Image.open(path).convert("RGB")


def main():
    keys = list(M.OPTIONS)
    n = len(keys)
    with tempfile.TemporaryDirectory() as tmp:
        imgs = [panel(k, Path(tmp) / f"opt-{k}.png") for k in keys]
    fig = plt.figure(figsize=(5.2 * n, 6.6), dpi=160)
    fig.text(0.015, 0.975, f"{M.TITLE}: concept options", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.935, "CONCEPT OPTIONS, NOT FOR FABRICATION. Same scale in every panel; borehole cut 0.4 m below ground. "
             "SHADED PREVIEW: the Cycles render replaces it.", fontsize=8, color=WARN, va="top")
    fig.text(0.985, 0.975, "github.com/BoujeeEnjinia1701/wellsense", fontsize=8, color=ACCENT, va="top", ha="right", family="monospace")
    for i, (k, im) in enumerate(zip(keys, imgs)):
        ax = fig.add_axes([i / n + 0.01, 0.2, 1 / n - 0.02, 0.68])
        ax.imshow(im); ax.axis("off")
        fig.text(i / n + 0.02, 0.17, f"Option {k}: {M.OPTIONS[k]}", fontsize=11, fontweight="bold", color=INK, va="top")
        fig.text(i / n + 0.02, 0.12, textwrap.fill(M.PRINCIPLES.get(k, ""), 52), fontsize=8.5, color=MUTED, va="top")
        if k == M.CHOSEN:
            fig.text((i + 1) / n - 0.02, 0.17, "CURRENT DESIGN", fontsize=8, fontweight="bold", color=ACCENT, va="top", ha="right")
    out = ROOT / "media/options.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
