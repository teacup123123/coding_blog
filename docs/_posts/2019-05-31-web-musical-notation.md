---
layout: post
title: "Efficiently blog about music, generating .MID and sheet"
author: Tikai Chang
tags: ["music","js","midi"]
comments: true
status: "done"
---

#### A bit of motivation and a prototype-draft of a music-blog infrastructure

Browsing the web, something occured to me.
I am about to start a blog about making music, and so one key ingredient is rendering musical notation on the fly.
The slow way will be to open up the music-editing software (MuseScore), and then somehow capture or export the images for use in web.

I think the main question will be, what will be more natural for me as a blogger, will it be bloggability (ascii-readability/ascii-writability) or direct visualization or even hearability of the music? I don't have an answer to this question.

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
- have a **compiler** that compiles my snippets into midi offline before uploading new content: I write in Vexflow, and then use MidiWriterJS to write to a `.mid` file, which I upload, playable locally by a blog reader to be implemented.
- have an **external site** that does the translation of snippet into `.mid`. Idem. Advantages of this is that the site is always online and I only need to edit the source files of snippets to see the change. The resources will be fetched dynamically.

I think I will explore the second option, so basically I will need a way to host
a site like the demo page of [the first project](#testmidi).
The static sites encodes the music source into an url string. The reader upon loading the page will fetch from this url a dynamically generated midi file. Might increase inter-site traffic but it saves me from compiling/exporting music... Also while I'm at it maybe I'll do the same thing with switching from mathjax to Katex?

Eventually, if I need to copy paste snippets from MuseScore I will have to devise some kind of translation software, but that is just heavy to implement...

So I'll keep updating this post as the system slowly goes online.

#### Kick off by setting up a Heroku node.js server

So first I sign in to Heroku and link to my github repo.
Then I follow line-wise the [Tutorial](https://devcenter.heroku.com/articles/getting-started-with-nodejs?singlepage=true):
1. download, login to heroku CLI
2. install node.js on my local machine with `sudo apt-get install nodejs`
3. clone the sample heroku node.js minimalistic app.
4. `heroku local web` to see the app running locally
5. `heroku create` if never done before.
6. rinse and repeat coding and deployment `git push heroku master`

#### Messed around and changed direction upon discovery of OSMD

I messed around and found [this demo](https://opensheetmusicdisplay.github.io/demo/). It claims to be able to render musicxml files. I fiddled around and managed to integrate it into this blog. Here is a first *imperfect* [example blog post]({{ site.baseurl }}{% post_url 2019-05-31-Zettai-Zetsumei %}).

So if you want to dwelve into how it was done. basically I digged into their [wiki-page](https://github.com/opensheetmusicdisplay/opensheetmusicdisplay/wiki)

So the coding style that I settled upon is the following liquid syntax (note the fictious introduction of two small spaces there between `{` , resp. `}`, and `%` otherwise liquid *will* indeed include the contents...)

```
{ % include stubmusic.html
  src = "190531-zz/Zettai_Zetsumei_by_Coe_shu_Nie.xml"
  zoom = 0.2
  % };
```
So I will keep all the music-xml files in a visible-data folder, and the included html snippet will be in charge of formatting the source file url correctly.
Here, `190531-zz` is shorthanded folder containing all resources for that `2019-05-31-Zettai-Zetsumei` post.

Finally a small javascript that is injected at the end of the page content everytime the `music` tag is detected by the liquid syntax:

```javascript
var list = document.getElementsByClassName("stubmusic");

for (var i = 0; i < list.length; i++) {
  var container = list[i];
  var osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(container);
  var src = container.getAttribute('src');
  var zoom = container.getAttribute('zoom');
  osmd.load(src);
  osmd.zoom = parseFloat(zoom);//Doesn't work :(
  osmd.setOptions({
    drawTitle: false,
    drawCredits: false,
    drawComposer: false,
    // drawPartNames: false,
    // drawLyricist: false
  })
  osmd.render();
}
```

Still haven't figured out how to render in canvas mode (seems to be faster than svg on the demo site), nor have I figured out how to adjust the zoom, it seems a little big for my taste. Also the disabling of Part names and Lyricist names doesn't remove the space intented for them. So you have this awkward space standing out of nowhere.

Seems to be a lot of lever to play around with. But there's not enough documentation yet and the OSMD project is still very young. So I guess I'll live with it for the moment.

As for **Heroku**, I'll find use for it sooner or later. Whatever dynamical/ dynamically generated content I'll delegate it to them.

So I think a next step is to also make a small mid player alongside every MusicXML-export, and hopefully that will be covered in a future post.

Let's stop here for this post. I'll make a new one when the .MID play function is implemented.
