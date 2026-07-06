/**
 * IntelliForge embeddable chat widget loader.
 *
 * Usage on upskill.intelliforge.tech (or any site):
 *
 *   <script
 *     src="https://YOUR-WIDGET-HOST/embed.js"
 *     data-position="bottom-right"
 *     defer
 *   ></script>
 *
 * Optional data attributes:
 *   data-position  — "bottom-right" (default) or "bottom-left"
 *   data-base      — override widget origin (defaults to script origin)
 */
(function () {
  "use strict";

  var script = document.currentScript;
  if (!script) return;

  var base = script.getAttribute("data-base");
  if (!base) {
    var src = script.src || "";
    base = src.replace(/\/embed\.js(?:\?.*)?$/, "");
  }
  if (!base) return;

  var position = script.getAttribute("data-position") || "bottom-right";
  var isLeft = position === "bottom-left";

  var styles = document.createElement("style");
  styles.textContent =
    "#if-chat-launcher{" +
    "position:fixed;bottom:24px;" +
    (isLeft ? "left:24px;" : "right:24px;") +
    "z-index:2147483646;width:56px;height:56px;border:none;border-radius:9999px;" +
    "background:#22c55e;color:#0f172a;cursor:pointer;" +
    "box-shadow:0 8px 32px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;" +
    "transition:transform .15s ease,box-shadow .15s ease;font-family:system-ui,sans-serif;" +
    "}" +
    "#if-chat-launcher:hover{transform:scale(1.05);box-shadow:0 12px 40px rgba(0,0,0,.4);}" +
    "#if-chat-launcher svg{width:26px;height:26px;}" +
    "#if-chat-panel{" +
    "position:fixed;bottom:92px;" +
    (isLeft ? "left:24px;" : "right:24px;") +
    "z-index:2147483645;width:min(400px,calc(100vw - 32px));" +
    "height:min(620px,calc(100dvh - 120px));display:none;" +
    "border-radius:14px;overflow:hidden;" +
    "box-shadow:0 20px 60px rgba(0,0,0,.45);border:1px solid rgba(248,250,252,.12);" +
    "background:#0f172a;" +
    "}" +
    "#if-chat-panel[data-open='true']{display:block;}" +
    "#if-chat-panel iframe{width:100%;height:100%;border:none;display:block;}" +
    "@media(max-width:480px){" +
    "#if-chat-panel{bottom:0;left:0;right:0;width:100%;height:min(85dvh,100dvh);border-radius:14px 14px 0 0;}" +
    "#if-chat-launcher{bottom:16px;" + (isLeft ? "left:16px;" : "right:16px;") + "}" +
    "}";
  document.head.appendChild(styles);

  var panel = document.createElement("div");
  panel.id = "if-chat-panel";
  panel.setAttribute("data-open", "false");
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "IntelliForge Bootcamp Assistant");

  var iframe = document.createElement("iframe");
  iframe.src = base + "/embed";
  iframe.title = "IntelliForge Bootcamp Assistant";
  iframe.allow = "clipboard-write";
  panel.appendChild(iframe);

  var launcher = document.createElement("button");
  launcher.id = "if-chat-launcher";
  launcher.type = "button";
  launcher.setAttribute("aria-label", "Open bootcamp assistant");
  launcher.setAttribute("aria-expanded", "false");
  launcher.setAttribute("aria-controls", "if-chat-panel");
  launcher.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
    '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v7A2.5 2.5 0 0 1 17.5 15H12l-4.2 3.15a.75.75 0 0 1-1.2-.6V15H6.5A2.5 2.5 0 0 1 4 12.5v-7Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' +
    "</svg>";

  var open = false;

  function setOpen(next) {
    open = next;
    panel.setAttribute("data-open", open ? "true" : "false");
    launcher.setAttribute("aria-expanded", open ? "true" : "false");
    launcher.setAttribute(
      "aria-label",
      open ? "Close bootcamp assistant" : "Open bootcamp assistant",
    );
  }

  launcher.addEventListener("click", function () {
    setOpen(!open);
  });

  window.addEventListener("message", function (event) {
    if (event.data === "intelliforge-chat-close") {
      setOpen(false);
    }
  });

  document.body.appendChild(panel);
  document.body.appendChild(launcher);
})();
