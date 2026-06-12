#!/usr/bin/env node
/**
 * 检查跨文档引用完整性
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname, resolve, relative } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '../../..');
const SKILLS_DIR = join(ROOT, 'skills');

function findMarkdownLinks(content: string): Array<{ text: string; path: string }> {
  const links: Array<{ text: string; path: string }> = [];

  // [text](path) 格式
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let match;
  while ((match = linkRegex.exec(content)) !== null) {
    const [, text, path] = match;
    if (path.endsWith('.md') && !path.startsWith('http')) {
      links.push({ text, path });
    }
  }

  // `references/xxx` 格式
  const rootRefRegex = /`(references\/[^`]+\.md)`/g;
  while ((match = rootRefRegex.exec(content)) !== null) {
    links.push({ text: '', path: match[1] });
  }

  // 见仓库根 `xxx.md`
  const rootRef2Regex = /见仓库根\s+`([^`]+\.md)`/g;
  while ((match = rootRef2Regex.exec(content)) !== null) {
    links.push({ text: '', path: match[1] });
  }

  return links;
}

function resolvePath(linkPath: string, sourceFile: string): string {
  if (linkPath.startsWith('/')) {
    return join(ROOT, linkPath.slice(1));
  } else if (linkPath.startsWith('references/')) {
    // 可能是技能内或仓库根
    const parts = sourceFile.split('/');
    const skillsIdx = parts.indexOf('skills');
    if (skillsIdx >= 0 && skillsIdx + 1 < parts.length) {
      const skillDir = parts.slice(0, skillsIdx + 2).join('/');
      const skillRef = join(skillDir, linkPath);
      if (existsSync(skillRef)) return skillRef;
    }
    return join(ROOT, linkPath);
  } else {
    return resolve(dirname(sourceFile), linkPath);
  }
}

function* walkDir(dir: string): Generator<string> {
  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      yield* walkDir(fullPath);
    } else if (entry.endsWith('.md')) {
      yield fullPath;
    }
  }
}

function checkReferences() {
  const missing: Array<{ source: string; link: string; text: string; resolved: string }> = [];
  let checked = 0;

  for (const mdFile of walkDir(SKILLS_DIR)) {
    const content = readFileSync(mdFile, 'utf-8');
    const links = findMarkdownLinks(content);

    for (const { text, path: linkPath } of links) {
      checked++;
      const target = resolvePath(linkPath, mdFile);

      if (!existsSync(target)) {
        missing.push({
          source: relative(ROOT, mdFile),
          link: linkPath,
          text,
          resolved: relative(ROOT, target)
        });
      }
    }
  }

  // 检查 references/
  const refsDir = join(ROOT, 'references');
  if (existsSync(refsDir)) {
    for (const mdFile of walkDir(refsDir)) {
      const content = readFileSync(mdFile, 'utf-8');
      const links = findMarkdownLinks(content);

      for (const { text, path: linkPath } of links) {
        checked++;
        const target = resolvePath(linkPath, mdFile);

        if (!existsSync(target)) {
          missing.push({
            source: relative(ROOT, mdFile),
            link: linkPath,
            text,
            resolved: relative(ROOT, target)
          });
        }
      }
    }
  }

  return { checked, missing };
}

const { checked, missing } = checkReferences();

console.log(`检查范围: ${ROOT}`);
console.log(`Skills 目录: ${SKILLS_DIR}\n`);

if (missing.length === 0) {
  console.log(`✅ PASS: 检查了 ${checked} 个引用，全部有效`);
  process.exit(0);
}

console.error(`❌ FAIL: 检查了 ${checked} 个引用，发现 ${missing.length} 个失效引用:\n`);

for (const item of missing) {
  console.error(`  文件: ${item.source}`);
  console.error(`  引用: ${item.link}`);
  if (item.text) console.error(`  文本: ${item.text}`);
  console.error(`  解析为: ${item.resolved}\n`);
}

process.exit(1);
