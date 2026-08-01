# ADR-0008: Copilot global para VS Code — prompts e instructions vía carpeta apuntada por settings

- **Estado**: aceptada
- **Fecha**: 2026-08-01
- **Ámbito**: proyecto

## Contexto

La revisión de paridad (ADR-0007) cerró el scope `project`, pero el scope `global` de
Copilot solo emitía `~/.copilot/copilot-instructions.md`, mientras que Claude global emite
`CLAUDE.md` + comandos globales (`review-changes`, `setup-standards`, `manage-context`).

Hallazgo verificado en la doc de VS Code (agosto 2026): los prompts/instructions
**globales** de VS Code no tienen una ruta fija de archivos como `~/.claude/commands/` de
Claude; se activan apuntando settings a una carpeta. Formato confirmado (objeto
`{ "ruta": true/false }`, admite claves con `~/`):

```jsonc
"chat.instructionsFilesLocations": { ".github/instructions": true, "~/.copilot/instructions": true },
"chat.promptFilesLocations":       { ".github/prompts": true,      "~/.copilot/prompts": true }
```

`~/.copilot/copilot-instructions.md` es la ruta de **GitHub Copilot CLI**, no de VS Code.

## Decisión

El generador Copilot (scope `global`) emite, además del archivo de la CLI, una estructura
que VS Code puede leer globalmente al apuntar los settings a `~/.copilot/`:

- `~/.copilot/instructions/standards.instructions.md` — estándares de ingeniería con
  `applyTo: '**'` (equivalente global al `CLAUDE.md` de estándares de Claude).
- `~/.copilot/prompts/{review-changes,setup-standards}.prompt.md` — prompts globales
  **stack-agnósticos** (autorados en `core/copilot/global-prompts/`). Se excluye
  `manage-context` por ser específico de Claude (compactación).
- `~/.copilot/README-vscode.md` — guía con el snippet exacto de `settings.json`.

## Consecuencias

- **Permitido/esperado**: con el settings apuntando a `~/.copilot/`, `/review-changes`,
  `/setup-standards` y los estándares globales están en cualquier proyecto de VS Code, sin
  commitear nada al repo — paridad con el global de Claude.
- **Regla**: los prompts globales no usan placeholders de stack (`${stack}`, `${test_cmd}`);
  el scope global corre con un preset ficticio `-`. Introducir uno rompe la generación.
- **Requiere acción del usuario**: a diferencia de Claude (ruta fija), el global de Copilot
  en VS Code exige configurar los dos settings una vez por máquina (documentado en el README).
- **Alcance**: solo agente `copilot`, scope `global`. No cambia project ni el generador Claude.
