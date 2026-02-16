function loadTab(type) {
    fetch(`/gui/tab/${type}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById("editor-content").innerHTML = html;
        });
    if (type == "pokemon") {
        loadPokemonList();
    }
}
async function createPokemon() {

    const data = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value
    };

    const response = await fetch("/abilities/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert("Response: " + JSON.stringify(result));
}


async function submitPokemon() {
    const input = document.getElementById("pokemonInput");
    const name = input.value.toLowerCase();

    // verifica se existe na lista
    const response = await fetch("/pokemon/names");
    const names = await response.json();

    if (!names.includes(name)) {
        // chama endpoint que vai buscar à pokeapi
        await fetch(`/pokemon/${name}`);
    }

    // reload página depois
    window.location.reload();
}

async function loadPokemonList() {
    const response = await fetch("/pokemon/pkm/all");
    const names = await response.json();
    const datalist = document.getElementById("pokemonSelect");
    datalist.innerHTML = '<option value="">Selecione um Pokémon...</option>';

    names.forEach(name => {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        datalist.appendChild(option);
    });
}

