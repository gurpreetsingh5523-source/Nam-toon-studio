// vscode_extension_sample/extension.js
// Sample VS Code extension activation logic
const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('namtoonstudio.helloWorld', function () {
        vscode.window.showInformationMessage('Nam-toon-studio VS Code Extension Activated!');
    });
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};