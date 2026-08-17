from pathlib import Path

PAGE = Path("app/page.tsx")
CSS = Path("app/globals.css")

page = PAGE.read_text(encoding="utf-8")

capsule_plain = '<button className="menu-feature" onClick={()=>go("collections")}>КАПСУЛЫ И КОЛЛЕКЦИИ</button>'
capsule_highlight = '<button className="menu-feature menu-highlight-action" onClick={()=>go("collections")}><span>КАПСУЛЫ И КОЛЛЕКЦИИ</span><Icon name="arrow"/></button>'
if capsule_plain in page:
    page = page.replace(capsule_plain, capsule_highlight, 1)

ready_variants = [
    '<button onClick={()=>go("collections")}>ГОТОВЫЕ РЕШЕНИЯ</button>',
    '<button onClick={()=>go("collections")}>EDITORIAL</button>',
]
ready_highlight = '<button className="menu-highlight-action menu-ready-solutions" onClick={()=>go("collections")}><span>ГОТОВЫЕ РЕШЕНИЯ</span><Icon name="arrow"/></button>'
if 'menu-ready-solutions' not in page:
    for variant in ready_variants:
        if variant in page:
            page = page.replace(variant, ready_highlight, 1)
            break

PAGE.write_text(page, encoding="utf-8")

css = CSS.read_text(encoding="utf-8")
marker = "/* MENU_HIGHLIGHT_SOLUTIONS_V1 */"
if marker not in css:
    css += r'''

/* MENU_HIGHLIGHT_SOLUTIONS_V1 */
.zara-menu .menu-highlight-action {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin: 4px 0;
  padding: 15px 16px 15px 18px !important;
  background: var(--cream, #f3f0ea);
  border: 1px solid var(--line, #deded9) !important;
  border-left: 2px solid var(--accent, #aa7650) !important;
  font-weight: 600;
  letter-spacing: .025em;
  text-align: left;
}
.zara-menu .menu-highlight-action svg {
  width: 18px;
  height: 18px;
  flex: 0 0 18px;
}
.zara-menu .menu-highlight-action:hover,
.zara-menu .menu-highlight-action:focus-visible {
  background: #ebe6dd;
}
.zara-menu .menu-ready-solutions {
  margin-top: 10px;
}
@media (max-width: 700px) {
  .zara-menu .menu-highlight-action {
    padding: 14px 14px 14px 16px !important;
  }
}
'''
    CSS.write_text(css, encoding="utf-8")

print("Highlighted Capsules & Collections and Ready Solutions in menu")
