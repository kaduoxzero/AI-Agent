# Runtime Installation Guide

## Overview

This document defines how to initialize the Agent Engineering Runtime.

## Initialization Order

1. Load runtime configuration
2. Discover Skill Registry
3. Validate Skill Manifest
4. Load Policy Engine
5. Initialize Memory Layer
6. Start Skill Router
7. Accept tasks

## Principles

- Core Runtime is industry independent.
- Domain capability is provided through extensions.
- Unsafe operations require governance checks.
