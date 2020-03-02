import $ from 'jquery'

const leafletFrame = document.getElementById('leaflet-iframe')

$(document).ready(function () {
    $('#leaflet-modal').on('show.bs.modal', function (event) {
        var btn = event.relatedTarget
        var leafletPath = btn.dataset.leafletUrl
        // Update img of modal
        leafletFrame.setAttribute('src', leafletPath + '#view=Fit')
    })
})
