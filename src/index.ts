// Astra / Codex Remote Sandbox Entrypoint
export function helloAstra(): string {
  return "Astra & Codex Remote Sandbox Ready!";
}

console.log(helloAstra());
console.log(`Environment initialized: Node ${process.version}`);
