"use strict";
/* HomeWatchdog - keeps Index as "home".
 *
 * This TV exposes a reliable per-app `visible` flag at http://127.0.0.1:8001.
 * Strategy each tick:
 *   - If our launcher, or any streaming/AirPlay app, is `visible:true` -> leave alone.
 *   - Else if a non-resident app is in the running list -> leave alone.
 *   - Else (nothing on screen = Samsung home) -> relaunch Index after a short debounce.
 *
 * Honest limits: ~2-3s Samsung flash on each exit; an HDMI/console input switched via
 * Samsung's own Source menu is invisible to us, so it may relaunch over a game; cannot
 * auto-start at power-on. Switching inputs *through* Index (tvwindow) avoids the game case.
 */
module.exports.onStart = function () {
  var MY = "MaxHome001.Home";
  var POLL = 1000, CONFIRM = 2;
  var gone = 0, cooldown = 0;
  var http = require("http");

  // Queryable via :8001 by id (our app by tizen id; store apps by numeric id) + AirPlay web app.
  var REST = [
    "MaxHome001.Home",        // our launcher
    "3201907018807",          // Netflix
    "111299001912",           // YouTube
    "3201910019365",          // Prime Video
    "3201601007625",          // Hulu
    "3201901017640",          // Disney+
    "3202301029760",          // HBO Max / Max
    "3201807016597",          // Apple TV
    "3202006020991",          // Peacock
    "3201710014981",          // Paramount+
    "NRi6kdBYJ0.AirPlayWebApp" // AirPlay receiver (tested on-device)
  ];
  // Non-resident apps with no known numeric id -> detected by presence in the running list.
  var CTX = ["Jz7aUrV2Q4", "OGLLvqej7u", "XtU8fQk2gN", "zigzSWa1hy", "ZmmGjO6VKO",
             "PvWgqxV3Xa", "GHI3a0zMSx"];

  function visible(id, cb) {
    var req = http.get({ host: "127.0.0.1", port: 8001, path: "/api/v2/applications/" + id, timeout: 900 },
      function (res) {
        var d = ""; res.on("data", function (c) { d += c; });
        res.on("end", function () { var v = false; try { v = JSON.parse(d).visible === true; } catch (e) {} cb(v); });
      });
    req.on("error", function () { cb(false); });
    req.on("timeout", function () { try { req.destroy(); } catch (e) {} cb(false); });
  }
  function anyVisible(cb) {
    var pend = REST.length, found = false;
    REST.forEach(function (id) { visible(id, function (v) { if (v) found = true; if (--pend === 0) cb(found); }); });
  }
  function anyCtx(cb) {
    try {
      tizen.application.getAppsContext(function (ctx) {
        for (var i = 0; i < ctx.length; i++) {
          var id = ""; try { id = ctx[i].appId || ""; } catch (e) {}
          for (var j = 0; j < CTX.length; j++) { if (id.indexOf(CTX[j]) === 0) return cb(true); }
        }
        cb(false);
      }, function () { cb(false); });
    } catch (e) { cb(false); }
  }
  function relaunch() {
    // The Tizen launch API will not foreground our app on this set; the local REST
    // launch endpoint does, so relaunch with a POST to :8001.
    try { tizen.application.launch(MY, function () {}, function () {}); }
    catch (e) {}
  }
  setInterval(function () {
    if (cooldown > 0) { cooldown--; return; }   // let a just-launched Index settle
    anyVisible(function (vis) {
      if (vis) { gone = 0; return; }
      anyCtx(function (ctxBusy) {
        if (ctxBusy) { gone = 0; return; }
        gone++;
        if (gone >= CONFIRM) { gone = 0; cooldown = 6; relaunch(); }
      });
    });
  }, POLL);
};
module.exports.onStop = function () {};
