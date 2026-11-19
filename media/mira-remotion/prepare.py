"""Generate Remotion props from two actual BART CLI inspections."""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "episodes.json").read_text(encoding="utf-8"))
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)

for episode, content in MANIFEST.items():
    points, faces = content["points"], content["faces"]
    fixture = content["fixture"]
    geometry = [f"v {x} {y} 0" for x, y in points]
    geometry += ["f " + " ".join(map(str, face)) for face in faces]
    data = ("\n".join(geometry) + "\n").encode("ascii")

    with tempfile.TemporaryDirectory(prefix="bart-video-") as folder:
        workspace = Path(folder) / "readme-demo"
        workspace.mkdir()
        (workspace / fixture).write_bytes(data)
        command = ["blender-agent", "--workspace", "readme-demo", "inspect", fixture]
        output = subprocess.check_output(command, cwd=folder, text=True)

    result = json.loads(output)
    assert (result["format"], result["vertices"], result["faces"]) == (
        "obj", len(points), len(faces)
    ), result
    captions = content["captions"]
    assert all(cue["startMs"] < cue["endMs"] <= 8800 for cue in captions)
    assert all(a["endMs"] <= b["startMs"] for a, b in zip(captions, captions[1:]))
    props = {**content, "inspection": result}
    (EVIDENCE / f"{episode}.props.json").write_text(
        json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{fixture}: {result['vertices']} vertices, {result['faces']} faces")
