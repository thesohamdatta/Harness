# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primary:** Developers and makers who build, customize, and flash their own wearable AI hardware. They are technically skilled, value autonomy and open-source, and are willing to solder, flash firmware, and self-host a backend.

**Secondary:** Privacy-conscious users who want a screenless AI assistant they can trust, routed through the developer audience as builders/deployers.

## Product Purpose

Aura is an open-source, screenless, voice-first AI pendant worn around the neck. It listens, sees, and remembers — without demanding your attention. Total BOM ~$50 USD. MIT licensed. The goal is to decouple AI utility from digital distraction.

## Positioning

**The third device.** Not a computer, not a phone — something worn. Aura's core thesis is attention-first AI: utility (transcription, visual memory, recall) delivered without notifications, feeds, or addictive loops. The attention economy is the explicit anti-reference.

## Operating Context

- Developer self-builds the pendant from off-the-shelf components (XIAO ESP32-S3 Sense, LiPo batteries, 3D-printed case)
- Firmware flashed via PlatformIO over USB-C
- Backend deployed via Docker (transcription via Deepgram/Whisper, LLM via Groq/OpenAI, memory via Pinecone)
- Paired via Omi companion app over Bluetooth LE
- Used hands-free; worn around neck; primary interaction is voice
- Target environment: real-world, on-the-go, social settings where phone use is inappropriate

## Capabilities and Constraints

**Confirmed:**

- Voice transcription via Groq LPU (<0.5s latency)
- Visual understanding via OV2640 camera + GPT-4o Vision / Moondream
- RAG memory retrieval via Pinecone vector store
- ESP32-S3: Wi-Fi 2.4 GHz + Bluetooth LE, 50×68×18mm, 80g, 4h active / 45min charge
- Battery: 6× 150mAh LiPo cells (900mAh total)

**Undecided / open:**

- Companion app experiences beyond pairing and browsing transcripts
- On-device processing split vs cloud reliance
- Multi-language support scope

## Brand Commitments

- Name: **Aura**
- Tagline: "Worn. Screenless. Aware."
- License: MIT
- Visual identity: Apple-inspired design system. SF Pro typography. Action Blue (#0066cc) as the single interactive accent. Frosted glass surfaces. Alternating light/dark full-bleed tiles. Photography-first presentation. **All visual design must follow Apple HIG principles rigorously.**
- Voice: Confident, quiet, present — the product should feel like a museum gallery, not a tech dashboard.
- Anti-reference: The attention economy. No notifications, no gamification, no engagement metrics.

## Evidence on Hand

- GitHub: https://github.com/thesohamdatta/aura
- Reference site content at `D:\PROJECTS\aura\website\`
- New website at `D:\PROJECTS\Harness\SDK\website\` (3 pages: index, manifesto, docs)
- Hardware: XIAO ESP32-S3 Sense BOM and build guide
- Backend: Docker-based stack with Deepgram/Groq/Pinecone

**Absences (do not fabricate):**

- No verified customer testimonials, case studies, or deployment metrics
- No Discord community (link is placeholder)
- No pricing or commercial claims (MIT licensed, no commercial tier documented)

## Product Principles

1. **Utility without distraction.** Every feature must earn its place by serving the user's real need, never an engagement metric. If it would work on a phone, it doesn't belong on Aura.
2. **Open-source by default.** All hardware, firmware, and backend code is MIT licensed. The user owns their data and their device.
3. **Attention-first.** The third device philosophy governs all product decisions. Aura augments presence, never competes with it.
4. **Developer autonomy.** The primary user is a builder. Provide clear docs, composable parts, and no gatekeeping.
5. **Design discipline.** Apple HIG principles apply to every pixel. No decorative chrome. One accent color. Photography-first. The surface is a gallery, not a control panel.

## Accessibility & Inclusion

- WCAG AA compliance target for all web surfaces
- Skip-to-content links, visible focus indicators, semantic HTML landmarks in existing implementation
- Screenless interaction model inherently supports some accessibility needs (vision-free use) but creates others (no visual feedback for hearing-impaired users)
