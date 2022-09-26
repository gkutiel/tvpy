function item(i) {
  return `
    <div class='item'>
      <div class='col'>
        <a target="_blank" href="https://www.imdb.com/title/${i.imdb_id}/">
          <img style="max-width:160px" src="data:image/jpgbase64,${i.poster_base64}"/>
        </a>      
      </div>
      <div class='col'>
        <h2>${i.name}</h2>
        <p>${i.overview}</p>
        <span><b>${i.rating}</b> by ${i.ratingCount.toLocaleString('en-US')} users</span>
      </div>
    </div>
  `
}

function render() {
  const items = document.getElementById('items')
  items.innerHTML = ''
  data.forEach(r => {
    const div = document.createElement('div')
    div.innerHTML = item(r)
    items.append(div)
  })
}

addEventListener('DOMContentLoaded', () => {
  data.sort((a, b) => b.rating - a.rating)
  render()

  const socket = new WebSocket("ws://localhost:8765")
  socket.onopen = function (e) { }
  socket.onclose = function (event) { }
  socket.onerror = function (error) { }
  socket.onmessage = function (event) {
    console.log(`[message]  ${event.data}`)
  }
})


