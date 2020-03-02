function slideMember(el, normalOv, hoverOv, hoverWidth) {
  const altImg = null//hoverOv.querySelector("img")
  // Load alternative image
  if (altImg && altImg.dataset.loaded === "false") {
    altImg.srcset = altImg.dataset.srcset
    altImg.dataset.loaded = "true"
  }
  normalOv.style.width = el.clientWidth - hoverWidth + "px"
  hoverOv.style.width = hoverWidth + "px"
  hoverOv.classList.add("hover")
}

function resetMember(el, normalOv, hoverOv) {
  normalOv.style.width = "100%"
  hoverOv.style.width = 0
  hoverOv.classList.remove("hover")
}

const members = document.getElementsByClassName("member")
for (let i = 0; i < members.length; ++i) {
  const el = members[i]
  const overlays = el.getElementsByTagName("div")
  const normalOv = overlays[0], hoverOv = overlays[1]
  el.addEventListener("mousemove", evt => {
    const offset = window.scrollX + el.getBoundingClientRect().left
    const hoverWidth = Math.min(el.clientWidth, evt.clientX - offset)
    slideMember(el, normalOv, hoverOv, hoverWidth)
  })
  el.addEventListener("touchmove", evt => {
    if (evt.targetTouches.length) {
      const touchX = evt.targetTouches[0].clientX
      const offset = window.scrollX + el.getBoundingClientRect().left
      const hoverWidth = Math.min(el.clientWidth, touchX - offset)
      slideMember(el, normalOv, hoverOv, hoverWidth)
    }
  })
  el.addEventListener("mouseleave", () => {
    resetMember(el, normalOv, hoverOv)
  })
  el.addEventListener("touchend", () => {
    resetMember(el, normalOv, hoverOv)
  })
}
