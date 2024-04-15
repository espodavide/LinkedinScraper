// script.js
function generateWordCloud() {
    // Ottieni i dati dal form
    var jobTitle = document.getElementById('jobTitle').value;
    var location = document.getElementById('location').value;
    console.log("Button_pressed"); 
    console.log(location); 
    console.log(jobTitle);
    console.log(" IL JSON ")
    console.log(JSON.stringify({
            "jobTitle": jobTitle,
            "location": location
        }))
    // Esegui la chiamata API
    fetch('/WordCloud', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "jobTitle": jobTitle,
            "location": location
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Dopo che la chiamata
        var url = '/WordCloudlandingpage' +
          '?jobTitle=' + encodeURIComponent(jobTitle) +
          '&location=' + encodeURIComponent(location);
          console.log(url)
        window.location.href = url;
    })
    .catch((error) => {
        console.error('Errore durante la chiamata API:', error);
        // Gestisci eventuali errori qui
    });
};
