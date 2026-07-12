#!/usr/bin/env python3
with open('/tmp/papers_full.txt', 'r') as f:
    text = f.read()

lines = text.strip().split('\n')
journal_papers = []
conf_papers = []
in_journal = False
in_conf = False

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    if '期刊' in line and '论文' in line:
        in_journal = True
        in_conf = False
        continue
    if '会议' in line and '论文' in line:
        in_journal = False
        in_conf = True
        continue
    if '发表' in line and '目录' in line:
        continue
    if in_journal:
        journal_papers.append(line)
    elif in_conf:
        conf_papers.append(line)

print(f"期刊论文总数: {len(journal_papers)}")
print(f"会议论文总数: {len(conf_papers)}")
print()
print("=== 期刊论文 ===")
for i, p in enumerate(journal_papers, 1):
    print(f"{i}. {p[:150]}")
print()
print("=== 会议论文 ===")
for i, p in enumerate(conf_papers, 1):
    print(f"{i}. {p[:150]}")