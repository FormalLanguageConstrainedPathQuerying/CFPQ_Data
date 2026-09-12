document.addEventListener("DOMContentLoaded", function () {
  var captionToAnchor = {
    "C alias analysis": "graphs-c-alias-analysis",
    "RDF": "graphs-rdf",
    "Java points-to graphs": "graphs-java-points-to",
    "Field-Sensitive Alias": "graphs-field-sensitive-alias",
    "Context-Sensitive Data-Flow": "graphs-context-sensitive-data-flow",
    "Data Provenance": "graphs-data-provenance",
    "Name Resolution": "graphs-name-resolution",
    "Biological graphs from UniProt": "graphs-biological-uniprot",
  };

  var sidebar = document.querySelector(".bd-sidebar-primary");
  if (!sidebar) return;

  var onIndex = /\/graphs\/index\.html$/.test(window.location.pathname);
  var prefix = onIndex ? "#" : "../index.html#";

  sidebar.querySelectorAll(".caption-text").forEach(function (span) {
    var text = span.textContent.trim();
    var anchor = captionToAnchor[text];
    if (anchor) {
      var a = document.createElement("a");
      a.href = prefix + anchor;
      a.className = "reference internal";
      span.textContent = "";
      span.appendChild(a);
      a.textContent = text;
    }
  });
});
