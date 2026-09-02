# Tasks

- [ ] Task 1: analyze existing tooling.
- [ ] Task 2: Create tool to automate uploading to yandex s3 that we use. It must upload local file. Credantials must be provided by user from cli. **[USER GUIDANCE]**: "ru-central1"
- [ ] Task 3: Autoamte migration from google drive (we use it for some graps and grammars and want to move all to yandex) to yandex s3. Do not download all items locally. Just handle items one-by-one: donload from gdrive, uplad to yandex (use created tool), remove local copy of downloaded item. **[USER GUIDANCE]**: "Name is an unique identifier. If names are equal, graphs are the same. It must not be stored twice. You can recheck it by comparing current urls for google drive." / "Only 59 .tar.gz" / "Part of migration. Be sure that you saved mapping between graph name and new url."
