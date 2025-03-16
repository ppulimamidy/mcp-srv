from mdutils import MdUtils

# Create a new Markdown file
mdFile = MdUtils(file_name='graph')

# Read the Mermaid content
with open('graph.mmd', 'r') as f:
    mermaid_content = f.read()

# Add the Mermaid diagram as a code block in Markdown
mdFile.new_header(level=1, title="LangGraph Visualization")
mdFile.write(f"```mermaid\n{mermaid_content}\n```")

# Create the Markdown file
mdFile.create_md_file()
print("Graph saved as graph.md")