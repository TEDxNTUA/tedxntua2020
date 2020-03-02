const scheduleTable = document.getElementById('schedule-table')
const stageSelector = document.getElementById('stage-selector')
stageSelector.addEventListener('change', evt => {
    scheduleTable.setAttribute('data-activetab', evt.target.value)
})
