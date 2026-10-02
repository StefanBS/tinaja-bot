# Tinaja Bot

A Discord bot for the TINAJA Ingeniería community server: it answers member commands and reports how many people are in, and active on, the server.

## Language

**Server**:
A Discord guild the bot has joined; in practice the TINAJA Ingeniería server.
_Avoid_: Guild (except when talking about the Discord library), channel

**Member**:
A person's Discord account that belongs to a Server. Bot accounts are not Members.
_Avoid_: User

**Online member**:
A Member whose presence is anything other than offline — online, idle and do-not-disturb all count.
_Avoid_: Active user

**Server Census**:
The current count of Members and Online members in each Server, published for monitoring.
_Avoid_: Stats, metrics (when meaning the counts themselves)

**Feature**:
One self-contained capability of the bot — a Command or a background behaviour such as the Server Census.
_Avoid_: Plugin, module (when meaning a capability rather than code)

**Command**:
A `!`-prefixed message a Member sends to ask the bot for something, e.g. `!exercism <profile>`.
_Avoid_: Slash command (the bot doesn't use them)

**Exercism profile**:
A public profile page on exercism.org that a Member shares with `!exercism`.
