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
const SKILL_ROOT = resolve(__dirname, '..');
const IS_SOURCE_REPO = existsSync(join(ROOT, '.git')) && existsSync(join(ROOT, 'references'));
const SKILL_SCAN_ROOT = IS_SOURCE_REPO ? SKILLS_DIR : SKILL_ROOT;

function findMarkdownLinks(content: string): Array<{ text: string; path: string }> {
  const links: Array<{ text: string; path: string }> = [];
  const seen = new Set<string>();
  const generatedEntryNames = new Set(['AGENTS.md', 'CLAUDE.md', 'CODEX.md', 'codex.md']);

  function normalizeDestination(rawPath: string): string {
    const trimmed = rawPath.trim();
    const destination = trimmed.startsWith('<') && trimmed.includes('>')
      ? trimmed.slice(1, trimmed.indexOf('>'))
      : trimmed.split(/\s+/, 1)[0];
    return destination.split('#', 1)[0].split('?', 1)[0];
  }

  function add(text: string, rawPath: string, skipGeneratedEntry = false) {
    const path = normalizeDestination(rawPath);
    const basename = path.split('/').pop();
    // Entry files in examples describe target-repo artifacts, not Skill dependencies.
    if (!path || !basename || (skipGeneratedEntry && generatedEntryNames.has(basename)) || seen.has(path)) return;
    seen.add(path);
    links.push({ text, path });
  }

  // [text](path) 格式
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let match;
  while ((match = linkRegex.exec(content)) !== null) {
    const [, text, path] = match;
    const normalizedPath = normalizeDestination(path);
    if (normalizedPath.endsWith('.md') && !normalizedPath.startsWith('http')) {
      add(text, path);
    }
  }

  // 反引号中的显式路径；要求带目录，避免把 AGENTS.md 等产物名误判为引用。
  const inlinePathRegex = /`((?:\.\.?\/|references\/|skills\/)[^`\s]*\.md(?:#[^`\s]+)?)`/g;
  while ((match = inlinePathRegex.exec(content)) !== null) {
    add('', match[1], true);
  }

  return links;
}

function resolvePath(linkPath: string, sourceFile: string): string {
  if (linkPath.startsWith('/')) {
    return join(ROOT, linkPath.slice(1));
  } else if (linkPath.startsWith('skills/')) {
    return join(ROOT, linkPath);
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

  for (const mdFile of walkDir(SKILL_SCAN_ROOT)) {
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
  if (IS_SOURCE_REPO && existsSync(refsDir)) {
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
console.log(`Markdown 范围: ${SKILL_SCAN_ROOT}`);
console.log(`模式: ${IS_SOURCE_REPO ? '源码仓全量' : '独立安装态'}\n`);

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
