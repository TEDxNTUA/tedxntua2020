// Section scroll handler
const observables = []
const obsIdToIdx = {}

// Add all sections to observables
const sxs = document.querySelectorAll('article.home-page .section-container > section')
sxs.forEach(sx => {
  observables.push({
    el: sx,
    overlays: sx.querySelectorAll('header, .nav-scrollable-tabs'),
  })
})
// Add footer to observables
observables.push({
  el: document.getElementById('footer'),
  overlays: [],
})

let activeIdx

function switchActive(newActiveIdx) {
  if (typeof activeIdx !== 'undefined') {
    // Hide current
    observables[activeIdx].overlays.forEach(overlay => {
      overlay.classList.remove('show')
    })
  }
  // Show new
  observables[newActiveIdx].overlays.forEach(overlay => {
    overlay.classList.add('show')
  })
  activeIdx = newActiveIdx
}

// Intersection observer that activates when element covers >50% of screen
// height.
// Adapted from: https://stackoverflow.com/q/57786082
const options = {
  threshold: Array(21).fill().map((_, x) => x / 20),
}
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const thisIdx = obsIdToIdx[entry.target.id]
    const h = entry.boundingClientRect.height
    const wh = window.innerHeight

    const viewportRatio = (h < wh) ? entry.intersectionRatio : (
      entry.intersectionRatio * h / wh
    )

    if (entry.isIntersecting && viewportRatio >= 0.5) {
      // Activate visible section
      switchActive(thisIdx)
    }
  })
}, options)

observables.forEach((item, idx) => {
  observer.observe(item.el)
  obsIdToIdx[item.el.id] = idx
})
