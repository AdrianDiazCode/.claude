# Plan: Update all @types/node to ^24

## @types/node version changes (15 files)

All `@types/node` entries changed to `"^24"`:

| # | File | Current |
|---|------|---------|
| 1 | `package.json` (root) | `~18.16.9` |
| 2 | `repos/auth_service/package.json` | `^22.5.5` |
| 3 | `repos/auth_service/app/package.json` | `^22.5.5` |
| 4 | `repos/auth_service/sdk/package.json` | `^20.11.2` |
| 5 | `repos/buildman-properties/package.json` | `^22.5.5` |
| 6 | `repos/buildman-properties/app/package.json` | `^22.5.5` |
| 7 | `repos/buildman-properties/sdk/package.json` | `^20.11.2` |
| 8 | `repos/country-state-city-codes/package.json` | `^22.5.5` |
| 9 | `repos/country-state-city-codes/app/package.json` | `^22.5.5` |
| 10 | `repos/country-state-city-codes/sdk/package.json` | `^20.11.2` |
| 11 | `repos/payments-service/package.json` | `^22.5.5` |
| 12 | `repos/payments-service/app/package.json` | `^22.5.5` |
| 13 | `repos/payments-service/sdk/package.json` | `^20.11.2` |
| 14 | `repos/lazy-models-base/package.json` | `24.8.0` |
| 15 | `repos/redux-lazy-models/package.json` | `24.8.0` |

## TypeScript upgrade (1 file)

`repos/lazy-models-base/package.json`: `"typescript": "4.9.5"` → `"typescript": "^5.9.2"` (aligns with other repos, required for @types/node@24)

## Verification

Run `npm install` in lazy-models-base to confirm the original build error is resolved.
