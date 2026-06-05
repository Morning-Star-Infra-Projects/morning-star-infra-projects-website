from pathlib import Path
root=Path(r"c:\Users\PRABHAKAR\OneDrive\Documents\hehe-3-backup")
updated=[]
for p in root.rglob('*.html'):
    s=p.read_text(encoding='utf-8')
    orig=s
    s=s.replace('src="/assets/images/Morning-Star-Infra-Projects-Footer-Logo.webp""','src="/assets/images/Morning-Star-Infra-Projects-Footer-Logo.webp"')
    if s!=orig:
        p.write_text(s,encoding='utf-8')
        updated.append(str(p.relative_to(root)))
print('Fixed files:')
for f in updated:
    print(f)
