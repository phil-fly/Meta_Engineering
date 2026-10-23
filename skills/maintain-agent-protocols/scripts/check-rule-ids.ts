#!/usr/bin/env node
/**
 * 检查规则编号唯一性与命名空间合法性
 *
 * 做两件事：
 * 1. 唯一性：同一编号不得在多个文件中被定义为规则。
 * 2. 命名空间：规则定义位的编号必须落在已知命名空间内。
 *    历史缺陷是只识别 `WF-`、`CON-`、`CHK-` 三个前缀，导致 `PERF001`
 *    这类"长得像编号但不在任何命名空间"的定义对校验完全不可见（假阴性）。
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, relative } from 'path';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '../../..');
const SKILLS_DIR = join(ROOT, 'skills');

/**
 * 允许出现在规则定义位的命名空间。
 * - WF / CON / CHK：协议包的通用规则编号族。
 * - CONF / DEC：产品需求技能确认记录与决策记录编号族。
 * - ISSUE：问题台账编号族。
 * 新增命名空间必须同时更新本集合与 `references/protocol/rule-ingestion.md`。
 */
const KNOWN_NAMESPACES = new Set(['WF', 'CON', 'CHK', 'CONF', 'DEC', 'ISSUE']);

/** 规则定义位：列表项、标题或表格首列，可带反引号包裹。 */
const DEFINITION_LINE =
  /^\s*(?:-\s+|#{1,6}\s+|\|\s*`?)([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)\b/;

/** 带命名空间的编号，例如 `CON-PERF-001`、`CONF-001`、`ISSUE-0001`。 */
const NAMESPACED_ID = /^([A-Z][A-Z0-9]*)-[A-Z0-9]/;

/** 无命名空间的裸编号，例如历史遗留的 `PERF001`。 */
const BARE_ID = /^[A-Z]{2,}[0-9]{2,}$/;

/**
 * 标准编号白名单：形如 `ISO-8601`、`RFC-2119`、`SHA256`、`UTF-8`。
 * 它们长得像规则编号，但属于标准名，不是协议规则，不应判为编号缺陷。
 */
const STANDARD_ID =
  /^(?:ISO|IEC|IEEE|RFC|ANSI|ECMA|W3C|UTF|SHA|AES|RSA|TLS|SSL|HTTP|UUID|MD|SEMVER)(?:-?\d+(?:\.\d+)*)?$/;

interface Definition {
  id: string;
  namespace: string;
}

function parseDefinition(token: string): Definition | null {
  if (STANDARD_ID.test(token)) {
    return null;
  }
  const namespaced = token.match(NAMESPACED_ID);
  if (namespaced) {
    return { id: token, namespace: namespaced[1] };
  }
  if (BARE_ID.test(token)) {
    return { id: token, namespace: '' };
  }
  return null;
}

function extractRuleIds(content: string): Record<string, string> {
  const ids: Record<string, string> = {};
  const lines = content.split('\n');

  for (const line of lines) {
    const match = line.match(DEFINITION_LINE);
    if (!match) continue;

    const definition = parseDefinition(match[1]);
    if (!definition) continue;

    ids[definition.id] = definition.namespace;
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
  const unnamespaced: Record<string, string[]> = {};
  const unknownNamespace: Record<string, string[]> = {};

  const scan = (dir: string) => {
    try {
      for (const mdFile of walkDir(dir)) {
        if (!shouldCheck(mdFile)) continue;

        const content = readFileSync(mdFile, 'utf-8');
        const ids = extractRuleIds(content);
        const relPath = relative(ROOT, mdFile);

        for (const [ruleId, namespace] of Object.entries(ids)) {
          if (!allIds[ruleId]) allIds[ruleId] = [];
          allIds[ruleId].push(relPath);

          const bucket = namespace === '' ? unnamespaced
            : KNOWN_NAMESPACES.has(namespace) ? null
              : unknownNamespace;
          if (bucket) {
            if (!bucket[ruleId]) bucket[ruleId] = [];
            bucket[ruleId].push(relPath);
          }
        }
      }
    } catch {
      /* 目录不存在时跳过 */
    }
  };

  scan(SKILLS_DIR);
  scan(join(ROOT, 'references'));

  const duplicates: Record<string, string[]> = {};
  for (const [ruleId, files] of Object.entries(allIds)) {
    if (files.length > 1) {
      duplicates[ruleId] = files;
    }
  }

  return { allIds, duplicates, unnamespaced, unknownNamespace };
}

const { allIds, duplicates, unnamespaced, unknownNamespace } = checkUniqueness();

console.log(`检查范围: ${ROOT}\n`);
console.log(`发现规则定义编号: ${Object.keys(allIds).length} 个`);
console.log(
  '扫描规则: 只统计列表项、标题或表格首列中的规则定义；忽略模板资产、正文引用和示例。',
);

const byType: Record<string, number> = {};
const BARE_PREFIX = '(未命名空间)';
for (const ruleId of Object.keys(allIds)) {
  const prefix = ruleId.includes('-') ? ruleId.split('-')[0] : BARE_PREFIX;
  byType[prefix] = (byType[prefix] || 0) + 1;
}

for (const [prefix, count] of Object.entries(byType).sort()) {
  const label = prefix === BARE_PREFIX ? prefix : `${prefix}-*`;
  console.log(`  - ${label}: ${count} 个`);
}

console.log();

const hasDuplicates = Object.keys(duplicates).length > 0;
const hasUnnamespaced = Object.keys(unnamespaced).length > 0;
const hasUnknown = Object.keys(unknownNamespace).length > 0;

if (!hasDuplicates && !hasUnnamespaced && !hasUnknown) {
  console.log('✅ PASS: 所有规则编号唯一且命名空间合法');
  process.exit(0);
}

if (hasDuplicates) {
  console.error(`❌ FAIL: 发现 ${Object.keys(duplicates).length} 个重复编号:\n`);

  for (const [ruleId, files] of Object.entries(duplicates).sort()) {
    console.error(`  ${ruleId} 出现在 ${files.length} 个文件:`);
    for (const file of files) {
      console.error(`    - ${file}`);
    }
    console.error();
  }
}

if (hasUnnamespaced) {
  console.error(
    `❌ FAIL: 发现 ${Object.keys(unnamespaced).length} 个未命名空间的规则编号:\n`,
  );
  console.error(
    `  允许的命名空间: ${[...KNOWN_NAMESPACES].map((n) => `${n}-*`).join('、')}\n`,
  );

  for (const [ruleId, files] of Object.entries(unnamespaced).sort()) {
    console.error(`  ${ruleId} 缺少命名空间前缀，出现在:`);
    for (const file of files) {
      console.error(`    - ${file}`);
    }
    console.error();
  }
}

if (hasUnknown) {
  console.error(
    `❌ FAIL: 发现 ${Object.keys(unknownNamespace).length} 个未知命名空间的规则编号:\n`,
  );
  console.error(
    `  允许的命名空间: ${[...KNOWN_NAMESPACES].map((n) => `${n}-*`).join('、')}`,
  );
  console.error(
    '  若该编号其实是标准名（如 ISO-8601、RFC-2119），把它加入本脚本的 STANDARD_ID 白名单，而不是注册命名空间。\n',
  );

  for (const [ruleId, files] of Object.entries(unknownNamespace).sort()) {
    const prefix = ruleId.split('-')[0];
    console.error(`  ${ruleId} 使用了未注册命名空间 ${prefix}-*，出现在:`);
    for (const file of files) {
      console.error(`    - ${file}`);
    }
    console.error();
  }
}

process.exit(1);
