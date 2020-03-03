const Pjax = require('pjax')
const on = require('pjax/lib/events/on')
const trigger = require('pjax/lib/events/trigger')
const clone = require('pjax/lib/util/clone')


const PAGE_CACHE = {}

/* Detect fast connections to enable prefetches
 *
 * Adapted from:
 * https://developer.mozilla.org/en-US/docs/Web/API/Network_Information_API
 */
let SHOULD_PREFETCH = false
let conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection
if (conn && (conn.effectiveType == '3g' || conn.effectiveType == '4g')) {
  SHOULD_PREFETCH = true
}

/**
 * Checks if link of given element is to a page with the same language as the
 * current one.
 *
 * @param {Anchor} el Anchor tag.
 * @returns {boolean} True if language is the same.
 */
function isSameLang (el) {
  return (
    el.pathname.substring(0, 4) === window.location.pathname.substring(0, 4)
  )
}

/**
 * Adapted from:
 * https://github.com/MoOx/pjax/blob/480334b18253c721ba648675e90261f948e2bca0/lib/proto/attach-link.js
 */
function checkIfShouldAbort (el) {
  return (
    // Is external link?
    el.protocol !== window.location.protocol ||
    el.host !== window.location.host ||
    // Is anchor on the same page?
    (el.hash &&
      el.href.replace(el.hash, "") ===
        window.location.href.replace(location.hash, "")
    ) ||
    el.href === window.location.href.split("#")[0] + "#" ||
    !isSameLang(el)
  )
}

/**
 * We override Pjax's loadUrl function so that requests for the same href are
 * cached.
 * Warning! This implementation is guaranteed to work only for simple cases
 * where only GET requests are made, no options are passed, etc.
 */
Pjax.prototype._noCacheHandleResponse = Pjax.prototype.handleResponse
Pjax.prototype._noCacheLoadUrl = Pjax.prototype.loadUrl
Pjax.prototype.handleResponse = function (responseText, request, href, options) {
  Pjax.prototype._noCacheHandleResponse.bind(this)(responseText, request, href, options)
  PAGE_CACHE[href] = responseText
}
Pjax.prototype.loadUrl = function (href, options) {
  if (PAGE_CACHE.hasOwnProperty(href)) {
    const responseText = PAGE_CACHE[href]
    this.state.href = href
    this.state.options = options
    try {
      this.loadContent(responseText, options)
    } catch (e) {
      trigger(document, 'pjax:error', options)
      return this.latestChance(href)
    }
  } else {
    this._noCacheLoadUrl(href, options)
  }
}
Pjax.prototype.prefetchUrl = function (el, options) {
  // Skip if already prefetched or should abort
  if (PAGE_CACHE.hasOwnProperty(el.href) || checkIfShouldAbort(el)) {
    return
  }

  this.doRequest(
    el.href,
    options,
    function (responseText, request, href, options) {
      PAGE_CACHE[el.href] = responseText
    },
  )
}

// Override Pjax's attachLink to handle other language and prefetches
Pjax.prototype._noHoverAttachLink = Pjax.prototype.attachLink
Pjax.prototype.attachLink = function (el) {
  // Don't attach if its a link to other language version
  if (!isSameLang(el)) return

  this._noHoverAttachLink(el)
  if (SHOULD_PREFETCH) {
    on(el, 'mouseenter', event => {
      const options = clone(this.options)
      options.triggerElement = el
      this.prefetchUrl(el, options)
    })
  }
}

// Create and expose
window.pjax = new Pjax({
  selectors: [
    'title',
    'meta[name=description]',
    'meta[property="og:image"]',
    '#nav',
    '#main',
    '#footer .language-switch',
    '.is-pjax',
  ],
  cacheBust: false,
  analytics: function () {
    if (window._paq) {
      window._paq.push(['trackPageView'])
    }
  }
})
