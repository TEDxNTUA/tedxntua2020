// Checkerboard grid view generator
const tabs = document.querySelectorAll("#lineup .tab-pane")

function createSpacer() {
  let spacer = document.createElement("span")
  spacer.setAttribute("aria-hidden", "true")
  return spacer
}

/**
* Creates checkerboard grid view.
*
* @param {Element} tabEl The tab element that contains the original
*   elements and that will store the generated checkerboard grid view.
* @param {number[][]} layout Describes the grid layout as a 2d array with
*   numbered slots. Slots with negative values produce empty cells.
*
*   For example this layout:
*   [[0, -1, 2, -1, 4],
*    [-1, 1, -1, 3, -1]]
*   will arrange the items in a W shape:
*     x x x
*      x x
*/
function createCheckerboardView(tabEl, layout) {
  if (!layout.length) return

  const simpleView = tabEl.children[0],
  checkerboardView = tabEl.children[1]

  checkerboardView.innerHTML = ""

  const rows = layout.length, cols = layout[0].length
  checkerboardView.style.gridTemplateColumns = "repeat(" + cols + ", 1fr)"

  // Build cube rows
  for (let i = 0; i < rows; ++i) {
    for (let j = 0; j < cols; ++j) {
      let elIdx = layout[i][j]
      if (elIdx >= 0 && elIdx < simpleView.children.length) {
        let clone = simpleView.children[elIdx].cloneNode(true)
        // Attach pjax listeners
        if (window.pjax) {
          window.pjax.attachLink(clone)
        }
        checkerboardView.appendChild(clone)
      } else {
        checkerboardView.appendChild(createSpacer())
      }
    }
  }
}

let layout = [
  [6, -1, 2, -1, 3],
  [-1, 5, -1, 0, -1],
  [-1, -1, 4, -1, 1],
  [-1, 9, -1, 7, -1],
  [-1, -1, 10, -1, 8],
  [-1, -1, -1, 11, -1],
]

for (const tabEl of tabs) {
  createCheckerboardView(tabEl, layout)
}
