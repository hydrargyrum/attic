# matrix redact room

## typical usage

```
matrix-redact-room.py --homeserver https://matrix.example.com --user my-login --save-login clean-room '!blablabla:matrix.example.com'
```

## if you need to interrupt then resume

look for the last log message containing

```
[+] initial page is t220-5183446_0_0_0_0_0_0_0_0
```

or

```
[+] page is now t220-5183446_0_0_0_0_0_0_0_0
```

The last token may vary

Then copy the last token and use it in the command like this at that checkpoint:

```
matrix-redact-room.py [OTHER ARGS AS PREVIOUSLY] clean-room '!blablabla:matrix.example.com' --since t220-5183446_0_0_0_0_0_0_0_0
```

## redact messages from a user only

```
matrix-redact-room.py [OTHER ARGS AS PREVIOUSLY] clean-room '!blablabla:matrix.example.com' --only-from-sender @somebody:matrix.example.com
```

# gitlab delete comments

## typical usage

Create an API token in account preferences

Run

```
gitlab-delete-your-comments.py https://gitlab.example.com
```

Feed it the token when asked

## archived projects

Comments from archived projects can't be deleted because they're read-only
