import {z} from "zod";

export const presenterDurationMs = 8800;

const caption = z.object({
  text: z.string().trim().min(1),
  startMs: z.number().int().min(0),
  endMs: z.number().int().max(presenterDurationMs),
  timestampMs: z.number().nullable(),
  confidence: z.number().min(0).max(1).nullable(),
});

const coordinate = z.number().min(0).max(1);
const vertexIndex = z.number().int().positive();

export const episodeSchema = z.object({
  presenter: z.object({
    kind: z.enum(["image", "video"]),
    file: z.string().regex(/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/),
    label: z.string().min(1),
  }),
  captions: z.array(caption).min(1),
  heading: z.string().min(1),
  fixture: z.string().regex(/^[a-zA-Z0-9][a-zA-Z0-9._-]*\.obj$/),
  inspection: z.looseObject({
    format: z.literal("obj"),
    vertices: z.number().int().min(3),
    faces: z.number().int().positive(),
  }),
  points: z.array(z.tuple([coordinate, coordinate])).min(3),
  faces: z.array(z.tuple([vertexIndex, vertexIndex, vertexIndex])).min(1),
}).superRefine((episode, context) => {
  const {presenter, captions, inspection, points, faces} = episode;
  const suffix = presenter.kind === "video" ? ".mp4" : ".png";
  if (!presenter.file.toLowerCase().endsWith(suffix)) {
    context.addIssue({code: "custom", path: ["presenter", "file"], message: "File extension must match the presenter media kind."});
  }

  let previousEnd = 0;
  for (const [index, cue] of captions.entries()) {
    if (cue.startMs < previousEnd || cue.endMs <= cue.startMs) {
      context.addIssue({code: "custom", path: ["captions", index], message: "Caption timing must be ordered, nonoverlapping, and positive."});
    }
    previousEnd = cue.endMs;
  }

  if (inspection.vertices !== points.length || inspection.faces !== faces.length) {
    context.addIssue({code: "custom", path: ["inspection"], message: "CLI counts must match the wireframe geometry."});
  }

  for (const [index, face] of faces.entries()) {
    if (new Set(face).size !== 3 || face.some(vertex => vertex > points.length)) {
      context.addIssue({code: "custom", path: ["faces", index], message: "Each face must reference three distinct declared vertices."});
    }
  }
});
