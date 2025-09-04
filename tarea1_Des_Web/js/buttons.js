

const portadabutton = document.getElementById("portada")
const portadaauxbutton = document.getElementById("portada2")
const sendbutton = document.getElementById("send-post")
const listbutton = document.getElementById("see-posts")
const statsbutton = document.getElementById("see-stats")


portadabutton.addEventListener("click", function() {
    window.location.href = "portada.html"
})

sendbutton.addEventListener("click", function() {
    window.location.href = "anuncio.html"
})

listbutton.addEventListener("click", function() {
    window.location.href = "avisos.html"
})

statsbutton.addEventListener("click", function() {
    window.location.href = "estadisticas.html"
})

portadaauxbutton.addEventListener("click", function() {
    window.location.href = "portada.html"
})