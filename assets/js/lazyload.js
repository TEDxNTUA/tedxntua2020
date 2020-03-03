function loadLazyImage(lazyImage) {
  if (lazyImage.dataset.loaded === "true") return

  if (lazyImage.dataset.src) {
    lazyImage.src = lazyImage.dataset.src
  }
  if (lazyImage.dataset.srcset) {
    lazyImage.srcset = lazyImage.dataset.srcset
  }
  lazyImage.dataset.loaded = "true"
}

function attachObserver() {
  const lazyImagesOnView = [].slice.call(
    document.querySelectorAll("img.lazy-on-view")
  )

  if ("IntersectionObserver" in window) {
    const lazyImageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const lazyImage = entry.target
          loadLazyImage(lazyImage)
          lazyImageObserver.unobserve(lazyImage)
        }
      })
    })

    lazyImagesOnView.forEach(lazyImage => {
      lazyImageObserver.observe(lazyImage)
    })
  }

  const lazyImagesOnHover = [].slice.call(
    document.querySelectorAll("img.lazy-on-hover")
  )

  lazyImagesOnHover.forEach(lazyImage => {
    lazyImage.addEventListener("mouseover", () => {
      loadLazyImage(lazyImage)
    })
    lazyImage.addEventListener("touchstart", () => {
      loadLazyImage(lazyImage)
    })
  })
}

document.addEventListener("DOMContentLoaded", attachObserver)
document.addEventListener("pjax:complete", attachObserver)
