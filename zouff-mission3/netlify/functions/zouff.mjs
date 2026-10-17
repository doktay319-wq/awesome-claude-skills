// Gedeelde opslag voor Zouff Mission 3 (kinderen, voortgang, ouderscode) in Netlify Blobs.
import { getStore } from "@netlify/blobs";

const OK_PATH = /^(?:(?:kids|progress)\/[A-Za-z0-9_-]{1,40}|config\/parent)$/;

export default async (req) => {
  const store = getStore({ name: "zouff", consistency: "strong" });
  const json = (o, s = 200) => new Response(JSON.stringify(o), {
    status: s, headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

  if (req.method === "GET") {
    const out = { kids: {}, progress: {}, parent: null };
    for (const [field, prefix] of [["kids", "kids/"], ["progress", "progress/"]]) {
      const { blobs } = await store.list({ prefix });
      await Promise.all(blobs.map(async (b) => {
        const v = await store.get(b.key, { type: "json" });
        if (v) out[field][b.key.slice(prefix.length)] = v;
      }));
    }
    const p = await store.get("config/parent", { type: "json" });
    out.parent = p && p.hash ? p.hash : null;
    return json(out);
  }

  if (req.method === "POST") {
    let body;
    try { body = await req.json(); } catch { return json({ error: "bad json" }, 400); }
    const ops = Array.isArray(body.ops) ? body.ops.slice(0, 20) : [];
    for (const op of ops) {
      if (typeof op.path !== "string" || !OK_PATH.test(op.path)) return json({ error: "bad path" }, 400);
      if (op.del) { await store.delete(op.path); continue; }
      const s = JSON.stringify(op.data || {});
      if (s.length > 200000) return json({ error: "too large" }, 413);
      await store.set(op.path, s);
    }
    return json({ ok: true });
  }
  return json({ error: "method" }, 405);
};

export const config = { path: "/api/zouff" };
