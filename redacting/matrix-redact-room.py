#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import asyncio
import json
from getpass import getpass
from time import time

from nio import AsyncClient
import nio.api


class Matrix:
    def __init__(self, args):
        self.client = AsyncClient(
            f"https://{args.homeserver}", f"@{args.user}:{args.homeserver}",
            store_path='.'
        )
        self.args = args

    def restore_login(self, saved):
        self.client.restore_login(
            saved['user_id'],
            saved['device_id'],
            saved['access_token'],
        )

    def get_login_save(self):
        return {
            'user_id': self.client.user_id,
            'device_id': self.client.device_id,
            'access_token': self.client.access_token,
        }

    async def login(self, password):
        await self.client.login(password, device_name=self.args.device_name)

    async def messages_stream(self, room_id, prev=''):
        prev_prev = None
        while prev_prev != prev:
            if prev:
                print(f"[+] page is now {prev}")

            resp = await self.client.room_messages(room_id, prev, limit=100)
            if not prev:
                print(f"[+] initial page is {resp.start}")

            prev_prev = prev
            prev = resp.end

            for msg in resp.chunk:
                yield msg

    async def list_rooms(self):
        resp = await self.client.joined_rooms()
        return resp.rooms

    async def clean_room(self, room_id, prev="", sender_filter=None):
        to_redact = (
            nio.events.room_events.MegolmEvent,  # event that was not decrypted
            nio.events.room_events.RoomMessageText,
            nio.events.room_events.RoomMessageImage,  # unencrypted image
            nio.events.room_events.RoomMessageUnknown,  # typically confetti message
            nio.events.room_events.RoomMessageEmote,  # "/me"?
            nio.events.room_events.RoomEncryptedImage,
            nio.events.room_events.RoomEncryptedVideo,
            nio.events.room_events.RoomEncryptedFile,
            nio.events.room_events.RoomNameEvent,
            nio.events.room_events.RoomTopicEvent,
            nio.events.room_events.RoomAvatarEvent,
            nio.events.room_events.RoomMemberEvent,  # typically nick change
        )

        async for event in self.messages_stream(room_id, prev):
            should_redact = False

            if isinstance(event, to_redact):
                should_redact = True

            elif isinstance(event, nio.events.room_events.RedactedEvent):
                print(f"[-] already redacted {event.event_id!r}")

            elif isinstance(event, nio.events.room_events.RedactionEvent):
                print(f"[-] skip redaction event {event.event_id!r}")

            elif isinstance(event, nio.events.room_events.RoomCreateEvent):
                print(f"[+] reached the end at {event.event_id!r}? {event.source}")
                break

            elif isinstance(event, nio.events.room_events.UnknownEvent):
                if event.source.get("type") == "m.reaction":
                    # reaction to message has no dedicated event class
                    should_redact = True
                else:
                    print(f"[-] skip unknown {type(event)} {event.event_id!r} {event.source}")

            else:
                print(f"[-] skip unhandled {type(event)} {event.event_id!r} {event.source}")

            if should_redact:
                if sender_filter and event.sender != sender_filter:
                    print(f"[-] skip other sender {type(event)} {event.sender} {event.event_id!r}")
                    continue

                print(f"[+] redacting {type(event)} {event.sender} {event.event_id!r}")
                print(f"[.] event content: {event}")
                t = time()
                await self.client.room_redact(room_id, event.event_id)
                print(f"[.] redacting took {time() - t:.2f} s")
                # server often performs throttling
                # so let's do it preventively to be more stealthy and avoid 429
                # the default synapse value is 1 redaction / 5 seconds
                await asyncio.sleep(5)


async def main():
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('--homeserver')
    parser.add_argument('--user')
    parser.add_argument('--device-name', default='matrix-bot')
    parser.add_argument('--save-login')
    subs = parser.add_subparsers(dest='cmd')

    subs.add_parser('list-rooms')

    sub = subs.add_parser('clean-room')
    sub.add_argument('room_id')
    sub.add_argument('--since', default='')
    # TODO: allow this arg to be present multiple times
    sub.add_argument('--only-from-sender', metavar='USER')

    sub = subs.add_parser('import-keys')
    sub.add_argument('key_file')

    args = parser.parse_args()

    mtx = Matrix(args)
    # login
    if args.save_login:
        try:
            with open(args.save_login) as fd:
                saved = json.load(fd)
        except FileNotFoundError:
            await mtx.login(getpass('Server password: '))
            with open(args.save_login, 'w') as fd:
                json.dump(mtx.get_login_save(), fd)
        else:
            mtx.restore_login(saved)
    else:
        await mtx.login(getpass('Server password: '))

    # commands
    if args.cmd == 'list-rooms':
        rooms = await mtx.list_rooms()
        for room in rooms:
            print(room)
    elif args.cmd == "clean-room":
        await mtx.clean_room(args.room_id, args.since, args.only_from_sender)
    elif args.cmd == 'import-keys':
        print("[.] warning: this operation can take a lot of time")
        # TODO: display progress
        await mtx.client.import_keys(args.key_file, getpass('Keyring passphrase: '))

    await mtx.client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
