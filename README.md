# TOTALITY OBD Equaliser

Variant-Aware Supervisory Vehicle Control and Ambient Dash System

## Overview

TOTALITY OBD Equaliser is a modular supervisory vehicle control framework designed to:

- identify connected vehicles and likely variants
- apply bounded high-level control logic
- preserve safety margins and lifecycle awareness
- support legacy fallback behavior
- provide a speedometer-first dash
- integrate calm Bennonacci ambient aesthetics
- use LLM reasoning for interpretation, classification, and reporting
- refine logic with SPARKI ignition-aware analysis

## Core idea

This is **not** a universal raw tune file.

It is a:

**cross-platform supervisory equaliser layer**

That means:
- universal logic
- variant-specific translation
- telemetry-aware scoring
- driver-seat mode selection
- advisory-first deployment

## Main system layers

1. Vehicle Identification Layer
2. Equaliser Control Core
3. Variant Profile Layer
4. Translation Adapter Layer
5. OBD Telemetry Layer
6. LLM Co-Pilot Layer
7. SPARKI Ignition Logic Layer
8. Bennonacci Ambient Visual Layer

## User-facing modes

- Stock Safe
- P-Mode
- Daily PRV
- Longevity Max
- Sport Smart
- Aggressive Controlled
- Heat-Soak Defense
- Wet / Low-Grip
- Tow / Load

## Legacy Holden support

For oldest compatible Holden hardware, the system backward-compiles to:

**Holden Legacy P-Mode**

This mode emphasizes:
- smooth drivability
- thermal reserve
- fueling headroom
- supervisory-only control depth
- speedometer-first default dash

## Visual system

The dash uses a calm **Bennonacci ambient** visual grammar:
- speedometer as default screen
- soft drift and fade timing
- no harsh flashing
- variant-aware themes:
  - Classic Holden
  - Glacier
  - Ocean
  - Nebula

## SPARKI

SPARKI adds ignition-aware reasoning:
- knock margin interpretation
- heat-soak sensitivity
- ignition stability scoring
- misfire suspicion
- combustion smoothness estimation
- safe request refinement

## Suggested first build order

1. preset pack
2. variant profile schema
3. rules engine
4. telemetry importer
5. scoring engine
6. dash UI
7. LLM prompts
8. simulation playback
9. advisory deployment testing

## Git init

```bash
git init
git add .
git commit -m "Initial TOTALITY OBD Equaliser release"
