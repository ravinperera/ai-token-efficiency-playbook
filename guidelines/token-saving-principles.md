# Token-Saving Principles

## 1. Context Is More Expensive Than Style

Short replies help, but the biggest waste is usually input context: long chat history, large files, repeated logs, and broad repo scans.

## 2. Search Before Reading

Use targeted search before opening files. Read the smallest useful file range.

## 3. Summarise Noisy Output

Terminal output, CI logs, and stack traces should be reduced to:

- command
- error
- relevant file/path
- likely cause
- next action

## 4. Avoid Repeating Known Context

Do not restate project background or previous decisions unless the user asks.

## 5. Use The Right Model For The Job

Use cheaper/faster models for summarisation, formatting, simple Q&A, and routine edits. Use stronger models for architecture, debugging, security review, and ambiguous reasoning.

## 6. Keep Memory Files Small

Long instruction files become permanent token tax. Keep them short, current, and actionable.

## 7. Preserve Accuracy

Token reduction is only useful if the result remains correct. Do not compress away assumptions, risks, commands, or verification results that matter.
