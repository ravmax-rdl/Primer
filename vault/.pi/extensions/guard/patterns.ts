const SENSITIVE_PATTERNS: RegExp[] = [
  /(?:^|[\\/])\.env(?:[.\\/_-]|$)/i,
  /(?:^|[\\/])(?:credentials?|secrets?)(?:[._-][^\\/]*)?(?:$|[\\/])/i,
  /(?:^|[\\/])id_(?:rsa|dsa|ecdsa|ed25519)(?:\.pub)?(?:$|[\\/])/i,
  /private[_ -]?key/i,
  /recovery[_ -]?(?:codes?|phrase)/i,
  /auth[_ -]?tokens?/i,
  /\.asc(?:["'\s]|$)/i,
];

export function hitsSensitivePath(text: string): string | null {
  if (!text) return null;
  for (const pattern of SENSITIVE_PATTERNS) {
    if (pattern.test(text)) return pattern.source;
  }
  return null;
}
