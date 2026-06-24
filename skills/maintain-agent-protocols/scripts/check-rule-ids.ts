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

const DEFINITION_LINE = /^\s*(?:-\s+|#{1,6}\s+|\|\s*`?)(WF-[A-Z0-9_-]+|CON-[A-Z0-9_-]+|CHK-[A-Z0-9_-]+)\b/;

function extractRuleIds(content: string): Record<string, string> {
  const ids: Record<string, string> = {};
  const lines = content.split('\n');

  for (const line of lines) {
    const match = line.match(DEFINITION_LINE);
    if (!match) continue;

    const ruleId = match[1];
    ids[ruleId] = ruleId.split('-')[0];
  }

  return ids;
}

function shouldCheck(filePath: string): boolean {
  return !filePath.includes('/templates/');
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
    if (!shouldCheck(mdFile)) continue;

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
      if (!shouldCheck(mdFile)) continue;

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
console.log(`发现规则定义编号: ${Object.keys(allIds).length} 个`);
console.log('扫描规则: 只统计列表项、标题或表格首列中的规则定义；忽略模板资产、正文引用和示例。');

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
