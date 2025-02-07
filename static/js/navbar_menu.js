$(document).ready(function () {
  function n() {
    var n = $("#main-nav").find("ul"),
      i = $("#main-nav").find(".indicator"),
      t = n.find("li").first().children().outerWidth();
    i.css("width", t + "px"),
      n.find("a").on("mouseover", function () {
        var n = $(this).outerWidth(),
          t = 0;
        $(this)
          .parent()
          .prevAll()
          .each(function () {
            t += parseInt($(this).find("a").outerWidth());
          }),
          i.css({
            width: n + "px",
            transform: "translate3d(" + t + "px, 0, 0)"
          });
      });
  }
  n();
});
