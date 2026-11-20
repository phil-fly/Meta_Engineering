#!/usr/bin/env node
/**
 * 检查模板占位符泄漏
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname, resolve, relative, basename } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '../../..');
const SKILLS_DIR = join(ROOT, 'skills');

const PLACEHOLDER_PATTERNS = [
  /<project>/gi,
  /<project-name>/gi,
  /<install-command>/gi,
  /<package-manager>/gi,
  /<framework>/gi,
  /<language>/gi,
  /<version>/gi,
  /<username>/gi,
  /<repo>/gi,
  /<path>/gi,
  /<filename>/gi,
  /<PLACEHOLDER[^>]*>/gi,
  /\{project\}/g,
  /\{command\}/g,
  /\$\{[A-Z_]+\}/g,
];

const EXCLUDE_PATTERNS = ['template', 'example', 'reference', 'blueprint'];

function shouldCheck(filePath: string): boolean {
  const pathLower = filePath.toLowerCase();

  if (pathLower.includes('/templates/')) return false;

  const name = basename(filePath, '.md').toLowerCase();
  return !EXCLUDE_PATTERNS.some(p => name.includes(p));
}

function findPlaceholders(content: string): Array<{ placeholder: string; line: number; context: string }> {
  const placeholders: Array<{ placeholder: string; line: number; context: string }> = [];

  for (const pattern of PLACEHOLDER_PATTERNS) {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      const start = Math.max(0, match.index - 30);
      const end = Math.min(content.length, match.index + match[0].length + 30);
      const context = content.slice(start, end).replace(/\n/g, ' ').trim();

      // 排除反引号包裹的占位符（作为示例说明）
      const beforeMatch = content.slice(Math.max(0, match.index - 5), match.index);
      const afterMatch = content.slice(match.index + match[0].length, Math.min(content.length, match.index + match[0].length + 5));
      if (beforeMatch.includes('`') && afterMatch.includes('`')) {
        continue; // 这是文档中的示例引用，不是泄漏
      }

      const line = content.slice(0, match.index).split('\n').length;

      placeholders.push({
        placeholder: match[0],
        line,
        context
      });
    }
  }

  return placeholders;
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

function checkPlaceholders() {
  const findings: Array<{ file: string; placeholders: Array<{ placeholder: string; line: number; context: string }> }> = [];
  let checked = 0;

  for (const mdFile of walkDir(SKILLS_DIR)) {
    if (!shouldCheck(mdFile)) continue;

    checked++;
    const content = readFileSync(mdFile, 'utf-8');
    const placeholders = findPlaceholders(content);

    if (placeholders.length > 0) {
      findings.push({
        file: relative(ROOT, mdFile),
        placeholders
      });
    }
  }

  // 检查根级协议
  for (const filename of ['AGENTS.md', 'CLAUDE.md', 'CODEX.md']) {
    const filePath = join(ROOT, filename);
    if (existsSync(filePath)) {
      checked++;
      const content = readFileSync(filePath, 'utf-8');
      const placeholders = findPlaceholders(content);

      if (placeholders.length > 0) {
        findings.push({ file: filename, placeholders });
      }
    }
  }

  return { checked, findings };
}

const { checked, findings } = checkPlaceholders();

console.log(`检查范围: ${ROOT}`);
console.log(`排除: 模板文件、示例文件、参考文件\n`);

if (findings.length === 0) {
  console.log(`✅ PASS: 检查了 ${checked} 个文件，未发现占位符泄漏`);
  process.exit(0);
}

console.error(`❌ FAIL: 检查了 ${checked} 个文件，发现 ${findings.length} 个文件有占位符泄漏:\n`);

let totalPlaceholders = 0;
for (const item of findings) {
  console.error(`  文件: ${item.file}`);
  for (const ph of item.placeholders) {
    totalPlaceholders++;
    console.error(`    行 ${ph.line}: ${ph.placeholder}`);
    console.error(`    上下文: ...${ph.context}...`);
  }
  console.error();
}

console.error(`共发现 ${totalPlaceholders} 个占位符`);
process.exit(1);
