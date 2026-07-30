# Case Study: Multi-File Refactor

This measured example shows how search results, interfaces, and one representative implementation can replace a full multi-file source dump when a repeated refactor is structurally uniform.

## Scenario

Ten TypeScript handler modules independently read `x-correlation-id`. A new `createRequestContext(request)` helper should replace that repeated logic while preserving logs, response bodies, repository contracts, and service behaviour.

## Before

The broad request included the complete contents of all ten handler modules. Each generated module contained twelve similar route handlers, so most of the context repeated imports, repository lookups, service calls, logging, and response construction.

Prompt shape:

```text
Refactor this service so every handler uses the new request context helper. I pasted all handler files because the helper may affect any route.

<91,217-character repository excerpt containing ten full modules>
```

## After

The focused request included:

- explicit acceptance criteria;
- a repository map produced by search;
- the helper interface;
- one representative handler excerpt;
- search evidence proving the same pattern exists in ten modules and nowhere else in production code;
- the relevant unit and integration test locations;
- a request to show the shared edit pattern rather than unchanged file bodies.

Prompt shape:

```text
Plan and implement a scoped refactor to use createRequestContext(request). Preserve API responses and service behaviour.

Acceptance criteria:
- handlers must stop reading x-correlation-id directly;
- correlationId must still appear in logs and response bodies;
- no repository or service signatures may change;
- add or update focused tests for the helper integration.

Repository map from search:
<five relevant path groups>

Helper interface:
<type and function signature>

Representative current code:
<one handler excerpt>

Search evidence:
rg -n 'x-correlation-id|randomUUID\(' src/handlers tests
reports the same direct-read pattern in the ten handler modules and no other production files.
```

## Measurement

The repository estimator reports:

| Context | Bytes | Characters | Words | Lines | Estimated tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| Before | 91,217 | 91,217 | 9,222 | 2,136 | 22,804 |
| After | 1,640 | 1,640 | 187 | 40 | 410 |
| Delta | -89,577 | -89,577 | -9,035 | -2,096 | -22,394 |

The result is specific to this generated fixture. It does not establish a fixed saving for real repositories or models.

## Reproduce the fixture

Run this from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
from textwrap import dedent

root = Path('/tmp/token-case-study-refactor')
root.mkdir(parents=True, exist_ok=True)


def build_module(index: int) -> str:
    handlers = []
    for route in range(1, 13):
        handlers.append(dedent(f'''\
export async function handleRoute{route:02d}(request: ApiRequest): Promise<ApiResponse> {{
  const correlationId = request.headers["x-correlation-id"] ?? randomUUID();
  logger.info({{ correlationId, route: "route-{route:02d}", module: "module-{index:02d}" }}, "request received");
  const user = await userRepository.findById(request.userId);
  if (!user) {{
    return {{ statusCode: 404, body: JSON.stringify({{ error: "user_not_found", correlationId }}) }};
  }}
  const result = await service.execute({{
    user,
    payload: request.body,
    correlationId,
    feature: "feature-{index:02d}-{route:02d}",
  }});
  logger.info({{ correlationId, resultId: result.id }}, "request completed");
  return {{ statusCode: 200, body: JSON.stringify({{ data: result, correlationId }}) }};
}}
'''))
    return dedent(f'''\
import {{ randomUUID }} from "node:crypto";
import {{ logger }} from "../logging/logger";
import {{ userRepository }} from "../repositories/user-repository";
import {{ service }} from "../services/service";
import type {{ ApiRequest, ApiResponse }} from "../types/api";

// Full source for src/handlers/module-{index:02d}.ts
''') + '\n'.join(handlers)

files = [
    f'--- src/handlers/module-{index:02d}.ts ---\n{build_module(index)}'
    for index in range(1, 11)
]

before = dedent('''\
Refactor this service so every handler uses the new request context helper. I pasted all handler files because the helper may affect any route. Please inspect the repository excerpt, decide what must change, update all relevant files, and explain the result.

Requirement:
Replace direct reads of x-correlation-id with createRequestContext(request), keep response payloads compatible, and do not change service behaviour.

Full repository excerpt:
''') + '\n\n'.join(files) + '\n'

after = dedent('''\
Plan and implement a scoped refactor to use createRequestContext(request). Preserve API responses and service behaviour.

Acceptance criteria:
- handlers must stop reading x-correlation-id directly;
- correlationId must still appear in logs and response bodies;
- no repository or service signatures may change;
- add or update focused tests for the helper integration.

Repository map from search:
- src/context/request-context.ts: defines createRequestContext(request)
- src/types/api.ts: defines ApiRequest and ApiResponse
- src/handlers/module-01.ts through module-10.ts: same repeated handler pattern
- tests/request-context.test.ts: helper unit tests
- tests/handler-context.test.ts: representative handler integration test

Helper interface:
export type RequestContext = {
  correlationId: string;
};

export function createRequestContext(request: ApiRequest): RequestContext;

Representative current code from src/handlers/module-01.ts:
const correlationId = request.headers["x-correlation-id"] ?? randomUUID();
logger.info({ correlationId, route: "route-01", module: "module-01" }, "request received");
const result = await service.execute({
  user,
  payload: request.body,
  correlationId,
  feature: "feature-01-01",
});
return { statusCode: 200, body: JSON.stringify({ data: result, correlationId }) };

Search evidence:
rg -n 'x-correlation-id|randomUUID\\(' src/handlers tests
reports the same direct-read pattern in the ten handler modules and no other production files.

Requested output:
Show the shared edit pattern, list affected files, and give the smallest verification commands. Do not paste unchanged handler bodies.
''')

(root / 'before.txt').write_text(before, encoding='utf-8')
(root / 'after.txt').write_text(after, encoding='utf-8')
PY

python3 scripts/estimate-context-size.py \
  /tmp/token-case-study-refactor/before.txt \
  /tmp/token-case-study-refactor/after.txt \
  --markdown
```

## Correctness safeguard

This technique is appropriate only after search confirms that the repeated pattern is genuinely uniform. Read additional files when modules have different side effects, error handling, ownership, tests, generated code, or compatibility requirements. The final change should still be verified with focused tests and a diff review across every affected file.
