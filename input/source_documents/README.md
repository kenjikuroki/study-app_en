# source_documents

StudyApp stores input source materials under:

`studyapp/input/source_documents/{app_id}/{category}/`

Here, `{category}` means the machine-safe `category_id`, not the display name.

## Official Structure

```text
studyapp/input/source_documents/
├─ linux/
│  ├─ basic_commands/
│  ├─ filesystem/
│  ├─ permissions/
│  ├─ users_groups/
│  ├─ processes/
│  ├─ package_management/
│  ├─ networking/
│  ├─ shell_scripting/
│  └─ _shared/
│
├─ git/
│  ├─ basics/
│  ├─ branching/
│  ├─ merge_rebase/
│  ├─ remote/
│  └─ workflow/
│
├─ docker/
├─ kubernetes/
└─ aws/
```

## Rules

- Separate folders by `app_id`.
- Separate subfolders by `category_id`.
- Put official documents, Markdown files, PDFs, URL lists, and notes into the matching category folder.
- IR Creator must always read `studyapp/input/source_documents/{app_id}/{category}/`.
- Pipeline Runner must use the same path.
- `source_document_path` must record this path.
- Cross-category materials go in `studyapp/input/source_documents/{app_id}/_shared/`.
- Do not place unknown materials directly under `studyapp/input/source_documents/`.

## Naming Rule

- Use `category_id` for folder names such as `basic_commands` or `merge_rebase`.
- Keep display labels such as `Linux Basics` or `Users & Groups` in metadata, not in folder names.

## Linux Mapping

- `basic_commands` -> `Linux Basics`
- `filesystem` -> `Filesystem`
- `permissions` -> `Permissions`
- `users_groups` -> `Users & Groups`
- `processes` -> `Processes`
- `package_management` -> `Package Management`
- `networking` -> `Networking`
- `shell_scripting` -> `Shell Scripting`
