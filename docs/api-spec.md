# API Spec (v1)

## Auth
- POST /api/auth/login

## Projects
- POST /api/projects
- GET /api/projects/<id>
- PATCH /api/projects/<id>
- POST /api/projects/<id>/autosave

## AI / Quality
- POST /api/projects/<id>/sections/<section_key>/improve
- POST /api/projects/<id>/plagiarism/check

## Diagrams
- POST /api/projects/<id>/diagrams/generate

## Uploads
- POST /api/projects/<id>/uploads/screenshots
- POST /api/projects/<id>/uploads/code

## Preview
- POST /api/projects/<id>/preview/render

## Exports
- POST /api/projects/<id>/exports/docx
- POST /api/projects/<id>/exports/pdf
- POST /api/projects/<id>/exports/zip
- GET /api/jobs/<job_id>

## Versions
- POST /api/projects/<id>/versions
- GET /api/projects/<id>/versions
- POST /api/projects/<id>/versions/<version_id>/restore

## Templates
- GET /api/templates
- POST /api/templates/custom
