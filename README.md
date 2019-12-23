# Mailer

![](https://github.com/daleal/mailer/workflows/build/badge.svg)

This module is a generic mailer API created only to serve as a microservice.

## Usage

```bash
cp .env.example .env  # change env variables

docker-compose build
docker-compose up     # The API can be found at port 5000
```

## Testing

To test the mailer, a sample script has been provided. To execute it, just run

```bash
python3 ghost_client.py [COMMAND] [*ARGS]
```

Where `[COMMAND]` is the name of the desired command and `[*ARGS]` corresponds to the arguments of the desired command separated by spaces. If a command has no arguments, `[*ARGS]` can be ignored. To see a list of every possible command, execute:

```bash
python3 ghost_client.py
```

Keep in mind that some API methods will require a `KEY`, so remember to have the same `KEY` environmental variable in the API server and in the script machine. The script automatically loads variables from a `.env` file, so putting the `KEY` in a `.env` file should be enough.
