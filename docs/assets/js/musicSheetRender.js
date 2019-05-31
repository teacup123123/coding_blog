  var list = document.getElementsByClassName("sheetmusic");

  for (var i = 0; i < list.length; i++) {
    var container = list[i];
    var osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(container);
    var src = container.getAttribute('src');
    var zoom = container.getAttribute('zoom');
    osmd.load(src);
    osmd.zoom = float(zoom);
    osmd.render();
  }

  var list = document.getElementsByClassName("stubmusic");

  for (var i = 0; i < list.length; i++) {
    var container = list[i];
    var osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(container);
    var src = container.getAttribute('src');
    var zoom = container.getAttribute('zoom');
    osmd.load(src);
    osmd.zoom = parseFloat(zoom);
    osmd.setOptions({
      drawTitle: false,
      drawCredits: false,
      drawComposer: false,
      // drawPartNames: false,
      // drawLyricist: false
    })
    osmd.render();
  }
