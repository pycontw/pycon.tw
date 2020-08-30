## Live broadcast settings
We have three broadcast channels, `R0`, `R1`, `R2`, just put the youtube video id into the following keys in the registry:

* `pycontw-2020.live.r0`
* `pycontw-2020.live.r1`
* `pycontw-2020.live.r2`

To do so, navigate to `/admin/registry/entry/` and create or update the key.

If the registry key is disabled or is an empty value, it will show "This broadcast is not ready yet."
The youtube video id is the `v` query parameter in the URL of a youtube video, something that looks like `Z_K9Bwgjiuc`.

### Test

In order to test it out, you will need to manual add a test attendee token.
The token needs to be a 32 byte hex string (`[0-9a-f]{32}`).

Go to `/admin/ext2020/attendee/` and add an entry.
Put `1234567890abcdef1234567890abcdef` in the token field for instance,
and make sure to make `verified` field `True`.

After creating the attendee entry, you can see the live braodcast page at `/ext/live?token=1234567890abcdef1234567890abcdef`.


## Attendee Token
We can import valid tokens by using the import / export tool in admin.
Go to `/admin/ext2020/attendee/` and click the import button on the top-right corner.

Use whatever format you like, the imported format should be a table that includes a header row and rows that contain the token.
Something like the following:

| token                            |
|:-------------------------------- |
| 1234567890abcdef1234567890abcde0 |
| 1234567890abcdef1234567890abcde2 |
| 1234567890abcdef1234567890abcde4 |
| 1234567890abcdef1234567890abcde6 |
