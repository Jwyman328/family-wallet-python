# TODOs
- commit latest refactor changes
- Fix naming of GlobalDataStoreContainer.py and ServiceContainer.py file names, make them snake case names
- on the FE fix tailwind so it works
    - https://blog.saeloun.com/2023/02/24/integrate-tailwind-css-with-electron/
- write tests for POST /wallet endpoint that sets the global descriptor
    - also write related tests for the wallet sevice that sets the descriptor,
    - also probably have to fix all test I broke from it.
- add addility to set the electrum server and the netwrok type in the login screen as well in the frontend and add endpoints for them as well.
- remove all the fe github build pipeline stuff that I don't want that I got from cloning a bioler late project

- get the flask app to be an executable file
    - https://www.youtube.com/watch?v=ty-n33mHwC4&ab_channel=Montreal-Python
    - use pyinstaller https://pyinstaller.org/en/stable/

- add a "login" screen where you can not pass until you have entered your pubkey.
    - then I can lockdown the other endpoints to require that the user is "logged in" and the pubkey is in the server?
- add better logging everywhere
- create a fee market in the ngiri mempool somehow
- add a pyproject.toml to manage ruff line length stuff so that ruff formatting is inline with the lsp?
- do async await getting the current memepool fee rates?

