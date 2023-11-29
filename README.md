# CredPoll
CredPoll is a utility tool for Responder that helps with keeping track of captured credentials with focus on versioned hashlist generation for password cracking. This tool is specially useful in large environments where there's an overwheming amount of hashes captured and multiple hashlists (with unique entries) need to be generated as they are obtained progressively.

## Actions
* list - this action simply returns a de-duped list of all accounts/identities (including domain info if applicable) for which credentials have been captured. In the case where a hashlist has been previously generated, this action also distinguishes between accounts captured since the last generation.
* extract - this action allows extracting credentials (either hashed or otherwise) for a specific account/identity that can be selected from the interactive prompt.
* hashlist - this action generates a unique hashlist by mantaining a cache of previously captured accounts and only including hashes for accounts captured since the last generation.
* reset - this action resets the cache state mantained by CredPoll.

## Usage
After cloning the repo, the tool can be run without any additional dependencies as long as it has read access to the responder logs directory (which can be manually specified if not at the default location).
```
usage: credpoll.py [-h] [--responder-logs-dir RESPONDER_LOGS_DIR] {list,extract,hashlist,reset}

Credential Polling for Responder

positional arguments:
  {list,extract,hashlist,reset}
                        action to perform

options:
  -h, --help            show this help message and exit
  --responder-logs-dir RESPONDER_LOGS_DIR
                        Responder logs directory to poll
```
