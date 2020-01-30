const Pjax = require('pjax')
const on = require('pjax/lib/events/on')
const trigger = require('pjax/lib/events/trigger')
const clone = require('pjax/lib/util/clone')


const PAGE_CACHE = {}

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
Pjax.prototype.prefetchUrl = function (href, options) {
  // Skip if already prefetched
  if (PAGE_CACHE.hasOwnProperty(href)) return

  this.doRequest(href, options, function (responseText, request, href, options) {
    PAGE_CACHE[href] = responseText
  })
}

// Override Pjax's parseDOM to prefetch when user hovers a link
Pjax.prototype._noHoverAttachLink = Pjax.prototype.attachLink
Pjax.prototype.attachLink = function (el) {
  this._noHoverAttachLink(el)
  on(el, 'mouseenter', event => {
    const options = clone(this.options)
    options.triggerElement = el
    this.prefetchUrl(el.href, options)
  })
}

const pjax = new Pjax({
  selectors: [
    'title',
    'meta[name=description]',
    '#main',
  ],
  cacheBust: false,
})
