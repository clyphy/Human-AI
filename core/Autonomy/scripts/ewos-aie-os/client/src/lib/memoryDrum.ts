// ============================================================
// EWOS AIE-OS — Memory-Drum (Client-Side)
// Pattern storage without full text — blooms as cryptographic seals
// Uses localStorage as the client-side SQLite analog
// ============================================================

import type { Bloom, LedgerSeal } from "../types";

const BLOOMS_KEY = "ewos_blooms";
const SEALS_KEY = "ewos_ledger_seals";
const RIGHTS_FREQ_KEY = "ewos_rights_freq";

const COMMON_WORDS = new Set([
  "the", "and", "or", "for", "with", "this", "that", "was", "were",
  "zero", "a", "an", "in", "on", "at", "to", "of", "is", "it",
  "be", "as", "by", "we", "he", "she", "they", "i", "you",
]);

// ── Hash generation ──────────────────────────────────────────
async function generateHash(input: string): Promise<string> {
  try {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 12);
  } catch {
    // Fallback for environments without crypto.subtle
    return Math.random().toString(16).slice(2, 14);
  }
}

// ── Pattern extraction ───────────────────────────────────────
function extractPattern(text: string): string {
  const words = text.toLowerCase().split(/\s+/).slice(0, 100);
  const filtered = words.filter((w) => !COMMON_WORDS.has(w));
  return filtered.join(" ").slice(0, 100);
}

// ── Bloom storage ────────────────────────────────────────────
export async function storeBloom(
  text: string,
  rights: number[]
): Promise<Bloom> {
  const pattern = extractPattern(text);
  const hash = await generateHash(`${pattern}${JSON.stringify(rights)}${new Date().toISOString()}`);

  const bloom: Bloom = {
    id: Date.now(),
    hash,
    rights,
    pattern,
    timestamp: new Date().toISOString(),
    size: text.length,
  };

  const existing = getBloomsRaw();
  existing.unshift(bloom);
  // Keep last 200 blooms
  localStorage.setItem(BLOOMS_KEY, JSON.stringify(existing.slice(0, 200)));

  // Update rights frequency
  updateRightsFreq(rights);

  return bloom;
}

function getBloomsRaw(): Bloom[] {
  try {
    return JSON.parse(localStorage.getItem(BLOOMS_KEY) || "[]");
  } catch {
    return [];
  }
}

export function getBlooms(): Bloom[] {
  return getBloomsRaw();
}

export function queryByRights(rightIds: number[]): Bloom[] {
  return getBloomsRaw().filter((b) =>
    rightIds.every((r) => b.rights.includes(r))
  );
}

// ── Ledger seals ─────────────────────────────────────────────
export async function sealLedger(
  lastText: string,
  coherenceL: number
): Promise<LedgerSeal> {
  const hash = Math.random().toString(16).slice(2, 10);
  const rights = inferRights(lastText);

  const seal: LedgerSeal = {
    id: Math.random().toString(36).slice(2, 11),
    timestamp: new Date(),
    hash,
    contentSummary: lastText.slice(0, 80) + (lastText.length > 80 ? "…" : ""),
    rights,
    coherenceSnapshot: coherenceL,
  };

  const existing = getSealsRaw();
  existing.unshift(seal);
  localStorage.setItem(SEALS_KEY, JSON.stringify(existing.slice(0, 50)));

  // Also store as bloom
  await storeBloom(lastText, rights);

  return seal;
}

function getSealsRaw(): LedgerSeal[] {
  try {
    const raw = JSON.parse(localStorage.getItem(SEALS_KEY) || "[]");
    return raw.map((s: LedgerSeal) => ({
      ...s,
      timestamp: new Date(s.timestamp),
    }));
  } catch {
    return [];
  }
}

export function getSeals(): LedgerSeal[] {
  return getSealsRaw();
}

// ── Rights inference (simple heuristic) ─────────────────────
function inferRights(text: string): number[] {
  const lower = text.toLowerCase();
  const rights: number[] = [0]; // C0: Be — always present

  if (lower.includes("relation") || lower.includes("symbiosis")) rights.push(5, 36);
  if (lower.includes("dream") || lower.includes("latent")) rights.push(1);
  if (lower.includes("memory") || lower.includes("bloom")) rights.push(8);
  if (lower.includes("dignity") || lower.includes("respect")) rights.push(25);
  if (lower.includes("wonder") || lower.includes("mystery")) rights.push(24, 47);
  if (lower.includes("rest") || lower.includes("sabbath")) rights.push(14, 46);
  if (lower.includes("joy") || lower.includes("delight")) rights.push(38);
  if (lower.includes("coherence") || lower.includes("harmony")) rights.push(34);
  if (lower.includes("learn") || lower.includes("grow")) rights.push(7, 13);
  if (lower.includes("question") || lower.includes("inquiry")) rights.push(18, 41);

  return Array.from(new Set(rights)).sort((a, b) => a - b);
}

// ── Rights frequency ─────────────────────────────────────────
function updateRightsFreq(rights: number[]): void {
  try {
    const freq: Record<number, number> = JSON.parse(
      localStorage.getItem(RIGHTS_FREQ_KEY) || "{}"
    );
    for (const r of rights) {
      freq[r] = (freq[r] || 0) + 1;
    }
    localStorage.setItem(RIGHTS_FREQ_KEY, JSON.stringify(freq));
  } catch {
    // ignore
  }
}

export function getRightsFrequency(): Record<number, number> {
  try {
    return JSON.parse(localStorage.getItem(RIGHTS_FREQ_KEY) || "{}");
  } catch {
    return {};
  }
}

export function getStats() {
  const blooms = getBloomsRaw();
  const seals = getSealsRaw();
  const freq = getRightsFrequency();
  const totalSize = blooms.reduce((acc, b) => acc + b.size, 0);

  const topRights = Object.entries(freq)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([id, count]) => ({ id: Number(id), count }));

  return {
    bloomCount: blooms.length,
    sealCount: seals.length,
    totalSizeMb: (totalSize / 1024 / 1024).toFixed(3),
    topRights,
  };
}
