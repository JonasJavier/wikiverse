/**
 * @vitest-environment node
 *
 * Repo-wide guards for DECISIONS §0.4 and §0.5.
 *
 *  - §0.4: no `dangerouslySetInnerHTML` anywhere in the frontend, no exception.
 *  - §0.5: `react-markdown` WITHOUT `rehype-raw` and WITH `skipHtml`.
 *
 * Files are parsed with the TypeScript compiler rather than grepped, so a
 * comment that explains the rule (several do) is not a violation, while a real
 * JSX attribute, object key or property access is — however it is spelled or
 * formatted.
 */
import { readdirSync, readFileSync } from "node:fs";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

import ts from "typescript";
import { describe, expect, it } from "vitest";

const SRC = fileURLToPath(new URL("..", import.meta.url));

/** Assembled, so this file never contains the forbidden name as a token itself. */
const FORBIDDEN = ["dangerously", "Set", "Inner", "HTML"].join("");

function sourceFiles(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return sourceFiles(path);
    return /\.(ts|tsx)$/.test(entry.name) ? [path] : [];
  });
}

function parse(name: string, text: string): ts.SourceFile {
  const kind = name.endsWith(".tsx") ? ts.ScriptKind.TSX : ts.ScriptKind.TS;
  return ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true, kind);
}

function walk(node: ts.Node, visit: (node: ts.Node) => void): void {
  visit(node);
  node.forEachChild((child) => walk(child, visit));
}

/** Every place a source file names the forbidden prop, as `line: text`. */
function forbiddenUses(file: ts.SourceFile): string[] {
  const hits: string[] = [];
  walk(file, (node) => {
    const named =
      (ts.isIdentifier(node) || ts.isStringLiteralLike(node)) && node.text === FORBIDDEN;
    if (named) {
      const { line } = file.getLineAndCharacterOfPosition(node.getStart(file));
      hits.push(`${line + 1}: ${node.parent.getText(file).slice(0, 80)}`);
    }
  });
  return hits;
}

/** The local names `react-markdown`'s default export is imported under. */
function reactMarkdownNames(file: ts.SourceFile): Set<string> {
  const names = new Set<string>();
  for (const statement of file.statements) {
    if (
      ts.isImportDeclaration(statement) &&
      ts.isStringLiteral(statement.moduleSpecifier) &&
      statement.moduleSpecifier.text === "react-markdown" &&
      statement.importClause?.name
    ) {
      names.add(statement.importClause.name.text);
    }
  }
  return names;
}

/** `<ReactMarkdown …>` elements that do not pass a truthy `skipHtml`. */
function markdownWithoutSkipHtml(file: ts.SourceFile): string[] {
  const names = reactMarkdownNames(file);
  if (names.size === 0) return [];
  const hits: string[] = [];
  walk(file, (node) => {
    if (!ts.isJsxOpeningElement(node) && !ts.isJsxSelfClosingElement(node)) return;
    if (!names.has(node.tagName.getText(file))) return;
    const skip = node.attributes.properties.find(
      (attr) => ts.isJsxAttribute(attr) && attr.name.getText(file) === "skipHtml",
    );
    const disabled =
      skip !== undefined &&
      ts.isJsxAttribute(skip) &&
      skip.initializer !== undefined &&
      skip.initializer.getText(file).replace(/\s/g, "") === "{false}";
    if (skip === undefined || disabled) {
      const { line } = file.getLineAndCharacterOfPosition(node.getStart(file));
      hits.push(`line ${line + 1}`);
    }
  });
  return hits;
}

const files = sourceFiles(SRC).map((path) => ({
  name: relative(SRC, path).replace(/\\/g, "/"),
  file: parse(path, readFileSync(path, "utf8")),
}));

describe("guard: no raw HTML rendering paths in src/", () => {
  it("actually scans the source tree", () => {
    expect(files.length).toBeGreaterThan(50);
    expect(files.some((f) => f.name === "components/search/Snippet.tsx")).toBe(true);
  });

  it("detects the forbidden prop when it is present (self-test)", () => {
    const sample = parse(
      "sample.tsx",
      `export const X = () => <div ${FORBIDDEN}={{ __html: "<b>x</b>" }} />;\n` +
        `export const Y = () => createElement("div", { ${FORBIDDEN}: { __html: "" } });\n` +
        `// a comment naming ${FORBIDDEN} is fine\n`,
    );
    expect(forbiddenUses(sample)).toHaveLength(2);
  });

  it(`no file under src/ uses ${FORBIDDEN} (DECISIONS §0.4)`, () => {
    const violations = files.flatMap(({ name, file }) =>
      forbiddenUses(file).map((hit) => `${name}:${hit}`),
    );
    expect(violations).toEqual([]);
  });

  it("no file imports rehype-raw (DECISIONS §0.5)", () => {
    const violations = files
      .filter(({ file }) =>
        file.statements.some(
          (s) =>
            ts.isImportDeclaration(s) &&
            ts.isStringLiteral(s.moduleSpecifier) &&
            s.moduleSpecifier.text === "rehype-raw",
        ),
      )
      .map(({ name }) => name);
    expect(violations).toEqual([]);
  });

  it("every <ReactMarkdown> passes skipHtml (DECISIONS §0.5)", () => {
    const users = files.filter(({ file }) => reactMarkdownNames(file).size > 0);
    expect(users.length).toBeGreaterThan(0);
    const violations = users.flatMap(({ name, file }) =>
      markdownWithoutSkipHtml(file).map((hit) => `${name}:${hit}`),
    );
    expect(violations).toEqual([]);
  });

  it("detects a <ReactMarkdown> without skipHtml (self-test)", () => {
    const sample = parse(
      "sample.tsx",
      `import Md from "react-markdown";\n` +
        `export const A = () => <Md>{"x"}</Md>;\n` +
        `export const B = () => <Md skipHtml={false}>{"x"}</Md>;\n` +
        `export const C = () => <Md skipHtml>{"x"}</Md>;\n`,
    );
    expect(markdownWithoutSkipHtml(sample)).toEqual(["line 2", "line 3"]);
  });
});
