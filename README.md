## tl;dr
Displays a list of your last ~8 months of Gemini crypto transfers on the command line.
Also displays your current total trading portfolio.

## About
I wanted a quick way of retrieving my latest transfers from the command line, without fiddling with
Gemini's web site or manual authentication.  This does the job, and is based on https://docs.gemini.com/rest-api/#transfers

<img width="1001" alt="geminixferscreenshot" src="https://user-images.githubusercontent.com/71786368/233816054-c308c3fc-ddde-4bfc-86be-183e252f183b.png">

## Getting Started

1. ```git clone https://github.com/ulysseskan/geminitransfers.git```
2. ```cd geminitransfers```
3. Within geminitransfers.py, edit `GEMINI_API_KEY`, `GEMINI_API_SECRET`, which you can obtain from
   https://exchange.gemini.com/settings/api The key needs read-only auditor permissions and time based nonces.
4. ```python3 geminitransfers.py```

### Prerequisites

You need a copy of Python 3.  I only tested with Python 3.10.  One way to install Python 3 is:

1. Install [Brew](https://brew.sh).
2. ```brew install python3```
3. Ensure Brew's executable bin directory is in your PATH variable, for example:<br>
```echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile```
4. Rename `config.py.sample` to `config.py` and put your API key and secret in that file
5. Run `python3 ./geminitransfers.py

## Potential improvements

- [ ] SSL certificate verification could be enabled by setting verify=True in the requests.post()
method, and the hashlib module could be used to encode the API secret properly.
- [ ] Don't use time-based nonces.

## Limitations

The transfers API request path has an undocumented limitation: it can only retrieve the last 8 or so
months of data.

## License

Distributed under the MIT License. See `LICENSE` for more information.
