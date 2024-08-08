# JSON Duplicate Remover

![Version](https://img.shields.io/badge/version-0.0.1-blue)
![VSCode](https://img.shields.io/badge/vscode-%3E%3D1.92.0-orange)

## Overview

**JSON Duplicate Remover** is a VSCode extension that helps you remove duplicate objects or lines from your JSON files. It utilizes a Python script to perform deduplication and provides categorized logging with log rotation.

## Features

- **Deduplicate JSON:** Remove duplicate objects from JSON files, including nested structures.
- **Logging:** Logs all operations, including the number of duplicates removed.
- **Contextual Menu:** Run the deduplication script directly from the file explorer or editor using the context menu.

## Installation

### From Source

1. Clone or download this repository.
2. Navigate to the extension folder.
3. Install dependencies: `npm install`.
4. Package the extension: `vsce package`.
5. Install the generated `.vsix` file by dragging it into the Extensions view in VSCode or using the command:

   ```sh
   code --install-extension json-duplicate-remover-0.0.1.vsix

### Manual Installation

If you have received the `.vsix` file directly:

1. Open VSCode.
2. Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
3. Click the `...` (More Actions) button and select `Install from VSIX...`.
4. Browse to the location of your `.vsix` file and install it.

### Usage

1. Open the JSON file you want to clean in VSCode.
2. Right-click the file in the file explorer or the editor.
3. Select `Run JSON Deduplication Script` from the context menu.
4. The script will run, and the cleaned JSON file will be saved.

### Configuration

- The Python script is embedded within the extension. You do not need to install Python separately.
- The logs will be saved in the same directory as the JSON file (`log.txt`).

### Requirements

- VSCode version 1.92.0 or higher.
- Node.js installed (for packaging or running the extension from source).

### Contributing

Feel free to fork this repository and submit pull requests. For any issues or feature requests, please open an issue on the repository.

### License

This extension is licensed under the [MIT License](./LICENSE.txt).

### Credits

This extension was created using the [Yeoman generator](https://code.visualstudio.com/api/get-started/your-first-extension) for VSCode extensions.
