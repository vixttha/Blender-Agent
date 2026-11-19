# BART mesh inspection episodes

The HyperFrames triangle pilot establishes the visual format. This Remotion composition tests whether the same opener, evidence reveal and end card can be remixed from data.

| Input | Triangle comparison frames | Square episode |
| --- | --- | --- |
| Presenter | Locked Mist headshot as a PNG | Silent, gently reframed MP4 made from that PNG |
| CLI | `inspect triangle.obj` returns 3 vertices and 1 face | `inspect square.obj` returns 4 vertices and 2 faces |
| Captions | Triangle script | Square mesh script |

Edit `episodes.json` to choose the presenter asset, author the timed text, and define the planar OBJ fixture and wireframe. `prepare.py` generates the fixture, calls the installed BART CLI, compares the counts with the declared geometry, and captures the result into the props consumed by `BartMeshInspection`. The renderer puts the exact reported values in a three-field excerpt. The video label identifies the presenter clip as still-based.

The [public Ubuntu workflow](../../.github/workflows/human-remotion.yml) renders triangle comparison frames and the full 18-second square episode from the same composition. The artifact includes both JSON prop sets, both comparison frames, the MP4, five review frames, and its media probe and checksum. Motion is driven by Remotion frames. Each caption stays in the same right-hand column, and the face reveal uses the supplied triangular mesh geometry.

The composition schema validates the presenter media type, the caption time window, and agreement between the measured counts and the wireframe. Mesh coordinates use normalized XY values from 0 to 1. Captions use millisecond timestamps within the 8.8-second presenter scene. Fonts load from the pinned files copied into `public/fonts` before frame capture. The public job tests both real episode prop sets and five malformed variants before rendering.
