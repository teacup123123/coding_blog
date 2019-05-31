---
layout: post
title: "Efficiently blog about music, generating .MID and sheet"
author: Tikai Chang
tags: ["music","js","midi"]
comments: true
status: "working"
---

Browsing the web, something occured to me.
I am about to start a blog about making music, and so one key ingredient is rendering musical notation on the fly.
The slow way will be to open up the music-editing software (MuseScore), and then somehow capture or export the images for use in web.

I think the main question will be, what will be more natural for me as a blogger, will it be bloggability (ascii-readability/ascii-writability) or direct visualization of the music? I don't have an answer to this question.

Thinking about the first bloggability aspect, I did a little bit of googling and found that there's this tool called
[Vexflow](http://www.vexflow.com/) which does in-browser rendering of sheet music
based on a markdown-like syntax

Then I saw a whole bunch of people who thought about similar stuff:
- [Testing MIDI with Vexflow and MIDI.js](https://github.com/fyhao/testmidi)
<a name="testmidi"></a>
- [MidiWriterJS with VexFlow Integration](http://grimmdude.com/MidiWriterJS/)
- [MIDI.js audio playing javascript library](https://www.midijs.net/)

So the ideal thing is to be able to write up small code snippets that will
directly render into sheet music snippet on the site, and also generate playable music

If you take a peek at the source code of this site, or already have an
understanding of Jekyll, yous should know this site is static.
Ideally, to do things DRYly(don't repeat yourself), it's best to have
the music source as a standalone snippet file.
I have few options:
- have a **compiler** that compiles my snippets into midi offline before uploading new content: I write in Vexflow, and then use MidiWriterJS to write to a `.mid` file, which I upload, playable locally by blog reader.
- have an **external site** that does the translation of snippet into `.mid`. Idem. Advantages of this is that the site is always online and I only need to edit the source file of snippets to see the change. The resources will be fetched dynamically.

I think I will explore the second option, so basically I will need a way to host
a site like the demo page [the first project](#testmidi).
The static sites encodes the source into an url string. The reader upon loading the page will fetch from this url a dynamically generated midi file. Might increase inter-site traffic but it saves me from compiling an additional step! As long as it's free...XD
Also while I'm at it maybe I'll do the same thing with switching from mathjax to Katex?

Eventually, if I need to copy paste snippets from MuseScore I will

So I'll keep updating this post as the system slowly goes online.

### Implementation

To be continued
