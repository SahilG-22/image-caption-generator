# PROJECT CONTEXT

## Project Title

AI-Based Image Caption Generator and Accessibility Assistant

## Project Status

Planning phase — coding has not started yet.

## Project Goal

Build a Python-based application that allows a user to upload an image, automatically generate a natural-language description using a pre-trained image captioning model, display the caption, and read the caption aloud using text-to-speech.

The project is intended to demonstrate Python programming, machine learning, image processing, software modularity, Git/GitHub collaboration, and accessibility.

## Core User Flow

```text
User uploads image
        ↓
Streamlit UI
        ↓
Image preprocessing
        ↓
Pre-trained image captioning model
        ↓
Generated caption
        ↓
Display caption
        ↓
Text-to-speech
```

## Project Scope

### Included

- Image upload through Streamlit
- Image validation
- Basic image preprocessing
- Pre-trained image captioning
- Caption display
- Text-to-speech
- Basic testing
- Model evaluation on a small test set
- Accessibility-focused UI considerations
- Git/GitHub based team development

### Not Included in MVP

- Training an image captioning model from scratch
- Fine-tuning the model
- Object detection
- Face recognition
- OCR
- Emotion recognition
- Multi-language support
- Mobile application
- Complex cloud infrastructure

These may be considered future enhancements.

## AI Model

Proposed model:

`Salesforce/blip-image-captioning-base`

The model is a pre-trained image-captioning model available through Hugging Face Transformers.

The exact implementation and compatible Transformers version will be finalized during environment setup.

## Technology Stack

- Python
- PyTorch
- Hugging Face Transformers
- Pillow
- Streamlit
- pyttsx3 for initial text-to-speech implementation
- pytest
- Git
- GitHub

## Architecture

```text
User
 ↓
Streamlit UI
 ↓
Image Processing
 ↓
Captioning Model
 ↓
Generated Caption
 ↓
 ├── Display
 └── Text-to-Speech
```

## Module Responsibilities

### Member A — Captioning

Primary responsibility:

- BLIP model integration
- Caption generation
- Model loading
- Captioning module interface

Expected interface:

```python
generate_caption(image)
```

### Member B — Image Processing and Evaluation

Primary responsibility:

- Image validation
- Image preprocessing
- Evaluation dataset
- Model evaluation
- Processing tests

Expected interface:

```python
preprocess_image(image)
```

### Member C — Streamlit UI

Primary responsibility:

- Streamlit application
- Image uploader
- Image display
- Caption display
- User-facing controls
- Accessibility-focused UI

### Member D — Utilities and Testing

Primary responsibility:

- Text-to-speech
- Utility functions
- Integration testing
- Error handling support
- Documentation coordination

Expected interface:

```python
speak_text(text)
```

## Git Workflow

One GitHub repository will be used.

### Main branch

`main`

The main branch should be protected. Direct commits should not be made to `main`.

### Feature branches

```text
feature/captioning
feature/image-processing
feature/ui
feature/testing-utils
```

Development flow:

```text
Create/update feature branch
        ↓
Commit changes
        ↓
Push branch
        ↓
Create Pull Request
        ↓
Code review
        ↓
Merge into main
```

## File Ownership

```text
src/captioning/*        → Member A
src/processing/*        → Member B
src/ui/*                → Member C
src/utils/*             → Member D
tests/*                 → Shared, coordinated by Member D
docs/*                  → Shared, coordinated by Member D
```

File ownership is intended to reduce merge conflicts. It does not prevent other members from contributing when necessary.

## Interface Rule

Modules should communicate through simple, stable interfaces.

For example:

```python
caption = generate_caption(image)
```

The UI should not depend on the internal implementation of the captioning model.

If an interface needs to change, the team should discuss the change before modifying dependent modules.

## Development Principle

The project should remain beginner-friendly.

Avoid unnecessary complexity, frameworks, services, or architectural changes unless they provide a clear benefit to the project.

## ChatGPT Collaboration Rule

This document represents the agreed project context.

Before making a major architectural change, explain:

1. What is changing
2. Why it is necessary
3. What impact it has on the existing project

The team should agree before the architecture is changed.

When modifying existing code, preserve existing interfaces unless there is a strong reason to change them.

## Current Decisions

| Decision                  | Status            |
| ------------------------- | ----------------- |
| Python                    | Approved          |
| Streamlit                 | Approved          |
| Pillow                    | Approved          |
| Hugging Face Transformers | Approved          |
| PyTorch                   | Approved          |
| BLIP image captioning     | Proposed/approved |
| Text-to-speech            | pyttsx3 proposed  |
| GitHub                    | Approved          |
| Modular architecture      | Approved          |
| Model training            | Out of scope      |
| Fine-tuning               | Out of scope      |

## Current Phase

Planning.

Next steps:

1. Create GitHub repository
2. Create protected `main` branch
3. Create feature branches
4. Set up Python environment
5. Install and test dependencies
6. Test BLIP independently
7. Finalize module interfaces
8. Begin implementation

Image captioning model:
Salesforce/blip-image-captioning-base

Framework:
Hugging Face Transformers

Backend:
PyTorch

Device:
Automatically select MPS/CUDA/CPU

Input:
PIL Image

Output:
Natural-language caption
