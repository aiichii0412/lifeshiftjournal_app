// 共通の小さな道具
(function () {
  var JST = 9 * 3600000; // 日付の数え方は日本時間の日付の境目で数える

  function jstDay(ms) { return Math.floor((ms + JST) / 86400000); }

  function load(key, fallback) {
    try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }
    catch (e) { return fallback; }
  }
  function save(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  // スタート日(はじめて開いた日)。あとで LINE 登録日などに置き換えられる。
  function startDay() {
    var s = load("lsj_start", null);
    if (!s) { s = Date.now(); save("lsj_start", s); }
    return s;
  }
  function todayNo() {
    var n = jstDay(Date.now()) - jstDay(startDay()) + 1;
    return Math.max(1, Math.min(28, n));
  }
  function doneSet() { return load("lsj_done", {}); }
  function setDone(n, on) {
    var d = doneSet(); if (on) d[n] = 1; else delete d[n]; save("lsj_done", d);
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  window.LSJ = { todayNo: todayNo, doneSet: doneSet, setDone: setDone, esc: esc };
})();
