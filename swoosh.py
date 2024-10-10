import os
import ast
from typing import List, Tuple
import sys

def get_file_docstring(filepath: str) -> str:
    with open(filepath, 'r') as file:
        try:
            tree = ast.parse(file.read(), filename=filepath)
        except:
            return ""
    return ast.get_docstring(tree) or ""

def get_function_info(filepath: str) -> List[Tuple[str, str, List[str]]]:
    functions = []

    with open(filepath, 'r') as file:
        try:
            tree = ast.parse(file.read(), filename=filepath)
        except: 
            return functions
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            docstring = ast.get_docstring(node) or ""
            params = [arg.arg for arg in node.args.args]  # Extract parameter names
            functions.append((name, docstring, params))
    
    return functions

def generate_html(directories: List[str], output_file: str) -> None:
    html_content = ["<html><head><title>Project Documentation</title>"]
    
    html_content.append("""
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        ul, #fileTree, #functionList { list-style-type: none; padding-left: 0; }
        li { margin-left: 20px; cursor: pointer; }
        .nested { display: none; }
        .active { display: block; }
        .caret { font-weight: bold; }
        .caret::before { content: "\\25B6"; margin-right: 6px; }
        .caret-down::before { content: "\\25BC"; }
        #functionList { display: none; }
        .toggle-btn { margin: 20px; padding: 10px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
        .search-box { margin: 20px; }
        #viewTitle { display: none; font-weight: bold; margin-top: 20px; }
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var togglers = document.getElementsByClassName("caret");
            for (var i = 0; i < togglers.length; i++) {
                togglers[i].addEventListener("click", function() {
                    this.parentElement.querySelector(".nested").classList.toggle("active");
                    this.classList.toggle("caret-down");
                });
            }
            
            // Toggle between file tree and function list views
            document.getElementById("toggleViewBtn").addEventListener("click", function() {
                var fileTree = document.getElementById("fileTree");
                var functionList = document.getElementById("functionList");
                var viewTitle = document.getElementById("viewTitle");
                
                if (fileTree.style.display === "none") {
                    fileTree.style.display = "block";
                    functionList.style.display = "none";
                    viewTitle.style.display = "none";
                } else {
                    fileTree.style.display = "none";
                    functionList.style.display = "block";
                    viewTitle.style.display = "block";
                }
            });
            
            // Search functionality
            document.getElementById("searchBox").addEventListener("input", function() {
                var query = this.value.toLowerCase();
                var files = document.querySelectorAll("#fileTree li, #functionList li");
                files.forEach(function(file) {
                    if (file.textContent.toLowerCase().includes(query)) {
                        file.style.display = "";
                    } else {
                        file.style.display = "none";
                    }
                });
            });
        });
    </script>
    </head><body>""")
    
    html_content.append("<h1>Project Documentation</h1>")
    html_content.append('<div class="search-box"><input type="text" id="searchBox" placeholder="Search functions or files..."></div>')
    html_content.append('<button id="toggleViewBtn" class="toggle-btn">Toggle View</button>')
    html_content.append('<div id="viewTitle"></div>')

    html_content.append('<ul id="fileTree">')

    all_functions = []

    for directory in directories:
        html_content.append(f'<li><span class="caret">{os.path.basename(directory)}</span>')
        html_content.append('<ul class="nested">')

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, directory)

                    html_content.append(f'<li><span class="caret">{relpath}</span>')
                    html_content.append('<ul class="nested">')
                    
                    file_docstring = get_file_docstring(filepath)
                    if file_docstring:
                        html_content.append(f"<li><strong>File Docstring:</strong> {file_docstring}</li>")
                    
                    functions = get_function_info(filepath)
                    if functions:
                        for func_name, func_docstring, params in functions:
                            param_list = ', '.join(params) if params else 'No parameters'
                            func_docstring_html = func_docstring if func_docstring else 'No docstring'
                            
                            html_content.append(f'<li><span class="caret">Function: {func_name}</span>')
                            html_content.append('<ul class="nested">')
                            html_content.append(f"<li><strong>Parameters:</strong> {param_list}</li>")
                            html_content.append(f"<li><strong>Docstring:</strong> {func_docstring_html}</li>")
                            html_content.append('</ul></li>')
                            
                            all_functions.append((relpath, func_name, param_list, func_docstring_html))
                    
                    html_content.append('</ul></li>')

        html_content.append('</ul></li>')

    html_content.append('</ul>')

    
    html_content.append('<ul id="functionList">')
    html_content.append('<h2>Function List</h2>')
    for filepath, func_name, param_list, func_docstring_html in all_functions:
        html_content.append(f'<li><strong>{func_name}</strong> in <em>{filepath}</em>')
        html_content.append('<ul>')
        html_content.append(f"<li><strong>Parameters:</strong> {param_list}</li>")
        html_content.append(f"<li><strong>Docstring:</strong> {func_docstring_html}</li>")
        html_content.append('</ul></li>')
    html_content.append('</ul>')

    html_content.append("</body></html>")
    
    with open(output_file, 'w') as file:
        file.write('\n'.join(html_content))
    
    print(f"HTML documentation written to {output_file}")





def main():
    args = sys.argv[1:]
    dirs = args
    output = 'documentation.html'
    generate_html(output, dirs)


if __name__ == '__main__':
    main()
