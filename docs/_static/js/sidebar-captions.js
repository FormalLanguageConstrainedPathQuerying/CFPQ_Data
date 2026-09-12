document.addEventListener("DOMContentLoaded", function () {
  var captionToAnchor = {
    "C alias analysis": "graphs_c_alias_analysis",
    "RDF": "graphs_rdf",
    "Java points-to graphs": "graphs_java_points_to",
    "Field-Sensitive Alias": "graphs_field_sensitive_alias",
    "Context-Sensitive Data-Flow": "graphs_context_sensitive_data_flow",
    "Data Provenance": "graphs_data_provenance",
    "Name Resolution": "graphs_name_resolution",
    "Biological graphs from UniProt": "graphs_biological_uniprot",
  };

  var sidebar = document.querySelector(".bd-sidebar-primary");
  if (!sidebar) return;

  sidebar.querySelectorAll(".caption-text").forEach(function (span) {
    var text = span.textContent.trim();
    var anchor = captionToAnchor[text];
    if (anchor) {
      var a = document.createElement("a");
      a.href = "#" + anchor;
      a.className = "reference internal";
      span.textContent = "";
      span.appendChild(a);
      a.textContent = text;
    }
  });
});
