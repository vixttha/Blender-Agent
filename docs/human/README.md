# BART human presenter trial

Status: character and production plan for owner review. The examples below are fictional presenter names. The product name is **Blender-Agent Refinement Toolkit**, the agent is **BART**, and the brand line is **Give shape to an idea.** Use “Mira from BART” or the corresponding presenter name in on-camera introductions.

## Character shortlist

| Candidate | Appearance | Personality and delivery | Fit for BART |
| --- | --- | --- | --- |
| **Mira Vale** | Mid-thirties, short dark curls, warm brown skin, charcoal chore jacket, a small mint stitch and a softly lit modeling desk. | Patient, observant and quietly curious. Starts with what the viewer can see and pauses for the result. “Let's inspect one triangle and count what came back.” | The practical technical artist. The work jacket suggests craft, the mesh backdrop ties her to the tool, and her delivery makes debugging approachable. |
| **Devon Reed** | Early forties, deep brown skin, close-cropped hair, stone work shirt with rolled sleeves, matte plywood workbench. | Warm, direct workshop teacher. Explains one step at a time and uses everyday words. “One face, three vertices. That's our check.” | The beginner guide. A tactile workbench makes digital geometry feel tangible, grounded pacing suits first-time users, and short explanations leave room for the screen capture. |
| **Ren Sato** | Early thirties, East Asian features, straight dark hair, slim glasses, ink-blue overshirt and a cool-toned workstation. | Focused, dry-witted geometry reviewer. States the expected numbers first and treats results as evidence. “Three vertices, one face. Good. Next check.” | The release-demo presenter. A restrained visual profile resembles the Facet art direction, the voice fits verification, and humor can carry an occasional release note. |

**Suggested first casting choice:** Mira Vale. She fits the quick start and can carry a troubleshooting video without changing tone. Choose a single presenter and keep a reference portrait, exactly selected HeyGen look, pronunciation, wardrobe, and voice consistent across the trial. Store account-bound IDs and source media outside the public branch until there is an approved public asset path.

## Visual direction

Test the draft **Facet** palette in wardrobe and graphics: Ink `#17252D`, Mist `#F4F6F2`, and one Mint `#38E6A8` detail. Use Ink/Mist for type contrast. Frame chest-up at eye level, with soft side light and unobstructed eyes and mouth. Keep identity cues consistent during movement. Use original portraits, simple studio backgrounds and a stock synthetic voice. The brand kit proposes a product mark built from mesh geometry. The presenter appears in video introductions and tutorials, while the product mark identifies the toolkit.

[Locked branding](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/issues/62) · [Draft visual system](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/9741c63beaa237ab6fcd3672e2dff5e49e759b5b/brand-identity/06-visual-system/system.md) · [Brand-kit trial PR](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/pull/80)

## First pilot

Try a **single 8–10 second spoken HeyGen clip** and target a **15–20 second edit** in landscape. Listen to the line at a natural pace in the audition.

| Approximate time | Picture and audio |
| --- | --- |
| 0–9 seconds | Presenter. “I'm Mira. Here's BART inspecting one triangle. We're looking for three vertices and one face.” |
| 9–16 seconds | Show the pinned quick-start fixture, command and returned counts. Hold the numbers long enough to read. |
| 16–18 seconds | Product name and brand line. |

Use the documented `blender-agent --workspace readme-demo inspect triangle.obj` fixture. The first demonstration exercises the Python inspection path and expects `format: obj`, `vertices: 3` and `faces: 1`. Capture genuine command output from the pinned walkthrough on a standard public runner. The wireframe overlay can explain the three vertices, and the video can label any reconstructed visuals as illustrations. Match captions to recorded speech.

[Verified walkthrough source](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/blob/3e7f9e02e61739825b56bcafecebbd0221cc9657/README.md#quick-start)

## Production handoffs

1. **Images** generates and iterates on the fictional portrait. Use one head-and-shoulders source image for HeyGen and preserve a matching reference for later episodes.
2. **HeyGen** validates the image as a Photo Avatar and supplies the presenter take. Select the exact avatar look and a synthetic voice, test the line inside the available free allowance, and check the actual account's sharing and export options. HeyGen documents a 10-second per-video free limit for Avatar IV and watermarks on free videos. Its download guide is written for paid users. If there is only a share link, review the audition there and use a clearly labeled still-image or synthetic stand-in for the public-runner edit test. A finished edit with HeyGen footage requires an authorized export.
3. **HyperFrames** authors a short HTML/CSS wireframe insert and renders it on a standard public runner. Label three vertices and one face, and keep the visual synchronized with the evidence capture. Use the pinned CLI version's lint, browser check and render commands.
4. **Remotion** assembles the supplied presenter take or labeled stand-in, the rendered wireframe insert, the actual inspection capture and timed captions. Use one final composition, version-locked dependencies and a standard GitHub-hosted `ubuntu-latest` job. The CI job consumes approved inputs and needs no HeyGen credentials.

[HeyGen Photo Avatars](https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars) · [HeyGen download guide](https://help.heygen.com/en/articles/9834825-how-to-download-or-export-a-video) · [HeyGen watermark policy](https://help.heygen.com/en/articles/11057301-how-to-remove-the-heygen-watermark) · [HyperFrames CLI](https://github.com/heygen-com/hyperframes/blob/main/docs/developers/cli.mdx) · [Remotion rendering](https://www.remotion.dev/docs/render) · [Remotion licensing](https://www.remotion.dev/docs/license/pricing) · [GitHub runner policy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job)

## Evidence to collect

- **Casting:** settled working name and appearance, reference revision, selected look, voice, and pronunciation. Check that the face reads at thumbnail size and lip movement is convincing in the audition.
- **Product accuracy:** pin the source SHA and link the public-runner job that captured the actual inspection output. Check the on-screen counts against that output.
- **Render:** record the tested checkout, event, runner, job link, dependency versions, filenames and media checks. For the 16:9 pilot check duration, dimensions, expected audio, caption alignment and readable output at playback size. Use test assets suitable for a public runner and keep the proof within $0 incremental spend.
- **Solo audit:** verify the avatar and capture are labeled accurately, dialogue matches captions, the edit contains no creator information or private media, and all public evidence is suitable for disclosure. Review the single pilot before wider use.

The owner selected **Mira Vale · Mist** and approved the locked headshot for the [$0 still-image pilot](pilot/README.md). The HeyGen screen test reached the monthly Avatar IV allowance. The pilot uses timed text for the exact audition script and a single HyperFrames edit on a public runner.
