// === CONFIG ===
const API_BASE = "https://website-project-9.onrender.com/api/v1/jokes"; // Flask backend URL

// === Helper function to show messages ===
function showMessage(msg, isError = false) {
  const jokeList = document.getElementById("jokeList");
  jokeList.innerHTML = `<p class="${isError ? 'has-text-danger' : 'has-text-grey'} has-text-centered is-size-5">${msg}</p>`;
}

// === Function: Fetch multiple jokes ===
async function fetchJokes(language, category, number) {
  const jokeList = document.getElementById("jokeList");
  showMessage("Loading jokes...");

  try {
    // Build URL depending on language, category, and number
    let url = API_BASE;

    // Always include language and category (use "any" if selected)
    url += `/${language || "any"}`;
    url += `/${category || "any"}`;

    // Handle number
    if (number && number !== "all") {
      url += `/${number}`;
    } else if (number === "all") {
      url += `/all`;
    }

    console.log("Fetching URL:", url); // debug

    const response = await fetch(url);

    // Check content type before parsing
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text(); // log response body
      console.error("Non-JSON response body:", text);
      throw new Error(`Unexpected response format: ${contentType}`);
    }

    const data = await response.json();

    if (!data.jokes || data.jokes.length === 0) {
      showMessage("No jokes found for this selection!", true);
      return;
    }

    // Render jokes: one per line
    jokeList.innerHTML = "";
    data.jokes.forEach((joke) => {
      const cardWrapper = document.createElement("div");
      cardWrapper.className = "column is-full";

      const card = document.createElement("div");
      card.className = "card mb-3";
      card.innerHTML = `
        <div class="card-content">
          <p class="title is-6">${joke.text}</p>
          <p class="subtitle is-7 has-text-grey">[${joke.language.toUpperCase()} | ${joke.category}]</p>
        </div>
      `;

      cardWrapper.appendChild(card);
      jokeList.appendChild(cardWrapper);
    });
  } catch (err) {
    showMessage(`Error: ${err.message}`, true);
  }
}

// === Function: Fetch joke by ID ===
async function fetchJokeById(id) {
  const jokeList = document.getElementById("jokeList");

  if (!id || isNaN(id)) {
    showMessage("Please enter a valid joke ID!", true);
    return;
  }

  showMessage("Fetching joke...");

  try {
    // Updated route for ID
    const url = `${API_BASE}/id/${id}`;
    console.log("Fetching URL by ID:", url); // debug
    const response = await fetch(url);

    // Check content type before parsing
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text();
      console.error("Non-JSON response body:", text);
      throw new Error(`Unexpected response format: ${contentType}`);
    }

    const data = await response.json();
    if (!data.joke) {
      showMessage("Joke not found!", true);
      return;
    }

    const joke = data.joke;

    jokeList.innerHTML = `
      <div class="column is-full">
        <div class="card">
          <div class="card-content">
            <p class="title is-6">${joke.text}</p>
            <p class="subtitle is-7 has-text-grey">[${joke.language.toUpperCase()} | ${joke.category}]</p>
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    showMessage(`Error: ${err.message}`, true);
  }
}

// === Event: Load random jokes button ===
document.getElementById("loadJokesBtn").addEventListener("click", () => {
  const language = document.getElementById("language").value;
  const category = document.getElementById("category").value;
  const number = document.getElementById("numJokes").value;
  const jokeId = document.getElementById("jokeIdInput").value.trim();

  // If an ID is entered, fetch by ID; otherwise fetch multiple jokes
  if (jokeId) {
    fetchJokeById(jokeId);
  } else {
    fetchJokes(language, category, number);
  }
});

// === Event: Joke ID input (fetch on Enter) ===
document.getElementById("jokeIdInput").addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    const id = e.target.value.trim();
    if (id) {
      fetchJokeById(id);
    }
  }
});