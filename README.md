# cat-wmill-workspace
A repo for automation of admin chores, using Windmill

https://www.windmill.dev/docs/advanced/local_development#local-development-recommended-setup


### How scripts show up in the filesystem

> Each script will be represented by a content file (.py, .ts, .go depending on the language) plus a metadata file (ending with .script.yaml). This file contains various metadata about the script, like a summary and description, but also the content of the lockfile and the schema of the script (i.e. the signature of its main method).

Source: [Local Development | Windmill](https://www.windmill.dev/docs/advanced/local_development)

### How to access resources like passwords and so on

1. Work locally as needed until you're comfortable with the code.
2. Define the credentials in windmill, at the [resources endpoint](https://app.windmill.dev/resources#). See the [docs for more about defining and using resources](https://www.windmill.dev/docs/core_concepts/resources_and_types).
2. Access them from a script with `wmill.getResource('u/user/foo')` for typescript, or `wmill.get_resource()` for python
3. Write script as needed, consuming the resource instead of using the local version.

