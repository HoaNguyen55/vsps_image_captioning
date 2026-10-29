-- drop manual "6.8 " / "1. " prefixes from headings; acmart numbers sections itself
function Header(h)
  local s = pandoc.utils.stringify(h)
  if h.content[1] and h.content[1].t == "Str" and h.content[1].text:match("^%d+[%.%d]*%.?$") then
    h.content:remove(1); if h.content[1] and h.content[1].t == "Space" then h.content:remove(1) end
  end
  return h
end
-- images: use the PDF rendering of each SVG
function Image(i) i.src = i.src:gsub("%.svg$", ".pdf"); return i end
