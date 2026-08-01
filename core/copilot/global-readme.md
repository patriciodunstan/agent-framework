# Copilot global en VS Code

Estos archivos (`~/.copilot/`) están disponibles en **todos** tus proyectos si apuntás
VS Code a estas carpetas. Agregá a tu `settings.json` **de usuario** (Ctrl+Shift+P →
"Preferences: Open User Settings (JSON)"):

```jsonc
{
  "chat.promptFilesLocations": {
    ".github/prompts": true,
    "~/.copilot/prompts": true
  },
  "chat.instructionsFilesLocations": {
    ".github/instructions": true,
    "~/.copilot/instructions": true
  }
}
```

- **Formato**: objeto `{ "ruta": true/false }` (verificado en la doc de VS Code, ago-2026).
  Si tu versión de VS Code muestra `chat.promptFilesLocations` como arreglo en el schema,
  usá `["~/.copilot/prompts"]` para esa clave.
- Con esto tenés, en cualquier proyecto y sin commitear nada al repo:
  - Prompts globales: `/review-changes`, `/setup-standards`.
  - Estándares de ingeniería globales (`standards.instructions.md`, `applyTo: '**'`).
- La primera carpeta (`.github/…`) mantiene los archivos por-proyecto; la segunda agrega
  los globales. VS Code busca en ambas.

> `~/.copilot/copilot-instructions.md` es para **GitHub Copilot CLI** (otra herramienta).
> Para VS Code, los estándares globales viven en `~/.copilot/instructions/`.

<!-- generado por agent-framework (global, copilot) -->
