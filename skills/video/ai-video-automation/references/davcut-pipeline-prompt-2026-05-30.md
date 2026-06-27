# DavCut + TCHUEKAM + Gemini — Pipeline d'Édition Autonome

Version: 1.0 — 30 May 2026
Auteur: TCHUEKAM (Giantect Empire)

## Architecture Actuelle

```
[User Prompt]
      │
      ▼
┌─────────────────────────────────────────┐
│            GEMINI CLI v0.44.1           │
│  (google-gemini, ACP-capable)           │
│                                         │
│  Rôles :                                │
│  - Vision : analyse les vignettes       │
│  - Scores clips (0-100)                 │
│  - Génère script voiceover              │
│  - Suggère améliorations post-draft     │
│  - Assigne mood tags                    │
└────────────────┬────────────────────────┘
                 │  JSON Edit Plan
                 ▼
┌─────────────────────────────────────────┐
│         TCHUEKAM (Hermes Agent)          │
│  (DeepSeek, GODMODE-enabled)            │
│                                         │
│  Rôles :                                │
│  - Reçoit le plan JSON de Gemini        │
│  - Construit la timeline DavCut         │
│  - Applique transitions + filtres       │
│  - Syncro sur les beats musicaux        │
│  - Déclenche l'export                   │
│  - Boucle sur nouveau prompt            │
└────────────────┬────────────────────────┘
                 │
                 ▼
         [DAVCUT TIMELINE]
                 │
                 ▼
         [USER REVIEW]
                 │
         ┌───────┴───────┐
         ▼               ▼
    [Gemini Review]  [User Override]
         │               │
         └───────┬───────┘
                 ▼
         [TCHUEKAM Applique]
                 │
                 ▼
         [FINAL EXPORT]
```

## Répartition des Rôles

| Tâche | Gemini CLI (ACP) | TCHUEKAM (Hermes) |
|-------|------------------|-------------------|
| Interpréter le prompt | ✅ Compréhension créative | ❌ |
| Scanner les clips (Vision) | ✅ Vignettes → scores 0-100 | ❌ |
| Sélectionner les meilleurs moments | ✅ Timestamps + ranking | ❌ |
| Écrire script voiceover | ✅ Génération texte | ❌ |
| Détecteur de mood | ✅ mood tag assigné | ❌ |
| Suggérer améliorations post-draft | ✅ Suggestions structurées JSON | ❌ |
| Construire la timeline | ❌ | ✅ Assemble clips dans DavCut |
| Appliquer transitions + filtres | ❌ | ✅ Color grade, transitions, captions |
| Beat sync audio | ❌ | ✅ Waveform → snap aux beats |
| Exporter vidéo | ❌ | ✅ Trigger export avec settings |
| Re-run pipeline | ❌ | ✅ Boucle sur nouveau prompt |

## Format d'Échange (Gemini → TCHUEKAM)

Gemini CLI reçoit le prompt utilisateur + scanne les vignettes, puis produit ce JSON pour TCHUEKAM :

```json
{
  "plan": {
    "mood": "cinematic",
    "duration_seconds": 60,
    "format": "youtube",
    "music_vibe": "upbeat_orchestral"
  },
  "clips": [
    {"file": "clip_01.mp4", "rank": 95, "start_at": 2.5, "duration": 8.0, "caption": "Welcome to the journey"},
    {"file": "clip_03.mp4", "rank": 88, "start_at": 0.0, "duration": 6.0, "caption": "Through the mountains"}
  ],
  "voiceover": "Full script text here...",
  "transitions": [
    {"between": [0, 1], "type": "crossfade", "duration": 0.5},
    {"between": [1, 2], "type": "fade_black", "duration": 1.0}
  ]
}
```

## Flux de Suggestions (Post-Draft)

Après que TCHUEKAM a construit la timeline, Gemini la revoit et envoie :

```json
{
  "suggestions": [
    {"type": "trim", "clip": 3, "action": "trim_end", "by_seconds": 4},
    {"type": "transition", "between": [4, 5], "effect": "fade_black"},
    {"type": "caption_sync", "clip": 2, "shift_ms": -300},
    {"type": "filter", "clip": 1, "apply": "warm_tone"}
  ]
}
```

L'utilisateur coche ✅ ou ❌ → TCHUEKAM applique les acceptés.

## Contraintes Techniques

- **TCHUEKAM → Gemini :** via ACP bridge configurable dans Hermes
- **Gemini → TCHUEKAM :** retour JSON direct dans le stdout
- **DavCut :** pilotable via CLI ou plugin (à vérifier)
- **Non-destructif :** les fichiers originaux ne sont jamais touchés
- **Undo :** chaque action TCHUEKAM est dans l'historique DavCut
- **Async :** tout tourne en arrière-plan, avec log live
- **Si un AI offline :** pause + notification à l'utilisateur — pas de crash

## CORE VISION

The user should be able to:
1. Drop raw footage into DavCut
2. Type or speak a prompt like "Make me a 60-second cinematic travel reel with upbeat music and captions"
3. Press Generate and watch both AIs build the entire video automatically

## HARD RULES

- AI must never auto-export without user pressing the Export button
- Every AI timeline action must be visible in the undo history
- Gemini Vision frame grabs are processed in memory only — never saved to disk
- If either AI goes offline mid-process → pause and notify user, don't crash
