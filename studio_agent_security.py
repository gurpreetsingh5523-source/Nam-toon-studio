import os
import glob
import re

class StudioAgentSecurity:
    def __init__(self, workspace):
        self.workspace = workspace
        self.sensitive_patterns = [
            r'sk-[A-Za-z0-9-_]{20,}',  # OpenAI key
            r'api[_-]?key\s*=\s*["\"][A-Za-z0-9-_]{10,}',
            r'token\s*=\s*["\"][A-Za-z0-9-_]{10,}',
            r'secret\s*=\s*["\"][A-Za-z0-9-_]{10,}',
        ]
        self.issues = []

    def scan_sensitive(self):
        py_files = glob.glob(os.path.join(self.workspace, "**/*.py"), recursive=True)
        for f in py_files:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                for pattern in self.sensitive_patterns:
                    for match in re.findall(pattern, content):
                        self.issues.append((f, match))
        return self.issues

    def auto_remove(self):
        for f, match in self.issues:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            new_content = content.replace(match, 'REMOVED_FOR_SECURITY')
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
        return len(self.issues)

if __name__ == "__main__":
    agent_sec = StudioAgentSecurity(workspace=os.getcwd())
    issues = agent_sec.scan_sensitive()
    if issues:
        print(f"Sensitive info found in {len(issues)} places. Removing...")
        removed = agent_sec.auto_remove()
        print(f"{removed} sensitive items auto-removed.")
    else:
        print("No sensitive info found. Workspace is secure!")
