// Variables with `u` prefix are measured in cube units
const header = document.querySelector("#simple-view header")
const cubeView = document.getElementById("cube-view")
const CUBE_SIZE_EM = 4,
  CUBE_SIDE_INV_RATIO = 4,
  uCUBE_SIDE_RATIO = 1 / CUBE_SIDE_INV_RATIO
cubeView.style.setProperty('--cube-size', CUBE_SIZE_EM)
cubeView.style.setProperty('--cube-side-ratio', uCUBE_SIDE_RATIO)

function createSpacer(uWidth) {
  let spacer = document.createElement("span")
  spacer.setAttribute("aria-hidden", "true")
  spacer.style.width = uWidth * CUBE_SIZE_EM + "em"
  return spacer
}

/**
* Creates cube view.
*
* @param {number[][]} cubeLayout Describes the layout without perspective.
* It is given as a list of [number of cubes, offset from left] tuples.
*
* For example, this layout:
*   x x x x
*    x x x
*       x x
* corresponds to [[4, 0], [3, 1], [2, 4]].
* @param {number} [uGutter=1] Unit width between cubes.
*/
function createCubeView(cubeLayout, uGutter=1) {
  const members = document.querySelectorAll("#simple-view .member")
  /* Perspective offset is the number of side unit widths that each row is
   * moved to the right in order to align the cubes and show perspectivity.
   * It is *decreased* by one for each row, since we have a
   * rightside-perspective.
   *
   * Initialization:
   * For each row, we calculate leftness as the offset that it would have
   * if we started the first row with zero perspective offset.
   * We initialize perspective offset to the negative of the minimum
   * leftness so that the leftmost row ends up with zero total left offset.
   */
  const uLeftness = cubeLayout.map(([cubeNum, uOffset], index) => {
    return uOffset - uCUBE_SIDE_RATIO * index
  })
  let uPerspectiveOffset = -Math.min(...uLeftness)

  let mIdx = 0, rows = [], uMaxWidth = 0
  // Build cube rows
  cubeLayout.forEach(([uCubes, uRowOffset], rowIndex) => {
    let uOffset = uRowOffset + uPerspectiveOffset
    let rowEl = document.createElement("div")
    rowEl.classList.add("cube-row")
    // Create spacer
    rowEl.appendChild(createSpacer(uOffset))
    // Create member elements
    for (let mOff = 0; mOff < uCubes && mIdx + mOff < members.length; ++mOff) {
      if (uGutter > 0 && mOff > 0) {
        // Add gutter before this cube, unless it's the first one
        rowEl.appendChild(createSpacer(uGutter));
      }
      let child = members[mIdx + mOff].cloneNode(true)
      child.classList.add(`c${(mIdx + mOff) % 3 + 1}`)
      rowEl.appendChild(child)
    }

    // Update member index
    mIdx += uCubes
    rows.push(rowEl)
    // Calculate row unit width
    let uWidth = uOffset + uCubes + (uCubes - 1) * uGutter + uCUBE_SIDE_RATIO
    if (uWidth > uMaxWidth) {
      uMaxWidth = uWidth
    }
    // Update perspective offset for next row
    uPerspectiveOffset -= uCUBE_SIDE_RATIO
  })

  // Render cube view
  cubeView.innerHTML = ""
  // Make header
  let newHeader = header.cloneNode(true)
  // Set width to first spacer's width
  newHeader.style.width = rows[0].childNodes[0].style.width
  cubeView.appendChild(newHeader)
  // Render cube rows
  rows.forEach(row => cubeView.appendChild(row))
  cubeView.style.setProperty('--cubeview-unit-width', uMaxWidth)
}

let layout = [[4, 1], [5, 0], [4, 1], [5, 0], [4, 1], [4, 2], [3, 3]]
// TRIANGULAR
// layout = [[3, 3], [4, 2], [4, 1], [5, 0], [4, 1], [5, 0], [4, 1]]
// SMALLER
// layout = [[6, 2], [7, 1], [8, 0], [7, 1]]
createCubeView(layout)
