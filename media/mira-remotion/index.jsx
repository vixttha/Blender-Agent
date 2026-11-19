import React from "react";
import {AbsoluteFill, Composition, Img, OffthreadVideo, Sequence, interpolate, registerRoot, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import previewProps from "./evidence/triangle.props.json";
import "./episode.css";

const clamp = {extrapolateLeft: "clamp", extrapolateRight: "clamp"};

function Presenter({presenter, captions}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const time = frame * 1000 / fps;
  const caption = captions.find(({startMs, endMs}) => startMs <= time && time < endMs);
  const src = staticFile(presenter.file);

  return (
    <AbsoluteFill className="intro" style={{display: "grid"}}>
      {presenter.kind === "video"
        ? <OffthreadVideo src={src} muted className="portrait" />
        : <Img src={src} className="portrait" alt="Mira Vale wearing her Mist look" />}
      <div className="intro-text">
        <p className="label mint">BART · Mesh inspection</p>
        <div className="intro-title" style={{opacity: interpolate(frame, [.1 * fps, .6 * fps], [0, 1], clamp)}}>
          <h1>Mira Vale</h1>
          <p className="label fog">Mist · {presenter.label}</p>
        </div>
        <div className="caption">{caption?.text}</div>
      </div>
    </AbsoluteFill>
  );
}

function Inspection({heading, fixture, inspection, points, faces}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const coordinates = points.map(([x, y]) => [160 + x * 420, 450 - y * 328]);

  return (
    <AbsoluteFill className="inspection" style={{display: "grid", opacity: interpolate(frame, [0, .6 * fps], [0, 1], clamp)}}>
      <div className="mesh">
        <p className="label">Wireframe illustration</p>
        <h2>{heading}</h2>
        <svg viewBox="0 0 760 530" role="img" aria-label="Wireframe of the inspected mesh">
          {faces.map((face, index) => (
            <polygon key={face.join("-")} points={face.map(vertex => coordinates[vertex - 1].join(",")).join(" ")}
              fill={index === 0 ? "#d9f3e6" : "#c7e9dd"} stroke="#17252d" strokeWidth="5" strokeLinejoin="round"
              opacity={interpolate(frame, [(.58 + index * .55) * fps, (.94 + index * .55) * fps], [0, 1], clamp)} />
          ))}
          {coordinates.map(([x, y], index) => (
            <g key={index} opacity={interpolate(frame, [(.88 + index * .18) * fps, (1.16 + index * .18) * fps], [0, 1], clamp)}>
              <circle cx={x} cy={y} r="13" fill="#38e6a8" stroke="#17252d" strokeWidth="4" />
              <text x={x - 18} y={y + (y < 250 ? -27 : 49)} fill="#17252d">V{index + 1}</text>
            </g>
          ))}
        </svg>
      </div>
      <div className="evidence" style={{opacity: interpolate(frame, [.6 * fps, .88 * fps], [0, 1], clamp)}}>
        <p className="label mint">Verified CLI result</p>
        <p className="command">blender-agent --workspace readme-demo inspect {fixture}</p>
        <pre>{JSON.stringify({format: inspection.format, vertices: inspection.vertices, faces: inspection.faces}, null, 2)}</pre>
        <p className="label fog receipt">Captured on public GitHub Actions</p>
      </div>
    </AbsoluteFill>
  );
}

function EndCard() {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill className="outro" style={{display: "grid", opacity: interpolate(frame, [0, .55 * fps], [0, 1], clamp)}}>
      <div>
        <p className="label mint">BART</p>
        <h2>Give shape to an idea.</h2>
        <p className="brand">Blender-Agent Refinement Toolkit</p>
      </div>
      <svg viewBox="0 0 375 380" aria-hidden="true">
        <path d="M16 321 158 40 362 321Z" fill="none" stroke="#62716f" strokeWidth="3" />
        <path d="M158 40 362 321 205 245Z" fill="#38e6a8" />
        <path d="M16 321 205 245 362 321" fill="none" stroke="#62716f" strokeWidth="3" />
      </svg>
    </AbsoluteFill>
  );
}

function Episode({presenter, captions, heading, fixture, inspection, points, faces}) {
  const {fps} = useVideoConfig();
  const inspectionStart = Math.round(8.2 * fps);
  const endStart = Math.round(14.55 * fps);
  return (
    <AbsoluteFill className="episode">
      <Sequence durationInFrames={Math.round(8.8 * fps)}>
        <Presenter presenter={presenter} captions={captions} />
      </Sequence>
      <Sequence from={inspectionStart} durationInFrames={Math.round(15.1 * fps) - inspectionStart} premountFor={fps}>
        <Inspection heading={heading} fixture={fixture} inspection={inspection} points={points} faces={faces} />
      </Sequence>
      <Sequence from={endStart} premountFor={fps}>
        <EndCard />
      </Sequence>
    </AbsoluteFill>
  );
}

registerRoot(() => (
  <Composition id="BartMeshInspection" component={Episode} width={1920} height={1080}
    fps={30} durationInFrames={540} defaultProps={previewProps} />
));
