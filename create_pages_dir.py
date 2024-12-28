import os

pages_dir = os.path.join(os.path.dirname(__file__), 'pages')
os.makedirs(pages_dir, exist_ok=True)
print(f"Created pages directory: {pages_dir}")
