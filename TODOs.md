# TODOs
- remove ngiri docker containers i am not relaly using
- pydantic for all response values.
    - this way we are validating our expected responses, and if they are not what we saying what they should be then we will throw an error. This should be cause and have a way to handle this response.  could use a context or a regular try catch
- pydantic for the post requests.
- style the frontend.
- remove all the fe github build pipeline stuff that I don't want that I got from cloning a bioler late project

- get the flask app to be an executable file
    - https://www.youtube.com/watch?v=ty-n33mHwC4&ab_channel=Montreal-Python
    - use pyinstaller https://pyinstaller.org/en/stable/

- create a fee market in the ngiri mempool somehow
- add a pyproject.toml to manage ruff line length stuff so that ruff formatting is inline with the lsp?
- do async await getting the current memepool fee rates?
    - I could do a web socket connection and use a background task for it?
    - maybe this is more of a nice to have after the main project is done.

