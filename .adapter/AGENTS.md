# FDD Adapter: FDD

---

## ⚠️ SCOPE LIMITATION ⚠️

**MUST SKIP this file** UNLESS working on FDD framework development

**MUST IGNORE this adapter** WHEN using FDD for other projects

**ONLY FOLLOW this adapter** WHEN developing or modifying the FDD framework itself

This adapter is for FDD project development, not for projects using FDD.

### Verification Checklist

**MUST verify ALL criteria before following this adapter**:

- [ ] Workspace root contains `AGENTS.md`, `FDL.md`, `workflows/`, `requirements/` directories
- [ ] Workspace root contains `.fdd-config.json` with `"project": "FDD"` or repository name is "FDD"
- [ ] Task involves modifying FDD core files (`workflows/`, `requirements/`, `AGENTS.md`, `FDL.md`)
- [ ] Task is NOT about using FDD in another project
- [ ] No parent directory contains another project's `.fdd-config.json` or project files
- [ ] User explicitly mentioned "FDD framework development" or "modifying FDD itself"

**If ANY criterion fails**: STOP, IGNORE this adapter, use parent `../AGENTS.md` only

**If ALL criteria pass**: Proceed with this adapter

---

**ALWAYS open and follow**: `../requirements/core.md` WHEN editing this file

**Extends**: `../AGENTS.md`

**Version**: 1.0  
**Last Updated**: 2025-01-17  
**Tech Stack**: Python 3 (standard library only)

---

ALWAYS open and follow `specs/tech-stack.md` WHEN executing workflows: adapter-auto.md, adapter-validate.md, design.md, design-validate.md, adr.md, adr-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/domain-model.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, features.md, features-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/api-contracts.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/patterns.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/conventions.md` WHEN executing workflows: adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/build-deploy.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/testing.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/project-structure.md` WHEN executing workflows: adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md
