const carForm = document.getElementById('car-form')
const carsDataBox = document.getElementById('cars-data-box')
const carInput = document.getElementById('cars')
const modelsDataBox = document.getElementById('models-data-box')
const modelInput = document.getElementById('models')
const btnBox = document.getElementById('btn-box')
const alertBox = document.getElementById('alert-box')
const modelText = document.getElementById('model-text')
const carText = document.getElementById('car-text')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

$.ajax({
    type: 'GET',
    url: '/cars-json/',
    success: function(response){
        console.log(response.data)
        const artistsData = response.data
        artistsData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            artistsDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})

artistInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedArtist = e.target.value

    alertBox.innerHTML=""
    modelsDataBox.innerHTML = ""
    modelText.textContent = "Choose a artist"
    modelText.classList.add("default")


    $.ajax({
        type: 'GET',
        url: `models-json/${selectedArtist}/`,
        success: function(response){
            console.log(response.data)
            const modelsData = response.data
            modelsData.map(item=>{
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                modelsDataBox.appendChild(option)
            })

            modelInput.addEventListener('change', e=>{
                btnBox.classList.remove('not-visible')
            })
        },
        error: function(error){
            console.log(error)
        }
    })
})

carForm.addEventListener('submit', e=>{
    e.preventDefault()
    console.log('submitted')

    $.ajax({
        type: 'POST',
        url: '/create/',
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'artist': artistText.textContent,
            'title': titleText.textContent,
        },
        success: function(response){
            console.log(response)
            alertBox.innerHTML = `<div class="ui positive message">
                                    <div class="header">
                                    Success
                                    </div>
                                    <p>Your order has been placed</p>
                                </div>`
        },
        error: function(error){
            console.log(error)
            alertBox.innerHTML = `<div class="ui negative message">
                                    <div class="header">
                                    Ops
                                    </div>
                                    <p>Something went wrong</p>
                                </div>`
        }
    })
})