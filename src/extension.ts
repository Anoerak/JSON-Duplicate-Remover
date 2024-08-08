import * as vscode from 'vscode';
import { Options } from 'python-shell'; // Import necessary types
import { PythonShell, PythonShellError } from 'python-shell'; // Import necessary types
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.runJsonDeduplication', () => {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0].uri.fsPath || '';
        const scriptPath = path.join(context.extensionPath, 'python', 'json_deduplication.py');
        const inputFilePath = path.join(workspaceFolder, 'input.json');
        const outputFilePath = path.join(workspaceFolder, 'output.json');
        const logFilePath = path.join(workspaceFolder, 'log.txt');

        const pythonPath = vscode.workspace.getConfiguration().get<string>('jsonDeduplication.pythonPath', 'python3');
        const pyOptions = {
            args: [inputFilePath, outputFilePath, logFilePath],
            pythonPath: pythonPath,
        };
        

        // Correct the function call
        PythonShell.run(scriptPath, pyOptions).then((options) => {
            vscode.window.showInformationMessage('JSON Deduplication started...');
        }).then(() => {
            vscode.window.showInformationMessage('JSON Deduplication completed successfully!');
        }).catch((error: PythonShellError) => {
            vscode.window.showErrorMessage(`Error: ${error.message}`);
        });
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
