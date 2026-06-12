#!/usr/bin/env node
/**
 * 检查规则编号唯一性
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, relative } from 'path';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '../../..');
const SKILLS_DIR = join(ROOT, 'skills');

const PATTERNS = {
  WF: /\bWF-[A-Z0-9_-]+\b/g,
  CON: /\bCON-[A-Z0-9_-]+\b/g,
  CHK: /\bCHK-[A-Z0-9_-]+\b/g,
};

function extractRuleIds(content: string): Record<string, string> {
  const ids: Record<string, string> = {};

  for (const [prefix, pattern] of Object.entries(PATTERNS)) {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      ids[match[0]] = prefix;
    }
  }

  return ids;
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

function checkUniqueness() {
  const allIds: Record<string, string[]> = {};

  for (const mdFile of walkDir(SKILLS_DIR)) {
    const content = readFileSync(mdFile, 'utf-8');
    const ids = extractRuleIds(content);

    for (const ruleId of Object.keys(ids)) {
      if (!allIds[ruleId]) allIds[ruleId] = [];
      allIds[ruleId].push(relative(ROOT, mdFile));
    }
  }

  // 扫描 references
  const refsDir = join(ROOT, 'references');
  try {
    for (const mdFile of walkDir(refsDir)) {
      const content = readFileSync(mdFile, 'utf-8');
      const ids = extractRuleIds(content);

      for (const ruleId of Object.keys(ids)) {
        if (!allIds[ruleId]) allIds[ruleId] = [];
        allIds[ruleId].push(relative(ROOT, mdFile));
      }
    }
  } catch {}

  const duplicates: Record<string, string[]> = {};
  for (const [ruleId, files] of Object.entries(allIds)) {
    if (files.length > 1) {
      duplicates[ruleId] = files;
    }
  }

  return { allIds, duplicates };
}

const { allIds, duplicates } = checkUniqueness();

console.log(`检查范围: ${ROOT}\n`);
console.log(`发现规则编号: ${Object.keys(allIds).length} 个`);

const byType: Record<string, number> = {};
for (const ruleId of Object.keys(allIds)) {
  const prefix = ruleId.split('-')[0];
  byType[prefix] = (byType[prefix] || 0) + 1;
}

for (const [prefix, count] of Object.entries(byType).sort()) {
  console.log(`  - ${prefix}-*: ${count} 个`);
}

console.log();

if (Object.keys(duplicates).length === 0) {
  console.log('✅ PASS: 所有规则编号唯一');
  process.exit(0);
}

console.error(`❌ FAIL: 发现 ${Object.keys(duplicates).length} 个重复编号:\n`);

for (const [ruleId, files] of Object.entries(duplicates).sort()) {
  console.error(`  ${ruleId} 出现在 ${files.length} 个文件:`);
  for (const file of files) {
    console.error(`    - ${file}`);
  }
  console.error();
}

process.exit(1);
